from rlsdk_python import RLSDK, EventTypes
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

class BasePlugin:
    
    def __init__(self, sdk: RLSDK):
        self.name = "BasePlugin"
        self.version = "1.0"
        self.author = "John Doe"
        self.description = "This is a base plugin"
        self.sdk = sdk

    def get_name(self):
        return self.name
    

    def get_version(self):
        return self.version
    

    def get_author(self):
        return self.author
    

    def get_description(self):
        return self.description
    

    def init(self):
        print("Plugin " + self.name + " initialized")
        pass
       
       
    def override_output(self, output: SimpleControllerState, packet: GameTickPacket):
        
        # in this method you can override the output of the bot
        
        return output