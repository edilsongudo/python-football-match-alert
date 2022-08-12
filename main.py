import json
import os
from datetime import datetime, timezone

import requests

headers = {
    'X-RapidAPI-Key': os.getenv('X-RapidAPI-Key'),
    'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com',
}


def write_to_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def read_from_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data


def search_team(name):
    url = 'https://api-football-v1.p.rapidapi.com/v3/teams'

    querystring = {'search': name}

    response = requests.request(
        'GET', url, headers=headers, params=querystring
    )

    return response.json()


def get_team_fixtures(team_id):
    """
    33 - Manchester United
    530 - Atletico Madrid
    541 - Real Madrid
    """

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
