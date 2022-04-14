/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module au_top_0 (
    input clk,
    input rst_n,
    output reg [7:0] led,
    input usb_rx,
    output reg outled,
    output reg usb_tx,
    output reg [23:0] io_led,
    output reg [7:0] io_seg,
    output reg [3:0] io_sel,
    input [4:0] io_button,
    input [23:0] io_dip
  );
  
  
  
  reg rst;
  
  wire [5-1:0] M_led_matrix_x;
  wire [3-1:0] M_led_matrix_y;
  wire [8-1:0] M_led_matrix_pixel;
  wire [1-1:0] M_led_matrix_led;
  reg [1-1:0] M_led_matrix_update;
  reg [24-1:0] M_led_matrix_color;
  matrix_1 led_matrix (
    .clk(clk),
    .rst(rst),
    .update(M_led_matrix_update),
    .color(M_led_matrix_color),
    .x(M_led_matrix_x),
    .y(M_led_matrix_y),
    .pixel(M_led_matrix_pixel),
    .led(M_led_matrix_led)
  );
  
  wire [1-1:0] M_reset_cond_out;
  reg [1-1:0] M_reset_cond_in;
  reset_conditioner_2 reset_cond (
    .clk(clk),
    .in(M_reset_cond_in),
    .out(M_reset_cond_out)
  );
  
  reg [4:0] x_coordinate;
  
  reg [2:0] y_coordinate;
  
  reg [7:0] pixel_no;
  
  always @* begin
    M_reset_cond_in = ~rst_n;
    rst = M_reset_cond_out;
    usb_tx = usb_rx;
    led = 8'h00;
    io_led = 24'h000000;
    io_seg = 8'hff;
    io_sel = 4'hf;
    x_coordinate = io_dip[0+0+4-:5];
    y_coordinate = io_dip[0+5+2-:3];
    pixel_no = M_led_matrix_pixel;
    io_led[0+0+4-:5] = x_coordinate;
    io_led[8+5+2-:3] = y_coordinate;
    M_led_matrix_update = 1'h1;
    M_led_matrix_color = 24'h000000;
    outled = M_led_matrix_led;
    io_led[8+0+0-:1] = 1'h0;
    if ((x_coordinate == M_led_matrix_x) && (y_coordinate == M_led_matrix_y)) begin
      M_led_matrix_color = 24'h010000;
    end
    io_led[16+7-:8] = pixel_no;
  end
endmodule
