import os
import time
import json
import requests
import schedule
import configparser

from server_parse import ServerParse
from player_filter import PlayerFilter


def reload_and_push(url: str,
                    server_data: ServerParse,
                    player_data: PlayerFilter) -> None:
    """Generates message containing all flagged players and sends the message
    to the specified webhook URL.
    """
    # Reload data from the server (in case something was changed) and get list
    # of players to send to Discord webhook.
    server_data.reload()
    flagged_players = player_data.run()

    embedded_message = '**Format:** __Username__: __Last Logged In__\n\n'
    for player in flagged_players:
        if player[0]:
            embedded_message += f'- `{player[0]["name"]}: {player[1]}`\n'

    message = {'username': 'Server Info Bot', 'content': embedded_message[:1999]}
    requests.post(url, data=json.dumps(message), headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.getenv('CONFIG_FILE'))

    # Instantiate data processing objects
    server_data = ServerParse(config.get('App', 'RootDirectory'))
    player_data = PlayerFilter(int(config.get('App', 'Threshold')),
                               server_data)

    schedule.every(int(config.get('App', 'UpdateFrequency'))).days.do(
        reload_and_push,
        config.get('App', 'WebhookURL'),
        server_data,
        player_data
        )

    while True:
        schedule.run_pending()
        time.sleep(1)

