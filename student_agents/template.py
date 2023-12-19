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
            valid_move[1] = self.minimax(gs, 5, float("-inf"), float("inf"), gs.whiteToMove)
        
        valid_moves.sort(key=lambda x: x[1], reverse=gs.whiteToMove)
        self.update_move(valid_moves[0][0], valid_moves[0][1], 3)
         
    


    def simpleHeuristic(self, gs):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        Returns 
        
        heuristic value of the current state 
        """

        pieces = ["N", "B", "R", "Q", "K", "p"]
        values_of_pieces = [4, 3, 5, 10, 0, 1] #King is 0 because it is not a piece that can be captured
        
       
        	

        

              
        if(gs.checkMate):
            return  -float("inf") if gs.whiteToMove else float("inf")
        elif(gs.staleMate):
            return 0
        else: 
            score = 0
            for i in range(36):
                piece = gs.board[i]
                if(piece != "--"):
                    if(piece[0]=="w"):
                        score += values_of_pieces[pieces.index(piece[1])]
                    else:
                        score -= values_of_pieces[pieces.index(piece[1])]
            return score
        

    def minimax(self, gs, max_depth, alpha, beta, isMaximizingPlayer):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        depth : int
            depth of the tree
       
        isMaximizingPlayer : bool
            true if it is the maximizing player's turn
        Returns
        -------
        best move for the current state
        its depth 
        and its score

        """
        if (max_depth == 0 or gs.checkMate or gs.staleMate):
            return self.simpleHeuristic(gs)
        valid_moves = gs.getValidMoves()
        random.shuffle(valid_moves)
        if (isMaximizingPlayer):
            maxEval = float("-inf")
            for move in valid_moves:
                gs.makeMove(move)
                eval = self.minimax(gs, max_depth - 1, alpha, beta, False)
                gs.undoMove()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = float("inf")
            for move in valid_moves:
                gs.makeMove(move)
                eval = self.minimax(gs, max_depth - 1, alpha, beta, True)
                gs.undoMove()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

       




    def initialize_move_list(self,gs, isMaximizingPlayer):
            valid_moves = gs.getValidMoves()
            move_eval = []
            for valid_move in valid_moves:
                move_eval.append([valid_move,float("-inf") if isMaximizingPlayer else float("inf")])
            return move_eval
        
        
        