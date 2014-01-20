#Tag Prediction 

##Set up
* download data csv files [here](http://www.kaggle.com/c/facebook-recruiting-iii-keyword-extraction/data).

##Algorithm
* My original solution is based on [Alex Minnaar's blog post](http://alexminnaar.com/2013/09/14/facebook-recruiting-iii-keyword-extraction-part-1/).
* Then, I'm trying to enrich the result through Machine Translation based Keyword Extraction, which is refered to the paper Zhiyuan Liu, Xinxiong Chen, Maosong Sun. Mining the Interests of Chinese Microbloggers via Keyword Extraction. Frontiers of Computer Science, Vol. 6, No. 1, pp. 76-87, 2012.

##Instructions
* In fact, the dataset is orginally used for Keyword Extraction task, which I treated as a simple tag prediction transforming into classification problem. 
* The Keyword Extraction task can be intuitively solved by creating tags directly from the texts, using lexicon methods. But, I will not include this in this repository.

