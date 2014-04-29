#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata


def unicode_normalize(text):
    return unicodedata.normalize('NFKC', text)

def term_frequency(terms):
    tf = {}
    for t in terms:
        if not tf.has_key(t):
            tf[t] = 0
        tf[t] += 1
    return tf

def document_frequency(texts):
    from itertools import chain
    all_terms = list(chain.from_iterable(texts)) # flatten
    df = {}
    for term in all_terms:
        df[term] = [term in text for text in texts].count(True)
    return df

def inverse_document_frequency(texts):
    df = document_frequency(texts)
    idf = {}
    for t in df.keys():
        idf[t] = 1.0/df[t]
    return idf

def tf_idf(texts):
    tfidf_list = []
    idf = inverse_document_frequency(texts)
    for terms in texts:
        tf = term_frequency(terms)
        tfidf = {}
        for t in idf.keys():
            if not tf.has_key(t):
                tfidf[t] = 0.0
            else:
                tfidf[t] = tf[t] * idf[t]
        tfidf_list.append(tfidf)
    return tfidf_list
    

def ngram(terms, n=2):
    ret = []
    for i in range(0, len(terms)-n+1):
        ret.append(terms[i:i+n])
    return ret
