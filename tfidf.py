from lib.mysql_connect import connect_to_mysql
from lib.storage_interface import get_all_foursquare_ids
import json
import nltk
import math

import re


class TFIDF():
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
    
    def _is_english_word(self, word):
        """default filter function"""
        if re.match("^[A-Za-z0-9_-]*$", word):
            return True
        return False
    
    def _tokenize(self,text, word_filter_function , stopwords):
        stopwords = set(stopwords)
        tokenized = self.tokenizer.tokenize(text)
        tokenized = [w.lower() for w in tokenized if w not in stopwords and word_filter_function(w)]
        return tokenized

    def compute_tfidf(self,docs, stopwords = None, word_filter_function = None, top_n_words = 20):
        if stopwords is None:
            stopwords = self.stopwords
        if word_filter_function is None:
            word_filter_function = self._is_english_word

        word_doc_freq = {} # for each word, how many docs it appears in
        global_words_freq = {}
        word_freq_list = []
        for doc in docs:
            words = self._tokenize(doc, word_filter_function, stopwords)
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
            print 'checking '
            print word_freq_list
            for w in d.keys():
                print 'word ',w,' appear ', d[w],'times and all ', word_doc_freq[w]
                score = d[w]*1.0/(1+math.log( word_doc_freq[w]  ))
                single_doc_tfidf.append( (score, w, global_words_freq[w] ) )
            docs_tfidf.append(single_doc_tfidf)
        tfidf_words = [] 
        for item in docs_tfidf:
            tfidf_words.append( sorted(item, key=lambda tup:tup[0], reverse=True)[:min(top_n_words, len(item)) ] ) 
        return tfidf_words


#docs = [" bad bad this is really a true store that NYC is a bad place", "NYC is a bad place? I don't really believe", "NYC ? you don't believe? you should", "why the fuck should I? NYC"]



#tfidf = TFIDF()
#print tfidf.compute_tfidf(docs)



def main():
    foursquare_ids = get_all_foursquare_ids()
    print foursquare_ids
    venues = {}
    cursor = connect_to_mysql()
    word_doc_freq = {}
    docs = [] 
    for id in foursquare_ids:
        sql = """select comments from venue_photo_instagram where comments is not NULL and foursquare_venue_id='"""+id + "'"
        venue_name = foursquare_ids[id]
        venues[venue_name] = {}

        cursor.execute(sql)
        res = cursor.fetchall()
        doc = ""
        for r in res:
            comments = json.loads(r['comments'])
            for sentence in comments:
                doc += sentence[1]
        docs.append(doc)
    t = TFIDF()
    res =  t.compute_tfidf(docs)
    for r in res:
        print r
    """
        for w in venues[venue_name].keys():
            if w in word_doc_freq:
                word_doc_freq[w]+=1
            else:
                word_doc_freq[w] = 1
        #comments.append( json.loads(r['comments']) )
        #print venues[venue_name]

    for venue_name in venues.keys():
        word_score = []
        words = venues[venue_name]
        for word in words:
            score = words[word]/(1+math.log(word_doc_freq[word]))
            word_score.append( (word, score) )
        
        print venue_name
        print sorted(word_score, key=lambda tup: tup[1], reverse=True)[0:5]
    """

main() 
