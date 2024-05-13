from rlsdk_python import RLSDK, EventTypes
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from colorama import Fore, Style

class MarlbotAPI:
    def __init__(self, sdk, plugin):
        self.plugin = plugin
        self.sdk = sdk
        
    def get_sdk(self):
        return self.sdk
    
    def on(self, event_type, callback):
        self.sdk.subscribe(event_type, callback)
        
    def off(self, event_type, callback):
        self.sdk.unsubscribe(event_type, callback)
        
    def log(self, message):
        print(Fore.GREEN + "[" + self.plugin.get_name() + "] " + Fore.RESET + message + Style.RESET_ALL)

class BasePlugin:
    
    def __init__(self):
        self.name = "BasePlugin"
        self.version = "1.0"
        self.author = "MarlburroW"
        self.description = "No description"
        self.api: MarlbotAPI = None
       

    def get_name(self):
        return self.name
    
    def get_version(self):
        return self.version

    def get_author(self):
        return self.author
    
    def get_description(self):
        return self.description
    
    def init(self):
        self.api.log("Plugin " + self.name + " initialized")
        pass
    
    def destroy(self):
        self.api.log("Plugin " + self.name + " destroyed")
        pass
       
    def override_output(self, output: SimpleControllerState, packet: GameTickPacket):
        # in this method you can override the output of the bot    
        return output
    
    
    def on_tick(self, packet: GameTickPacket):
        # this method is called every tick
        pass
    
    
    def set_api(self, api: MarlbotAPI):
        self.api = api


