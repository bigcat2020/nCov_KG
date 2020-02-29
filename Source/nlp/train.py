# -*- coding: utf-8 -*-
import sklearn
import pycrfsuite
import jieba.posseg as posg

#训练文件处理类
class TrainFormat:
    def getSentence(self, token ):
        sentence= ''
        for t in token:
            sentence += t[0]
        return sentence

    # 使用jieba分词为token填充分词标记和词性标记
    def cutSegment(self, token):
        wordlist = posg.cut( self.getSentence(token) )
        res = list()
        index=0
        for w in wordlist:
            for i in range(len(w.word)):
                if len(w.word) == 1: #由一个字组成的词
                    status = 'S'
                elif i == 0:
                    status = 'B' #词语开始
                elif i == len(w.word) - 1:
                    status = 'E' #词语结束
                else:
                    status = 'I' #词语中间
                token[index][1]=status
                token[index][2]=w.flag
                index += 1
        return res

    # 读入训练数据
    def loadDataFile(self, dataFile):
        res=list()
        with open( dataFile, 'r', encoding='utf-8' ) as f:
            lines= f.readlines()
            res_line= list()
            for line in lines:
                if line.split(' ').__len__()>=2:
                    word= line.split(' ')[0]
                    type= line.split(' ')[1].replace('\n','').replace('\r','')
                    res_line.append([word,'','',type])
                else:
                    self.cutSegment(res_line)
                    res.append(res_line)
                    res_line=list()
        return res

    def get_type_encode(self, text):
        if text.__contains__('PRO'):
            return 'product_name'
        elif text.__contains__('PER'):
            return 'person_name'
        elif text.__contains__('TIM'):
            return 'time'
        elif text.__contains__('ORG'):
            return 'org_name'
        elif text.__contains__('LOC'):
            return 'location'
        else:
            return 'unknown'
    
    # 将句子切分为一个一个的字，用于输入实体识别
    def split_by_words(self, sentence):
        res=list()
        for word in sentence:
            res.append([word,'','',''])
        self.cutSegment(res)
        return res

    # 输出按boson语料的格式规范化后的命名实体标记
    def format_boson_data_encode(self, text, tag ):
        res=""
        status=0
        for i in range(len(text)):
            if status == 0 and tag[i] == 'O':
                res += text[i]
            elif status == 0 and tag[i] != 'O':
                status = 1
                res += "{{" + self.get_type_encode(tag[i]) + ":" + text[i]
            elif status == 1 and str(tag[i]).startswith('I'):
                res += text[i]
            elif status == 1:
                res += "}}"
                if tag[i] == 'O':
                    status = 0
                    res += text[i]
                else:
                    status = 1
                    res += "{{" + self.get_type_encode(tag[i]) + ":" + text[i]
        return res

#CRF训练类
class CRFTrainee:
    #训练模型输出文件
    __model_name='./train.model'
    #训练发射概率矩阵
    __train_sents=list()
    #测试发射概率矩阵
    __test_sents=list()
    #文本训练集
    __X_train=[]
    #标签训练集
    __y_train=[]
    #文本测试集
    __X_test=[]
    #标签测试集
    __y_test=[]
 
    #根据
    def word2features(self, sent, i):
        word = sent[i][0]
        cuttag = sent[i][1]
        postag = sent[i][2]
        features = [
            'bias',
            'word='+word,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'cuttag=' + cuttag,
        ]
        if i > 0:
            word1 = sent[i - 1][0]
            postag1 = sent[i - 1][2]
            cuttag1 = sent[i - 1][1]
            features.extend([
                '-1:word='+word1,
                '-1:postag=' + postag1,
                '-1:cuttag=' + cuttag1,
            ])
        else:
            features.append('BOS')

        if i < len(sent) - 1:
            word1 = sent[i + 1][0]
            postag1 = sent[i + 1][2]
            cuttag1 = sent[i + 1][1]
            features.extend([
                '+1:word=' + word1,
                '+1:postag=' + postag1,
                '+1:cuttag=' + cuttag1,
            ])
        else:
            features.append('EOS')

        return features

    def sent2features(self, sent):
        return [self.word2features(sent, i) for i in range(len(sent))]


    def sent2labels(self, sent):
        return [label for token, cuttag, postag, label in sent]


    def sent2tokens(self, sent):
        return [token for token, cuttag, postag, label in sent]

    # 加载数据
    def loadTrainFiles(self, train_file='./example.train',test_file='./example.test'):
        format = TrainFormat()
        self.__train_sents = format.loadDataFile(train_file)
        self.__test_sents = format.loadDataFile(test_file)
        
        self.__X_train = [self.sent2features(s) for s in self.__train_sents]
        self.__y_train = [self.sent2labels(s) for s in self.__train_sents]
        self.__X_test = [self.sent2features(s) for s in self.__test_sents]
        self.__y_test = [self.sent2labels(s) for s in self.__test_sents]

    # 训练
    def train(self):
        trainer = pycrfsuite.Trainer()

        for xseq, yseq in zip(self.__X_train, self.__y_train):
            trainer.append(xseq, yseq)
        trainer.set_params({
            'c1': 1.0,   # L1协方差
            'c2': 1e-3,  # L2协方差
            'max_iterations': 50,  #最大迭代次数
            'feature.possible_transitions': True
        })
        trainer.train(self.__model_name)
    
    def ner( self, text ):
        format = TrainFormat()
        tagger = pycrfsuite.Tagger()
        tagger.open(self.__model_name)
        sent=format.split_by_words(text)
        tag_result=tagger.tag(self.sent2features(sent))
        text_result=format.format_boson_data_encode(text,tag_result)
        return text_result

    #测试训练结果
    def test( self, inputFile, outputFile ):
        input_file=open(inputFile,'r',encoding='utf-8')
        result=self.ner(input_file.read())
        output_file= open(outputFile,'w',encoding='utf-8')
        try:
            output_file.write(result)
        finally:
            output_file.close()

#测试代码
trainer = CRFTrainee()
#trainer.loadTrainFiles('example.train', 'example.test')
#trainer.train()
trainer.test( './abc.txt', './output1.txt' )