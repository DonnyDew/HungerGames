import random
import json

# Player class
class Player:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.alive = True
        self.items = []
        self.kill_count = 0
    
    def has_item(self):
        return len(self.items) > 0
    

# Team class
class Team:
    def __init__(self, player1, player2, team_number):
        self.members = [player1, player2]
        self.alive = True
        self.name = f"District {team_number}"

    def is_team_alive(self):
        return any(player.alive for player in self.members)

# Scenarios class
class Scenarios:
    
    # Add kill scenarios for each item
    item_kill_scenarios = {
        "sword": [
            "{killer} uses their sword to stab {victim} in the heart.",
            "{killer} swings their sword and beheads {victim}."
        ],
        "bow and arrows": [
            "{killer} shoots an arrow into {victim}'s heart.",
            "{killer} fires a flurry of arrows, one of which hits {victim}'s head."
        ],
        "bag full of explosives": [
            "{killer} tosses a bag full of explosives at {victim}, blowing them up.",
            "{killer} strategically places the bag full of explosives and lures {victim} into the trap."
        ],
        "knife": [
            "{killer} stealthily approaches {victim} and slits their throat with a knife.",
            "{killer} throws their knife, which lodges in {victim}'s chest."
        ],
        "axe": [
            "{killer} swings their axe, splitting {victim}'s skull.",
            "{killer} throws their axe, which hits {victim} squarely in the chest."
        ],
        "bare hands": [
            "{killer} uses their bare hands to strangle {victim}, their grip tightening until they succumbs to the lack of air.",
            "{killer} fiercely grapples with {victim}, and breaks their neck, ending their life.",
            "{killer} seizes the opportunity and pushes {victim} into a nearby body of water, where they struggle in vain against the strong currents.",
            "{killer} ambushes {victim} from behind, smashing their skull with a heavy rock found nearby."
        ]
        }
    three_person_item_kill_scenarios = {
        "sword": [
        "{killer}, with the assistance of {next_player}, uses their sword to deliver the final, fatal blow to {victim}.",
        "Under the cover provided by {next_player}, {killer} swings their sword and beheads {victim}."
        ],
        "bow and arrows": [
            "{killer}, aided by {next_player}, takes careful aim and shoots an arrow into {victim}'s heart.",
            "With {next_player} distracting {victim}, {killer} fires a flurry of arrows, one of which hits {victim}'s head."
        ],
        "bag full of explosives": [
            "{killer}, with {next_player}'s help, tosses a bag full of explosives at {victim}, blowing them up.",
            "{killer}, under the cover of {next_player}, strategically places the bag full of explosives and lures {victim} into the trap."
        ],
        "knife": [
            "Using the distraction provided by {next_player}, {killer} stealthily approaches {victim} and slits their throat with a knife.",
            "{killer}, with {next_player}'s assistance, throws their knife, which lodges in {victim}'s chest."
        ],
        "axe": [
            "{killer}, with {next_player} providing a diversion, swings their axe, splitting {victim}'s skull.",
            "With {next_player} distracting {victim}, {killer} throws their axe, which hits {victim} squarely in the chest."
        ],
        'bare hands' : [
            "With {next_player} holding {victim} down, {killer} uses their bare hands to strangle them, their grip tightening until {victim} succumbs to the lack of air.",
            "{next_player} distracts {victim} while {killer} fiercely grapples with them, breaking their neck and ending their life.",
            "While {next_player} distracts {victim}, {killer} seizes the opportunity and pushes {victim} into a nearby body of water, where they struggle in vain against the strong currents.",
            "With {next_player} keeping {victim} distracted, {killer} ambushes them from behind, smashing their skull with a heavy rock found nearby."
        ]
    }

    special_event_scenario = {
        "Toxic Fog": {
            "alive": [
                "Terrifyingly close to the toxic fog, {Player} scavenges for a gas mask or any protection to prolong their survival.",
                "With the toxic fog closing in, {Player} takes a risky leap across a ravine to escape its deadly clutches.",
                "{Player} barely manages to outrun the encroaching toxic fog, coughing heavily but still alive.",
                "Using a piece of cloth as a makeshift mask, {Player} navigates through the toxic fog, emerging on the other side coughing but alive."
            ],
            "dead": [
                "The toxic fog proves to be too much for {Player} as they succumb to its deadly embrace.",
                "{Player} is so toxic that even their last breath is toxic.",
                "{Player}'s desperate attempts to escape the toxic fog are in vain as they fall, choking and gasping for air.",
                "{Player} stumbles and falls within the toxic fog, their body soon still."
            ]
        },
        "ThunderStorm" : {
            "alive" : [
                "As the thunder roars and the lightning dances, {Player} finds shelter just in time, surviving the wrath of the thunderstorm.",
                "{Player} takes cover under a dense canopy of trees, avoiding the worst of the thunderstorm.",
                "Despite the deafening thunder and blinding lightning, {Player} manages to find a cave for shelter, surviving the storm.",
                "{Player} barely avoids a lightning strike, quickly taking cover under a rocky overhang until the thunderstorm passes."
            ],
            "dead": [
                "The thunderstorm proves too formidable for {Player} to overcome, and they are lost to the relentless tempest.",
                "{Player} takes cover under a dense canopy of trees, avoiding the worst of the thunderstorm.",
                "Despite the deafening thunder and blinding lightning, {Player} manages to find a cave for shelter, surviving the storm.",
                "{Player} barely avoids a lightning strike, quickly taking cover under a rocky overhang until the thunderstorm passes."
            ]
        },
        "Tracker Jackers": {
            "alive": [
                "{Player} manages to outpace a swarm of Tracker Jackers, escaping their deadly stings.",
                "Despite the chaos of a Tracker Jacker attack, {Player} remains calm and finds shelter, avoiding the deadly swarm.",
                "{Player} cleverly uses smoke to disorient the Tracker Jackers, escaping unscathed."
            ],
            "dead": [
                "Overwhelmed by a swarm of Tracker Jackers, {Player} succumbs to their lethal stings.",
                "{Player} is tragically unable to escape a Tracker Jacker attack and falls to their venomous stings.",
                "In a fatal turn of events, {Player} crosses paths with a Tracker Jacker nest and is swarmed before they can escape."
            ]
        },
        "Mutant Wolves": {
            "alive": [
                "{Player} manages to climb a tree just in time to escape a pack of mutant wolves.",
                "With quick thinking, {Player} scares off the mutant wolves using a fire torch.",
                "Despite the terrifying sight of the mutant wolves, {Player} stands their ground and manages to fend off the creatures."
            ],
            "dead": [
                "{Player} is tragically overtaken by a pack of mutant wolves, meeting a gruesome end.",
                "Caught off guard, {Player} stands no chance against the vicious mutant wolves.",
                "In a desperate run for their life, {Player} is ultimately caught and overwhelmed by the mutant wolves."
            ]
        },
        "El Chapo": {
            "alive": [
                "Despite the sudden appearance of El Chapo, {Player} stays calm and manages to evade his notice.",
                "{Player} crosses paths with El Chapo but quickly blends into the surroundings, avoiding detection.",
                "In an unexpected turn of events, {Player} forms a temporary alliance with El Chapo, gaining protection.",
                "{Player} faces off against El Chapo, injures him, and manages to escape.",
                "{Player} bribes El Chapo with a Mountain Dew and is allowed to live"
            ],
            "dead": [
                 "{Player} becomes a target of El Chapo and is unable to escape his ruthless attack.",
                "El Chapo corners {Player}, leading to their unfortunate demise.",
                "In a tragic turn of events, {Player} attempts to confront El Chapo, only to be overpowered and eliminated.",
                "{Player} makes friends with El Chapo but then overdoses on the drugs he gave"
            ]
        }
    }


    hand_fight_scenarios  = [
        "{killer} uses their bare hands to strangle {victim}, their grip tightening until they succumbs to the lack of air.",
        "{killer} fiercely grapples with {victim}, and breaks their neck, ending their life.",
        "{killer} seizes the opportunity and pushes {victim} into a nearby body of water, where they struggle in vain against the strong currents.",
        "{killer} ambushes {victim} from behind, smashing their skull with a heavy rock found nearby."
    ]

    double_kill_scenarios = {
        "sword": [
            "{killer} launches into a deadly dance, their sword cutting through both {victim} and {next_player} in swift, brutal strokes.",
            "With a fearsome battle cry, {killer} charges, their sword slicing through {victim} before piercing {next_player}'s heart."
        ],
        "bow and arrows": [
            "{killer} lets loose a rain of arrows, each finding their mark in {victim} and {next_player}.",
            "With a deadly accuracy, {killer} shoots an arrow into {victim}'s heart, before quickly notching another and striking {next_player} in the head."
        ],
        "bag full of explosives": [
            "{killer} tosses a bag full of explosives between {victim} and {next_player}, the resulting explosion leaving no chance for survival.",
            "With a wicked grin, {killer} lures {victim} and {next_player} into a trap filled with explosives. The ensuing blast leaves no survivors."
        ],
        "knife": [
            "{killer} lunges at {victim}, slitting their throat with a knife, then spins around and throws the same knife into {next_player}'s chest.",
            "Moving like a shadow, {killer} silently dispatches {victim} with a swift stab, before hurling their knife into {next_player}."
        ],
        "axe": [
            "{killer} wields their axe with deadly force, splitting {victim}'s skull and then {next_player}'s chest in a single, mighty swing.",
            "{killer} spins in a deadly arc, their axe slicing through both {victim} and {next_player} before they can react."
        ],
        "bare hands": [
            "{killer} launches into a flurry of violence, strangling {victim} before turning and snapping {next_player}'s neck.",
            "With a fierce determination, {killer} overpowers {victim}, breaking their neck. Without missing a beat, they turn and push {next_player} into a nearby river."
        ]
    }

    romantic_scenarios = [
        "{male} and {female} hold each others hands.",
        "{female} and {male} cuddle together for warmth.",
        "{female} gives {male} a sweet kiss.",
        "Seeing the fear in {female}'s eyes, {male} pulls her into a reassuring embrace"
    ]

    friend_scenarios = [
        "{player1} and {player2} bond over shared experiences.",
        "{player1} and {player2} build a strong friendship.",
        "{player1} saves {player2} from a dangerous situation, strengthening their friendship.",
        "{player1} and {player2} bond over shared stories from their home districts.",
        "{player1} and {player2} sit down together and have a cold Mountain Dew."
    ]

    cornucopia_scenarios = [
        "{player} runs away from the cornucopia without grabbing anything.",
        "{player} finds a hidden cache of food and water at the cornucopia.",
        "{player} discovers a medical kit at the cornucopia.",
        "{player} stumbles upon a camouflage kit at the cornucopia, which could help them blend into the environment."
    ]

    cornucopia_kill_scenarios = {
        "sword": [
            "{killer} grabs a sword from the cornucopia and uses it to kill {victim}.",
            "{killer} runs straight for the sword and uses it to slice {victim} in two."
        ],
        "bag full of explosives": [
            "{killer} finds a bag full of explosives at the cornucopia and uses them to blow up {victim}."
        ],
        "bow and arrows": [
            "{killer} manages to get a bow and arrows from the cornucopia and shoots {victim}.",
            "While being chased from the cornucopia {killer} picks up a bow and arrows and does a 180 spin shooting {victim}."
        ],
        "axe": [
            "{killer} finds an axe and uses it to murder {victim}.",
            "{killer} runs straight for an axe and immediately decapitates {victim}."
        ],
        "knife": [
            "{killer} picks up a knife from the cornucopia and stabs {victim}.",
            "{killer} grabs a knife from the cornucopia and stabs {victim} while they are picking up a backpack."
        ]
    }

    scavenging_scenarios = [
        "{player} finds an apple tree and picks some apples.",
        "{player} stumbles upon a cache of medical supplies.",
        "{player} manages to catch a rabbit for dinner.",
        "{player} finds a Mountain Dew KickStart MangoLime!"
    ]

    sponsor_scenarios = [
        "{player} receives a bottle of water from a sponsor.",
        "{player} is given a warm blanket by a sponsor.",
        "{player} gets a surprise package from a sponsor. It contains a knife.",
    ]

    natural_death_scenarios = [
        "{player} dies from hypothermia.",
        "{player} dies from dehydration.",
        "{player} accidentally eats poisonous berries and dies.",
        "{player} does not keep up with the shrinking border and vaporized",
        "{player} overdoes on Mountain Dew and dies."
    ]

    night_scenarios = [
        "{player} makes a fire to keep warm.",
        "{player} finds a safe place to sleep for the night.",
        "{player} stays awake all night, keeping watch.",
        "{player} tries finding other tributes to kill."
    ]

    night_silly_scenario = [
        "{player} attempts to climb a tree for a better view of the stars, but gets stuck and turns into a makeshift 'tree-owl'.",
        "{player} tries to cook a meal in the moonlight, but only succeeds in attracting a pack of raccoons to the camp.",
        "{player} spends the night trying to decode the hoots of an owl, convinced it is trying to send a message.",
        "{player} spends the night arguing with a shadow, mistaking it for a rival competitor."
    ]   

    day_silly_scenario = [
        "{player} trips over a rock and spends the day believing they have discovered a new species of 'moving stones'.",
        "{player} tries to create a smoke signal message, but accidentally sets a damp log on fire, resulting in a cloud of steam instead.",
        "{player} has a staring contest with a frog after being stung by a rogue tracker jacker.",
        "{player} is down bad after recieving Taco Bell as a sponsor gift.",
        "{player} draws a Mountain Dew tier list in the dirt.",
        "{player} sees a monkey and tries communitcating with it."

    ]

    teammate_scenario = [
        "{player1} and {player2} steal from an enemy camp while hunting",
        "{player1} and {player2} discuss their chances of winning, and any possible allies among the other teams",
        "{player1} and {player2} set up camp in a cave after clearing the area of any other teams",
        "{player2} and {player1} split rations and supplies to prep for any emergencies",
        "{player2} and {player1} hide in some bushes and strategize about where other teams may be",
    ]

    teammate_cor_scenario = [
        "{player1} and {player2} run away together"
    ]


    @staticmethod
    def get_death_scenario(killer, victim):
        if victim.alive:
            victim.alive = False
            killer.alive = True
            killer.kill_count += 1
            game.deaths[victim.name] = (game.day, game.time, victim.kill_count)
            if killer.has_item():
                # The killer uses their item to kill the victim
                item = random.choice(killer.items)  # Choose the item randomly from the killer's items list
                if game.day != 1:
                    return random.choice(Scenarios.item_kill_scenarios[item]).format(killer=killer.name, victim=victim.name)
                else:
                    return random.choice(Scenarios.cornucopia_kill_scenarios[item]).format(killer=killer.name, victim=victim.name, item=item)  
            else:
                # The killer doesn't have any items, so they fight hand-to-hand
                return random.choice(Scenarios.item_kill_scenarios["bare hands"]).format(killer=killer.name, victim=victim.name)
                
    def get_three_player_death_scenario(killer, victim, next_player):
        victim.alive = False
        game.deaths[victim.name] = (game.day, game.time, victim.kill_count)
        
        if killer.has_item():
            item = random.choice(killer.items)
            if game.get_team(next_player) == game.get_team(killer):
                killer.kill_count += 1
                return f"{random.choice(Scenarios.three_person_item_kill_scenarios[item]).format(killer=killer.name, next_player=next_player.name, victim=victim.name)}"

            elif game.get_team(next_player) == game.get_team(victim):
                next_player.alive = False
                killer.kill_count += 2
                game.deaths[next_player.name] = (game.day, game.time, next_player.kill_count)
                
                return f"{random.choice(Scenarios.double_kill_scenarios[item]).format(killer=killer.name, victim=victim.name, next_player=next_player.name)}"
            else:
                return "This should not be printed"
        else:
            if game.get_team(next_player) == game.get_team(killer):
                killer.kill_count += 1
                return f"{random.choice(Scenarios.three_person_item_kill_scenarios['bare hands']).format(killer=killer.name, next_player=next_player.name, victim=victim.name)}"
            
            elif game.get_team(next_player) == game.get_team(victim):
                next_player.alive = False
                killer.kill_count += 2
                game.deaths[next_player.name] = (game.day, game.time, next_player.kill_count)
                return f"{random.choice(Scenarios.double_kill_scenarios['bare hands']).format(killer=killer.name, victim=victim.name, next_player=next_player.name)}"
            else:
                return "This should not be printed"


    @staticmethod
    def get_social_scenario(player1, player2):
        if player1.gender != player2.gender:
            if player1.gender == "male" and player2.gender == "female":
                return random.choice(Scenarios.romantic_scenarios).format(male=player1.name, female=player2.name)
            else:
                return random.choice(Scenarios.romantic_scenarios).format(male=player2.name, female=player1.name)
        else:
            return random.choice(Scenarios.friend_scenarios).format(player1=player1.name, player2=player2.name)
    
    @staticmethod
    def get_cornucopia_scenario(player,victim, death_func):
        # 60% chance to get an item
        if random.random() < .6:
            item = random.choice(["sword", "bow and arrows", "bag full of explosives", "knife", "axe"])
            player.items.append(item)  # Add the item to the player's items list
            if random.random() < .3 and victim.alive:  
                return death_func(player, victim)
            return f"{player.name} grabbed a {item} from the cornucopia."
        else:
            # If the player doesn't get an item, return a different scenario
            return random.choice(Scenarios.cornucopia_scenarios).format(player=player.name)


    @staticmethod
    def get_scavenging_scenario(player):
        return random.choice(Scenarios.scavenging_scenarios).format(player=player.name)
    
    @staticmethod
    def get_silly_day_scenario(player):
        return random.choice(Scenarios.day_silly_scenario).format(player=player.name)

    @staticmethod
    def get_silly_night_scenario(player):
        return random.choice(Scenarios.night_silly_scenario).format(player=player.name)

    @staticmethod
    def get_sponsor_scenario(player):
        return random.choice(Scenarios.sponsor_scenarios).format(player=player.name)

    @staticmethod
    def get_natural_death_scenario(player):
        game.deaths[player.name] = (game.day, game.time, player.kill_count)
        return random.choice(Scenarios.natural_death_scenarios).format(player=player.name)
    
    @staticmethod
    def get_night_scenario(player):
        return random.choice(Scenarios.night_scenarios).format(player=player.name)
    
    @staticmethod
    def get_special_event_scenario(player, survive, special_event):
        if survive:
            message = random.choice(Scenarios.special_event_scenario[special_event]["alive"])
        else:
            player.alive = False
            game.deaths[player.name] = (game.day, game.time, player.kill_count)
            message = random.choice(Scenarios.special_event_scenario[special_event]["dead"])
        
        return message.format(Player=player.name)
    
    @staticmethod
    def get_teammate_scenario(player1,player2):
        return random.choice(Scenarios.teammate_scenario).format(player1=player1.name, player2=player2.name)
    
    @staticmethod
    def get_cor_teammate_scenario(player1,player2):
        return random.choice(Scenarios.teammate_cor_scenario).format(player1=player1.name, player2=player2.name)
    


# Game class
class Game:
    _instance = None

    def __new__(cls, teams):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, teams):
        self.teams = teams
        self.day = 0
        self.time = "Day"
        self.deaths = {}
        self.previous_alive_players = []
        self.simulation = []
    
    def get_team(self, player):
        # Find the team that the player belongs to
        for team in self.teams:
            if player in team.members:
                return team
        return None
    
    def get_teammates(self, player):
        # Get the team of the player
        team = self.get_team(player)
        if team is None:
            return []

        # Return all other members of the team
        return [teammate for teammate in team.members if teammate != player and teammate.alive]
    
    def get_unique_teams(self, players):
        # Initialize an empty set to store the unique teams
        unique_teams = set()

        # Iterate over the players
        for player in players:
            # Get the team of the player and add it to the set
            team = self.get_team(player)
            if team is not None:
                unique_teams.add(team)

        # Return the set of unique teams
        return unique_teams


    def get_alive_teams(self):
        return [team for team in self.teams if team.is_team_alive()]

    def get_alive_players(self, update=False):
        if update or not hasattr(self, 'alive_players'):
            self.alive_players = [player for team in self.teams for player in team.members if player.alive]
            self.previous_alive_players = getattr(self, 'alive_players', self.alive_players)
        return self.alive_players
    
    def print_deaths(self):
        text = []

        day_deaths = {name: details for name, details in self.deaths.items() if details[0] == self.day and details[1] == "Day"}
        previous_night_deaths = {name: details for name, details in self.deaths.items() if details[0] == self.day - 1 and details[1] == "Night"}
        all_deaths = {**previous_night_deaths, **day_deaths}  # Merge both dictionaries

        if all_deaths:
            text.append(f"\nDeaths during Day {self.day} and Night {self.day - 1}:")
            for name, details in all_deaths.items():
                text.append(f"{name} was killed.")
        else:
            text.append(f"\nNo deaths during Day {self.day} and Night {self.day - 1}.")
        return text


    def simulate_day(self):
        if len(self.get_alive_players(update=True)) == 1:  # Check if there's only one player left
            self.previous_alive_players = getattr(self, 'alive_players', [])
            return
        self.day += 1
        self.time = "Day"
        #print(f"\nDay {self.day}")
        alive_players_start = [player.name for player in self.get_alive_players(update=True)]
        events = []
        alive_players = self.get_alive_players()
        random.shuffle(alive_players)
        alive_players_copy = alive_players.copy()  # Make a copy to iterate over
        
        players_in_event = []
        unique_teams = self.get_unique_teams(alive_players)
        if self.day == 1:
            # Special rules for the first day
            for player in alive_players_copy:  # Iterate over the copy
                if not player.alive:  # Skip if the player is dead
                    if player in alive_players:  # Check if the player is still in the list before trying to remove
                        alive_players.remove(player)
                    continue
                # Create a weighted list of all possible scenarios for the player
                scenarios = [(Scenarios.get_cornucopia_scenario, 1)]
                scenario_assigned = False

                # Randomly select one scenario based on the weights
                while True:
                    potential_victims = [p for p in alive_players if p != player and p not in players_in_event]
                    if not potential_victims:
                        break  # Skip the current player if there are no potential victims
                    chosen_victim = random.choice(potential_victims)
                    scenario_func, scenario_args = random.choices(
                        [(s[0], (player, chosen_victim, Scenarios.get_death_scenario if self.get_team(player) != self.get_team(chosen_victim) else Scenarios.get_cor_teammate_scenario)) 
                        if s[0] == Scenarios.get_cornucopia_scenario else (s[0], (player, chosen_victim)) 
                        if s[0] in [Scenarios.get_death_scenario] else (s[0], (player,)) 
                        for s in scenarios], 
                        weights=[s[1] for s in scenarios], 
                        k=1)[0]

                    # Check if the selected scenario is a kill scenario and the players are on the same team
                    if scenario_func == Scenarios.get_death_scenario and self.get_team(player) == self.get_team(scenario_args[1]):
                        scenario_func = Scenarios.get_cor_teammate_scenario
                        scenario_args = (player, scenario_args[1])
                        players_in_event.extend([player, scenario_args[1]])

                    # If the selected scenario is a kill scenario, add the victim to the list of players in an event
                    if scenario_func in [Scenarios.get_death_scenario, Scenarios.get_cor_teammate_scenario]:
                        players_in_event.append(scenario_args[1])
                        if scenario_args[1] in alive_players:  # Check if the player is still in the list before trying to remove
                            alive_players.remove(scenario_args[1])  # Immediately update the alive_players list

                    players_in_event.append(player)  

                    # Execute the selected scenario
                    scenario_result = scenario_func(*scenario_args)
                    
                    if scenario_result is not None:
                        events.append(scenario_result)
                        scenario_assigned = True
                    break
                if not scenario_assigned:  # If no scenario was assigned, the player runs away
                    events.append(f"{player.name} runs away from the cornucopia without grabbing anything.")
                    players_in_event.append(player)
                    
        
        
        elif len(alive_players) == 2 and self.get_team(alive_players[0]) != self.get_team(alive_players[1]):
            events.append("Tributes have been teleported into an arena for Sudden Death!")
            events.append(Scenarios.get_death_scenario(alive_players[0], alive_players[1]))
            alive_players[1].alive = False
            self.get_alive_players(update=True)
          
        elif len(alive_players) == 3 and len(unique_teams) == 2 and game.get_team(alive_players[0]) != game.get_team(alive_players[1]):
            events.append("Tributes have been teleported into an arena for Sudden Death!")
            killer = alive_players[0]
            victim = alive_players[1]
            next_player = alive_players[2]
            events.append(Scenarios.get_three_player_death_scenario(killer, victim, next_player))
            
            victim.alive = False
            
            if self.get_team(next_player) == self.get_team(victim):
                next_player.alive = False
            self.get_alive_players(update=True)
               
                          
        else:
            
            if len(alive_players_copy) >= 3 and random.random() < 0.1:  # 10% chance for the special event to happen if there are at least 3 players
                
                special_event_list = ["Toxic Fog", "ThunderStorm", "Tracker Jackers" , "Mutant Wolves", "El Chapo"]
                special_event = random.choice(special_event_list)
                events.append(f"Special Event: {special_event}!")
                guaranteed_survivors = random.sample(alive_players_copy, 2)  # Select two guaranteed survivors
                for player in alive_players_copy:  # Iterate over the copy
                    if player in guaranteed_survivors:
                        survive = True
                    else:
                        survive = random.random() < 0.5  # 50% chance to survive
                    events.append(Scenarios.get_special_event_scenario(player, survive, special_event))  # Pass in the survive flag
                    players_in_event.append(player)
                    if not survive:
                        alive_players.remove(player)
                
            for player in alive_players.copy():  # Iterate over a copy
                if not player.alive or player in players_in_event:  # Skip if the player is dead or has already been in an event
                    if player in alive_players:  # Check if the player is still in the list before trying to remove
                        alive_players.remove(player)
                    continue

                other_players = [p for p in alive_players if p != player and p not in players_in_event]
               
                scenarios = [(Scenarios.get_sponsor_scenario, 0.15), 
                            (Scenarios.get_natural_death_scenario, 0.1), 
                            (Scenarios.get_scavenging_scenario, 0.3), 
                            (Scenarios.get_death_scenario, 0.25),
                            (Scenarios.get_silly_day_scenario, 0.1)]
                
                # Include social scenarios only if there are other players
                if other_players and len(self.get_alive_teams()) > 2:
                    scenarios.append((Scenarios.get_social_scenario, 0.1))

                if not other_players:
                    # If no other players, make the player perform an individual activity
                    scenario_func, scenario_args = random.choices(
                        [(s[0], (player,)) 
                        for s in scenarios if s[0] not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario]], 
                        weights=[s[1] for s in scenarios if s[0] not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario]], 
                        k=1)[0]
                else:
                    while True:
                        scenario_func, scenario_args = random.choices(
                            [(s[0], (player, random.choice(other_players))) 
                            if s[0] in [Scenarios.get_death_scenario, Scenarios.get_social_scenario] else (s[0], (player,)) 
                            for s in scenarios], 
                            weights=[s[1] for s in scenarios], 
                            k=1)[0]
                        if scenario_func not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario] or scenario_args[1] not in players_in_event:
                            break
                    if scenario_func == Scenarios.get_death_scenario and len(alive_players) >= 3:
                        if self.get_team(player) == self.get_team(scenario_args[1]):  # Check if they are on the same team
                            scenario_func = Scenarios.get_teammate_scenario
                            players_in_event.extend([player, scenario_args[1]])
                            scenario_args = (player, scenario_args[1])
                        else:
                            # Choose a player that has not been in an event yet
                            next_players = [p for p in alive_players if p != player and p != scenario_args[1] and p not in players_in_event]
                            if next_players:
                                next_player = next_players[0]
                                if self.get_team(player) != self.get_team(scenario_args[1]) and self.get_team(next_player) in [self.get_team(player), self.get_team(scenario_args[1])]:
                                    scenario_func = Scenarios.get_three_player_death_scenario
                                    scenario_args = (player, scenario_args[1], next_player)
                                    players_in_event.append(next_player)

                # Add players to the players_in_event list
                players_in_event.append(player)
                if scenario_func in [Scenarios.get_social_scenario, Scenarios.get_death_scenario, Scenarios.get_three_player_death_scenario]:
                    players_in_event.append(scenario_args[1])
                    alive_players.remove(scenario_args[1])
                if scenario_func == Scenarios.get_three_player_death_scenario:
                    players_in_event.append(scenario_args[2])
                    alive_players.remove(scenario_args[2])
                if scenario_func in [Scenarios.get_natural_death_scenario]:
                    alive_players.remove(player)
                    player.alive = False

                events.append(scenario_func(*scenario_args))
                if len(self.get_alive_teams()) == 1:
                    #print("Only one team is left. Ending the day early.")
                    break 
        leaderboard = self.generate_leaderboard()
        self.simulation.append({
            'day': self.day,
            'alive_players': alive_players_start,
            'events': events,
            'leaderboard': leaderboard
        })                   

    def simulate_night(self):
        self.time = "Night"
        for player in self.get_alive_players(update=True):
            if not player.alive and player.name not in self.deaths:
                self.deaths[player.name] = (self.day, self.time, player.kill_count)
        printDeaths = self.print_deaths()
        self.previous_alive_players = getattr(self, 'alive_players', [])
        
        if len(self.get_alive_players(update=True)) == 1:  # Check if there's only one player left
            return
        
        alive_players_start = [player.name for player in self.get_alive_players(update=True)]
        events = []

        alive_players = self.get_alive_players()
        random.shuffle(alive_players)
        unique_teams = self.get_unique_teams(alive_players)
        players_in_event = []

        if len(alive_players) == 2 and self.get_team(alive_players[0]) != self.get_team(alive_players[1]):
            events.append("Tributes have been teleported into an arena for Sudden Death!")
            events.append(Scenarios.get_death_scenario(alive_players[0], alive_players[1]))
            alive_players[1].alive = False
            self.get_alive_players(update=True)
            
            
        elif len(alive_players) == 3 and len(unique_teams) == 2 and game.get_team(alive_players[0]) != game.get_team(alive_players[1]):
            events.append("Tributes have been teleported into an arena for Sudden Death!")
            killer = alive_players[0]
            victim = alive_players[1]
            next_player = alive_players[2]
            events.append(Scenarios.get_three_player_death_scenario(killer, victim, next_player))
            victim.alive = False
            
            if self.get_team(next_player) == self.get_team(victim):
                next_player.alive = False
            self.get_alive_players(update=True)
            
                
             
        else:
            for player in alive_players.copy():  # Iterate over a copy
                if not player.alive or player in players_in_event:  # Skip if the player is dead or has already been in an event
                    if player in alive_players:  # Check if the player is still in the list before trying to remove
                        alive_players.remove(player)
                    continue

                other_players = [p for p in alive_players if p != player and p not in players_in_event]
               
                scenarios = [(Scenarios.get_sponsor_scenario, 0.1), 
                            (Scenarios.get_natural_death_scenario, 0.1), 
                            (Scenarios.get_night_scenario, 0.4), 
                            (Scenarios.get_death_scenario, 0.1),
                            (Scenarios.get_silly_night_scenario, 0.1)]
                
                # Include social scenarios only if there are other players
                if other_players and len(self.get_alive_teams()) > 2:
                    scenarios.append((Scenarios.get_social_scenario, 0.05))

                if not other_players:
                    # If no other players, make the player perform an individual activity
                    scenario_func, scenario_args = random.choices(
                        [(s[0], (player,)) 
                        for s in scenarios if s[0] not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario]], 
                        weights=[s[1] for s in scenarios if s[0] not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario]], 
                        k=1)[0]
                else:
                    while True:
                        scenario_func, scenario_args = random.choices(
                            [(s[0], (player, random.choice(other_players))) 
                            if s[0] in [Scenarios.get_death_scenario, Scenarios.get_social_scenario] else (s[0], (player,)) 
                            for s in scenarios], 
                            weights=[s[1] for s in scenarios], 
                            k=1)[0]
                        if scenario_func not in [Scenarios.get_death_scenario, Scenarios.get_social_scenario] or scenario_args[1] not in players_in_event:
                            break
                    
                    if scenario_func == Scenarios.get_death_scenario and len(alive_players) >= 3:
                        if self.get_team(player) == self.get_team(scenario_args[1]):  # Check if they are on the same team
                            scenario_func = Scenarios.get_teammate_scenario
                            players_in_event.extend([player, scenario_args[1]])
                            scenario_args = (player, scenario_args[1])
                        else:
                            # Choose a player that has not been in an event yet
                            next_players = [p for p in alive_players if p != player and p != scenario_args[1] and p not in players_in_event]
                            if next_players:
                                next_player = next_players[0]
                                if self.get_team(player) != self.get_team(scenario_args[1]) and self.get_team(next_player) in [self.get_team(player), self.get_team(scenario_args[1])]:
                                    scenario_func = Scenarios.get_three_player_death_scenario
                                    scenario_args = (player, scenario_args[1], next_player)
                                    players_in_event.append(next_player)

                # Add players to the players_in_event list
                players_in_event.append(player)
                if scenario_func in [Scenarios.get_social_scenario, Scenarios.get_death_scenario, Scenarios.get_three_player_death_scenario]:
                    players_in_event.append(scenario_args[1])
                    alive_players.remove(scenario_args[1])
                if scenario_func == Scenarios.get_three_player_death_scenario:
                    players_in_event.append(scenario_args[2])
                    alive_players.remove(scenario_args[2])
                if scenario_func in [Scenarios.get_natural_death_scenario]:
                    alive_players.remove(player)
                    player.alive = False

                events.append(scenario_func(*scenario_args))
                if len(self.get_alive_teams()) == 1:
                    events.append("Only one team is left. Ending the day early.")
                    break     
                       
        leaderboard = self.generate_leaderboard()
        self.simulation.append({
            'night': self.day,
            'deaths': printDeaths,
            'alive_players': alive_players_start,
            'events': events,
            'leaderboard' : leaderboard
        })
    def generate_leaderboard(self):
        player_dict = {p.name: p for team in self.teams for p in team.members}
        
        #print("\nKill Leaderboard:")
        alive_player_names = {p.name for p in self.get_alive_players()}  # Names of the alive players

        # Get kill counts for dead players
        kill_counts = [(self.get_team(player_dict[p_name]).name, p_name, 'Died on ' + time_of_death + ' ' + str(day_of_death), kill_count) 
                for p_name, (day_of_death, time_of_death, kill_count) in self.deaths.items()
                if p_name not in alive_player_names]

        # Get kill counts for alive players
        kill_counts += [(self.get_team(p).name, p.name, 'Alive', p.kill_count) 
                        for p in self.get_alive_players()]

        # Sort by team name (which includes district number), then by player name
        kill_counts.sort(key=lambda x: (x[0], x[1]))

        # Print sorted leaderboard
        leaderboard = [(team_name, player_name, status, kill_count)
                       for team_name, player_name, status, kill_count in kill_counts]
        return leaderboard

    def start(self):
        self.previous_alive_players = []
        while len(self.get_alive_teams()) > 1:
            self.simulate_day()
            #self.generate_leaderboard()
            if (len(self.get_alive_teams()) > 1):
                self.simulate_night()
                #self.generate_leaderboard()
        
        #print("\nThe game has ended. The winner is:")
        winners = []
        for team in self.get_alive_teams():
            for player in team.members:
                if player.alive:
                    winners.append(f"{player.name} from {team.name}")
        #print("\nKill Leaderboard:")
        
        final_leaderboard = self.generate_leaderboard()
        self.simulation.append({
            'final_leaderboard': final_leaderboard,
            'winners' : winners
        })
        with open('json.json', 'w') as json_file:
            json.dump(self.simulation, json_file, indent = 2)
        return json.dumps(self.simulation, indent = 2)

# Create players
player1 = Player("Player 1", "male")
player2 = Player("Player 2", "female")
player3 = Player("Player 3", "male")
player4 = Player("Player 4", "female")
player5 = Player("Player 5", "male")
player6 = Player("Player 6", "female")
player7 = Player("Player 7", "male")
player8 = Player("Player 8", "female")
player9 = Player("Player 9", "male")
player10 = Player("Player 10", "female")
player11 = Player("Player 11", "male")
player12 = Player("Player 12", "female")
'''
player13 = Player("Player 13", "male")
player14 = Player("Player 14", "female")
player15 = Player("Player 15", "male")
player16 = Player("Player 16", "female")
player17 = Player("Player 17", "male")
player18 = Player("Player 18", "female")
player19 = Player("Player 19", "male")
player20 = Player("Player 20", "female")
player21 = Player("Player 21", "male")
player22 = Player("Player 22", "female")
player23 = Player("Player 23", "male")
player24 = Player("Player 24", "female")
'''
# Create teams
team1 = Team(player1, player2,1)
team2 = Team(player3, player4,2)
team3 = Team(player5, player6,3)
team4 = Team(player7, player8,4)
team5 = Team(player9, player10,5)
team6 = Team(player11, player12,6)
'''
team7 = Team(player13, player14, 7)
team8 = Team(player15, player16, 8)
team9 = Team(player17, player18, 9)
team10 = Team(player19, player20, 10)
team11 = Team(player21, player22, 11)
team12 = Team(player23, player24, 12)
'''

# Create game and start it
#game = Game([team1, team2, team3, team4, team5, team6, team7, team8, team9, team10, team11, team12])  # add all teams to this list
game = Game([team1, team2, team3, team4, team5, team6])
data = game.start()










    
