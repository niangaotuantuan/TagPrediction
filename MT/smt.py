class IBM_model_1():

    def __init__(self):
        self.t = {}

    def train(self, e_words, f_words, pairs):
        '''
        initialize t(e|f) uniformly
        do
            set count(e|f) to 0 for all e,f
            set total(f) to 0 for all f
            for all sentence pairs (e_s,f_s)
                for all words e in e_s
                    total_s = 0
                for all words f in f_s
                    total_s += t(e|f)
                for all words e in e_s
                    for all words f in f_s
                        count(e|f) += t(e|f) / total_s
                        total(f) += t(e|f) / total_s
            for all f in domain( total(.) )
                for all e in domain( count(.|f) )
                    new t(e|f) = count(e|f) / total(f)
        until convergence
        '''
        t = self.t
        #uniform
        for e in e_words:
            for f in f_words:
                t[(e, f)] = 1.0/(len(e_words) * len(f_words))
        # do until converge
        converge = False
        while not converge:
            tp = {}
            # set count(e, f) to 0
            count = {}
            for e in e_words:
                for f in f_words:
                    count[(e, f)] = 0.0
            #set total(f) to 0
            total = {}
            for f in f_words:
                total[f] = 0.0
            # for all random sentence pairs
            for each in pairs:
                (e_s, f_s) = each
                #for all words in e_s
                total_s = {}
                for e in e_s:
                    total_s[e] = 0.0
                    # for all words in f_s
                    for f in f_s:
                        total_s[e] = total_s[e] + t[(e, f)]
                #for all words in e_s
                for e in e_s:
                    #for all words in f_s
                    for f in f_s:
                        count[(e, f)] = count[(e, f)] + (t[(e, f)]/total_s[e])
                        total[f] = total[f] + (t[(e, f)]/total_s[e])
            # for all f
            for f in f_words:
                #for all e
                for e in e_words:
                    tp[(e, f)] = count[(e, f)]/total[f]
            converge = True 
            for key in tp:
                d = abs(t[key] - tp[key])
                if d > 0.001:
                    converge = False
            t.update(tp)


if __name__ == '__main__': main()
