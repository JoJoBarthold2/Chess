import template as template_agent
import ChessEngine 

def test_initialize_move_list_for_white():
    gs = ChessEngine.GameState()
    gs.board = ['--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--']
    gs.whiteToMove = True

    agent = template_agent.Agent()
    valid_moves = agent.initialize_move_list(gs, True)

    expected_moves = gs.getValidMoves()
    for move in expected_moves:
        assert move.pieceMoved[0] == 'w'
    assert valid_moves == expected_moves

def test_initialize_move_list_for_black():
    gs = ChessEngine.GameState()
    gs.board = ['--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--',
                '--', '--', '--', '--', '--', '--']
    gs.whiteToMove = False

    agent = template_agent.Agent()
    valid_moves = agent.initialize_move_list(gs, False)

    expected_moves = gs.getValidMoves()
    for move in expected_moves:
        assert move.pieceMoved[0] == 'b'
    assert valid_moves == expected_moves