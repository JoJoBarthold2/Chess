import random
# import sys
# # caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, 'C:/Users/morit/OneDrive/Desktop/Chess')
import ChessEngine


class Agent:
    def __init__(self):
        self.move_queue = None
        self.maxDepth = 5
        nextMove = None
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
        self.nextMove = None
        self.negamax(gs, gs.getValidMoves(), self.maxDepth, 1 if gs.whiteToMove else -1, -float("inf"), float("inf"))
        self.update_move(self.nextMove, 0, 0)
    
    def negamax(self,gs, validMoves, depth, turn, alpha, beta):
         
        if depth == 0:
            return turn * self.heuristic(gs)
        maxScore = -float("inf")
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = -self.negamax(gs, nextMoves, depth -1, -turn, -beta, -alpha)
            if score > maxScore:
                maxScore = score
                if depth == self.maxDepth:
                    self.nextMove = move
            gs.undoMove()
            gs.checkmate, gs.stalemate = False, False
            if maxScore > alpha: #prune
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

    def heuristic(self, state, max_or_min = True):
        value =0
        pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
        nightScore = [1, 1, 1, 1, 1, 1,
                      1, 2, 2, 2, 2, 1,
                      1, 2, 3, 3, 2, 1,
                      1, 2, 3, 3, 2, 1,
                      1, 2, 2, 2, 2, 1,
                      1, 1, 1, 1, 1, 1]
        bishopScore = [   3, 3, 2, 1, 1, 4,
                          3, 4, 3, 2, 4, 3,
                          2, 3, 4, 4, 3, 2,
                          1, 2, 4, 4, 2, 1,
                          1, 4, 3, 2, 4, 1,
                          4, 1, 2, 1, 1, 4]
        queenScore = [1, 1, 3, 1, 1, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 1, 3, 1, 1, 1]
        rookScore = [1, 1, 1, 1, 1, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 1, 1, 1, 1, 1]
        pawnScore = [1, 1, 1, 1, 1, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 1, 1, 1, 1, 1]
        
        dummyScore = [0, 0, 0, 0, 0, 0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0]
        piecePosScores = {"K": dummyScore, "Q": queenScore, "R": rookScore, "B": bishopScore, "N": nightScore, "p": pawnScore}

        if state.checkMate:
        
            if max_or_min:
                value = - float("inf")
            else:
                value = float("inf")
            return value
        elif state.staleMate:
            return value 
    
        for i in range(len(state.board)):   
            piece = state.board[i]
            piecePosScore = 0
            if piece != "--":
                
                piecePosScore = piecePosScores[piece[1]][i]
                if piece[0] == "w":
                    value += pieceScore[piece[1]]+ piecePosScore * .2
                elif piece[0] == "b":
                    value -= pieceScore[piece[1]]+  piecePosScore * .2
        return value

#if __name__ == '__main__':
#    piecePosScores = {"K": 0, "Q": 9, "R": 5, "B": 2, "N": 2, "p": 1}
#    print(piecePosScores["--"][0])
    
    