from lib.mysql_connect import connect_to_mysql
from lib.storage_interface import get_all_foursquare_ids
import json
import nltk
import math

import re

def is_english_word(word):
    if re.match("^[A-Za-z0-9_-]*$", word):
        return True
    return False

def tokenize(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tokenized = tokenizer.tokenize(text)
    tokenized = [w.lower() for w in tokenized if w not in stopwords and is_english_word(w)]
    return tokenized

def main():
    foursquare_ids = get_all_foursquare_ids()
    print foursquare_ids
    venues = {}
    cursor = connect_to_mysql()
    word_doc_freq = {}
    global_word_freq = {}
    for id in foursquare_ids:
        sql = """select caption from plazas_instaphoto where caption is not NULL and foursquare_venue_id='"""+id + "'"
        venue_name = foursquare_ids[id]
        venues[venue_name] = {}

        cursor.execute(sql)
        res = cursor.fetchall()
        for r in res:
            comments = [r['caption']]
            for sentence in comments:
                words = tokenize(sentence)
                for word in words:
                    if word in global_word_freq:
                        global_word_freq[word]+=1
                    else:
                        global_word_freq[word] = 1

                    if word in venues[venue_name]:
                        venues[venue_name][word] += 1
                    else:
                        venues[venue_name][word] = 1
        for w in venues[venue_name].keys():
            if w in word_doc_freq:
                word_doc_freq[w]+=1
            else:
                word_doc_freq[w] = 1
    too_common_word = set()
    for word in sorted(global_word_freq.items(), key = lambda tup: tup[1], reverse=True)[:300]:
        too_common_word.add(word[0])
    for venue_name in venues.keys():
        word_score = []
        words = venues[venue_name]
        for word in words:
            score = words[word]/(1+math.log(word_doc_freq[word]))
            if word not in too_common_word:
                word_score.append( (word, score, words[word]) )
        
        print venue_name.encode('utf-8','ignore')
        print sorted(word_score, key=lambda tup: tup[1], reverse=True)[0:50]
main() 

    
    
