import student_agents.template as template_agent
import ChessEngine 

checkkmate = ChessEngine.GameState()
checkkmate.checkMate = True


def test_heuristic():
 assert template_agent.Agent.simpleHeuristic(template_agent.Agent(),checkkmate) == -float("inf")


