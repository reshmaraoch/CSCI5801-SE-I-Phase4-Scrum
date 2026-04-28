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
        
    
    
    
    def test_jump_ignores_pieces_in_between(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.D3)
        assert game.board.piece_at(chess.D3).piece_type == chess.KNIGHT
        assert game.board.piece_at(chess.B1) is None
        
    def test_jump_fails_if_destination_occupied_by_self(self):
        game = SpellChessGame()
        ok = game.cast_jump(chess.B1, chess.C2)
        assert not ok
    
    def test_jump_fails_if_destination_occupied_by_opponent(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)
        game.make_move(chess.E7, chess.E5)
        ok = game.cast_jump(chess.E4, chess.E5)
        assert not ok
        
    def text_jump_cooldown_set_to_2_after_cast(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.D3)
        assert game.jump_cooldown[chess.WHITE] == 2
        
    def test_jump_cooldown_decrements_each_caster_turn(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.D3)
        game.make_move(chess.E2, chess.E4)
        game.make_move(chess.E7, chess.E5)
        assert game.jump_cooldown[chess.WHITE] == 1 
    
    def test_jump_recast_blocked_during_cooldown(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.D3) 
        game.make_move(chess.E2, chess.E4)
        game.make_move(chess.E7, chess.E5)
        ok = game.cast_jump(chess.G1, chess.F3)
        assert not ok
        
    def test_new_game_resets_jump_charges_and_cooldown(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.D3)
        game.new_game()
        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3
        assert game.jump_cooldown[chess.WHITE] == 0
        assert game.jump_cooldown[chess.BLACK] == 0
        

class TestGameStateDisplay:
    """Unit test cases for Test Game Display."""
    
    def test_status_shows_whose_turn(self):
        game = SpellChessGame()
        assert "white" in game.status_text().lower()
        game.make_move(chess.E2, chess.E4)
        assert "black" in game.status_text().lower()
        
    def test_status_shows_check(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)
        game.make_move(chess.E7, chess.E5)
        game.make_move(chess.D1, chess.H5)
        game.make_move(chess.B8, chess.C6)
        game.make_move(chess.F1, chess.C4)
        game.make_move(chess.G8, chess.F6)
        game.make_move(chess.H5, chess.F7)
        assert "check" in game.status_text().lower()
        
    def test_freeze_label_shows_current_player_charges(self):
        game = SpellChessGame()
        assert "5" in game.freeze_info_text()
        game.cast_freeze(chess.E4)
        assert "4" in game.freeze_info_text()
        
    def test_freeze_label_shows_cooldown_turns(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E4)
        assert "3" in game.freeze_info_text()
        
    def test_jump_label_shows_cooldown_turns(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.C3)
        assert "2" in game.jump_info_text()
        
    def test_freeze_label_shows_frozen_note(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E7)
        game.make_move(chess.E2, chess.E4)
        assert game.current_turn() == chess.BLACK
        assert "frozen" in game.freeze_info_text().lower()
    
    
        

    
    
        
    
        
        