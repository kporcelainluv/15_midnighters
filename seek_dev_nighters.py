import requests
import datetime
from datetime import datetime
from pytz import timezone


def load_attempts(url, payload):
    data_from_devman_api = requests.get(url, params=payload).json()
    for user_info in data_from_devman_api["records"]:
        yield {
            'username': user_info['username'],
            'timestamp': user_info['timestamp'],
            'timezone': user_info['timezone'],
        }


def get_midnighters(dict_of_users_info):
    midnighters = set()
    for user_info in dict_of_users_info:
        user_time_zone = timezone(user_info["timezone"])
        time_stamp = user_info["timestamp"]
        fmt = '%H'
        user_commit_time = datetime.fromtimestamp(time_stamp, tz=user_time_zone)
        if "00" <= user_commit_time.strftime(fmt) <= "05":
            midnighters.add(user_info["username"])
    return midnighters


if __name__ == '__main__':
    url = "https://devman.org/api/challenges/solution_attempts/"
    print("The midnighters are: ")
    for page_number in range(1, 11):
        payload = {'page': page_number}
        active_devman_users = load_attempts(url, payload)
        midnighters = get_midnighters(active_devman_users)
        for user_name in midnighters:
            print(user_name)
