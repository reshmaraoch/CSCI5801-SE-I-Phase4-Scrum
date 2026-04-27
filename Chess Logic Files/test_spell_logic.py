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

# class TestFreezeTarget:
#     """Casting Freeze should mark the opponent's color as frozen."""

#     def test_freeze_affects_opponent_not_caster(self):
#         game = SpellChessGame()
#         # White casts freeze
#         game.cast_freeze(chess.E5)
#         # The frozen color should be Black (the opponent), not White
#         assert game.freeze_effect_color == chess.BLACK


# class TestNewGameResetsBoard:
#     """Calling new_game() should bring the board back to the starting position."""

#     def test_board_resets_after_moves(self):
#         game = SpellChessGame()
#         game.board.push_san("e4")
#         game.new_game()
#         assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug — document it!                 #
# ------------------------------------------------------------------ #

#Testing Spell Features

#Freeze Spell
class TestFreezeSpellFeatures:
    """Unit tests cases for Freeze spell behavior."""

    def test_freeze_starts_with_five_charges_for_both_players(self):
        game = SpellChessGame()

        assert game.freeze_remaining[chess.WHITE] == 5
        assert game.freeze_remaining[chess.BLACK] == 5

    def test_freeze_cast_uses_one_charge(self):
        game = SpellChessGame()

        result = game.cast_freeze(chess.E5)

        assert result is True
        assert game.freeze_remaining[chess.WHITE] == 4

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E5)

        assert game.freeze_effect_color == chess.BLACK

    def test_freeze_area_includes_center_square(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E4)

        assert chess.E4 in game.freeze_effect_squares

    def test_freeze_area_has_nine_squares_in_middle_of_board(self):
        squares = squares_in_3x3(chess.E4)

        expected_squares = {
            chess.D3, chess.E3, chess.F3,
            chess.D4, chess.E4, chess.F4,
            chess.D5, chess.E5, chess.F5,
        }

        assert squares == expected_squares

    def test_freeze_cannot_be_cast_when_no_charges_left(self):
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0

        result = game.cast_freeze(chess.E5)

        assert result is False

    def test_freeze_sets_three_turn_cooldown(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E5)

        assert game.freeze_cooldown[chess.WHITE] == 3

#Jump Spell
class TestJumpSpellFeatures:
    """Unit test cases for Jump spell behavior."""

    def test_jump_starts_with_three_charges_for_both_players(self):
        game = SpellChessGame()

        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3

    def test_jump_cast_uses_one_charge(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.B1, chess.A3)

        assert result is True
        assert game.jump_remaining[chess.WHITE] == 2

    def test_jump_destination_must_be_empty(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.B1, chess.D2)

        assert result is False
        assert game.board.piece_at(chess.B1) is not None

    def test_jump_cannot_move_king(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.E1, chess.E3)

        assert result is False
        assert game.board.piece_at(chess.E1) is not None

    def test_jump_must_be_within_chebyshev_distance_two(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.B1, chess.B5)

        assert result is False
        assert game.board.piece_at(chess.B1) is not None

    def test_jump_sets_two_turn_cooldown(self):
        game = SpellChessGame()

        game.cast_jump(chess.B1, chess.A3)

        assert game.jump_cooldown[chess.WHITE] == 2