import os
import re
from pyltp import SentenceSplitter # 中文分句

def clean_text(txt):
    #txt = re.sub('[0-9a-zA-Z]+', '', txt)
    txt = txt.replace('\n','')
    txt = txt.replace('\t','')
    txt = txt.replace('【','')
    txt = txt.replace('】','')
    txt = txt.replace('/','')
    txt = txt.replace('\\','')
    txt = txt.replace('?','？')
    txt = txt.replace(',','，')
    txt = txt.replace(';','；')
    txt = txt.replace("'",'')
    txt = txt.replace('"','')
    txt = txt.replace(' ','')
    return txt

def find_questions_in_file( txt_file ):
    with open(txt_file,'r',encoding='utf8') as f:
        txt = f.read()
        txt = clean_text(txt)
        sents = SentenceSplitter.split(txt)# 分句
        #print(len(sents))
        qlist = list()
        for s in sents:
            if s[len(s)-1]=='？' and len(s)>3 and len(s)<=32:
                qlist.append(s+'\n')
    return qlist

def save_questions( qlist, outfile ):
    with open(outfile,'w',encoding='utf8') as f:
        f.writelines(qlist)

rootdir = './dataset/weibo'
all_files = os.listdir(rootdir) #列出文件夹下所有的目录与文件
questions = list()
for i in range(0,len(all_files)):
    path = os.path.join(rootdir,all_files[i])
    if os.path.isfile(path):
        questions += find_questions_in_file(path)

save_questions(questions,'./dataset/questions.txt')
print(len(questions))

#再对questions.txt进行二次清洗
import csv

KEY_WORDS=list(['ECMO','措施','政策','策略','监管','案','例','诊','院','治','愈','死','去世','逝世',
    '多少','人','是','哪位','什么','哪里','怎么','新冠','新型冠状','来源','药物','特效药',
    '治疗','症','预','护','设备','非典','SARS','MERS','CDC','病毒','炎','复工','健康码','封城','感染',
    '传染','呼吸','毒','传播','检疫','H1N1','医','药','病','疾','疫','冠','肺','省','市','国'])
lines = list()
with open('./dataset/questions.txt','r',encoding='utf8') as f:
    lines = f.readlines()
    out = list()
    for ll in lines:
        ss = ll.split('，')
        for w in KEY_WORDS:
            if ss[len(ss)-1].find(w)>=0:
                out.append(ss[len(ss)-1])#+'\n')
save_questions( out, './dataset/q2.txt')
