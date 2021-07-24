from config.base import *

try:
    from config.prod import *
except:
    try:
        from config.dev import *
    except:
        pass