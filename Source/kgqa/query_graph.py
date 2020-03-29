from config import graph, similar_words
#from spider.show_profile import get_profile
import codecs
import os
import json
import base64
import pyltp 
import os
LTP_DATA_DIR = '../../data/ltp_model'  # ltp模型目录的路径

def cut_words(words):
    segmentor = pyltp.Segmentor()
    seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    segmentor.load(seg_model_path)
    words = segmentor.segment(words)
    array_str="|".join(words)
    array=array_str.split("|")
    segmentor.release()
    return array

def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(array)  # 词性标注
    pos_str=' '.join(postags)
    pos_array=pos_str.split(" ")
    postagger.release()  # 释放模型
    return pos_array

def get_target_array(words):
    target_pos=['nh','ni','ns','n']
    target_array=[]
    seg_array=cut_words(words)
    pos_array = words_mark(seg_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos: #识别出人名、地名、
            target_array.append(seg_array[i])
    target_array.append(seg_array[1])
    print(target_array)
    return target_array

def get_KGQA_answer(array):
    #print(array)
    data_array=[]
    for i in range(len(array)-2):
        if i==0:
            name=array[0]
        else:
            name=data_array[-1]['p.Name']
        print( similar_words[array[i]] )
        print( similar_words[array[i+1]] )
        print( name )
        sql = "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (similar_words[array[i]], similar_words[array[i+1]], name)
        print(sql)

#        data = graph.run(
#            "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
#                similar_words[array[i+1]], similar_words[array[i+1]], name)
#        )
       
        data = list(data)
        print(data)
        data_array.extend(data)
        
        print("="*36)
    #with open("./spider/images/"+"%s.jpg" % (str(data_array[-1]['p.Name'])), "rb") as image:
    #        base64_data = base64.b64encode(image.read())
    #        b=str(base64_data)
          
#    return [get_json_data(data_array), get_profile(str(data_array[-1]['p.Name'])), b.split("'")[1]]
#def get_answer_profile(name):
#    with open("./spider/images/"+"%s.jpg" % (str(name)), "rb") as image:
#        base64_data = base64.b64encode(image.read())
#        b = str(base64_data)
#    return [get_profile(str(name)), b.split("'")[1]]

while True:
    question = input('请输入问题（exit结束）：')
    if question=='exit':
        break
    get_KGQA_answer(get_target_array(question))
    #answer = get_KGQA_answer(get_target_array(question))
    #print(answer)



