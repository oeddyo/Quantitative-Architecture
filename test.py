from lib.mysql_connect import connect_to_mysql
from lib.mysql_connect import add_table_venue_meta
import foursquare
import json

client = foursquare.Foursquare(client_id='DLUNE4USSPBVIT4EHHRVELL23DPM5JREGXIXMPIF5VR5AWIB', client_secret='W30U1BPIOUY1RD0MF0EPXO2DG40URUR1E0PVP4UNUVGOFISX')

add_table_venue_meta()


#print client.users()

res =  client.venues.search(params={'limit':50,'query': 'plaza', 'near':'New York City', 'categoryId':'4bf58dd8d48988d164941735'})
res = client.venues('40a55d80f964a52020f31ee3')

print res
#print type(res['venues'])
"""

for r in res['venues']:
    print r.keys()
    print r['name']
    print '->',r['categories'][0]['name']
"""


connect_to_mysql()


