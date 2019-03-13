from Scripts import npc


class NpcAgent(npc.Npc):

    def __init__(self, name, health, description, home):
        super().__init__(name, health, description)

        # A room in the dungeon where the agent will return to.
        self.home = home
        self.currentRoom = ''

        # List of possible commands.
        self.options = []

    # Clear the list of options
    def ClearOptions(self):
        self.options.clear()

    def Move(self):
        print("")


class AgentBuilder:

    def __init__(self, dungeon):
        # The dungeon the agents are being created for.
        self.dungeon = dungeon

        # List of agents
        self.agents = []

    def BuildAgents(self):
        # Create ai agents.
        guardAgent = NpcAgent("City Guard", 1, "A guard of the city.", "SouthGate")
        merchantAgent = NpcAgent("Spice Merchant", 1, "A merchant in rich silks.", "Market")
        citizenAgent = NpcAgent("Citizen", 1, "An ordinary citizen.", "SouthRoad")

        # Add agents to list.
        self.agents.append(guardAgent)
        self.agents.append(merchantAgent)
        self.agents.append(citizenAgent)

    def SetUpAgents(self):
        # Setup agent values.
        for agent in self.agents:
            agent.currentRoom = agent.home
            self.dungeon.agents[agent.name] = agent
