from Scripts import npc


class NpcAgent(npc.Npc):

    def __init__(self, name, health, description, home, type):
        super().__init__(name, health, description)

        # A room in the dungeon where the agent will return to.
        self.home = home

        # The room the agent is currently in.
        self.currentRoom = ''

        # The type of character the agent is, e.g. merchant, guard, noble.
        self.type = type

        # List of possible commands.
        self.options = ["go", "wait", "say"]

        # An equal probability weighting.
        self.defaultWeight = 1 / len(self.options)

        # Values to set probability of choosing one of the above options. Must add to 1.0!
        self.optionWeights = [self.defaultWeight] * len(self.options)

        # List of possible directions to move
        self.moveDirections = []

    # Clear the list of options
    def ClearOptions(self):
        self.options.clear()

class AgentBuilder:

    """
    Types of agent:
        guard, merchant, commoner, noble
    """

    def __init__(self, dungeon):
        # The dungeon the agents are being created for.
        self.dungeon = dungeon

        # List of agents
        self.agents = []

    def BuildAgents(self):
        # Create ai agents.
        guardAgent = NpcAgent("City Guard", 1, "A guard of the city.", "SouthGate", "guard")
        merchantAgent = NpcAgent("Spice Merchant", 1, "A merchant in rich silks.", "Market", "merchant")
        citizenAgent = NpcAgent("Citizen", 1, "An ordinary citizen.", "SouthRoad", "commoner")

        guardAgent.optionWeights = [0.2, 0.6, 0.2]
        merchantAgent.optionWeights = [0.3, 0.4, 0.3]
        citizenAgent.optionWeights = [0.5, 0.3, 0.2]

        # Add agents to list.
        self.agents.append(guardAgent)
        self.agents.append(merchantAgent)
        self.agents.append(citizenAgent)

    def SetUpAgents(self):
        # Setup agent values and add to dictionary of agents.
        for agent in self.agents:
            agent.currentRoom = agent.home
            self.dungeon.agents[agent.name] = agent


class ConversationPieces:

    def __init__(self):
        self.greetings = ["Hello.", "Hi."]
        self.farewells = ["Goodbye.", "Farewell."]

        self.genericIdle = ["..."]

        self.guardIdle = ["Mind your manners traveller.", "No lollygagging."]
        self.merchantIdle = ["Out of my way traveller.", "Spices! Fresh spices! Dried spices!"]


