import requests
import datetime
from datetime import datetime
from pytz import timezone
import pytz


def load_attempts():
    url = "https://devman.org/api/challenges/solution_attempts/?page=2"
    info = requests.get(url).json()
    pages = 1
    for page in range(pages):
        for user_info in info["records"]:
            yield {
                'username': user_info['username'],
                'timestamp': user_info['timestamp'],
                'timezone': user_info['timezone'],
            }


def get_midnighters(dict_of_users):
    utc = pytz.utc
    for user_info in dict_of_users:
        user_time_zone = timezone(user_info["timezone"])
        time_stamp = user_info["timestamp"]
        fmt = '%H:%M'
        local_time = utc.localize(datetime.utcfromtimestamp(time_stamp))
        time_in_user_time_zone = local_time.astimezone(user_time_zone)
        if time_in_user_time_zone.strftime(fmt) > "00:00":
            if time_in_user_time_zone.strftime(fmt) < "05:00":
                print(user_info["username"])

if __name__ == '__main__':
    print("The midnighters are: ")
    midnighters = load_attempts()
    get_midnighters(midnighters)
