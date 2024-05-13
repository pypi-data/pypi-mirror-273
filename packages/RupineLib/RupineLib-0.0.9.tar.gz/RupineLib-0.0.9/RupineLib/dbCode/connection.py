import psycopg2

def connect(user,pw,host,Port,database):
    heroku_db_url = "postgres://{}:{}@{}:{}/{}".format(user,pw,host,Port,database)
    connection =  psycopg2.connect(heroku_db_url, sslmode='require')
    return connection

def connectURI(connectionStr):
    connection =  psycopg2.connect(connectionStr, sslmode='require')
    return connection
