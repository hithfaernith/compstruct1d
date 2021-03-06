/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module math_unit_15 (
    input [15:0] a,
    input [15:0] b,
    input [5:0] alufn,
    output reg [15:0] res
  );
  
  
  
  wire [16-1:0] M_player_clip_move_res;
  player_clip_move_unit_19 player_clip_move (
    .a(a),
    .b(b),
    .res(M_player_clip_move_res)
  );
  wire [16-1:0] M_enemy_move_left_res;
  enemy_move_left_unit_20 enemy_move_left (
    .a(a),
    .b(b),
    .res(M_enemy_move_left_res)
  );
  wire [16-1:0] M_solo_msb_res;
  solo_msb_unit_21 solo_msb (
    .a(a),
    .b(b),
    .res(M_solo_msb_res)
  );
  
  localparam ERROR = 16'haaaa;
  
  always @* begin
    
    case (alufn)
      6'h00: begin
        res = a + b;
      end
      6'h01: begin
        res = a - b;
      end
      6'h02: begin
        res = a * b;
      end
      6'h03: begin
        res = a / b;
      end
      6'h08: begin
        res = M_player_clip_move_res;
      end
      6'h09: begin
        res = M_enemy_move_left_res;
      end
      6'h0a: begin
        res = M_solo_msb_res;
      end
      default: begin
        res = 16'haaaa;
      end
    endcase
  end
endmodule
