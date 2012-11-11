from pytfidf import TFIDF
from lib.mysql_connect import connect_to_mysql
import json

def main():
    sql = "select manhattan_venues_meta.id as id,  venue_photo_instagram.comments as comment, categoriesName as cate from manhattan_venues_meta, venue_photo_instagram where manhattan_venues_meta.id = venue_photo_instagram.foursquare_venue_id and venue_photo_instagram.comments is not NULL  "
    
    cursor = connect_to_mysql()
    cursor.execute(sql)
    comments = {}
    counter = {}
    for r in cursor.fetchall():
        if r['id'] in counter:
            counter[r['id']]+=1
        else:
            counter[r['id']] = 1
        if counter[r['id']]>300:
            continue
        cmts =  json.loads(r['comment'])
        cate = r['cate']
        if cate not in comments:
            comments[cate] = ""
        else:
            for cmt in cmts:
                comments[cate]+=cmt[1]
    #print comments
    print 'doc construction done'
    cate_names = []
    docs = []
    for k in comments.keys():
        cate_names.append(k)
        docs.append(comments[k].encode("utf-8",'ignore'))
    tf_idf = TFIDF()
    print 'begin compute'
    words_list = tf_idf.compute_tfidf(docs, top_n_words=500)
    for i in range(len(cate_names)):
        #cate_names[i][1] = cate_names[i][1].encode("utf-8", 'ignore')
        #cate_names[i] = (cate_names[i][0], cate_names[i][1].encode('utf-8', 'ignore'), cate_names[i][2])

        print cate_names[i].encode('utf-8', 'ignore')
        print words_list[i]
main()
