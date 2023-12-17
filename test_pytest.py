import student_agents.template as template_agent
import ChessEngine 

checkkmate = ChessEngine.GameState()
checkkmate.checkMate = True

staleMate = ChessEngine.GameState()
staleMate.staleMate = True

good_for_white = ChessEngine.GameState()

good_for_white.board = ['bN', '--', 'bQ', 'bK', 'bB', '--',
                      'bp', 'bp', 'bp', '--', 'bp', 'bp',
                      '--', '--', '--', '--', '--', '--',
                      '--', '--', '--', '--', '--', '--',
                      'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
                      'wN', 'wB', 'wQ', 'wK', 'wB', 'wN']
good_for_white.whiteToMove = True

def test_heuristic_for_checkmate():
 assert template_agent.Agent.simpleHeuristic(template_agent.Agent(),checkkmate) == -float("inf")

def test_heuristic_for_stalemate():
 assert template_agent.Agent.simpleHeuristic(template_agent.Agent(),staleMate) == 0

def test_heuristic_for_good_for_white():
 assert template_agent.Agent.simpleHeuristic(template_agent.Agent(),good_for_white) == 8




