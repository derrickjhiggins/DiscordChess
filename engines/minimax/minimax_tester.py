import unittest
from minimax import minimax
from minimax_No_ab import minimax_No_ab
import chess

class MiniMaxTestCase(unittest.TestCase):
    def test_ab_pruning(self):
        withPruningBoard = chess.Board()
        withoutPruningBoard = chess.Board()
        turn = 0

        while not (withPruningBoard.is_checkmate() or withPruningBoard.is_stalemate() or withPruningBoard.is_fivefold_repetition()):
            if turn % 2 == 0:
                pruningMove = minimax(withPruningBoard, 2, float('-inf'), float('inf'), True)
                withoutPruningMove = minimax_No_ab(withoutPruningBoard, 2, float('-inf'), float('inf'), True)
                self.assertEqual(pruningMove, withoutPruningMove)
                withPruningBoard.push(pruningMove[1])
                withoutPruningBoard.push(withoutPruningMove[1])
            else:
                pruningMove = minimax(withPruningBoard, 2, float('-inf'), float('inf'), False)
                withoutPruningMove = minimax_No_ab(withoutPruningBoard, 2, float('-inf'), float('inf'), False)
                self.assertEqual(pruningMove, withoutPruningMove)
                withPruningBoard.push(pruningMove[1])
                withoutPruningBoard.push(withoutPruningMove[1])
            turn += 1
            print(pruningMove, withoutPruningMove)
            pruningOutcome = withPruningBoard.outcome()
            withoutPruningOutcome = withoutPruningBoard.outcome()
        print(pruningOutcome, withoutPruningOutcome)
        self.assertEqual(pruningOutcome, withoutPruningOutcome)

    def test_optimal_move_generation(self):
        # test with specific instances of checkmate in 1/2 moves that correct move is chosen
        pass

if __name__ == "__main__":
    unittest.main()