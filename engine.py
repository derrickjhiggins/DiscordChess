import asyncio
import chess
import chess.engine
path = "/usr/local/Cellar/stockfish/16/bin/stockfish"

async def enginePlay() -> None:
    transport, engine = await chess.engine.popen_uci(path)

    board = chess.Board()
    while not board.is_game_over():
        result = await engine.play(board, chess.engine.Limit(time=0.5))
        board.push(result.move)
        print(board,end='\n\n')

    print(board.outcome())
    await engine.quit()

if __name__ == "__main__":
    asyncio.run(enginePlay())