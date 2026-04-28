"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

import chess
from spell_logic import SpellChessGame, squares_in_3x3, squares_in_jump_range


# ------------------------------------------------------------------ #
#  Demo tests — provided to students as examples                      #
# ------------------------------------------------------------------ #

class TestFreezeTarget:
    """Casting Freeze should mark the opponent's color as frozen."""

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        # The frozen color should be Black (the opponent), not White
        assert game.freeze_effect_color == chess.BLACK


class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug — document it!                 #
<<<<<<< HEAD
# ------------------------------------------------------------------ #

# tests standard chess moves
class TestStandardChess:
    def test_pawn_single_advance(self):
        # move: e2 -> e3
        game = SpellChessGame()

        result = game.make_move(chess.E2, chess.E3)

        assert result is True
        assert game.board.piece_at(chess.E3) is not None
        assert game.board.piece_at(chess.E2) is None

    def test_pawn_double_advance_at_start(self):
        game = SpellChessGame()

        result = game.make_move(chess.E2, chess.E4)

        assert result is True
        assert game.board.piece_at(chess.E4) is not None
        assert game.board.piece_at(chess.E2) is None

    def test_pawn_cannot_double_advance_after_start(self):
        game = SpellChessGame()

        game.make_move(chess.E2, chess.E4)
        game.board.turn = chess.WHITE
        result = game.make_move(chess.E4, chess.E6)

        assert result is False
        assert game.board.piece_at(chess.E6) is None
        assert game.board.piece_at(chess.E4) is not None

    def test_pawn_captures_diagonally(self):
        # white(e4) captures black(d5)
        game = SpellChessGame()
        white = chess.Piece(chess.PAWN, chess.WHITE)
        black = chess.Piece(chess.PAWN, chess.BLACK)

        game.board.set_piece_at(chess.E4, white)
        game.board.set_piece_at(chess.D5, black)

        result = game.make_move(chess.E4, chess.D5)

        assert result is True
        assert game.board.piece_at(chess.D5).piece_type == chess.PAWN
        assert game.board.piece_at(chess.D5).color == chess.WHITE
        assert game.board.piece_at(chess.E4) is None

    def test_pawn_cannot_capture_straight(self):
        game = SpellChessGame()
        game.board.clear()
        
        white = chess.Piece(chess.PAWN, chess.WHITE)
        black = chess.Piece(chess.PAWN, chess.BLACK)

        game.board.set_piece_at(chess.E4, white)
        game.board.set_piece_at(chess.E5, black)

        result = game.make_move(chess.E4, chess.E5)

        assert result is False
        assert game.board.piece_at(chess.E4).piece_type == chess.PAWN
        assert game.board.piece_at(chess.E4).color == chess.WHITE
        assert game.board.piece_at(chess.E5).piece_type == chess.PAWN
        assert game.board.piece_at(chess.E5).color == chess.BLACK

    def test_castling_kingside(self):
        game = SpellChessGame()
        
        # clear squares
        game.board.remove_piece_at(chess.F1)
        game.board.remove_piece_at(chess.G1)

        result = game.make_move(chess.E1, chess.G1) # king to g1, rook implicitly to f1

        assert result is True
        assert game.board.piece_at(chess.G1).piece_type == chess.KING
        assert game.board.piece_at(chess.F1).piece_type == chess.ROOK
        assert game.board.piece_at(chess.E1) is None
        assert game.board.piece_at(chess.H1) is None
    
    def test_castling_queenside(self):
        game = SpellChessGame()
        
        # clear squares
        game.board.remove_piece_at(chess.D1)
        game.board.remove_piece_at(chess.C1)

        result = game.make_move(chess.E1, chess.C1) # king to c1, rook implicitly to d1

        assert result is True
        assert game.board.piece_at(chess.C1).piece_type == chess.KING
        assert game.board.piece_at(chess.D1).piece_type == chess.ROOK
        assert game.board.piece_at(chess.E1) is None
        assert game.board.piece_at(chess.A1) is None
    
    def test_en_passant(self):
        game = SpellChessGame()
        game.board.clear()

        white = chess.Piece(chess.PAWN, chess.WHITE)
        black = chess.Piece(chess.PAWN, chess.BLACK)

        # start: white e5, black d7
        game.board.set_piece_at(chess.E5, white)
        game.board.set_piece_at(chess.D7, black)

        game.board.turn = chess.BLACK

        game.make_move(chess.D7, chess.D5)  # black double advances
        result = game.make_move(chess.E5, chess.D6)  # white captures en passant

        assert result is True
        assert game.board.piece_at(chess.D6) is not None
        assert game.board.piece_at(chess.D5) is None
=======
# ------------------------------------------------------------------ #
>>>>>>> 8faf33053924e2c12094e049a8e6b2b2e00af25f
