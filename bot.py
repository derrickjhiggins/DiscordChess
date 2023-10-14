import discord
import os
import chess
import time
import asyncio
import json
from dotenv import load_dotenv
from src.chess_functions import *
from src.engines.minimax.minimax import minimax
import platform

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = os.getenv('TOKEN')
operating_system = platform.platform()
matches = {} # userid: [board, selectedEnginePath]

# define new permissions
file_path = '/path/to/your/file.txt'

# set komodo permissions
file_path = '/app/src/engines/komodo-14/Linux/komodo-14.1-linux-bmi2'

new_permissions = 0o755

try:
    # Change the file permissions
    os.chmod(file_path, new_permissions)
    print(f"Permissions for {file_path} have been changed to {new_permissions:o}")
except OSError as e:
    print(f"Error: {e}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(f"Operating system: {operating_system}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    
    if message.author.id in matches:
        board = matches[message.author.id][0]

	################## GAME LOGIC ######################
    if channel == "chess":

        # reset current game 
        if user_message == "$play":
            board = chess.Board()
            matches[message.author.id] = [board]
            enginePath = ''
            await message.channel.send("Select an engine to play against by clicking an emoji:")
            engine_selection_msg, emojis = '', []
            with open("./src/engines/engines_config.json", "r") as config_file:
                chess_engines = json.load(config_file)

                # get engine data
                for engine, engine_data in chess_engines.items():
                    emoji = engine_data['emoji']
                    emojis.append(emoji)
                    engine_selection_msg += f'{emoji}: {engine}\n'
                select_engine = await message.channel.send(engine_selection_msg)

                # display emoji reactions
                for emoji in emojis:
                    await select_engine.add_reaction(emoji)

		# show help commands
        elif user_message == "$help":
            with open("./src/engines/help.txt", 'r') as help_file:
                contents = help_file.read()
                hyperlink = "<https://en.wikipedia.org/wiki/Algebraic_notation_(chess)>"
                await message.channel.send(f"{contents} [here]({hyperlink}).")
		
		# display current board
        elif user_message == '$board':
            await display_board(board, message)
			
		# display legal moves
        elif user_message == '$legal_moves':
            await message.channel.send(board.legal_moves)
			
		# no engine selected
        elif not matches[message.author.id][1]:
            await message.channel.send("Please select your engine first.")
			
		# attempted player move (not minimax)
        else:
            board = matches[message.author.id][0]
            enginePath = matches[message.author.id][1]
            try:
                # capitalization correction for pawn movement
                if len(user_message) == 2:
                    user_message = user_message.lower()
                board.push_san(user_message)
                await display_board(board, message)
                await notify_checks(board, message)
				
				# engine to move
                if enginePath == "minimax": # minimax engine move
                    engineMove = minimax(board, 3, float('-inf'), float('inf'), False)
                    board.push(engineMove[1])
                else: # other engine move
                    engineMove = await engine_play(enginePath, board)
                    board.push(engineMove.move)
                await display_board(board, message)
                await notify_checks(board, message)
                
            except ValueError as e:
                await message.channel.send("That is an invalid move. Please try again. For command help or proper san move notation, type '$help'.")

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    elif len(matches[user.id]) > 1: # ensure only 1 emoji selected
        return

    channel = str(reaction.message.channel.name)
    emoji = reaction.emoji

    if channel == "chess":
        board = matches[user.id][0]
        with open("./src/engines/engines_config.json", "r") as config_file:
            chess_engines = json.load(config_file)

            selected_engine = None
            for engine, engine_data in chess_engines.items():
                if emoji == engine_data['emoji']:
                    selected_engine = engine
                    break

            if selected_engine:
                enginePath = chess_engines[selected_engine]["path"]
                matches[user.id].append(enginePath)
                await reaction.message.channel.send(f"You selected {selected_engine} as the engine to play against.")
                await display_board(board, reaction.message)
            else:
                await reaction.message.channel.send("Invalid emoji selection.")


if __name__ == "__main__":
	asyncio.run(client.run(token))