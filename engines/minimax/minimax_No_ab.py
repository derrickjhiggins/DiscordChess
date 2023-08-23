from evaluation import get_board_score
import chess
calls = 0

def minimax_No_ab(board, depth, alpha, beta, maximizingPlayer):
    global calls
    calls += 1
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return get_board_score(board), None

    if maximizingPlayer: # white to move
        maxEval = float('-inf'), None
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            evaluation = minimax_No_ab(boardCopy, depth - 1, alpha, beta, False)

            # get best move
            if evaluation[0] > maxEval[0]:
                maxEval = evaluation[0], move

        return maxEval

    else: # black to move
        minEval = float('inf'), None
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            evaluation = minimax_No_ab(boardCopy, depth - 1, alpha, beta, True)
            if evaluation[0] < minEval[0]:
                minEval = evaluation[0], move

        return minEval