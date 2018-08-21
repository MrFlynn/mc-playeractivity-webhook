# mc-playeractivity-webhook
This application reports inactive players on a given Minecraft server to a 
webhook periodically. The number of days a player is inactive, the frequency
with which to report those inactive players, as well as where to send the 
message (using a webhook) can all be configured in this program's `config.ini`.

### Usage:
1. Edit the settings in the provided example configuration file 
(`config.ini.example`) to match the settings corresponding to your needs and
the webhook the inactive player list should be posted to. **Note:** if using 
Docker, keep the `RootDirectory` setting the same.
2. Rename the file to `config.ini`.
3. If using docker, just run these commands:
```bash
$ docker build -t mc-playeractivity-webhook:latest .
$ docker run -v /path/to/server:/server mc-playeractivity-webhook:latest -d
```
4. If not using Docker, run these commands:
```bash
$ pip3 install -r requirements.txt
$ export CONFIG_FILE="config.ini"
$ python3 main.py
```