import requests
import datetime
from datetime import datetime
from pytz import timezone
import pytz


def load_attempts(url, payload):
    data_from_devman_api = requests.get(url, params=payload).json()
    pages = 1
    for page in range(pages):
        for user_info in data_from_devman_api["records"]:
            yield {
                'username': user_info['username'],
                'timestamp': user_info['timestamp'],
                'timezone': user_info['timezone'],
            }


def get_midnighters(dict_of_user):
    list_of_midnighters = []
    utc = pytz.utc
    for user_info in dict_of_user:
        user_time_zone = timezone(user_info["timezone"])
        time_stamp = user_info["timestamp"]
        fmt = '%H:%M'
        user_local_time = utc.localize(datetime.utcfromtimestamp(time_stamp))
        time_in_user_time_zone = user_local_time.astimezone(user_time_zone)
        if time_in_user_time_zone.strftime(fmt) > "00:00":
            if time_in_user_time_zone.strftime(fmt) < "05:00":
                list_of_midnighters.append(user_info["username"])
    return list_of_midnighters

if __name__ == '__main__':
    url = "https://devman.org/api/challenges/solution_attempts/"
    payload = {'page': 2}
    active_devman_users = load_attempts(url, payload)
    list_of_midnighters = get_midnighters(active_devman_users)
    print("The midnighters are: ")
    for user_name in list_of_midnighters:
        print(user_name)
