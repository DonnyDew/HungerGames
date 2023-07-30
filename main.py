import eel
from hungerGamesSim import Player, Team, Game

eel.init('web')
# Global variables to store the teams, players, and simulation results
players = []
teams = []
simulation_results = None

@eel.expose
def create_players_and_teams(player_names, player_genders):
    
    global players
    global teams

    # Create the players
    players = [Player(name, gender) for name, gender in zip(player_names, player_genders)]

    # Create the teams
    # This is just a simple example where each team has two players. You might need to adjust it.
    teams = [Team(players[i], players[i+1], i//2+1) for i in range(0, len(players), 2)]
    

@eel.expose
def start_simulation():
    
    global simulation_results

    # Create the game
    game = Game(teams)
    
    # Run the simulation
    simulation_results = game.start()
    
    
@eel.expose
def get_simulation_results():
    return simulation_results

# Start the app
eel.start('start.html')

