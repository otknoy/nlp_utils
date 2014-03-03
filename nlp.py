#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata
import MeCab

def tokenizer(text, pos=False):
    import MeCab
    uni = text.encode('utf-8')
    tagger = MeCab.Tagger("-Ochasen")
    node = tagger.parseToNode(uni)

    terms = []
    posids = []
    while node:
        surface = node.surface
        features = node.feature.split(',')
        basic_form = features[6]
        if basic_form == '*':
            basic_form = surface
        terms.append(basic_form.decode('utf-8'))
        posids.append(node.posid)
        node = node.next
    if pos:
        return terms[1:-1], posids[1:-1]
    else:
        return terms[1:-1]


noun_posids = range(36, 67+1)
verb_posids = range(31, 33+1)
pronoun_posids = [59, 60]
independent_posids = [58, 66, 67]

def select(terms, posids, condition):
    _terms = []
    _posids = []
    for term, posid in zip(terms, posids):
        if condition(posid):
            _terms.append(term)
            _posids.append(posids)
    return _terms, _posids

def select_noun(terms, posids):
    condition = lambda posid: posid in noun_posids
    return select(terms, posids, condition)

    

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


if __name__ == '__main__':
    docs = [u'山下さんは山下くんと東京特許許可局へ行った。',
            u'山下さんは山下くんと北海道へ行った。',
            u'山下さんは下山くんと New York へ行った。',
            u'山上さんは山下くんと東京特許許可局へ行った。',]             

    texts = []
    for text in docs:
        terms, posids = tokenizer(text, pos=True)
        terms, posids = select_noun(terms, posids)
        texts.append(terms)


    print 'ngram'
    for text in texts:
        for terms in ngram(text):
            print '(' + ' '.join(terms) + ')',
        print
    print

    print 'term frequency'
    for terms in texts:
        print ' '.join(terms)
        
        tf = term_frequency(terms)
        print ' '.join(["[%s: %d]" % (t, f) for t, f in tf.items()])
    print

    print 'document frequency'
    df = document_frequency(texts)
    for t, w in df.items():
        print t, w
    print

    print 'inverse document frequency'
    idf = inverse_document_frequency(texts)
    for t, w in idf.items():
        print t, w
    print

    print 'tf-idf'
    tfidf_list = tf_idf(texts)
    for tfidf in tfidf_list:
        for t, w in tfidf.items():
            print w,
        print

