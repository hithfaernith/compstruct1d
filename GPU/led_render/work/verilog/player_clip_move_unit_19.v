/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module player_clip_move_unit_19 (
    input [15:0] a,
    input [15:0] b,
    output reg [15:0] res
  );
  
  
  
  localparam UP = 1'h0;
  
  localparam DOWN = 1'h1;
  
  localparam LEFT = 2'h2;
  
  localparam RIGHT = 2'h3;
  
  reg [4:0] x;
  reg [2:0] y;
  
  reg [15:0] player_position;
  
  reg [15:0] player_move;
  
  reg [15:0] new_position;
  
  always @* begin
    player_position = a;
    player_move = b;
    new_position = 1'h0;
    new_position[0+7-:8] = player_position[0+7-:8];
    x = player_position[0+4-:5];
    y = player_position[5+2-:3];
    if (x == 1'h0) begin
      player_move[2+0-:1] = 1'h0;
    end else begin
      if (x == 5'h1f) begin
        player_move[3+0-:1] = 1'h0;
      end
    end
    if (y == 3'h7) begin
      player_move[0+0-:1] = 1'h0;
    end else begin
      if (y == 1'h0) begin
        player_move[1+0-:1] = 1'h0;
      end
    end
    if (player_move[0+0-:1] == 1'h1) begin
      new_position[5+2-:3] = player_position[5+2-:3] + 1'h1;
    end else begin
      if (player_move[1+0-:1] == 1'h1) begin
        new_position[5+2-:3] = player_position[5+2-:3] - 1'h1;
      end else begin
        if (player_move[2+0-:1] == 1'h1) begin
          new_position[0+4-:5] = player_position[0+4-:5] - 1'h1;
        end else begin
          if (player_move[3+0-:1] == 1'h1) begin
            new_position[0+4-:5] = player_position[0+4-:5] + 1'h1;
          end
        end
      end
    end
    res = new_position;
  end
endmodule
