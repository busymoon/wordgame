#coding: utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:08:22 2019

@author: brian
"""


from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords,wordnet
from nltk.stem import PorterStemmer
import random

stop_words = set(stopwords.words("english"))
ps = PorterStemmer()
#print(stop_words)

class RI(object):
    
    sent_list = []
    
    word_map = dict()
    
    @classmethod
    def s(cls, w ):
        w = ps.stem(w)
        docs = cls.word_map[w]
        idx = int(len(docs)*random.random())
        return cls.sent_list[docs[idx]]
    
    @classmethod
    def process(cls, p):
        
        s_list = sent_tokenize(p)
        
        for s in s_list:
            
            if not wordnet.synsets(s[0]):
                return
            
            #print(s)
            idx = len(cls.sent_list)
            cls.sent_list.append(s)
        
            words = word_tokenize(s)
            if len(words)<10:
                continue
            
            for w in set(words):
                w = w.lower()
                
                if not wordnet.synsets(w):
                    continue
            
                if w not in stop_words:
                    #print(w)
                    w = ps.stem(w)
                    if w not in cls.word_map:
                        cls.word_map[w] = []
                    if idx not in cls.word_map[w]:
                        cls.word_map[w].append(idx)

fns=["Black Beauty.txt","Paris.txt"]
count = 0
for fn in fns:
    with open(fn,"r") as f:
        for line in f.readlines():
            count = count+1
            if count % 1000==0:
                print(count)
        
            RI.process(line)
            #print("------------->")
            #print(line)


import json
s = json.dumps({"sent_list":RevertedIndex.sent_list,"word_map":RevertedIndex.word_map},
               skipkeys=False, indent=4, sort_keys=False)

with open("out.js","w") as out:
    out.write(s)

print(s)

print(RevertedIndex.sentence("soul"))
print(RevertedIndex.sentence("hunt"))
    