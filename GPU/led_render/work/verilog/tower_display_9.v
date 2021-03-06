/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module tower_display_9 (
    input [23:0] tower_positions,
    input [11:0] tower_disks,
    input [4:0] x,
    input [2:0] y,
    output reg [23:0] color
  );
  
  
  
  reg [7:0] tower_position;
  
  reg [4:0] tower_x;
  reg [2:0] tower_y;
  
  reg [15:0] tower_pixels;
  
  reg [1:0] disk_pixels_x;
  reg [1:0] disk_pixels_y;
  
  reg pixel_has_disk;
  
  reg [3:0] tower;
  
  integer k;
  
  always @* begin
    color = 24'h000000;
    for (k = 1'h0; k < 2'h3; k = k + 1) begin
      tower_position = tower_positions[(k)*8+7-:8];
      tower_y = tower_position[5+2-:3];
      tower_x = tower_position[0+4-:5];
      tower = tower_disks[(k)*4+3-:4];
      
      case (tower)
        4'h0: begin
          tower_pixels = 16'h0000;
        end
        4'h1: begin
          tower_pixels = 16'h000f;
        end
        4'h2: begin
          tower_pixels = 16'h0007;
        end
        4'h3: begin
          tower_pixels = 16'h007f;
        end
        4'h4: begin
          tower_pixels = 16'h0003;
        end
        4'h5: begin
          tower_pixels = 16'h003f;
        end
        4'h6: begin
          tower_pixels = 16'h0037;
        end
        4'h7: begin
          tower_pixels = 16'h037f;
        end
        4'h8: begin
          tower_pixels = 16'h0001;
        end
        4'h9: begin
          tower_pixels = 16'h001f;
        end
        4'ha: begin
          tower_pixels = 16'h0017;
        end
        4'hb: begin
          tower_pixels = 16'h017f;
        end
        4'hc: begin
          tower_pixels = 16'h0013;
        end
        4'hd: begin
          tower_pixels = 16'h013f;
        end
        4'he: begin
          tower_pixels = 16'h0137;
        end
        4'hf: begin
          tower_pixels = 16'h137f;
        end
        default: begin
          tower_pixels = 16'hffff;
        end
      endcase
      if ((y < tower_y) && (x == tower_x)) begin
        color = 24'hff0000;
      end else begin
        if ((x <= tower_x + 3'h4) && (y < 3'h4) && (tower_x < x)) begin
          disk_pixels_x = x - (tower_x + 1'h1);
          disk_pixels_y = y;
          pixel_has_disk = tower_pixels[(disk_pixels_y)*4+(disk_pixels_x)*1+0-:1];
          if (pixel_has_disk) begin
            color = 24'h824b00;
          end
        end
      end
    end
  end
endmodule
