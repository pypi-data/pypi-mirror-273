import websocket
import json
import logging
import traceback
import ssl
import time
from pprint import pprint

logger = logging.getLogger(__name__)


class GameStateListener:
    def on_game_state_changed(self) -> None:
        """Called when the game state changes

        """
        pass


class ScoreboardClient:
    def __init__(self, scoreboard_server: str, scoreboard_port: int,
                 use_ssl: bool = False):
        """init

        Args:
            scoreboard_server (str): server to connect to
            scoreboard_port (int): port to connect to
        """
        self.n_messages_received = 0
        self.game_json_dict = {}
        self.exceptions = []
        self.scoreboard_server = scoreboard_server
        self.scoreboard_port = scoreboard_port
        self.is_connected_to_server = False
        self.scoreboard_version = None
        self.use_ssl = use_ssl
        # keep track of the game id so we can detect when a new game starts
        self.game_id = None

        # indicator of whether the game state has changed since the last time
        # we checked
        self.game_state_dirty = False

        # list of listeners to update when game state changes
        self.game_state_listeners = []

    def add_game_state_listener(self, listener: GameStateListener) -> None:
        """Add a listener to be notified when the game state changes

        Args:
            listener (GameStateListener): listener to add
        """
        self.game_state_listeners.append(listener)
        
    def start(self):
        """Start the websocket client
        """
        protocol = "wss" if self.use_ssl else "ws"
        n_iterations = 0
        while True:
            n_iterations += 1
            if n_iterations > 1:
                logger.info(f"Trying to reconnect to server, iteration {n_iterations}.")
            ws = websocket.WebSocketApp(#f"ws://{self.scoreboard_server}:{self.scoreboard_port}?ssl=true&ssl_cert_reqs=CERT_NONE",
                # this is the right url for wsproxy
                f"{protocol}://{self.scoreboard_server}:{self.scoreboard_port}/WS/",
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close,
                                        on_ping=self.on_ping)
            self.ws = ws
            mykwargs = {
                "ping_interval": 30
            }
            if self.use_ssl:
                mykwargs["sslopt"] = {"cert_reqs": ssl.CERT_NONE}
            ws.run_forever(
                        #, proxy_type="socks5", http_proxy_host=self.scoreboard_server
                        **mykwargs
                        )
            logger.warn("Websocket connection closed. Waiting 1s and then reconnecting...")
            time.sleep(1)
            logger.warn("Reconnecting...")
        
        
    def on_message(self, ws, message) -> None:
        """Attempt to parse a message. If it contains game state,
        update the game state.

        Args:
            ws (_type_): websocket
            message (_type_): message from the server
        """
        self.n_messages_received += 1
        try:
            message_dict = json.loads(message)
            # ignore clock updates
            #message_dict = {
            #    key: message_dict[key]
            #    for key in message_dict
            #    if not key.startswith("ScoreBoard.CurrentGame.Clock")}
            #logger.debug("About to try to load game state from message...")
            if "state" in message_dict: # we got a valid message with game state
                message_game_state_dict = message_dict["state"]

                # store scoreboard version separately, because it doesn't get resent for a new game
                if "ScoreBoard.Version(release)" in message_game_state_dict:
                    self.scoreboard_version = message_game_state_dict["ScoreBoard.Version(release)"]
                if "ScoreBoard.CurrentGame.Game" in message_game_state_dict:
                    message_game_id = message_game_state_dict["ScoreBoard.CurrentGame.Game"]
                    self.game_id = message_game_id
                    if self.game_id is not None and self.game_id != message_game_id:
                        # new game! I seem to have big trouble parsing new game data
                        # after this point, so instead get a new connection
                        ws.close()
                        logger.warning("New game! Wiping out game state. Game ID: " + message_game_id)
                        self.game_json_dict = {}
                        self.start()
                        return
                if "state" in self.game_json_dict: # if we already have a game state...
                     # Update the game json.
                    # first, remove any keys that are overwritten by null values in the message.
                    # This gets a bit complicated. Frank says:
                    # A key being set to null should delete
                    # * an exact match
                    # * anything that starts with the key followed by a . (Keys sent will not end with a .)
                    if "ScoreBoard.Version(release)" in message_game_state_dict:
                        self.scoreboard_version = message_game_state_dict["ScoreBoard.Version(release)"]
                    nullvalue_message_keys = [key for key in message_game_state_dict
                                              if message_game_state_dict[key] is None] 
                    for key in nullvalue_message_keys:
                        if key in self.game_json_dict["state"]:
                            del self.game_json_dict["state"][key]
                        for state_key in self.game_json_dict["state"]:
                            if state_key.startswith(key + "."):
                                del self.game_json_dict["state"][state_key]

                    # Special handling for current jammer. If the jam has just ended, null out
                    # the current jammers. There are no known jammers until they're redefined
                    # for the next jam.
                    if 'ScoreBoard.Clock(Jam).Running' in message_game_state_dict and \
                      not message_game_state_dict['ScoreBoard.Clock(Jam).Running']:
                        for team_number in (1, 2):
                            for akey in [
                                f"ScoreBoard.Team({team_number}).Position(Jammer).Name",
                                f"ScoreBoard.Team({team_number}).Position(Jammer).RosterNumber"
                            ]:
                                try:
                                    del self.game_json_dict["state"][akey]
                                except Exception:
                                    pass

                    # now, add all the new data from the message.
                    for key in message_game_state_dict:
                        if message_game_state_dict[key] is not None:
                            self.game_json_dict["state"][key] = message_game_state_dict[key]
                else:
                    logger.debug("Replacing game_json_dict with message_dict")
                    self.game_json_dict = message_dict
                # determine whether there was a meaningful change to the game state
                for key in message_game_state_dict:
                    if not key.startswith("ScoreBoard.CurrentGame.Clock") and key != "ScoreBoard.Version(release)":
                        self.game_state_dirty = True
                        #pprint(message_dict, indent=4)
                        logger.debug(f"Setting game state dirty because {key}. Updating listeners.")
                        for listener in self.game_state_listeners:
                            listener.on_game_state_changed()
                        break
            #logger.debug("Loaded game state from message.")
        except Exception as e:
            self.exceptions.append(e)
            formatted_lines = traceback.format_exc().splitlines()
            for line in formatted_lines:
                print("EXC: " + line)
        # if game doesn't have a scoreboard version, but we do, add it to the game state
        if "ScoreBoard.Version(release)" not in self.game_json_dict["state"]:
            logger.debug(f"game state missing scoreboard version. In hand: {self.scoreboard_version}")
            if self.scoreboard_version is not None:
                logger.debug(f"Adding scoreboard version to message: {self.scoreboard_version}")
                self.game_json_dict["state"]["ScoreBoard.Version(release)"] = self.scoreboard_version

        
    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning(f"### websocket closed: code={close_status_code}, msg={close_msg} ###")
        self.is_connected_to_server = False
        # try to clean up the socket connection
        try:
            logger.info("Closing ws...")
            ws.keep_running = False
            ws.close()
            logger.info("ws closed.")
        except Exception as e:
            logger.warning(f"ws.close() failed: {e}")
        # wait a second
        time.sleep(1)
        
    def on_ping(self, ws):
        self.send_custom_message(ws, { "action": "Ping" })

    def on_open(self, ws):
        """Send the registration message to the server

        Args:
            ws (_type_): websocket
        """
        logger.info("Opened connection.")
        self.send_custom_message(ws,
        {
          "action": "Register",
          "paths": [
              "ScoreBoard.Version(release)",
              "ScoreBoard.CurrentGame",
          ]
        })
        self.is_connected_to_server = True
        logger.debug("Sent registration message")

    def send_custom_message(self, ws, msg):
        msg_json = json.dumps(msg)
        if ws and ws.sock.connected:
            ws.send(msg_json)
        else:
            logger.debug("ws api is not connected.")