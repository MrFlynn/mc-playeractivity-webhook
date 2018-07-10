import server_parse
import itertools

from datetime import timedelta, datetime


class PlayerFilter:
    def __init__(self,
                 num_days: int,
                 server_data: server_parse.ServerParse) -> None:
        """Initializes filter class. Stores number of days since cutoff and
        instance of ServerParse class.

        :param num_days: number of days preceeding current date for cutoff.
        :param server_data: instance of ServerParse class. Access to whitelist,
            server_name, and player data.
        :return: None
        """
        self.num_days = num_days
        self.server_data = server_data

    def _get_outdated_players(self) -> list:
        """Returns a list of players who haven't been on the server since the
        cutoff date.

        :return: list of tuples, each with player UUIDs and last active time.
        """
        full_player_list = self.server_data.get_uuids_and_mtime()
        cutoff_date = timedelta(days=-self.num_days)  # Date -n days ago.

        return list(filter(
            lambda x: datetime.fromtimestamp(x[1]) < cutoff_date,
            full_player_list))

    def _never_logged_players(self) -> list:
        """Creates a list of players who have never logged in.

        :return: list of player UUIDs.
        """
        # List of UUIDs of players who have playerdata files.
        # pylint: disable=E1136
        player_uuids = list(zip(*self.server_data.get_uuids_and_mtime)[0])

        all_player_uuids = []
        for player in self.server_data.whitelist:
            all_player_uuids.append(player['uuid'])

        # Returns set difference of all players and those who have played.
        return list(set(all_player_uuids) - set(player_uuids))

    def run(self) -> list:
        """Generates a list of names and dates (or never if they haven't joined
        ) of players that should be posted to the webhook.

        :return: list of tuples with player names and their last active date.
        """
        # Get UUIDs of all players that need to be flagged as inactive.
        outdated_players = self._get_outdated_players()
        never_logged_in = self._never_logged_players()

        # Final list of all players usernames and their last active time.
        flagged_players = []

        # Get list of players usernames who have logged in, but not since the
        # cutoff.
        for player in outdated_players:
            username = self.server_data.whitelist_lookup_by_uuid(player[0])
            date_string = datetime.fromtimestamp(player[1]).date().isoformat()

            flagged_players.append((username, date_string))

        # Get list of players who have never logged in.
        flagged_players.extend(
            [(self.server_data.whitelist_lookup_by_uuid(n),
                'Never.') for n in never_logged_in]
            )

        return flagged_players
