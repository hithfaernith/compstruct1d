/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module enemy_display_11 (
    input [63:0] enemy_positions,
    input [15:0] enemy_dirs,
    input [4:0] x,
    input [2:0] y,
    output reg [23:0] color
  );
  
  
  
  reg [4:0] enemy_x;
  reg [2:0] enemy_y;
  
  reg [7:0] enemy_position;
  
  reg [3:0] k;
  
  always @* begin
    color = 24'h000000;
    for (k = 1'h0; k < 4'h8; k = k + 1) begin
      enemy_position = enemy_positions[(k)*8+7-:8];
      enemy_x = enemy_position[0+4-:5];
      enemy_y = enemy_position[5+2-:3];
      if ((enemy_x == x) && (enemy_y == y) && (enemy_dirs[(k)*2+1-:2] != 2'h0)) begin
        color = 24'h00ff00;
      end
    end
  end
endmodule
