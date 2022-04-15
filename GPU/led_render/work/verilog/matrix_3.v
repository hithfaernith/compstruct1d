/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

/*
   Parameters:
     WIDTH = 32
     HEIGHT = 16
     NUM_PIXELS = WIDTH*HEIGHT
*/
module matrix_3 (
    input clk,
    input rst,
    input update,
    input [23:0] color,
    output reg [4:0] x,
    output reg [3:0] y,
    output reg [8:0] pixel,
    output reg led
  );
  
  localparam WIDTH = 6'h20;
  localparam HEIGHT = 5'h10;
  localparam NUM_PIXELS = 11'h200;
  
  
  wire [9-1:0] M_writer_pixel;
  wire [1-1:0] M_writer_led;
  reg [1-1:0] M_writer_update;
  reg [24-1:0] M_writer_color;
  ws2812b_writer_7 writer (
    .clk(clk),
    .rst(rst),
    .update(M_writer_update),
    .color(M_writer_color),
    .pixel(M_writer_pixel),
    .led(M_writer_led)
  );
  
  reg [8:0] pixel_no;
  
  reg [3:0] modulo_pixel;
  
  reg [4:0] x_position;
  
  always @* begin
    M_writer_color = color;
    M_writer_update = update;
    pixel = M_writer_pixel;
    led = M_writer_led;
    pixel_no = M_writer_pixel;
    x_position = pixel_no / 5'h10;
    modulo_pixel = pixel_no - x_position * 5'h10;
    x = x_position;
    if (x_position[0+0-:1] == 1'h0) begin
      y = 5'h10 - modulo_pixel - 1'h1;
    end else begin
      y = modulo_pixel;
    end
  end
endmodule
