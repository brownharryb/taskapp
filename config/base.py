import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


GEOCODE_API = 'http://geocode-maps.yandex.ru/1.x/'
GEOCODE_REQUEST_TIMEOUT = 5

LOG_FILENAME = os.path.join(BASEDIR, 'task.log')

# GEO COORDINATE FORMAT PATTERNS
GEO_COORDINATE_FORMATS = [
    r'^-?([1-9]+)(\.)(\d+),-?([1-9]+)(\.)(\d+)$',  # float, float pattern
    r'^(N|S|E|W)([1-9]+)(\.)(\d+),(N|S|E|W)([1-9]+)(\.)(\d+)$',  # float[direction],float[direction]
    r'^([1-9]+)(\.)(\d+)(,?)(N|S|E|W),([1-9]+)(\.)(\d+)(,?)(N|S|E|W)$',  # float[direction],float[direction]
    r'^(-?)([1-9]+)(\.|)(\d+)°(\d+)(\.|)(\d+)(\'|\′)(\d+)(\.|)(\d+)("|″)(N|S|E|W|),'
    r'(-?)([1-9]+)(\.|)(\d+)°(\d+)(\.|)(\d+)(\'|\′)(\d+)(\.|)(\d+)("|″)(N|S|E|W|)'
]

SESSION_COOKIE_SECURE = False
