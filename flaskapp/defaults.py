ADMINAPI_AUDIENCE = "default_adminapi_audience"
ADMINAPI_CLIENTID = "default_adminapi_clientid"
TAGTOKEN_CLIENTID = "default_tagtoken_clientid"
RATELIMIT_HEADERS_ENABLED = True
RATELIMIT_ENABLED = True
RATELIMIT_STORAGE_URL = "memory://"
RATELIMIT_DEFAULT = "80/hour,100/day,2000/year"
RATELIMIT_STRATEGY = "fixed-window-elastic-expiry"
HASHIDS_OFFSET = 0
DROP_ON_INIT = False
WSB_PORT = 5000
WSB_HOST = "localhost"
WSB_PROTOCOL = "http://"
