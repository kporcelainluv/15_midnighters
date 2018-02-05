import requests
import datetime
from datetime import datetime
from pytz import timezone


def fetch_data_from_url(payload, url):
    return requests.get(url, params=payload).json()


def load_user_info(data_attempt):
    for attempt in data_attempt["records"]:
        yield {
            "username": attempt["username"],
            "timestamp": attempt["timestamp"],
            "timezone": attempt["timezone"],
        }


def get_midnighters(attempts):
    midnighters = set()
    beginning_of_midnight = 0
    end_of_midnight = 5
    for attempt in attempts:
        time_zone = timezone(attempt["timezone"])
        timestamp = attempt["timestamp"]
        user_commit_time = (datetime.fromtimestamp(timestamp, tz=time_zone))
        if beginning_of_midnight <= user_commit_time.hour <= end_of_midnight:
            midnighters.add(attempt["username"])
    return midnighters


def collect_midnighters_from_all_pages(url):
    page = 1
    set_of_all_midnighters = set()
    while True:
        payload = {"page": page}
        data_attempt = fetch_data_from_url(payload, url)
        num_of_pages = data_attempt["number_of_pages"]
        active_devman_users = load_user_info(data_attempt)
        midnighters = get_midnighters(active_devman_users)
        for user in midnighters:
            set_of_all_midnighters.add(user)
        page += 1
        if page > num_of_pages:
            break
    return set_of_all_midnighters


if __name__ == "__main__":
    url = "https://devman.org/api/challenges/solution_attempts/"
    print("The midnighters are: ")

    for user in collect_midnighters_from_all_pages(url):
        print(user)
