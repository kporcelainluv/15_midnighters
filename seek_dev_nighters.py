import requests
import datetime
from datetime import datetime
from pytz import timezone


def extract_data_from_url(payload):
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
    for user_info in users_info:
        user_time_zone = timezone(user_info["timezone"])
        time_stamp = user_info["timestamp"]
        user_commit_time = (datetime.fromtimestamp(time_stamp, tz=user_time_zone)).hour

        beginning_of_midnight = 0
        end_of_midnight = 5
        if beginning_of_midnight <= user_commit_time <= end_of_midnight:
            midnighters.add(user_info["username"])
    return midnighters


if __name__ == '__main__':
    url = "https://devman.org/api/challenges/solution_attempts/"
    print("The midnighters are: ")
    set_of_users = set()
    page = 1
    number_of_pages = extract_data_from_url(payload={'page': page})["number_of_pages"]

    while page <= number_of_pages:
        payload = {'page': page}
        data_attempt = extract_data_from_url(payload)
        active_devman_users = load_user_info(data_attempt)
        midnighters = get_midnighters(active_devman_users)
        for user in midnighters:
            set_of_users.add(user)
        page += 1

    for user in set_of_users:
        print(user)
