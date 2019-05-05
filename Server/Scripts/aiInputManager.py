from colorama import Fore, init
import random
from Scripts import npcAgent, server
import numpy

import sys, os

class AiInputManager:

    def __init__(self, dungeon):

        # The current dungeon
        self.dungeon = dungeon

        self.agentInput = ''
        self.splitInput = ''
        self.command = ''

        # Possible movement directions in the dungeon.
        self.directions = ["north", "south", "east", "west"]

        self.conversation = npcAgent.ConversationPieces()

        # Initialise colorama
        init()

        self.verboseLog = False

    def Move(self, agent, direction):

        # Move to a new room
        newRoom = self.dungeon.Move(agent.currentRoom, direction)

        # Check if the player has actually changed rooms.
        if agent.currentRoom == newRoom:
            return "\nThere is nowhere to go in this direction."

        else:
            self.MessagePlayers(agent, "<br><font color=red>" + agent.name + " leaves the room, heading " + direction + ". </font>", True)

            agent.currentRoom = newRoom

            self.MessagePlayers(agent, "<br><font color=orange>" + agent.name + " enters the room from the " + direction + ". </font>", True)

            return "\n" + direction + "\n" + self.dungeon.rooms[agent.currentRoom].entryDescription

    # Check the current room for connections and add valid paths as options for the agent to take.
    def GetOptions(self, agent):
        # Clear any current options.
        agent.moveDirections.clear()

        self.LogOutput("Possible directions from this room.")

        for connection in self.dungeon.rooms[agent.currentRoom].connections:
            if self.dungeon.rooms[agent.currentRoom].connections[connection] != "":
                agent.moveDirections.append(connection)

        self.LogOutput(agent.moveDirections)

    # Choose which command to use.
    def MakeChoice(self, agent):
        self.LogOutput("AI making choice.")

        # Get a random choice from the agent's option list, based on the list of probabilities.
        optionChoice = numpy.random.choice(agent.options, p=agent.optionWeights)

        self.LogOutput("Choice: " + optionChoice)

        # Wait in room.
        if optionChoice == "wait":
            self.LogOutput("Waiting in room")
            self.LogOutput(Fore.CYAN + "AI current room: " + agent.currentRoom + "\n" + Fore.RESET)

            timeToWait = 4
            return timeToWait

        # Say something.
        elif optionChoice == "say":

            if agent.type == "guard":
                self.Say(agent, self.conversation.guardIdle[random.randint(0, len(self.conversation.guardIdle) - 1)])

            elif agent.type == "merchant":
                self.Say(agent, self.conversation.merchantIdle[random.randint(0, len(self.conversation.merchantIdle) - 1)])

            else:
                self.Say(agent, self.conversation.genericIdle[random.randint(0, len(self.conversation.genericIdle) - 1)])

            timeToWait = 3
            return timeToWait

        # Move to new room.
        elif optionChoice == "go":
            # Direction to move in
            moveDirection = agent.moveDirections[random.randint(0, len(agent.moveDirections) - 1)]

            self.LogOutput("Moving " + moveDirection)
            self.Move(agent, moveDirection)

            self.LogOutput(Fore.CYAN + "AI current room: " + agent.currentRoom + "\n" + Fore.RESET)

            self.Say(agent, self.conversation.greetings[random.randint(0, len(self.conversation.greetings) - 1)])

            timeToWait = 4
            return timeToWait

        else:
            print(Fore.RED + "Something is very wrong, an ai agent has chosen an option outside of it's programming! Look out!" + Fore.RESET)

            timeToWait = 1
            return timeToWait

    # Agent chooses some conversation pieces to say.
    def Say(self, agent, message):
        self.MessagePlayers(agent, "<br><font color=Yellow>" + agent.name + " says \"" + message + "\"</font>")

    # Outputs a message to other players. If sameRoomOnly is set to true, the message is only sent to players
    # in the same room as the player sending the message.
    def MessagePlayers(self, agent, message, sameRoomOnly=True):
        # For all other players in the game (excluding the speaker) display the message.
        for playerClient in self.dungeon.players:
            if self.dungeon.players[playerClient] != agent:

                # If the message should only be hear by players in the same room
                if sameRoomOnly is True:
                    if self.dungeon.players[playerClient].currentRoom == agent.currentRoom:
                        server.Server.OutputJson(playerClient, message)
                else:
                    server.Server.OutputJson(playerClient, message)

    def LogOutput(self, output):
        if self.verboseLog is True:
            print(output)