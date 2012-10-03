"""fetch temporal data for each hour/day/week/month from venue_stats table"""
from lib.storage_interface import get_all_foursquare_ids
from lib.storage_interface import get_all_stats

from lib.mysql_connect import connect_to_mysql
from datetime import timedelta
import datetime
import sys
import csv

def export_temporal_data(time_window, start_time, end_time):
    fetched_results = get_all_stats()
    ids = get_all_foursquare_ids()
    venue_dic = {}
    for r in ids.keys():
        venue_dic[r] = [] 
    
    cur_time = start_time
    """round time to nearest hour/day/week"""
    if time_window == 'hour':
        time_window = timedelta(hours=2)
        cur_time = cur_time - timedelta(minutes=cur_time.minute, seconds=cur_time.second, microseconds = cur_time.microsecond) + timedelta(hours=1)
    elif time_window == 'day':
        time_window = timedelta(days=1)
        cur_time = cur_time - timedelta(hours = cur_time.hour, minutes=cur_time.minute, seconds=cur_time.second, microseconds = cur_time.microsecond) + timedelta(days=1)
    elif time_window == 'week':
        time_window = timedelta(weeks=1)
        cur_time = cur_time - timedelta(hours = cur_time.hour, minutes=cur_time.minute, seconds=cur_time.second, microseconds = cur_time.microsecond)+timedelta(weeks=1)
     
    data_type = 'checkinsCount'
    time_list = []
    time_list.append('Plaza/Time')
    while cur_time > start_time and cur_time <= end_time:
        print cur_time
        time_list.append(cur_time.hour)
        for id in venue_dic.keys():
            sql = "select * from venue_stats where id =  '" + id + "' and time between '" + str(cur_time) + "' and '" + str(cur_time+time_window) +"'"
            cursor = connect_to_mysql()
            cursor.execute(sql)
            res = cursor.fetchall()
            if len(res) != 0:
                tmp = [val[data_type] for val in res ]
                value = max(tmp) - min(tmp) 
            else:
                value = 0
            venue_dic[id].append( value )
        cur_time+= time_window
    f = open('./temporal_2hour.csv', 'wt')
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow( time_list)
    
    for key in venue_dic.keys():
        venue_dic[key].insert(0, ids[key])
        writer.writerow( venue_dic[key] )
    print data_type
    print time_list
    for id in ids.keys():
        print ids[id], venue_dic[id]

def main():
    #export_temporal_data('week')
    #export_temporal_data('day')
    start_time = datetime.datetime(2012,9,30,20,00,00)
    end_time = datetime.datetime(2012,10,03,11,00,00)
    export_temporal_data('hour', start_time, end_time)
main()
