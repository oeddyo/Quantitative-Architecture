#!/usr/bin/python
# -*- coding: utf8 -*-
from venue_search import VenueSearch

import cherrypy
import foursquare
import config
import json
import Queue
from job import Job
class Root:
    def __init__(self):
        pass
    def return_none(self):
        return None
    return_none.exposed = True
    
    def search_venue(self, **params):
        """The user would search venue and then the results show on front-end. After that, the user would choose which venues to fetch"""
        if 'near' not in params and ( 'lon' not in params or 'lat' not in params):
            raise cherrypy.HTTPError(404);
        _search = VenueSearch()
        _res = _search.do_search(params)
        return json.dumps(_res)
    search_venue.exposed = True
    

    def get_status(self):
        client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
        all_plazas = client.venues.search(params={'near':'New York City', 'limit':50, 'intent':'browse', 'radius':5000, 'categoryId':'4bf58dd8d48988d164941735'} )
        queue = Queue.Queue()
        
        for i in range(3):
            t = Job(queue)
            t.setDaemon(True)
            t.start()
        ids = []
        for v in all_plazas['venues']:
            ids.append(v['id'])
            queue.put(v['id']) 
        queue.join()
        return "done"
        """
        """
        return 'ok'
    
    get_status.exposed = True



    def get_history(self, name):
        time_array, score_array= get_history_scores(name)
        chart = google_chart_api.LineChart(score_array)
        chart.bottom.labels = time_array
        chart.left.min = 0
        chart.left.max = 1
        chart.left.labels = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        chart.left.label_positions = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        return chart.display.Img(500, 250)
    get_history.exposed = True

    def search(self, keyword = None):
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        tmp_res = self.query_handler.query(keyword)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Content-Type'] = 'application/json'
        print cherrypy.response.headers
        if tmp_res is None:
            raise cherrypy.HTTPError(404);
        else:
            return json.dumps(tmp_res, default=dthandler)
    search.exposed = True

    def getall(self):
        res = get_daily_digest()
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Content-Type'] = 'application/json'
        
        #this part is to compute a few max values
        today_date = datetime.datetime.now( timezone('US/Eastern'))
        today_date = today_date.replace(tzinfo=None)
        max_found_days = max( [ (today_date - w['found_date']).days for w in res ] )
        max_created_days = max([ (today_date - w['created_at']).days for w in res ] )
        max_followers = max( [ w['followers_count'] for w in res])

        res_string = "["
        for e in res:
            #filter out those handlers with 0 score on server side
            if( e['score'] <=0.0001 ):
                continue
            try:
                tweets_list = json.loads(e['tweets'])
                to_return_list = []
                # only return 5 tweets for speed concern
                for i in range( min(5, len(tweets_list) ) ):
                    to_return_list.append( tweets_list[i] )
                e['tweets'] = to_return_list
            except:
                continue
            #hardcode "saved_in_db" as true for front-end's convenience
            e['saved_in_db'] = True
            
            e['hotness'] =  0.25*(1 - e['score'] ) + 0.25*(1-(today_date - e['found_date']).days*1.0/max_found_days) + 0.35*(1-(today_date - e['created_at']).days*1.0/max_created_days) + 0.15*(1- e['followers_count']*1.0/max_followers)  
            #print 'hot',e['hotness']
            
            #for safari, change the data format here
            e['found_date'] = e['found_date'].strftime("%Y/%m/%d %H:%M:%S")
            e['created_at'] = e['created_at'].strftime("%Y/%m/%d %H:%M:%S")

            res_string+= json.dumps(e, default=dthandler)
            res_string+=','
        return res_string[:-1]+']'

        #return json.dumps(res, default=dthandler)
    getall.exposed = True
    
    def set_delete(self, screen_name):
        delete_daily_digest(screen_name)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Content-Type'] = 'application/json'
    set_delete.exposed = True

    def set_like(self, screen_name):
        like_daily_digest(screen_name)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Content-Type'] = 'application/json'
    set_like.exposed = True
    
    def set_unlike(self,screen_name):
        unlike_daily_digest(screen_name)
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Content-Type'] = 'application/json'
    set_unlike.exposed = True

    def login(self, u=None, p=None):
        print type(u)
        print type(p)
        return u,p
    login.exposed = True




global_conf = {
        'global':{'server.environment': 'production',
            'engine.autoreload_on' :True,
            'engine.autoreload_frequency':5,
            'server.socket_host': '0.0.0.0',
            'server.socket_port':8080,
            }
        }

cherrypy.config.update(global_conf)

cherrypy.quickstart(Root(), '/', global_conf)
