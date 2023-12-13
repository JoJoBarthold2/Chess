from ChessEngine import Move
import time


class MrReplay:
    def __init__(self, move_log=None, color=None):
        # color either 'b' or 'w'
        self.move_queue = None

        self.nextMove = None
        self.counter = None
        self.currentDepth = None
        self.start = None
        self.timeout = None
        self.globalBestMove = None
        self.globalBestScore = None
        self.nextMoveScore = None

        self.move_log = move_log
        self.counter = color
        #self.color = 0 if color == 'w' else 1

    def get_move(self):
        move = None
        while not self.move_queue.empty():
            move = self.move_queue.get()
        return move

    def update_move(self, move, score=-1, depth=-1):
        self.move_queue.put([move, score, depth])

    def clear_queue(self, outer_queue):
        self.move_queue = outer_queue


    def findBestMove(self, gs):
        """
        AI that plays a random Move out of the legal Moves

        Parameters
        ----------
        validMoves : list
            list of valid/legal moves

        Returns
        -------
        Move

        """
        counter = self.counter.get()
        start, end = self.move_log[counter]
        mv = Move(start, end, gs.board)
        counter += 2
        self.counter.put(counter)
        self.update_move(mv, -1, -1)

        while True:
            time.sleep(1)

