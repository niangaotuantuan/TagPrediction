import cPickle
import math

f = open('smt_model.dict', 'rb')
model = cPickle.load(f)
f.close()

def tranlate_prob(w, t, model):
    w = w.encode('utf-8')
    t = t.encode('utf-8')
    if (w, t) in model.keys():
        return model[(w, t)]
    else:
        return 0

def keywords(candidates, texts):
    results = []
    for p, text in zip(candidates, texts):
        probs = []
        for t in p:
            total_value = 0
            for word in text:
                tf = text.count(word)*1.0/len(text)
                idf = math.log(len(texts)/(len([1 for x in texts if x.count(word)]))+1)
                tf_idf = tf/idf
                total_value += tranlate_prob(word, t)*tf_idf
            probs.append(total_value)
        sorted_probs = sorted(probs, reverse=True)
        keywords = []
        for value in sorted_probs:
            keywords.append(p[probs.index(value)])
        results.append(keywords)