from os import environ

BOT_TOKEN = environ.get('BOT_TOKEN', None)
BOT_OWNER = int(environ.get('BOT_OWNER', None))
CHANNEL_ID = int(environ.get('CHANNEL_ID', None))
LOG_CHANNEL_ID = int(environ.get('LOG_CHANNEL_ID', None))
# реклама
IN_VOICES = '20'
ADDITIONAL = '10'
PG_HOST = environ.get('PG_HOST', None)
PG_DATABASE = environ.get('PG_DATABASE', None)
PG_USER = environ.get('PG_USER', None)
PG_PASSWORD = environ.get('PG_PASSWORD', None)
