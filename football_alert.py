import json
import os
from datetime import datetime, timezone

import requests
from twilio.rest import Client

CLUBS = {
    'Real Madrid': 541,
    'Atletico Madrid': 530,
    'Manchester United': 33,
}

headers = {
    'X-RapidAPI-Key': os.getenv('X-RapidAPI-Key'),
    'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com',
}

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_sms(body):
    message = client.messages.create(
        body=body,
        from_=os.getenv('TWILIO_FROM_PHONE'),
        to=os.getenv('TWILIO_TO_PHONE'),
    )

    print(message.sid)


def write_to_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def read_from_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data


def write_fixtures_to_json_files():
    for club_name, club_id in CLUBS.items():
        data = get_team_fixtures(club_id)
        write_to_json_file(data, f'{club_name}.json')


def search_team(name):
    url = 'https://api-football-v1.p.rapidapi.com/v3/teams'

    querystring = {'search': name}

    response = requests.request(
        'GET', url, headers=headers, params=querystring
    )

    return response.json()


def get_team_fixtures(team_id):

    url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'

    querystring = {'season': '2022', 'team': str(team_id)}

    response = requests.request(
        'GET', url, headers=headers, params=querystring
    )

    return response.json()


def get_how_many_minutes_remaing(date):
    now = datetime.now(timezone.utc)
    date = datetime.fromisoformat(date)
    remaing = date - now
    minutes = remaing.total_seconds() / 60
    return minutes


def main():
    for club_name in CLUBS.keys():
        data = read_from_json_file(f'{club_name}.json')
        fixtures = data['response']
        for fixture in fixtures:
            date = fixture['fixture']['date']
            minutes = int(get_how_many_minutes_remaing(date))
            if minutes >= -60 and minutes <= 60:
                home = fixture['teams']['home']['name']
                away = fixture['teams']['away']['name']
                body = f"""Hi, Edilson,

                {home} x {away} starts in {minutes} minutes.

                I think you may want to watch this game :)

                Best Regards,
                Bot
                """
                send_sms(body)
                print(f'{home} x {away} starts in {minutes} minutes')
                print()
