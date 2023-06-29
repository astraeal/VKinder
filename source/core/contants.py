# CONFIG

# Path to SQLite database file
DATABASE_PATH = 'database.sqlite'

# How many users will be found per request to VK API
USERS_PER_REQUEST = 20


# VIRTUAL ENVIRONMENT VARIABLES

# Name of environment variable that stores community token for VK API
COMMUNITY_TOKEN_VAR = 'COMMUNITY_TOKEN'

# Name of environment variable that stores application token for VK API
APPLICATION_TOKEN_VAR = 'APPLICATION_TOKEN'

# Names of required evnironment variables
REQUIRED_ENV_VARS = [
    'APPLICATION_TOKEN',
    'COMMUNITY_TOKEN',
]
