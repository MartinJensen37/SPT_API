import requests, json
import matplotlib.pyplot as plt
import os

class spt_cls():
        
    def __init__(self) -> None:
        self.host = "https://api.spacetraders.io/v2/"
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept-Language'] = 'en_US'

        if os.path.isfile(".\API_key.txt") == False: # Check if API_key file exist, if not, create it
            f = open("API_key.txt", "w")
            f.close()

        with open("API_key.txt", "r") as api_key_file: # read from the API_key file. 
            self.headers['Authorization'] = 'Bearer ' + api_key_file.read()

        check_agent = self.get_agent() # If this is old or empty the status code for the agent will be 401
        if check_agent.status_code == 401: # Check if an agent exist and otherwise generate a new API key
            api_key = self.create_agent()
            print(api_key.json())
            decoded = api_key.json()
            self.headers['Authorization'] = decoded['data']['token']
            with open("API_key.txt", "w") as api_key_file:
                api_key_file.write(decoded['data']['token'])
                api_key_file.close()

    def create_agent(self):
        data = {"symbol": "agent-name", # Pick a faction and a name for the agent
                "faction": "COSMIC"}

        response = requests.post(self.host + "/register", headers={'Content-Type': 'application/json'}, json=data)
        print(type(response), "response type")
        return response

    def get_agent(self):
        """Get agent information

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        response = requests.get(self.host + "/my/agent/", headers=self.headers)
        
        return response
    
    def get_systems(self):
        """Get list of systems

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        response = requests.get(self.host + "/systems/", headers=self.headers)

        return response

    def get_waypoints(self, system_id:str):
        """Get waypoints from a certain system

        Parameters
        ----------
        system_id : str
            give the id of the system 

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        response = requests.get(self.host + "/systems/" + system_id + "/waypoints", headers=self.headers)

        return response

    def ship_orbit(self, ship_id:str):
        """Sends a ship into orbit

        Parameters
        ----------
        ship_id : str
            Give the id of the ship that should be sent into orbit

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        response = requests.post(self.host + "/my/ships/" + ship_id + "/orbit", headers=self.headers)

        return response
    
    def ship_dock(self, ship_id:str):
        """Sends ship to dock

        Parameters
        ----------
        ship_id : str
            Give the id of the ship that should be docked

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        response = requests.post(self.host + "/my/ships/" + ship_id + "/dock", headers=self.headers)

        return response
    
    def set_ship_mode(self, mode_id:str):
        """Sets the mode of the ship
 

        Parameters
        ----------
        mode_id : str
        - The possible modes are:
            - CRUISE: Cruise flight mode is the default mode for all ships. It consumes fuel at a normal rate and travels at a normal speed.
            - BURN: Burn flight mode consumes fuel at a faster rate and travels at a faster speed.
            - DRIFT: Drift flight mode consumes the least fuel and travels at a much slower speed. Drift mode is useful when your ship has run out of fuel and you need to conserve what little fuel you have left.
            - STEALTH: Stealth flight mode runs with systems at a minimum, making it difficult to detect. It consumes fuel at a normal rate but travels at a reduced speed.

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """
        response = requests.post(self.host + "/my/ships/" + mode_id + "/orbit", headers=self.headers)

        return response
    def navigate_to_waypoint(self, ship_id:str, waypoint_symbol:str):
        """Navigate a ship to a certain waypoint

        Parameters
        ----------
        ship_id : str
            Give the id of the ship that has to be sent
        waypoint_symbol : str
            Give the symbol for the desired waypoint 

        Returns
        -------
        response : <Response>
            returns a HTTP response object
        """

        data = {"waypointSymbol": waypoint_symbol}

        response = requests.post(self.host + "/my/ships/" + ship_id + "/navigate", headers=self.headers, json=data)
        return response
    
    def plot_systems(self):
        """Plots all known systems in a scatter plot
        """
        response = self.get_systems()
        res_dict = json.loads(response._content.decode('utf-8'))
        name = []
        x = []
        y = []
        for system in range(len(res_dict['data'])):
            name.append(res_dict['data'][system]['symbol'])
            x.append(res_dict['data'][system]['x'])
            y.append(res_dict['data'][system]['y'])

        plt.scatter(x, y)
        for i in range(len(name)):
            plt.annotate(name[i], (x[i], y[i]))
        plt.grid()
        plt.show()


def main():
    print("Running from class file!")
    spt_instance = spt_cls()
    spt_instance.plot_systems()

if __name__=="__main__":
    main()