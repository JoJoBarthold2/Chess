import random
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:/Users/morit/OneDrive/Desktop/Chess')
import ChessEngine


class Agent:
    def __init__(self):
        self.move_queue = None

    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score, depth):
        """
        :param move: Object of class Move, like a list element of gamestate.getValidMoves()
        :param score: Integer; not really necessary, just for informative printing
        :param depth: Integer; not really necessary, just for informative printing
        :return:
        """
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue

    def findBestMove(self, gs):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        Returns
        -------
        none

        """
        valid_moves = self.initialize_move_list(gs, gs.whiteToMove)
        move_eval = []
        
        for move in valid_moves:
            if gs.whiteToMove:
                move_eval.append([move, float('-inf')])
            else:
                move_eval.append([move, float('inf')])
    
        for i in range(len(move_eval)):
            move_eval[i][1] = self.negamax(move_eval[i][0], 2, gs.whiteToMove, gs)
        move_eval.sort(key=lambda x: x[1], reverse=gs.whiteToMove)

    def initialize_move_list(self, gs, white_to_move):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        white_to_move : bool
            True if white is to move, False if black is to move
        Returns
        -------
        valid_moves : list
            list of valid moves

        """
        valid_moves = gs.getValidMoves()
        if white_to_move:
            for i in range(len(valid_moves)-1, -1, -1):
                if valid_moves[i].pieceMoved[0] != 'w':
                    valid_moves.remove(valid_moves[i])
        else:
            for i in range(len(valid_moves)-1, -1, -1):
                if valid_moves[i].pieceMoved[0] != 'b':
                    valid_moves.remove(valid_moves[i])
        return valid_moves

if __name__ == '__main__':
    gs = ChessEngine.GameState()
    gs.board = ['--', 'bp', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--']
    gs.whiteToMove = False

    agent = Agent()
    valid_moves = agent.initialize_move_list(gs, False)

    expected_moves = gs.getValidMoves()
    for move in expected_moves:
        print(move.pieceMoved[0])
    
    