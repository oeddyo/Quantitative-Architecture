import MySQLdb

def connect_to_mysql():
    sql_conn = MySQLdb.connect(host='localhost', user='root', passwd='131415', db='quan_arch', charset='utf8', use_unicode = True)
    sql_conn.autocommit(True)
    sql_db = sql_conn.cursor(MySQLdb.cursors.DictCursor)
    return sql_db

def add_table_venue_meta():
    sql = """
    CREATE TABLE IF NOT EXISTS venue_meta(
    id VARCHAR(50) NOT NULL,
    name VARCHAR(200) ,
    lat DOUBLE ,
    lng DOUBLE ,
    postCode VARCHAR(20) ,
    city VARCHAR(100) ,
    state VARCHAR(100),
    country VARCHAR(100),
    verified BOOL,
    checkinCount INT(20),
    userCount INT(20),
    tipCount INT(20),
    url VARCHAR(500),
    likesCount INT(20),
    rating  DOUBLE,
    ratingSignals   INT(20),
    photoCount  INT(20),
    tipsCount   INT(20),
    PRIMARY KEY(id)
    )   ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)
def add_table_daily_digest():
    sql = """
    CREATE TABLE IF NOT EXISTS daily_digest(
        user_id bigint(20) unsigned NOT NULL,
        screen_name VARCHAR(100) NOT NULL DEFAULT '',
        followers_count int NOT NULL DEFAULT 0,
        created_at datetime DEFAULT NULL,
        found_date datetime DEFAULT NULL,
        description VARCHAR(500) ,
        tweets TEXT,
        deleted  TINYINT(1) NOT NULL DEFAULT 0,
        score DOUBLE NOT NULL DEFAULT 0,
        img_url VARCHAR(500)  DEFAULT '',
        url VARCHAR(500) DEFAULT '',
        mention_count INT(10)  DEFAULT 0,
        PRIMARY KEY(user_id)

    ) ENGINE InnoDB DEFAULT CHARSET=utf8;

    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_seeds():
    sql = """
    CREATE TABLE IF NOT EXISTS  seeds_updating(
    user_id bigint(20) unsigned NOT NULL,
    hub double NOT NULL DEFAULT 0,
    betweenness double NOT NULL DEFAULT 0,
    in_degree int NOT NULL DEFAULT 0,
    PRIMARY KEY(user_id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)


def add_table_prob():
    """table to store how likely a person tweet about a start-up within his latest 200 tweets"""
    sql = """
    CREATE TABLE IF NOT EXISTS user_prob_updating(
    user_id bigint(20) unsigned NOT NULL,
    prob double NOT NULL DEFAULT 0,
    PRIMARY KEY(user_id)
    ) ENGINE InnoDB DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_tweet_mention():
    sql = """
    CREATE TABLE IF NOT EXISTS tweet_mention_updating (
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    tweet_id bigint(20) unsigned NOT NULL DEFAULT '0',
    mentioned_id bigint(20) unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (id),
    KEY mentioned_id (mentioned_id),
    KEY tweet_id (tweet_id)
	) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;"""
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_tweets():

    sql = """
	CREATE TABLE IF NOT EXISTS tweets_updating (
	  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  retweet_id bigint(20) unsigned NOT NULL,
	  twitter_id bigint(20) unsigned NOT NULL,
	  user_id bigint(20) unsigned DEFAULT NULL,
	  text text,
	  language varchar(50) DEFAULT NULL,
	  screen_name varchar(50) DEFAULT NULL,
	  location text,
	  in_reply_to_status_id bigint(20) unsigned DEFAULT NULL,
	  in_reply_to_user_id bigint(20) unsigned DEFAULT NULL,
	  retweet_user_id bigint(20) unsigned DEFAULT NULL,
	  truncated tinyint(1) DEFAULT '0',
	  in_reply_to_screen_name varchar(50) DEFAULT NULL,
	  created_at datetime DEFAULT NULL,
	  retweet_count int(11) DEFAULT NULL,
	  lat varchar(50) DEFAULT NULL,
	  lon varchar(50) DEFAULT NULL,
	  profile_image_url varchar(500) DEFAULT NULL,
	  source text,
	  retweeted tinyint(1) DEFAULT '0',
	  coordinates blob,
	  favorited tinyint(1) DEFAULT '0',
	  geo blob,
        place blob,
      mention_index varchar(300) DEFAULT '',
	  PRIMARY KEY (id),
	  UNIQUE KEY unique_tweet (twitter_id),
	  KEY index_tweet (twitter_id),
	  KEY twitter_id_dataset_id (twitter_id),
	  KEY in_reply_to_status_id (in_reply_to_status_id),
	  KEY in_reply_to_status_id_created_at (in_reply_to_status_id,created_at),
	  KEY in_reply_to_user_id (in_reply_to_user_id),
	  KEY in_reply_to_screen_name (in_reply_to_screen_name),
	  KEY in_reply_to_user_id_created_at (in_reply_to_user_id,created_at),
	  KEY retweet_count (retweet_count),
	  KEY screen_name (screen_name),
	  KEY user_id (user_id)
	) ENGINE=MYISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
	""" 
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_friendships():

    sql = """
	CREATE TABLE IF NOT EXISTS friendships_updating (
	  id int(10) unsigned NOT NULL AUTO_INCREMENT,
	  follower_user_id bigint(20) unsigned DEFAULT NULL,
	  followed_user_id bigint(20) unsigned DEFAULT NULL,
	  PRIMARY KEY (id),
	  KEY followed_user_id (followed_user_id),
	  KEY follower_user_id (follower_user_id)
	) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
	""" 
    sql = """
	CREATE TABLE IF NOT EXISTS friendships_updating (
	  follower_user_id bigint(20) unsigned NOT NULL,
	  followed_user_id bigint(20) unsigned NOT NULL,
	  PRIMARY KEY (follower_user_id, followed_user_id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	""" 
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_users():
    sql = """
	CREATE TABLE IF NOT EXISTS users_updating (
	  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	  user_id bigint(20) unsigned NOT NULL DEFAULT '0',
	  verified tinyint(1) NOT NULL DEFAULT '0',
	  profile_image_url text,
	  geo_enabled tinyint(1) NOT NULL DEFAULT '0',
	  followers_count int(11) NOT NULL,
	  protected tinyint(1) NOT NULL DEFAULT '0',
	  location text,
	  listed_count int(11) NOT NULL,
	  utc_offset int(11) DEFAULT '0',
	  statuses_count int(11) NOT NULL,
	  description text,
	  friends_count int(11) NOT NULL,
	  screen_name varchar(50) NOT NULL,
	  lang varchar(50) DEFAULT NULL,
	  favourites_count int(11) NOT NULL,
	  name varchar(50) NOT NULL,
	  url varchar(255) DEFAULT NULL,
	  created_at datetime NOT NULL,
	  time_zone varchar(50) DEFAULT NULL,
	  UNIQUE KEY id (id),
	  UNIQUE KEY user_id (user_id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """ 
    cursor = connect_to_mysql()
    cursor.execute(sql)


















def add_table_entities():
    sql = """
	CREATE TABLE IF NOT EXISTS entities (
	  id int(10) unsigned NOT NULL,
	  user_id bigint(20) unsigned DEFAULT NULL,
	  name varchar(50) DEFAULT NULL,
	  screen_name varchar(50) DEFAULT NULL,
	  indices varchar(255) DEFAULT NULL,
	  text text,
	  url varchar(255) DEFAULT NULL,
	  expanded_url varchar(255) DEFAULT NULL,
	  display_url varchar(255) DEFAULT NULL,
	  type varchar(50) NOT NULL DEFAULT '',
	  entity_id int(11) unsigned NOT NULL AUTO_INCREMENT,
	  PRIMARY KEY (entity_id),
	  KEY id (id)
	) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
	""" 
    cursor = connect_to_mysql() 
    cursor.execute(sql)

def add_table_locations():

    sql = """

	CREATE TABLE IF NOT EXISTS locations (
	    user_id bigint(20) NOT NULL DEFAULT '0',
	    screen_name varchar(50) DEFAULT NULL,
	    location text,
	    city varchar(50) DEFAULT NULL,
	    country varchar(50) DEFAULT NULL,
	    state varchar(50) DEFAULT NULL,
	    lat varchar(50) DEFAULT NULL,
	    lon varchar(50) DEFAULT NULL,
	    PRIMARY KEY (user_id)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    """ 
    cursor = connect_to_mysql()
    cursor.execute(sql)


def add_table_urls():
    sql = """
    CREATE TABLE IF NOT EXISTS urls(
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    user_id  bigint(20) unsigned NOT NULL DEFAULT '0',
    score double NOT NULL DEFAULT 0,
    url VARCHAR(100) NOT NULL DEFAULT '',
    PRIMARY KEY(id),
    KEY user_id (user_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
    """
    cursor = connect_to_mysql()
    cursor.execute(sql)

def add_table_urls_from_tweets():
    sql = """
    CREATE TABLE IF NOT EXISTS urls_from_tweets(
    url VARCHAR(200) NOT NULL DEFAULT '',
    tweet_id bigint(20) unsigned NOT NULL DEFAULT '0',
    created_at datetime DEFAULT NULL,
    PRIMARY KEY (tweet_id)
    )ENGINE=InnoDB  DEFAULT CHARSET=utf8;"""
    cursor = connect_to_mysql()
    cursor.execute(sql)

