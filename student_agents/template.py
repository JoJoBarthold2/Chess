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
        # TODO


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
        values_of_pieces = [4, 3, 5, 9, 0, 1] #King is 0 because it is not a piece that can be captured
        my_pieces = []
        if (gs.whiteToMove): #set the color of the player
            color = "w"
        else:
            color = "b"	

        
        for i in range( 0,len(pieces) ):    #modify the pieces to match the color of the player
                my_pieces.append( color + pieces[i])
              
        if(gs.checkMate):
            return  -float("inf")
        elif(gs.staleMate):
            return 0
        else: 
            score = 0
            for i in range(36):
                piece = gs.board[i]
                if(piece != "--"):
                    if(piece in my_pieces):
                        score += values_of_pieces[pieces.index(piece[1])]
                    else:
                        score -= values_of_pieces[pieces.index(piece[1])]
            return score

         

