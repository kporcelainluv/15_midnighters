import requests
import datetime
from datetime import datetime
from pytz import timezone


def fetch_data_from_url(payload):
    return requests.get(url, params=payload).json()


def load_user_info(data_attempt):
    for attempt in data_attempt["records"]:
        yield {
            'username': attempt['username'],
            'timestamp': attempt['timestamp'],
            'timezone': attempt['timezone'],
        }


def get_midnighters(attempts):
    midnighters = set()
    beginning_of_midnight = 0
    end_of_midnight = 5
    for attempt in attempts:
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

    while True:
        payload = {'page': page}
        data_attempt = fetch_data_from_url(payload)
        if page < data_attempt["number_of_pages"]:
            active_devman_users = load_user_info(data_attempt)
            midnighters = get_midnighters(active_devman_users)
            for user in midnighters:
                set_of_midnighters.add(user)
            page += 1
        else:
            break

    for user in set_of_midnighters:
        print(user)
