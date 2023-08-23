from evaluation import get_board_score
import chess
calls = 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    global calls
    calls += 1
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return get_board_score(board), None

    if maximizingPlayer: # white to move
        maxEval = float('-inf'), None
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            evaluation = minimax(boardCopy, depth - 1, alpha, beta, False)

            # get best move
            if evaluation[0] > maxEval[0]:
                maxEval = evaluation[0], move
            alpha = max(alpha, evaluation[0])
            if beta <= alpha:
                break

        return maxEval

    else: # black to move
        minEval = float('inf'), None
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            evaluation = minimax(boardCopy, depth - 1, alpha, beta, True)
            if evaluation[0] < minEval[0]:
                minEval = evaluation[0], move
            beta = min(beta, evaluation[0])
            if beta <= alpha:
                break

        return minEval


if __name__ == "__main__":
    board = chess.Board()
    turn = 0
    while not (board.is_checkmate() or board.is_stalemate() or board.is_fivefold_repetition()):
        if turn % 2 == 0:
            move = minimax(board, 1, float('-inf'), float('inf'), True)
            print(move)
            board.push(move[1])
        else:
            move = minimax(board, 3, float('-inf'), float('inf'), False)
            print(move)
            board.push(move[1])
        print(board)
        print(calls)
        turn += 1
    print(board.outcome())