import os
import codecs
import cPickle
import math
import random

from smt import IBM_model_1

   
class Document(object):
    def __init__(self, tokenizer, title, text):
        self.title_list = tokenizer.cut(title)
        self.text_list = tokenizer.cut(text)


def load_data(location='./corpus'):
    documents = []
    tokenizer = Tokenizer()
    files = [x for x in os.listdir(location) if x.endswith('.txt')]
    for f_name in files:
        f = codecs.open('%s/%s' % (location, f_name), 'r', encoding='utf-8')
        data = f.readlines()
        f.close()
        if len(data) > 2:
            title = data[0]
            text = ''.join(data[1:-1])
            keywords = data[-1]
            d = Document(tokenizer, title, text)
            if len(d.text_list):
                documents.append(d)
            else:
                print f_name
    return documents


def prepare_train_sets(documents):
    #document
    e_words = set()
    #title
    f_words = set()
    #d-t
    pairs = []
    for document in documents:
        title_list = document.title_list
        for title_word in title_list:
            f_words.add(title_word)
        text_words = document.text_list
        text_words_set = set(text_words)
        text_words_set_list = list(text_words_set)
        tf_idfs = []
        for word in text_words_set_list:
            tf = text_words.count(word)*1.0/len(text_words)
            idf = math.log(len(documents)/(len([1 for x in documents if x.text_list.count(word)]))+1)
            tf_idfs.append(tf/idf)
        tf_idfs_sum = sum(tf_idfs)
        probs = [tf_idf/tf_idfs_sum for tf_idf in tf_idfs]
        for i in range(1, len(tf_idfs)):
            probs[i] = probs[i] + probs[i-1]
        t_sentence = []
        set_length = len(text_words_set_list)
        for i in range(0, len(title_list)):
            (t, index) = (random.random(), 0)
            for p in probs:
                if p > t:
                    break
                index += 1
                if index >= set_length:
                    index = 0
            try:
                choosen = text_words_set_list[index]
            except:
                print index, set_length
            e_words.add(choosen)
            t_sentence.append(choosen)
        pairs.append((t_sentence, title_list))
    return e_words, f_words, pairs


def main():
    e_words, f_words, pairs = prepare_train_sets(load_data())
    model = IBM_model_1()
    model.train(e_words, f_words, pairs)
    f = open('smt_model.dict', 'wb')
    cPickle.dump(model.t, f)
    f.close()
        

if __name__ == '__main__': main()
