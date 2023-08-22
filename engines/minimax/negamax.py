from evaluation import get_board_score
import chess

def minimax(board, depth, alpha, beta, maximizingPlayer):
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
                maxEval = evaluation
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
                minEval = evaluation
            beta = min(beta, evaluation[0])
            if beta <= alpha:
                break

        return minEval


if __name__ == "__main__":
    board = chess.Board()
    board.push_san('d4')
    board.push_san('d6')
    board.push_san('e4')
    move = minimax(board, 2, float('-inf'), float('inf'), False)
    print(move)