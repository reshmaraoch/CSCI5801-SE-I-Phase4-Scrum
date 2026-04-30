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

# Tests for standard chess moves
class TestStandardChess:
    """Unit test cases for Standard Chess moves"""
    # PAWN TESTS
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
    
    #ROOK TESTS
    def test_rook_vertical_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.A2)

        result = game.make_move(chess.A1, chess.A2)

        assert result is True
        assert game.board.piece_at(chess.A1) is None
        assert game.board.piece_at(chess.A2).piece_type == chess.ROOK

    def test_rook_horizontal_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.B1)

        result = game.make_move(chess.A1, chess.B1)

        assert result is True
        assert game.board.piece_at(chess.A1) is None
        assert game.board.piece_at(chess.B1).piece_type == chess.ROOK

    def test_rook_cannot_jump(self):
        game = SpellChessGame()

        result = game.make_move(chess.A1, chess.A3)

        assert result is False
        assert game.board.piece_at(chess.A3) is None
    
    #KNIGHT TESTS
    def test_knight_L_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.B2)
        result = game.make_move(chess.B1, chess.A3)
        
        assert result is True
        assert game.board.piece_at(chess.B1) is None
        assert game.board.piece_at(chess.A3) == chess.KNIGHT

    def test_knight_cannot_move_non_L(self):
        game = SpellChessGame()
        
        result = game.make_move(chess.B1, chess.B3)
        
        assert result is False
        assert game.board.piece_at(chess.B1) == chess.KNIGHT

    def test_knight_can_jump(self):
        game = SpellChessGame()
        result = game.make_move(chess.B1, chess.A3)
        
        assert result is True

    #BISHOP TESTS
    def test_bishop_diag_advance(self):
        game = SpellChessGame()

        result = game.make_move(chess.C1, chess.A3)
        
        assert result is True
        assert game.board.piece_at(chess.C1) is None
        assert game.board.piece_at(chess.A3) == chess.BISHOP

    def test_bishop_cannot_jump(self):
        game = SpellChessGame()

        result = game.make_move(chess.C1, chess.E3)
        
        assert result is False
        assert game.board.piece_at(chess.C1) == chess.BISHOP   
    
    #QUEEN TESTS
    def test_queen_vertical_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.D2)

        result = game.make_move(chess.D1,chess.D3)
        
        assert result is True
        assert game.board.piece_at(chess.D1) is None
        assert game.board.piece_at(chess.D3) == chess.QUEEN

    def test_queen_horizontal_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.C1)

        result = game.make_move(chess.D1,chess.C1)
        
        assert result is True
        assert game.board.piece_at(chess.D1) is None
        assert game.board.piece_at(chess.C1) == chess.QUEEN

    def test_queen_diag_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.C2)

        result = game.make_move(chess.D1,chess.B3)
        
        assert result is True
        assert game.board.piece_at(chess.D1) is None
        assert game.board.piece_at(chess.B3) == chess.QUEEN

    def test_queen_cannot_jump(self):
        game = SpellChessGame()

        result = game.make_move(chess.D1, chess.D3)
        
        assert result is False
        assert game.board.piece_at(chess.D1) == chess.QUEEN

    #KING TESTS
    def test_king_vertical_single_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.E2)

        result = game.make_move(chess.E1, chess.E2)

        assert result is True
        assert game.board.piece_at(chess.E1) is None
        assert game.board.piece_at(chess.E2) == chess.KING
    
    def test_king_horizontal_single_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.F1)

        result = game.make_move(chess.E1, chess.F1)

        assert result is True
        assert game.board.piece_at(chess.E1) is None
        assert game.board.piece_at(chess.F1) == chess.KING 
    
    def test_king_diag_single_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.D2)

        result = game.make_move(chess.E1, chess.D2)

        assert result is True
        assert game.board.piece_at(chess.E1) is None
        assert game.board.piece_at(chess.D2) == chess.KING

    def test_king_cannot_multi_advance(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.E2)

        result = game.make_move(chess.E1, chess.E3)

        assert result is False
        assert game.board.piece_at(chess.E1) == chess.KING

    #SPECIAL MOVE TESTS
    def test_pawn_promotion_to_queen(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.E7, chess.Piece(chess.PAWN, chess.WHITE))

        result = game.make_move(chess.E7, chess.E8, promotion=chess.QUEEN)

        assert result is True
        assert game.board.piece_at(chess.E8).piece_type == chess.QUEEN
        assert game.board.piece_at(chess.E8).color == chess.WHITE
        assert game.board.piece_at(chess.E7) is None

    def test_pawn_promotion_to_knight(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.E7, chess.Piece(chess.PAWN, chess.WHITE))

        result = game.make_move(chess.E7, chess.E8, promotion=chess.KNIGHT)

        assert result is True
        assert game.board.piece_at(chess.E8).piece_type == chess.QUEEN
        assert game.board.piece_at(chess.E8).color == chess.WHITE
        assert game.board.piece_at(chess.E7) is None

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

    def test_new_game_starting_position(self):
        game = SpellChessGame()

        # white pieces
        assert game.board.piece_at(chess.A1) == chess.Piece(chess.ROOK, chess.WHITE)
        assert game.board.piece_at(chess.B1) == chess.Piece(chess.KNIGHT, chess.WHITE)
        assert game.board.piece_at(chess.C1) == chess.Piece(chess.BISHOP, chess.WHITE)
        assert game.board.piece_at(chess.D1) == chess.Piece(chess.QUEEN, chess.WHITE)
        assert game.board.piece_at(chess.E1) == chess.Piece(chess.KING, chess.WHITE)
        assert game.board.piece_at(chess.F1) == chess.Piece(chess.BISHOP, chess.WHITE)
        assert game.board.piece_at(chess.G1) == chess.Piece(chess.KNIGHT, chess.WHITE)
        assert game.board.piece_at(chess.H1) == chess.Piece(chess.ROOK, chess.WHITE)
        for file in range(8):
            assert game.board.piece_at(chess.square(file, 1)) == chess.Piece(chess.PAWN, chess.WHITE)

        # black pieces
        assert game.board.piece_at(chess.A8) == chess.Piece(chess.ROOK, chess.BLACK)
        assert game.board.piece_at(chess.B8) == chess.Piece(chess.KNIGHT, chess.BLACK)
        assert game.board.piece_at(chess.C8) == chess.Piece(chess.BISHOP, chess.BLACK)
        assert game.board.piece_at(chess.D8) == chess.Piece(chess.QUEEN, chess.BLACK)
        assert game.board.piece_at(chess.E8) == chess.Piece(chess.KING, chess.BLACK)
        assert game.board.piece_at(chess.F8) == chess.Piece(chess.BISHOP, chess.BLACK)
        assert game.board.piece_at(chess.G8) == chess.Piece(chess.KNIGHT, chess.BLACK)
        assert game.board.piece_at(chess.H8) == chess.Piece(chess.ROOK, chess.BLACK)
        for file in range(8):
            assert game.board.piece_at(chess.square(file, 6)) == chess.Piece(chess.PAWN, chess.BLACK)

        # middle
        for file in range(8):
            for rank in range(2, 6):
                assert game.board.piece_at(chess.square(file, rank)) is None
                
# Tests for Freeze spell
class TestFreezeSpell:
    """Unit test cases for Freeze Spell features"""

    def test_initial_freeze_charges(self):
        game = SpellChessGame()
        assert game.freeze_remaining[chess.WHITE] == 5
        assert game.freeze_remaining[chess.BLACK] == 5

    def test_freeze_charge_reduction(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        assert game.freeze_remaining[chess.WHITE] == 4

    def test_no_freeze_when_zero_charges(self):
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0
        assert game.cast_freeze(chess.E5) is False

    def test_freeze_once_per_turn(self):
        game = SpellChessGame()
        assert game.cast_freeze(chess.E5) is True
        assert game.cast_freeze(chess.D5) is False

    def test_freeze_valid_center_square(self):
        game = SpellChessGame()
        assert game.cast_freeze(chess.E4) is True

    def test_freeze_3x3_area(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E4)
        assert chess.E4 in game.freeze_effect_squares
        assert chess.D3 in game.freeze_effect_squares

    def test_freeze_affects_opponent_only(self):
        game = SpellChessGame()

        result = game.cast_freeze(chess.E5)

        assert result is True
        assert game.freeze_effect_color == chess.BLACK
    
    def test_frozen_opponent_piece_cannot_move(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E7)

        result = game.make_move(chess.E7, chess.E5)

        assert result is False
    
    def test_freeze_lasts_one_opponent_turn_only(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E7)

        blocked = game.make_move(chess.E7, chess.E5)

        game.make_move(chess.G1, chess.F3)

        allowed = game.make_move(chess.E7, chess.E5)

        assert blocked is False
        assert allowed is True

    def test_frozen_piece_still_blocks_movement_path(self):
        game = SpellChessGame()

        game.board.clear()
        game.board.set_piece_at(chess.H1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.H8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.A1, chess.Piece(chess.ROOK, chess.WHITE))
        game.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))
        game.board.turn = chess.WHITE

        game.cast_freeze(chess.B3)

        result = game.make_move(chess.A1, chess.A4)

        assert result is False
        assert game.board.piece_at(chess.A3) is not None
    
    def test_frozen_piece_still_gives_check(self):
        game = SpellChessGame()

        game.board.clear()
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.H8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.E8, chess.Piece(chess.ROOK, chess.BLACK))
        game.board.turn = chess.WHITE

        game.cast_freeze(chess.E8)

        assert game.board.is_check() is True
    
    def test_no_valid_moves_when_all_moves_start_from_frozen_square(self):
        game = SpellChessGame()

        game.board.clear()
        game.board.set_piece_at(chess.A1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.H8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.E7, chess.Piece(chess.PAWN, chess.BLACK))
        game.board.turn = chess.WHITE

        game.cast_freeze(chess.E7)

        moves = game.get_legal_moves()

        black_pawn_moves = [m for m in moves if m.from_square == chess.E7]

        assert black_pawn_moves == []
    
    def test_freeze_cooldown_set_to_three_after_cast(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E5)

        assert game.freeze_cooldown[chess.WHITE] == 3
    
    def test_freeze_cooldown_decreases_by_one_on_caster_turn(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E5)

        starting_value = game.freeze_cooldown[chess.WHITE]

        game.make_move(chess.G1, chess.F3)   # White move 
        game.make_move(chess.G8, chess.F6)   # Black move
        game.make_move(chess.F3, chess.G1)   # White turn starts again

        new_value = game.freeze_cooldown[chess.WHITE]

        assert new_value == starting_value - 1
    
    def test_freeze_recast_blocked_during_cooldown(self):
        game = SpellChessGame()

        first_cast = game.cast_freeze(chess.E5)
        second_cast = game.cast_freeze(chess.D5)

        assert first_cast is True
        assert second_cast is False
    
    def test_new_game_resets_freeze_usage_and_cooldown(self):
        game = SpellChessGame()

        game.cast_freeze(chess.E5)

        game.new_game()

        assert game.freeze_remaining[chess.WHITE] == 5
        assert game.freeze_remaining[chess.BLACK] == 5
        assert game.freeze_cooldown[chess.WHITE] == 0
        assert game.freeze_cooldown[chess.BLACK] == 0
        assert game.freeze_effect_color is None

#Tests for Jump Spell
class TestJumpSpellFeatures:
    """Unit test cases for Jump Spell features"""

    def test_initial_jump_charges(self):
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3

    def test_jump_charge_consumption(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.C3)
        assert game.jump_remaining[chess.WHITE] == 2

    def test_no_jump_when_zero_charges(self):
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 0
        assert game.cast_jump(chess.B1, chess.C3) is False

    def test_jump_once_per_turn(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.B1, chess.C3) is True
        assert game.cast_jump(chess.G1, chess.F3) is False

    def test_jump_valid_piece_and_destination(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.B1, chess.C3) is True

    def test_king_cannot_jump(self):
        game = SpellChessGame()

        # artificially place king selection attempt
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))

        assert game.cast_jump(chess.E1, chess.E3) is False
    
    def test_jump_destination_must_be_within_chebyshev_distance_two(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.B1, chess.B4)

        assert result is False

    def test_valid_jump_moves_piece_to_destination(self):
        game = SpellChessGame()

        result = game.cast_jump(chess.B1, chess.D2)

        assert result is True
        assert game.board.piece_at(chess.D2) is not None
        assert game.board.piece_at(chess.B1) is None

    
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
    
    
        

    
    
        
    
        
        
