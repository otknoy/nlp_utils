#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MeCab

def parse(text, pos=False):
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

# verb_posids = range(31, 33+1)
# pronoun_posids = [59, 60]
# independent_posids = [58, 66, 67]

def select(terms, posids, condition):
    _terms = []
    _posids = []
    for term, posid in zip(terms, posids):
        if condition(posid):
            _terms.append(term)
            _posids.append(posids)
    return _terms, _posids

def select_noun(terms, posids):
    noun_posids = range(36, 67+1)    
    condition = lambda posid: posid in noun_posids
    return select(terms, posids, condition)
