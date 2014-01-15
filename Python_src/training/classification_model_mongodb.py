import csv as csv 
from itertools import product
import sys
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import os

train_filename = 'pre_process_train.csv'
test_filename = 'pre_process_test.csv'
output_filename = 'output.csv'
f1_output_filename = 'f1_output.csv'

title_threshold = 0.5
body_threshold = 0.4
support_threshold = 1

client = MongoClient()
db = client.kaggle_facebook

def main():
    find_all_combinations_of_words_and_tags_in_title(train_filename)
    find_all_combinations_of_words_and_tags_in_body(train_filename)
    run_model(test_filename)
    #find_best_threshold(train_filename)
    
    
def find_best_threshold(train_filename):
    global title_threshold
    global body_threshold
    for title_t in range(0, 10):
        for body_t in range(0,10):
            title_threshold = float(title_t)/float(10)
            body_threshold = float(body_t)/float(10)
            print 'thresholds are ('+str(title_threshold)+','+str(body_threshold)+')'
            test_model(train_filename)
    

def find_all_combinations_of_words_and_tags_in_title(train_filename):
    find_all_combinations_helper(train_filename,1)


def find_all_combinations_of_words_and_tags_in_body(train_filename):
    find_all_combinations_helper(train_filename,2)


def find_all_combinations_helper(train_filename,index=1):
    print 'training...'
    try:
        word_tag_combination_counter=get_word_tag_combination_counter(index)
    except IOError:
        with open(r'..'+os.path.sep+'csv'+os.path.sep+train_filename) as r, open(r'..'+os.path.sep+'csv'+os.path.sep+str(index)+'.tmp', "w") as w:
            header = r.next()
            rdr = csv.reader(r)
            for row in rdr:
                a=row[index].lower() # a string containing the title (or body)
                b=row[3].lower() # a string containing the list of tags
                for x, y in product(a.split(), b.split()):
                    w.write("{},{}\n".format(x, y))
        word_tag_combination_counter=get_word_tag_combination_counter(index)
    
	# count the combinations
    word_counter={} # key: word/tag pair, value: number of times they co-occur
    with open('..'+os.path.sep+'csv'+os.path.sep+train_filename,'rb') as file_name:
        reader=csv.reader(file_name)
        for row in reader:
            for word in row[index].lower().split():
                if word in word_counter:
                    word_counter[word]+=1
                else:
                    word_counter[word]=1
    print 'finished counting words'
    print 'dict size is '+str(len(word_tag_combination_counter))

    probabilities = db['temp'+str(index)]
    for pair in word_tag_combination_counter:
        word = pair.split()[0]
        tag = pair.split()[1]
        support = word_tag_combination_counter[pair]
        score = float(word_tag_combination_counter[pair]) / float(word_counter[word])
        if index==1:
            if score>=title_threshold and support>=support_threshold:
                probability = {'word':word,'tag':tag, 'score':score}
                probabilities.insert(probability)
        else:
            if score>=body_threshold and support>=support_threshold:
                probability = {'word':word,'tag':tag, 'score':score}
                probabilities.insert(probability)
    print 'done'


def get_word_tag_combination_counter(index=1):
    word_tag_combination_counter={}
    with open('..'+os.path.sep+'csv'+os.path.sep+str(index)+'.tmp','rb') as file_name:
        reader=csv.reader(file_name)
        for row in reader:
            pair=row[0]+' '+row[1]
            if pair in word_tag_combination_counter:
                word_tag_combination_counter[pair]+=1
            else:
                word_tag_combination_counter[pair]=1
    return word_tag_combination_counter


if __name__ == '__main__':
    main()