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

        for s in s_list:

            if not wordnet.synsets(s[0]):
                return

            #print(s)
            idx = len(cls.sent_list)
            cls.sent_list.append(s + u"--*{}*".format(f_name))

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
        return s_list[-1]

fns=["Black Beauty","Paris","aesop"]
count = 0
buffer=""
for fn in fns:
    with open(fn+".txt","r") as f:
        for line in f.readlines():
            count = count+1
            if count % 1000==0:
                print(count)

            RI.process(line,fn)

import json
s = json.dumps(RI.sent_list,skipkeys=False, indent=4, sort_keys=False)

with open("out_sent_list.js","w") as out:
    out.write(s)

s = json.dumps(RI.word_map,skipkeys=False, indent=4, sort_keys=False)

with open("out_word_map.js","w") as out:
    out.write(s)

print(s)

print(RI.s("soul"))
print(RI.s("hunt"))
