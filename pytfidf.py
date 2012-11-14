from lib.mysql_connect import connect_to_mysql
from lib.storage_interface import get_all_foursquare_ids
import json
import nltk
import math
import enchant
import re

from nltk import pos_tag, word_tokenize

class TFIDF():
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.checker  = enchant.Dict("en_US") 
    def _word_filter(self, word, stopwords, global_word_freq):
        """default filter function"""
        if re.match("^[A-Za-z_]*$", word) and len(word)>=3 and word not in stopwords and global_word_freq[word] > 2 and global_word_freq[word]<500 and self.checker.check(word):  # english character? length? stopword? freq appear?
            return True
        return False
    
    def _tokenize(self,text, word_filter_function , stopwords):
        stopwords = set(stopwords)
        tokenized = self.tokenizer.tokenize(text)
        tokenized = [w.lower() for w in tokenized]
        #if w not in stopwords and word_filter_function(w)]
        return tokenized
    
    def compute_tfidf(self,docs, stopwords = None, word_filter_function = None, top_n_words = 50):
        if stopwords is None:
            stopwords = self.stopwords
        if word_filter_function is None:
            word_filter_function = self._word_filter
        word_doc_freq = {} # for each word, how many docs it appears in
        global_words_freq = {}
        word_freq_list = []
        doc_cnt = 0
        for doc in docs:
            print doc_cnt

            words = self._tokenize(doc, word_filter_function, stopwords)
            tagged_words = pos_tag(words)
            words = [w[0] for w in tagged_words if w[1]=='NN' or w[1]=='NNS']
            doc_cnt+=1
            word_freq = {}
            for w in words:
                global_words_freq[w] = global_words_freq.get(w, 0) + 1
                word_freq[w] = word_freq.get(w,0) + 1
            word_freq_list.append( word_freq )
            for w in set(words):
                word_doc_freq[w] = word_doc_freq.get(w, 0) + 1
        docs_tfidf = []
        for d in word_freq_list:
            single_doc_tfidf = []
            for w in d.keys():
                if self._word_filter(w, stopwords, global_words_freq):
                    score = d[w]*1.0/(1+math.log( word_doc_freq[w]  ))
                    single_doc_tfidf.append( (score, w, global_words_freq[w], d[w]) )
            docs_tfidf.append(single_doc_tfidf)
        tfidf_words = [] 
        for item in docs_tfidf:
            tfidf_words.append( sorted(item, key=lambda tup:tup[0], reverse=True)[:min(top_n_words, len(item)) ] ) 
        return tfidf_words


def main():
    foursquare_ids = get_all_foursquare_ids()
    print foursquare_ids
    venues = {}
    cursor = connect_to_mysql()
    word_doc_freq = {}
    docs = [] 
    names = []
    comments_count = []
    for id in foursquare_ids:
        sql = """select caption from plazas_instaphoto where caption is not NULL and foursquare_venue_id='"""+id + "'"
        venue_name = foursquare_ids[id]
        venues[venue_name] = {}
        
        cursor.execute(sql)
        res = cursor.fetchall()
        doc = ""
        for r in res:
            comments = r['caption']
            #comments = json.loads(r['caption'])
            for sentence in comments:
                #doc += sentence[1]
                doc += sentence
        docs.append(doc)
        names.append( venue_name )
        comments_count.append( len(res) )
    t = TFIDF()
    res =  t.compute_tfidf(docs)
    for i in range(len(res) ):
        print 'Plaza name : '+names[i]
        print 'Comments for this Plaza : ' + str(comments_count[i])
        print res[i]

main() 
