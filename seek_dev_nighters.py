import requests
import datetime
from datetime import datetime
from pytz import timezone


def fetch_data_from_url(payload):
    return requests.get(url, params=payload).json()


def load_user_info(data_attempt):
    for user_info in data_attempt["records"]:
        yield {
            'username': user_info['username'],
            'timestamp': user_info['timestamp'],
            'timezone': user_info['timezone'],
        }


def get_midnighters(users_info):
    midnighters = set()
    beginning_of_midnight = 0
    end_of_midnight = 5
    for attempt in users_info:
        user_time_zone = timezone(attempt["timezone"])
        time_stamp = attempt["timestamp"]
        user_commit_time = (datetime.fromtimestamp(time_stamp, tz=user_time_zone)).hour
        if beginning_of_midnight <= user_commit_time <= end_of_midnight:
            midnighters.add(attempt["username"])
    return midnighters


if __name__ == '__main__':
    url = "https://devman.org/api/challenges/solution_attempts/"
    print("The midnighters are: ")
    set_of_midnighters = set()
    page = 1
    number_of_pages = 1

    while page <= number_of_pages:
        payload = {'page': page}
        data_attempt = fetch_data_from_url(payload)
        number_of_pages = data_attempt["number_of_pages"]
        active_devman_users = load_user_info(data_attempt)
        midnighters = get_midnighters(active_devman_users)
        for user in midnighters:
            set_of_midnighters.add(user)
        page += 1

    for user in set_of_midnighters:
        print(user)
