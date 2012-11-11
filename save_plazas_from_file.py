from lib.mysql_connect import connect_to_mysql

lines =  open('plazas.csv').readlines()
cursor = connect_to_mysql()
for line in lines[1:]:
    venue_id = line.strip()
    cursor.execute("REPLACE INTO plazas (id) values (%s) ",(venue_id) )


