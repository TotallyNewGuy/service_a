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
    # 'ClkLkN': 30375,
    # 'ClkLkS': 30374,
    "UICHdN": 30068,
    "UICHdS": 30069,
    "OHareS": 30172,
    "OHareN": 30171,
    "JffPkS": 30248,
    # "JffPkN": 30247,
    "FstPkN": 30076,
    "FstPkS": 30077,
}

TRAIN_TRACKER_KEY = "771cb31a8e2b49a39ebacffe2f5a7aba"