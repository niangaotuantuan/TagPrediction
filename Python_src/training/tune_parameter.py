import csv as csv 
from itertools import product
import sys
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import os


def run_model(test_filename):
    titles_probabilities = db['temp1']
    titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    body_probabilities.create_index([("word", ASCENDING)])
    print 'predicting...'
    test_file_object = csv.reader(open('..'+os.path.sep+'csv'+os.path.sep+test_filename, 'rb'))
    header = test_file_object.next()
    output_file = csv.writer(open('..'+os.path.sep+'csv'+os.path.sep+output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
    output_file.writerow(['Id','Tags'])
    for row in test_file_object:
        predicted_tags = []
        # find tags based on title
        for word in row[1].lower().split():
            find_result = titles_probabilities.find({'word':word})#,'score':{'$gte':title_threshold}})
            for tag_result in find_result:
                if not tag_result['tag'] in predicted_tags:
                    predicted_tags.append(tag_result['tag'])
        # find tags based on body
        for word in row[2].lower().split():
            find_result = body_probabilities.find({'word':word})#,'score':{'$gte':body_threshold}})
            for tag_result in find_result:
                if tag_result['tag'] not in predicted_tags:
                    predicted_tags.append(tag_result['tag'])
        output_file.writerow([int(row[0]),' '.join(predicted_tags)])
    print 'done'


def test_model(train_filename):
    titles_probabilities = db['temp1']
    titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    body_probabilities.create_index([("word", ASCENDING)])
    print 'testing...'
    test_file_object = csv.reader(open('..'+os.path.sep+'csv'+os.path.sep+train_filename, 'rb'))
    header = test_file_object.next()
    output_file = csv.writer(open('..'+os.path.sep+'csv'+os.path.sep+f1_output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
    output_file.writerow(['Id','F1 score'])
    max_to_test = 100
    f1_mean = 0
    i=0
    for row in test_file_object:
        predicted_tags = [] # the set of tags that will be predicted for the given post
        # find tags based on title
        for word in row[1].lower().split():
            find_result = titles_probabilities.find({'word':word,'score':{'$gte':title_threshold}})
            for tag_result in find_result:
                if not tag_result['tag'] in predicted_tags:
                    predicted_tags.append(tag_result['tag'])
        # find tags based on body
        for word in row[2].lower().split():
            find_result = body_probabilities.find({'word':word,'score':{'$gte':body_threshold}})
            for tag_result in find_result:
                if tag_result['tag'] not in predicted_tags:
                    predicted_tags.append(tag_result['tag'])
        output_file.writerow([int(row[0]),F1_score(row[3].lower().split(),predicted_tags)])
        f1_mean += F1_score(row[3].lower().split(),predicted_tags)
        i+=1
        if i==max_to_test:
            break
    print 'done, F1 mean is '+str(float(f1_mean)/float(max_to_test))

	
# kaggle use F1-score as loss function
def F1_score(tags,predicted): 
    tags = set(tags)
    predicted = set(predicted)
    tp = len(tags & predicted)
    fp = len(predicted) - tp
    fn = len(tags) - tp
 
    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
 
        return 2*((precision*recall)/(precision+recall))
    else:
        return 0


if __name__ == '__main__':
    main()