from zoneinfo import ZoneInfo

TZINFO = ZoneInfo('America/Chicago')
TRAIN_BASE_URL = "http://lapi.transitchicago.com/api/1.0/"
ROUTE = "Blue"
cta_day_type = {
    "Weekday": 1,
    "Saturday": 2,
    "Sunday": 3,
}

stop_map = {
    "UICHdN": 30068,
    "UICHdS": 30069,
    "OHareS": 30172,
    "OHareN": 30171,
    "JffPkS": 30248,
    "FstPkN": 30076,
    "FstPkS": 30077,
}