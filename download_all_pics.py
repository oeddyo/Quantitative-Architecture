from lib.mysql_connect import connect_to_mysql

from urllib import urlretrieve
import os

def downloader():
    sql = "select venue_photo_4sq.url as url, venue_meta.name as name from venue_photo_4sq, venue_meta where venue_photo_4sq.venue_id = venue_meta.id"
    cursor =  connect_to_mysql()
    cursor.execute(sql)
    rows = cursor.fetchall()
    my_cnt = 0
    files_dic = {}
    for r in rows:
        if r['name'] not in files_dic:
            files_dic[r['name']] = []
        else:
            files_dic[r['name']].append( r['url'] )
    
    for k in files_dic.keys():
        os.mkdir('/Users/eddiexie/work/quan_arch/pics/'+k)
        pic_count = 0
        for _url in files_dic[k]:
            try:
                pic_count+=1
                print 'working on %s\t %d'%(_url, pic_count)
                out_path = '/Users/eddiexie/work/quan_arch/pics/'+k+'/'+str(pic_count)+'.jpg'
                urlretrieve(_url, out_path)
            except:
                continue

downloader()
