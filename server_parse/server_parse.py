import os
import json


class ServerParse:
    def __init__(self, directory: str) -> None:
        """Initializes class. Stores root directory to server and loads
        whitelist and server name.

        :param directory: directory containing all server files (configurations
            saves, etc.).
        :return: None
        """
        self.directory = directory

        # Strip training forward slash.
        if self.directory[-1] == '/':
            self.directory = self.directory[:-1]

        self.reload()

    def _get_world_name(self, filename: str = 'server.properties') -> str:
        """Reads the level-name property from the server properties file.

        :param filename: filename of the server properties file. Defaults to
            server.properties.
        :return: level name of server.
        """
        with open(f'{self.directory}/{filename}', 'r') as f:
            lines = f.readlines()

        # Get the line with the level name and extract the name.
        level_name_line = list(filter(lambda x: 'level-name' in x, lines))
        return level_name_line[0].split('=').strip()

    def _read_whitelist(self, filename: str = 'whitelist.json') -> object:
        """Reads the whitelist JSON file into a python dictionary and stores
        it.

        :param filename: name of the file containing whitelist information (
            player UUIDS and usernames). Defaults to whitelist.json.
        :return: Dictionary contents of whitelist file.
        """
        json_file = open(f'{self.directory}/{filename}', 'r')
        return json.load(json_file)

    def reload(self) -> None:
        """Reloads the world name and the whitelist file.

        :return: None
        """
        self.world_name = self._get_world_name()
        self.whitelist = self._read_whitelist()

    def get_uuids_and_mtime(self) -> list:
        """Creates a list of tuples containing the UUID of each player and
        their last playerdata modification time (this can be used to
        approximate their last login time).

        :return: list of tuples.
        """
        files = os.listdir(f'{self.directory}/{self.world_name}/playerdata/')

        uuids_and_mtimes = []
        for file in files:
            # Get the file content modification time (mtime).
            mtime = os.path.getmtime(
                f'{self.directory}/{self.world_name}/playerdata/{file}')

            # Use tuples because the intersertion order is deterministic.
            uuids_and_mtimes.append((file.split('.')[0], mtime))

        return uuids_and_mtimes

    def whitelist_lookup_by_uuid(self, uuid: str) -> str:
        """Looks up username from whitelist file based on the supplied UUID.

        :param uuid: UUID of the user to look up.
        :return: username corresponding to `uuid`.
        """
        matching_uuid = list(
            filter(lambda x: x['uuid'] == uuid, self.whitelist))
        return matching_uuid[0]
