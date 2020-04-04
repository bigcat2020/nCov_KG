#import pandas as pd
import jieba.posseg as pg
import csv
import random

entity_file={'nr':'人名.csv','ns':'地区.csv','nt':'机构.csv','nz':'医学.csv'}
root_path = './data'
entity_dict = dict()

def load_stopwords( stopfile ):
    stopword_dict = dict()
    with open(stopfile,'r',encoding='utf8') as f:
        lines = f.readlines()
        for l in lines:
            l = l.replace('\n','')
            stopword_dict[l] = 1
    return stopword_dict

def load_entity():
    for k, efile in entity_file.items():
        entity_dict[k] = list()
        with open(root_path+efile,'r',encoding='utf8') as f:
            lines = f.readlines()
            for l in lines:
                l = l.split(',')
                entity_dict[k].append(l[0])

def change_entity( id, numbers ): #随机读取n个数字
    entity=list()
    for i in range(numbers):
        index = random.randint(0,len(entity_dict[id])-1)
        entity.append(entity_dict[id][index])
    return entity

def check_jieba():
    with open('./q3.txt','r',encoding='utf8') as f:
        csvfile = csv.reader(f)
        lines = list()
        for q in csvfile:
            wordpos = pg.cut(q[0])
            line = ''
            for w in wordpos:
                lines += w.word + '(' + w.flag + ') '
            line += '\n'
            lines.append(line)
    with open('./check.txt','w',encoding='utf8') as f:
        f.writelines(lines)

def data_augment():
    stopword_dict = load_stopwords('./data/stopwords.txt')    
    expand_questions = dict()
    with open('./data/q3.txt','r',encoding='utf8') as f:
        csvfile = csv.reader(f)
        for q in csvfile:
            if len(q)==2:
                expand_questions[q[0]] = q[1] #先增加原句
                wordpos = pg.cut(q[0])
                expand = None
                wordlist=list()
                for w in wordpos: #我 r,爱 v,北京 ns,天安门 ns，钟南山 ns
                    wordlist.append(w)
                
                if len(wordlist)>6:
                    continue

                for i in range(len(wordlist)):
                    if wordlist[i].word in stopword_dict:
                        continue
                    if wordlist[i].flag in entity_file:
                        changes = change_entity(wordlist[i].flag, 200)
                        for c in changes:
                            ques = ''
                            for j in range(len(wordlist)):
                                if i==j:
                                    ques += c
                                else:
                                    ques += wordlist[j].word
                            if len(ques)<=20:
                                expand_questions[ques]=q[1]

    questions = list()
    for k,v in expand_questions.items():
        line = k+','+v+'\n'
        questions.append(line)
    random.shuffle(questions) #随机乱序
    
    n = len(questions)
    ntrain = int(n*0.8)
    nval = int(n*0.1)
    with open('./data/train.txt','w',encoding='utf8') as f:
        f.writelines(questions[:ntrain])
    with open('./data/val.txt','w',encoding='utf8') as f:
        f.writelines(questions[ntrain:ntrain+nval])
    with open('./data/test.txt','w',encoding='utf8') as f:
        f.writelines(questions[ntrain+nval:])
    print(n,ntrain,nval)

#
#load_entity()
#check_jieba()
#data_augment()