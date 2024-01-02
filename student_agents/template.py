import random


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
       
        

        """
        valid_moves = self.initialize_move_list(gs, gs.whiteToMove)
        random.shuffle(valid_moves)
        for valid_move in valid_moves:
            valid_move[1] = self.negamax(gs, 5, float("-inf"), float("inf"))
        
        valid_moves.sort(key=lambda x: x[1], reverse=gs.whiteToMove)
        self.update_move(valid_moves[0][0], valid_moves[0][1], 3)
         
    


    def evaluate(self, gs):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        Returns 
        
        heuristic value of the current state 
        """

        pieces = ["N", "B", "R", "Q", "K", "p"]
        values_of_pieces = [4, 3, 5, 9, 0, 1] #King is 0 because it is not a piece that can be captured
        if(gs.checkMate):
            return  -float("inf") if gs.whiteToMove else float("inf")
        elif(gs.staleMate):
            return 0
        else: 
            score = 0
            for i in range(36):
                piece = gs.board[i]
                if(piece != "--"):
                    if(piece[0] == "w"):
                        score += values_of_pieces[pieces.index(piece[1])]
                    else:
                        score -= values_of_pieces[pieces.index(piece[1])]
            return score
        

    def negamax(self, gs, depth, alpha, beta):
        if depth == 0 or gs.checkMate or gs.staleMate:
            return self.evaluate(gs)  # Return the evaluation of the board

        max_eval = -float('inf')
        for move in gs.getValidMoves():
            gs.makeMove(move)
            eval = -self.negamax(gs, depth - 1, -beta, -alpha)
            gs.undoMove
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break  # Beta cutoff

        return max_eval    
        
    def initialize_move_list(self,gs, isMaximizingPlayer):
            valid_moves = gs.getValidMoves()
            move_eval = []
            for valid_move in valid_moves:
                move_eval.append([valid_move,float("-inf") if isMaximizingPlayer else float("inf")])
            return move_eval