"""
Download all the plazas metas for all the ids in plazas
"""

from lib.foursqure_wrapper import download_meta_data
from lib.mysql_connect import connect_to_mysql

def main():
    sql = "select id from plazas"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    for r in cursor.fetchall():
        venue_meta = download_meta_data(r['id'])
        save_venue_meta(venue_meta, table = 'plazas_meta')

main()
