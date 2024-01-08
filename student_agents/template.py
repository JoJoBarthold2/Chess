import random
import sys
sys.path.append('C:/Users/morit/OneDrive/Desktop/Chess')
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
        """
        if self.count_pieces(gs) <= 5:
            depth = 8
        elif self.count_pieces(gs) <= 8:
            depth = 6
        elif self.count_pieces(gs) <= 3:
            depth = 10
        else: 
            depth = 4
        valid_moves = self.initialize_move_list(gs, gs.whiteToMove)
        

        for i in range(len(valid_moves)):
            valid_moves[i][1] = self.minimax(gs, depth, float("-inf"), float("inf")) #white is maximizing player
        if gs.whiteToMove:
            best_move = max(valid_moves, key=lambda x: x[1])
        else:  
            best_move = min(valid_moves, key=lambda x: x[1])
        
        
        
        self.update_move(best_move[0], best_move[1], depth)
         
    


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
        values_of_pieces = [3, 3, 5, 10, 0, 1] #King is 0 because it is not a piece that can be captured
        
        pawn_endgame_value_white = [2, 2, 2, 2, 2, 2, #first row is irrelevant but i just did this for being save
                      1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
                      1, 1, 1, 1, 1, 1,
                      0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                      0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
                      0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        
        pawn_endgame_value_black = pawn_endgame_value_white[::-1]


       

        	
      
        

              
        if(gs.checkMate):
            return  float("-inf") if gs.whiteToMove else float("inf")
        elif(gs.staleMate):
            return 0
        else: 
            score = 0
            for i in range(36):
                piece = gs.board[i]
                if(piece != "--"):
                    if(piece[0]=="w"):
                        if(piece[1]=="p" and self.count_pieces(gs) <= 8):
                            score += pawn_endgame_value_white[i]
                        else:
                            score +=  values_of_pieces[pieces.index(piece[1])]
                       
                    else:
                        if(piece[1]=="p" and self.count_pieces(gs) <= 8):
                            score -= pawn_endgame_value_black[i]
                        else:
                            score -=   values_of_pieces[pieces.index(piece[1])]
            return score
        

    def minimax(self, gs, max_depth, alpha, beta):
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
       int
              heuristic value of the current state

        """
        if (max_depth == 0 or gs.checkMate or gs.staleMate):
            return self.simpleHeuristic(gs)
        valid_moves = gs.getValidMoves()
        random.shuffle(valid_moves)
        if (gs.whiteToMove):
            maxEval = float("-inf")
            for move in valid_moves:
                gs.makeMove(move)
                eval = self.minimax(gs, max_depth - 1, alpha, beta)
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
                eval = self.minimax(gs, max_depth - 1, alpha, beta)
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
        
        
    def count_pieces(self, gs):
        """
        Parameters
        ----------
        gs : Gamestate
            current state of the game
        Returns
        -------
        int
            number of pieces on the board
        """
        count = 0
        for i in range(36):
            if gs.board[i] != "--":
                count += 1
        return count

# if __name__ == '__main__':
#     gs = ChessEngine.GameState()
#     gs.board = ['--', '--', '--', '--', '--', '--',
#                 '--', 'bp', '--', '--', '--', '--',
#                 '--', '--', 'wp', '--', '--', '--',
#                 '--', '--', '--', '--', '--', '--',
#                 '--', '--', '--', '--', '--', '--',
#                 '--', '--', '--', '--', '--', '--']
#     gs.whiteToMove = True

#     agent = Agent()
#     valid_moves = gs.getValidMoves()
    
#    #print(move.pieceMoved() for move in agent.initialize_move_list(gs, gs.whiteToMove))
#     agent.findBestMove(gs)
    
#     print(agent.get_move())
        