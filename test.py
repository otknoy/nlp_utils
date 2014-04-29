#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import nlp.tokenizer
    import nlp.processing

    docs = [u'山下さんは山下くんと東京特許許可局へ行った。',
            u'山下さんは山下くんと北海道へ行った。',
            u'山下さんは下山くんと New York へ行った。',
            u'山上さんは山下くんと東京特許許可局へ行った。',]             

    texts = []
    for text in docs:
        terms, posids = nlp.tokenizer.parse(text, pos=True)
        terms, posids = nlp.tokenizer.select_noun(terms, posids)
        texts.append(terms)


    print 'ngram'
    for text in texts:
        for terms in nlp.processing.ngram(text):
            print '(' + ' '.join(terms) + ')',
        print
    print

    print 'term frequency'
    for terms in texts:
        print ' '.join(terms)
        
        tf = nlp.processing.term_frequency(terms)
        print ' '.join(["[%s: %d]" % (t, f) for t, f in tf.items()])
    print

    print 'document frequency'
    df = nlp.processing.document_frequency(texts)
    for t, w in df.items():
        print t, w
    print

    print 'inverse document frequency'
    idf = nlp.processing.inverse_document_frequency(texts)
    for t, w in idf.items():
        print t, w
    print

    print 'tf-idf'
    tfidf_list = nlp.processing.tf_idf(texts)
    for tfidf in tfidf_list:
        for t, w in tfidf.items():
            print w,
        print

