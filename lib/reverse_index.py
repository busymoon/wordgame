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
        return docs[idx],cls.sent_list[docs[idx]]

    @classmethod
    def process(cls, p, f_name):
        s_list = sent_tokenize(p)
        next = ""

        for s in s_list:
            if next:
                s = next + s
                next = ""
            words = word_tokenize(s)
            if len(words)<5:
                if len(s)<30:
                    next=  s
                continue

            if len(s)>100 or 5>sum([1 if wordnet.synsets(wrd) else 0 for wrd in words]):
                # print("abandomed:"+s)
                continue

            idx = len(cls.sent_list)
            cls.sent_list.append(s + u"--*{}*".format(f_name))

            for w in set(words):
                w = w.lower()
                if not wordnet.synsets(w):
                    continue
                if w not in stop_words:
                    w = ps.stem(w)
                    if w not in cls.word_map:
                        cls.word_map[w] = []
                    if idx not in cls.word_map[w]:
                        cls.word_map[w].append(idx)

fns=["Black Beauty","Paris","aesop","book_bug_1_nodrm","book_bug_2","book_bug_3_nodrm"]
count = 0
buffer=""
for fn in fns:
    with open(fn+".txt","r") as f:
        for line in f.readlines():
            if line.strip()=="":
                continue
            count = count+1
            if count % 1000==0:
                print("processed line {} get sentence{}".format(count,len(RI.sent_list)))

            buffer = buffer + line
            if len(buffer)>1000:
                offset = buffer.rfind(".")
                if offset < 0:
                    cnt = buffer
                    buffer = ""
                else:
                    cnt = buffer[:offset]
                    buffer = buffer[offset+1:]
                RI.process(cnt,fn)


import json
s = json.dumps(RI.sent_list,skipkeys=False, indent=4, sort_keys=False)

with open("out_sent_list.js","w") as out:
    out.write("sent_list="+s)

s = json.dumps(RI.word_map,skipkeys=False, indent=4, sort_keys=False)

with open("out_word_map.js","w") as out:
    out.write("word_map="+s)

print(s)

print(RI.s("soul"))
print(RI.s("hunt"))
