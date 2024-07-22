import time
import json
from valclient.client import Client
import threading
import os
import keyboard

dictionary = {
import time
import json
from valclient.client import Client
import threading
import os
import keyboard

# Default configuration dictionary
dictionary = {
    "instantlocker": {
        "region": "na",
        "preferred_agent": "",
        "save_config": True
    }
}

# Path to config file
cfg_path = "config.json"

# Function to setup initial config file
def setup_config():
    while True:
        save_config = input("Do you want to save the configuration? (yes/no): ").strip().lower()
        if save_config in ["yes", "no"]:
            dictionary['instantlocker']['save_config'] = (save_config == "yes")
            break
        else:
            print("Please enter 'yes' or 'no'.")

    if dictionary['instantlocker']['save_config']:
        while True:
            preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
            if preferred_agent in ValorantAgentInstalocker.agents:
                dictionary['instantlocker']['preferred_agent'] = preferred_agent
                break
            else:
                print("Please enter a valid agent name.")

        with open(cfg_path, "w") as f:
            f.write(json.dumps(dictionary, indent=4))

# Function to load existing config file
def load_config():
    if not os.path.exists(cfg_path):
        setup_config()
        time.sleep(2)

    with open(cfg_path) as json_file:
        config_data = json.load(json_file)

    instantlocker_config = config_data.get('instantlocker', {})
    if instantlocker_config.get('save_config') and ('preferred_agent' not in instantlocker_config or not instantlocker_config['preferred_agent']):
        print("No agent found in config")
        time.sleep(2)
        os._exit(0)

    return config_data

# Class to handle Valorant agent instalocker
class ValorantAgentInstalocker:
    agents = {
        "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
        "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
        "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
        "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
        "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
        "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
        "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
        "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
        "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
        "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
        "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
        "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
        "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
        "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
        "omen": "8e253930-4c05-31dd-1b6c-968525494517",
        "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
        "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
        "viper": "707eab51-4836-f488-046a-cda6bf494859",
        "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
        "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
        "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
        "deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
        "iso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
        "clove": "1dbf2edd-4729-0984-3115-daa5eed44993"
    }

    def __init__(self, region, preferred_agent):
        self.region = region.lower()
        self.preferred_agent = preferred_agent
        self.seenMatches = []
        self.pause_instalock = False

        if not self.is_valid_agent(self.preferred_agent):
            print("Invalid agent in config")
            time.sleep(2)
            os._exit(0)

    def is_valid_agent(self, agent):
        return agent in self.agents

    def initialize_client(self):
        while True:
            try:
                self.client = Client(region=self.region)
                self.client.activate()
                self.run_instalocker()
            except Exception as e:
                time.sleep(2)

    def choose_preferred_agent(self):
        return self.preferred_agent

    def run_instalocker(self):
        while True:
            time.sleep(0.01)
            try:
                if self.pause_instalock:
                    continue

                session_state = self.client.fetch_presence(self.client.puuid)['sessionLoopState']
                match_id = self.client.pregame_fetch_match()['ID']

                if session_state == "PREGAME" and match_id not in self.seenMatches:
                    start_time = time.time()
                    agent_id = self.agents[self.preferred_agent]
                    self.client.pregame_select_character(agent_id)
                    self.client.pregame_lock_character(agent_id)
                    end_time = time.time()
                    duration = end_time - start_time
                    self.seenMatches.append(match_id)
                    print(f"Locked {self.preferred_agent.capitalize()} in {duration:.2f} seconds")
                    self.pause_instalock = True
                    print("InstaLocker paused. F10 to resume.")
            except Exception as e:
                return []

    def toggle_pause(self):
        self.pause_instalock = not self.pause_instalock
        state = "paused" if self.pause_instalock else "running"
        print(f"InstaLocker {state}")


# Function to handle the initial setup and key validation
def main():
    global data  # Declare data as global to use in this function
    data = load_config()
    try:
        enable_instalock = data['instantlocker']
        if data['instantlocker']['save_config']:
            preferred_agent = data['instantlocker']["preferred_agent"].lower()
        else:
            while True:
                preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
                if preferred_agent in ValorantAgentInstalocker.agents:
                    break
                else:
                    print("Please enter a valid agent name.")
    except KeyError:
        os._exit(0)

    instantlocker_instance = ValorantAgentInstalocker(region=data['instantlocker']["region"], preferred_agent=preferred_agent)
    instantlock_thread = threading.Thread(target=instantlocker_instance.initialize_client)
    instantlock_thread.daemon = True
    instantlock_thread.start()

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for cleaner output
    print(f"InstaLocker started")
    print(f"Lock agent: {preferred_agent.capitalize()}\n")

    # Continuously monitor keyboard inputs
    while True:
        if keyboard.is_pressed("ctrl+shift+x"):
            os._exit(0)
        if keyboard.is_pressed("f10"):
            instantlocker_instance.toggle_pause()
            time.sleep(0.5)  # To prevent multiple toggles from a single key press
        time.sleep(0.1)


if __name__ == "__main__":
    main()
import time
import json
from valclient.client import Client
import threading
import os
import keyboard

# Default configuration dictionary
dictionary = {
    "instantlocker": {
        "region": "na",
        "preferred_agent": "",
        "save_config": True
    }
}

# Path to config file
cfg_path = "config.json"

# Function to setup initial config file
def setup_config():
    while True:
        save_config = input("Do you want to save the configuration? (yes/no): ").strip().lower()
        if save_config in ["yes", "no"]:
            dictionary['instantlocker']['save_config'] = (save_config == "yes")
            break
        else:
            print("Please enter 'yes' or 'no'.")

    if dictionary['instantlocker']['save_config']:
        while True:
            preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
            if preferred_agent in ValorantAgentInstalocker.agents:
                dictionary['instantlocker']['preferred_agent'] = preferred_agent
                break
            else:
                print("Please enter a valid agent name.")

        with open(cfg_path, "w") as f:
            f.write(json.dumps(dictionary, indent=4))

# Function to load existing config file
def load_config():
    if not os.path.exists(cfg_path):
        setup_config()
        time.sleep(2)

    with open(cfg_path) as json_file:
        config_data = json.load(json_file)

    instantlocker_config = config_data.get('instantlocker', {})
    if instantlocker_config.get('save_config') and ('preferred_agent' not in instantlocker_config or not instantlocker_config['preferred_agent']):
        print("No agent found in config")
        time.sleep(2)
        os._exit(0)

    return config_data

# Class to handle Valorant agent instalocker
class ValorantAgentInstalocker:
    agents = {
        "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
        "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
        "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
        "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
        "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
        "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
        "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
        "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
        "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
        "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
        "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
        "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
        "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
        "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
        "omen": "8e253930-4c05-31dd-1b6c-968525494517",
        "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
        "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
        "viper": "707eab51-4836-f488-046a-cda6bf494859",
        "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
        "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
        "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
        "deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
        "iso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
        "clove": "1dbf2edd-4729-0984-3115-daa5eed44993"
    }

    def __init__(self, region, preferred_agent):
        self.region = region.lower()
        self.preferred_agent = preferred_agent
        self.seenMatches = []
        self.pause_instalock = False

        if not self.is_valid_agent(self.preferred_agent):
            print("Invalid agent in config")
            time.sleep(2)
            os._exit(0)

    def is_valid_agent(self, agent):
        return agent in self.agents

    def initialize_client(self):
        while True:
            try:
                self.client = Client(region=self.region)
                self.client.activate()
                self.run_instalocker()
            except Exception as e:
                time.sleep(2)

    def choose_preferred_agent(self):
        return self.preferred_agent

    def run_instalocker(self):
        while True:
            time.sleep(0.01)
            try:
                if self.pause_instalock:
                    continue

                session_state = self.client.fetch_presence(self.client.puuid)['sessionLoopState']
                match_id = self.client.pregame_fetch_match()['ID']

                if session_state == "PREGAME" and match_id not in self.seenMatches:
                    start_time = time.time()
                    agent_id = self.agents[self.preferred_agent]
                    self.client.pregame_select_character(agent_id)
                    self.client.pregame_lock_character(agent_id)
                    end_time = time.time()
                    duration = end_time - start_time
                    self.seenMatches.append(match_id)
                    print(f"Locked {self.preferred_agent.capitalize()} in {duration:.2f} seconds")
                    self.pause_instalock = True
                    print("InstaLocker paused. F10 to resume.")
            except Exception as e:
                return []

    def toggle_pause(self):
        self.pause_instalock = not self.pause_instalock
        state = "paused" if self.pause_instalock else "running"
        print(f"InstaLocker {state}")


# Function to handle the initial setup and key validation
def main():
    global data  # Declare data as global to use in this function
    data = load_config()
    try:
        enable_instalock = data['instantlocker']
        if data['instantlocker']['save_config']:
            preferred_agent = data['instantlocker']["preferred_agent"].lower()
        else:
            while True:
                preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
                if preferred_agent in ValorantAgentInstalocker.agents:
                    break
                else:
                    print("Please enter a valid agent name.")
    except KeyError:
        os._exit(0)

    instantlocker_instance = ValorantAgentInstalocker(region=data['instantlocker']["region"], preferred_agent=preferred_agent)
    instantlock_thread = threading.Thread(target=instantlocker_instance.initialize_client)
    instantlock_thread.daemon = True
    instantlock_thread.start()

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for cleaner output
    print(f"InstaLocker started")
    print(f"Lock agent: {preferred_agent.capitalize()}\n")

    # Continuously monitor keyboard inputs
    while True:
        if keyboard.is_pressed("ctrl+shift+x"):
            os._exit(0)
        if keyboard.is_pressed("f10"):
            instantlocker_instance.toggle_pause()
            time.sleep(0.5)  # To prevent multiple toggles from a single key press
        time.sleep(0.1)


if __name__ == "__main__":
    main()
import time
import json
from valclient.client import Client
import threading
import os
import keyboard

# Default configuration dictionary
dictionary = {
    "instantlocker": {
        "region": "na",
        "preferred_agent": "",
        "save_config": True
    }
}

# Path to config file
cfg_path = "config.json"

# Function to setup initial config file
def setup_config():
    while True:
        save_config = input("Do you want to save the configuration? (yes/no): ").strip().lower()
        if save_config in ["yes", "no"]:
            dictionary['instantlocker']['save_config'] = (save_config == "yes")
            break
        else:
            print("Please enter 'yes' or 'no'.")

    if dictionary['instantlocker']['save_config']:
        while True:
            preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
            if preferred_agent in ValorantAgentInstalocker.agents:
                dictionary['instantlocker']['preferred_agent'] = preferred_agent
                break
            else:
                print("Please enter a valid agent name.")

        with open(cfg_path, "w") as f:
            f.write(json.dumps(dictionary, indent=4))

# Function to load existing config file
def load_config():
    if not os.path.exists(cfg_path):
        setup_config()
        time.sleep(2)

    with open(cfg_path) as json_file:
        config_data = json.load(json_file)

    instantlocker_config = config_data.get('instantlocker', {})
    if instantlocker_config.get('save_config') and ('preferred_agent' not in instantlocker_config or not instantlocker_config['preferred_agent']):
        print("No agent found in config")
        time.sleep(2)
        os._exit(0)

    return config_data

# Class to handle Valorant agent instalocker
class ValorantAgentInstalocker:
    agents = {
        "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
        "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
        "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
        "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
        "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
        "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
        "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
        "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
        "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
        "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
        "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
        "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
        "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
        "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
        "omen": "8e253930-4c05-31dd-1b6c-968525494517",
        "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
        "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
        "viper": "707eab51-4836-f488-046a-cda6bf494859",
        "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
        "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
        "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
        "deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
        "iso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
        "clove": "1dbf2edd-4729-0984-3115-daa5eed44993"
    }

    def __init__(self, region, preferred_agent):
        self.region = region.lower()
        self.preferred_agent = preferred_agent
        self.seenMatches = []
        self.pause_instalock = False

        if not self.is_valid_agent(self.preferred_agent):
            print("Invalid agent in config")
            time.sleep(2)
            os._exit(0)

    def is_valid_agent(self, agent):
        return agent in self.agents

    def initialize_client(self):
        while True:
            try:
                self.client = Client(region=self.region)
                self.client.activate()
                self.run_instalocker()
            except Exception as e:
                time.sleep(2)

    def choose_preferred_agent(self):
        return self.preferred_agent

    def run_instalocker(self):
        while True:
            time.sleep(0.01)
            try:
                if self.pause_instalock:
                    continue

                session_state = self.client.fetch_presence(self.client.puuid)['sessionLoopState']
                match_id = self.client.pregame_fetch_match()['ID']

                if session_state == "PREGAME" and match_id not in self.seenMatches:
                    start_time = time.time()
                    agent_id = self.agents[self.preferred_agent]
                    self.client.pregame_select_character(agent_id)
                    self.client.pregame_lock_character(agent_id)
                    end_time = time.time()
                    duration = end_time - start_time
                    self.seenMatches.append(match_id)
                    print(f"Locked {self.preferred_agent.capitalize()} in {duration:.2f} seconds")
                    self.pause_instalock = True
                    print("InstaLocker paused. F10 to resume.")
            except Exception as e:
                return []

    def toggle_pause(self):
        self.pause_instalock = not self.pause_instalock
        state = "paused" if self.pause_instalock else "running"
        print(f"InstaLocker {state}")


# Function to handle the initial setup and key validation
def main():
    global data  # Declare data as global to use in this function
    data = load_config()
    try:
        enable_instalock = data['instantlocker']
        if data['instantlocker']['save_config']:
            preferred_agent = data['instantlocker']["preferred_agent"].lower()
        else:
            while True:
                preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
                if preferred_agent in ValorantAgentInstalocker.agents:
                    break
                else:
                    print("Please enter a valid agent name.")
    except KeyError:
        os._exit(0)

    instantlocker_instance = ValorantAgentInstalocker(region=data['instantlocker']["region"], preferred_agent=preferred_agent)
    instantlock_thread = threading.Thread(target=instantlocker_instance.initialize_client)
    instantlock_thread.daemon = True
    instantlock_thread.start()

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for cleaner output
    print(f"InstaLocker started")
    print(f"Lock agent: {preferred_agent.capitalize()}\n")

    # Continuously monitor keyboard inputs
    while True:
        if keyboard.is_pressed("ctrl+shift+x"):
            os._exit(0)
        if keyboard.is_pressed("f10"):
            instantlocker_instance.toggle_pause()
            time.sleep(0.5)  # To prevent multiple toggles from a single key press
        time.sleep(0.1)


if __name__ == "__main__":
    main()

}

cfg_path = "config.json"

def setup_config():
    if 'preferred_agent' not in dictionary['instantlocker'] or not dictionary['instantlocker']['preferred_agent']:
        while True:
            preferred_agent = input("Enter preferred agent (jett, reyna, gekko, etc): ").strip().lower()
            if preferred_agent in ValorantAgentInstalocker.agents:
                dictionary['instantlocker']['preferred_agent'] = preferred_agent
                break
            else:
                print("name a valid agent plz")

        with open(cfg_path, "w") as f:
            f.write(json.dumps(dictionary, indent=4))

def load_config():
    if not os.path.exists(cfg_path):
        setup_config()
        time.sleep(2)

    with open(cfg_path) as json_file:
        config_data = json.load(json_file)

    instantlocker_config = config_data.get('instantlocker', {})
    if 'preferred_agent' not in instantlocker_config or not instantlocker_config['preferred_agent']:
        print("No agent found in config")
        time.sleep(2)
        os._exit(0)

    return config_data

class ValorantAgentInstalocker:
    agents = {
        "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
        "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
        "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
        "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
        "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
        "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
        "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
        "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
        "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
        "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
        "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
        "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
        "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
        "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
        "omen": "8e253930-4c05-31dd-1b6c-968525494517",
        "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
        "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
        "viper": "707eab51-4836-f488-046a-cda6bf494859",
        "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
        "gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
        "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
        "deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
        "iso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
        "clove": "1dbf2edd-4729-0984-3115-daa5eed44993"
    }

    def __init__(self, region, preferred_agent):
        self.region = region.lower()
        self.preferred_agent = preferred_agent
        self.seenMatches = []
        self.pause_instalock = False

        if not self.is_valid_agent(self.preferred_agent):
            print("Invalid agent in config")
            time.sleep(2)
            os._exit(0)

    def is_valid_agent(self, agent):
        return agent in self.agents

    def initialize_client(self):
        while True:
            try:
                self.client = Client(region=self.region)
                self.client.activate()
                self.run_instalocker()
            except Exception as e:
                time.sleep(2)

    def choose_preferred_agent(self):
        return self.preferred_agent

    def run_instalocker(self):
        while True:
            time.sleep(0.01)
            try:
                if self.pause_instalock:
                    continue

                session_state = self.client.fetch_presence(self.client.puuid)['sessionLoopState']
                match_id = self.client.pregame_fetch_match()['ID']

                if session_state == "PREGAME" and match_id not in self.seenMatches:
                    start_time = time.time()
                    agent_id = self.agents[self.preferred_agent]
                    self.client.pregame_select_character(agent_id)
                    self.client.pregame_lock_character(agent_id)
                    end_time = time.time()
                    duration = end_time - start_time
                    self.seenMatches.append(match_id)
                    print(f"Locked {self.preferred_agent.capitalize()} in {duration:.2f} seconds")
                    self.pause_instalock = True
                    print("InstaLocker paused. F10 to resume.")
            except Exception as e:
                return []

    def toggle_pause(self):
        self.pause_instalock = not self.pause_instalock
        state = "paused" if self.pause_instalock else "running"
        print(f"InstaLocker {state}")


def main():
    global data
    data = load_config()
    try:
        enable_instalock = data['instantlocker']
        preferred_agent = data['instantlocker']["preferred_agent"].lower()
    except KeyError:
        os._exit(0)

    instantlocker_instance = ValorantAgentInstalocker(region=data['instantlocker']["region"], preferred_agent=preferred_agent)
    instantlock_thread = threading.Thread(target=instantlocker_instance.initialize_client)
    instantlock_thread.daemon = True
    instantlock_thread.start()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"InstaLocker started")
    print(f"Lock agent: {preferred_agent.capitalize()}\n")

    while True:
        if keyboard.is_pressed("ctrl+shift+x"):
            os._exit(0)
        if keyboard.is_pressed("f10"):
            instantlocker_instance.toggle_pause()
            time.sleep(0.5)
        time.sleep(0.1)



if __name__ == "__main__":
    main()
