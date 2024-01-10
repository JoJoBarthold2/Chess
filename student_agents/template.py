import random



class Agent:
    def __init__(self):
        self.move_queue = None
        self.maxDepth = 0
        self.value = 0
        self.ZobristTable = self.initTable()
        self.lookupTable = {}
        
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
        orderedMoves = self.initialize_move_list(gs.getValidMoves())
        while True: #iterative deepening
            self.maxDepth += 1
            
            self.nextMove = None
            orderedMoves = self.negamaxFirst(gs, orderedMoves, self.maxDepth, 1 if gs.whiteToMove else -1, -float("inf"), float("inf"))
            bestScore = orderedMoves[0][1]
            self.update_move(self.nextMove, bestScore, self.maxDepth)



    def initialize_move_list(self,moves): 
        """helper function that creates a list of moves we can later sort"""
        move_eval = []
        for move in moves:
            move_eval.append([move,float("-inf")])
        return move_eval


    def negamaxFirst(self,gs, orderedMoves, depth, turn, alpha, beta):
        """returns sorted list of moves based on the heuristic,which can be used to order moves for next deepening iteration"""
        
        if depth == 0 or gs.checkMate or gs.staleMate or gs.draw or gs.staleMate:
            return turn * self.heuristic(gs)
        maxScore = -float("inf")
        for i in range(len(orderedMoves)):
            gs.makeMove(orderedMoves[i][0])
            gs.getValidMoves()
            nextMoves = gs.getValidMoves()
            score = -self.negamax(gs, nextMoves, depth -1, -turn, -beta, -alpha)
            orderedMoves[i][1] = score
            if score > maxScore:
                maxScore = score
                if depth == self.maxDepth:
                    self.nextMove = orderedMoves[i][0]
            gs.undoMove()
            
            if maxScore > alpha: #prune
                alpha = maxScore
            if alpha >= beta:
                break
        orderedMoves.sort(key = lambda x: x[1], reverse = True)
        return orderedMoves
    




    def negamax(self,gs, validMoves, depth, turn, alpha, beta):
        """simpler version of negamax for the subsequent iterations of negamax""" 
        if depth == 0 or gs.checkMate or gs.staleMate or gs.draw or gs.staleMate:
            return turn * self.heuristic(gs)
        maxScore = -float("inf")
        for move in validMoves:

            gs.makeMove(move)
            gs.getValidMoves()
            nextMoves = gs.getValidMoves()
            score = -self.negamax(gs, nextMoves, depth -1, -turn, -beta, -alpha)
            if score > maxScore:
                maxScore = score
                if depth == self.maxDepth:
                    self.nextMove = move
            gs.undoMove()
            
            if maxScore > alpha: #prune
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

    def heuristic(self, state):
        """function that evaluates a gamestate based on the pieces and their position"""
        h = self.computeHash(state, self.ZobristTable)
        if h in self.lookupTable:
            return self.lookupTable[h]
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
        queenScore = [1, 1, 8, 1, 1, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 3, 3, 2, 1,
                        1, 2, 2, 2, 2, 1,
                        1, 1, 6, 1, 1, 1]
        whitePawnScore = [10, 10, 10, 10, 10, 10,
                        9, 9, 9, 9, 9, 9,
                        8, 8, 8, 8, 8, 8,
                        1, 2, 4, 4, 1, 1,
                        2, 4, 1, 1, 4, 2,
                        0, 0, 0, 0, 0, 0]
        blackPawnScore = [0, 0, 0, 0, 0, 0,
                        2, 4, 1, 1, 1, 2,
                        1, 2, 1, 1, 4, 1,
                        1, 2, 4, 4, 2, 1,
                        9, 9, 9, 9, 9, 9,
                        10, 10, 10, 10, 10, 10]
        dummyScore = [0, 0, 0, 0, 0, 0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0,
                        0,0,0,0,0,0]
        piecePosScores = {"K": dummyScore, "Q": dummyScore, "B": bishopScore, "N": nightScore, "wp": whitePawnScore, "bp": blackPawnScore}

        if state.checkMate:
        
            if state.whiteToMove:
                value = - float("inf")
            else:
                value =  float("inf")
            return value
        elif state.staleMate or state.draw or state.staleMate:
            return value 
    
        for i in range(len(state.board)):   
            piece = state.board[i]
            piecePosScore = 0
            if piece != "--":
                if piece[1] == "p":
                    piecePosScore = piecePosScores[piece][i]
                else:
                    piecePosScore = piecePosScores[piece[1]][i]
                if piece[0] == "w":
                    value += pieceScore[piece[1]]+ piecePosScore * .1
                elif piece[0] == "b":
                    value -= pieceScore[piece[1]]+  piecePosScore * .1
        self.lookupTable[h] = value
        return value
   
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
    # Generates a Random number from 0 to 2^64-1
    def randomInt(self):
        min = 0
        max = pow(2, 36)
        return random.randint(min, max)
    
    # This function associates each piece with
    # a number
    def indexOf(self, piece):
        if (piece=='wp'):
            return 0
        elif (piece=='wN'):
            return 1
        elif (piece=='wB'):
            return 2
        elif (piece=='wQ'):
            return 3
        elif (piece=='wK'):
            return 4
        elif (piece=='bp'):
            return 5
        elif (piece=='bN'):
            return 6
        elif (piece=='bB'):
            return 7
        elif (piece=='bQ'):
            return 8
        elif (piece=='bK'):
            return 9
        else:
            return -1
    
    # Initializes the table
    def initTable(self):
        # 6x6x9 array
        ZobristTable = [[self.randomInt() for k in range(10)] for j in range(36)]
        return ZobristTable
    
    # Computes the hash value of a given board
    def computeHash(self,gs, ZobristTable):
        h = 0
        for i in range(36):
            if (gs.board[i] != '-'):
                piece = self.indexOf(gs.board[i])
                h ^= ZobristTable[i][piece]
        return h


#----------------------- explanation----------------------  
# We used negamax as a basic framework. One of the reasons for this was that we had problems implementing classing min-max search , as stated in the forum. Also it is shorter to write
# We use a relatively simple heuristic, we simply add up values of the pieces and then also add weighting values with certain look up tables for each piece
# We used iterative deepening to use the available time optimally. To reduce the effort for computing the evaluation we added hashing. We used Zobrist hashing since it is popular
# for chess engines and also quite effective. 
#  Another important aspect of iterative deepening is that we try use the previos iteration to guess a good move oder so we can prune a lot of moves. This is done by remembering
# the scores of this iteration and keeping them in a list in decending order. This approach is somewhat naive but it had good results for us. 