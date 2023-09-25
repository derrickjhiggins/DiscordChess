import chess.engine

async def display_board(board, message):
	formatted_board = f"```\n{board.unicode(empty_square=' ', borders=True, invert_color=True)}```"
	await message.channel.send(formatted_board)

async def notify_checks(board, message):
    # check for check/checkmate/statemate
    if board.is_checkmate():
        winner = "White" if board.outcome().winner else "Black"
        await message.channel.send(f"Checkmate: {winner} wins!\nType '$play' to begin a new match.")
        return					
    elif board.is_check():
        await message.channel.send("Check.")
    elif board.is_stalemate() or board.is_fivefold_repetition():
        await message.channel.send("Stalemate.")
        return
	
async def engine_play(enginePath, board) -> None:
    transport, engine = await chess.engine.popen_uci(enginePath)
    result = await engine.play(board, chess.engine.Limit(time=0.1))
    await engine.quit()
    return result