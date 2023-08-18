import discord
import os
import chess
import time
import asyncio
import json
from dotenv import load_dotenv
from chess_functions import *

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = os.getenv('TOKEN')

board, enginePath = chess.Board(), ''

@client.event
async def on_ready():
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	username = str(message.author).split("#")[0]
	channel = str(message.channel.name)
	user_message = str(message.content)

	################## GAME LOGIC ######################
	if channel == "chess":
		global board, enginePath

		# show help commands
		if user_message == "$help":
			with open("help.txt", 'r') as help_file:
				contents = help_file.read()
				hyperlink = "<https://en.wikipedia.org/wiki/Algebraic_notation_(chess)>"
				await message.channel.send(f"{contents} [here]({hyperlink}).")
				
		elif user_message == "Stockfish":
			engine = "Stockfish"
			await message.channel.send("You will play against Stockfish: ELO ~3800.")
			await print_board(board, message)
			with open("engines_config.json", "r") as config_file:
				enginePath = json.load(config_file)['engines'][engine]['path']

		# restart match
		elif user_message == "$restart":
			board = chess.Board()
			await message.channel.send("Let's restart. Welcome to ChessBot. Are you ready to play? Please enter your moves in strategic algebra notation.\nUse command '$help' at any time for help.")
			time.sleep(1)
			await print_board(board, message)
		
		# print current board
		elif user_message == '$board':
			await print_board(board, message)
			
		# print legal moves
		elif user_message == '$legal_moves':
			await message.channel.send(board.legal_moves)
			
		# no engine selected
		elif not enginePath:
			await message.channel.send("Please select your engine first.")
			
		# attempted player move
		else:
			try:
				board.push_san(user_message)
				await print_board(board, message)
				await notify_checks(board, message)
				
				# engine move
				engineMove = await engine_play(enginePath, board)
				board.push(engineMove.move)
				await print_board(board, message)
				await notify_checks(board, message)
				
			except ValueError as e:
				await message.channel.send("That is an invalid move. Please try again. For command help or proper san move notation, type '$help'.")

if __name__ == "__main__":
	asyncio.run(client.run(token))