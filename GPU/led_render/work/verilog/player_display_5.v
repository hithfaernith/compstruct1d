/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module player_display_5 (
    input clk,
    input rst,
    input [7:0] player_position,
    input [3:0] player_disk,
    input [4:0] x,
    input [2:0] y,
    output reg [23:0] color
  );
  
  
  
  reg [2:0] player_y;
  
  reg [4:0] player_x;
  
  reg [4:0] disk_length;
  
  always @* begin
    color = 24'h000000;
    player_y = player_position[5+2-:3];
    player_x = player_position[0+4-:5];
    disk_length = 3'h5;
    
    case (player_disk)
      4'h0: begin
        disk_length = 1'h0;
      end
      4'h1: begin
        disk_length = 1'h1;
      end
      4'h2: begin
        disk_length = 2'h2;
      end
      4'h4: begin
        disk_length = 2'h3;
      end
      4'h8: begin
        disk_length = 3'h4;
      end
    endcase
    if (y == player_y) begin
      if (x == player_x) begin
        color = 24'h0000ff;
      end else begin
        if (x > player_x) begin
          if (disk_length >= (x - player_x)) begin
            color = 24'h200132;
          end
        end
      end
    end
  end
endmodule