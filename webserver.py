#!/usr/bin/python
# -*- coding: utf8 -*-
from venue_search import VenueSearch

import cherrypy
import foursquare
import config
import json
import Queue
from job import Job
import threading
from threading import Thread
import time
from lib.mysql_connect import add_table_venue_meta
from lib.mysql_connect import add_table_venue_photo_4sq


class Root:
    def __init__(self):
        self.jobs = {}
        self.next_job_id = 0
        add_table_venue_meta()
        add_table_venue_photo_4sq()
        self.downloading = threading.Event()
        t = Thread(target = self.infinit_consume)
        t.setDaemon(True)
        t.start()
    def infinit_consume(self):
        while True:
            print 'in infinite loop, try to consume'
            self.consume()
            time.sleep(5)
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
    
    def consume(self):
        print 'Try to consuming'
        if self.downloading.isSet():
            print 'Busy, next time, and I quit'
        for job_id in sorted(self.jobs.keys()):
            if self.jobs[job_id].status=='Wating' and not self.downloading.isSet():
                print 'free and now I could process ', job_id
                self.downloading.set()
                job = self.jobs[job_id]
                t = Thread(target = job.submit, args=(self.downloading,))
                t.start()
 
    def submit_job(self, ids_string):
        if type(ids_string) is not unicode:
            raise cherrypy.HTTPError(404);
        ids = ids_string.split(',')
        ids = [str(id) for id in ids]
        #client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
        #all_plazas = client.venues.search(params={'near':'New York City', 'limit':50, 'intent':'browse', 'radius':5000, 'categoryId':'4bf58dd8d48988d164941735'} )
        #ids = []
        #for v in all_plazas['venues']:
        #    ids.append(v['id'])
        job = Job(ids) 
        self.jobs[self.next_job_id] = job
        self.next_job_id += 1
        return 'job submitted' 
    submit_job.exposed = True

    def get_jobs_status(self):
        reports = []
        for k in self.jobs.keys():
            reports.append(self.jobs[k].report())
        return json.dumps(reports)
    get_jobs_status.exposed = True
    
global_conf = {
        'global':{'server.environment': 'production',
            'engine.autoreload_on': True,
            'engine.autoreload_frequency':5,
            'server.socket_host': '0.0.0.0',
            'server.socket_port':8080,
            }
        }

cherrypy.config.update(global_conf)
cherrypy.quickstart(Root(), '/', global_conf)
