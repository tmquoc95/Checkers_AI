class TimeUp(Exception):
    pass

try:
    raise TimeUp()
except (TimeUp):
    print ("OK")