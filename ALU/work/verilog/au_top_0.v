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
    output reg usb_tx,
    output reg [23:0] io_led,
    output reg [7:0] io_seg,
    output reg [3:0] io_sel,
    input [4:0] io_button,
    input [23:0] io_dip
  );
  
  
  
  reg rst;
  
  wire [1-1:0] M_reset_cond_out;
  reg [1-1:0] M_reset_cond_in;
  reset_conditioner_1 reset_cond (
    .clk(clk),
    .in(M_reset_cond_in),
    .out(M_reset_cond_out)
  );
  wire [1-1:0] M_btn_cond_out;
  reg [1-1:0] M_btn_cond_in;
  button_conditioner_2 btn_cond (
    .clk(clk),
    .in(M_btn_cond_in),
    .out(M_btn_cond_out)
  );
  wire [1-1:0] M_manual_reset_button_out;
  button_conditioner_2 manual_reset_button (
    .clk(clk),
    .in(io_button[2+0-:1]),
    .out(M_manual_reset_button_out)
  );
  wire [1-1:0] M_pause_switch_out;
  button_conditioner_2 pause_switch (
    .clk(clk),
    .in(io_dip[16+2+0-:1]),
    .out(M_pause_switch_out)
  );
  wire [1-1:0] M_pause_button_out;
  button_conditioner_2 pause_button (
    .clk(clk),
    .in(io_button[1+0-:1]),
    .out(M_pause_button_out)
  );
  wire [2-1:0] M_segment_counter_value;
  counter_3 segment_counter (
    .clk(clk),
    .rst(rst),
    .value(M_segment_counter_value)
  );
  
  wire [8-1:0] M_segment_display_seg_out1;
  wire [8-1:0] M_segment_display_seg_out2;
  wire [8-1:0] M_segment_display_seg_out3;
  wire [8-1:0] M_segment_display_seg_out4;
  reg [16-1:0] M_segment_display_number;
  reg [4-1:0] M_segment_display_decimal;
  multi_segment_4 segment_display (
    .clk(clk),
    .rst(rst),
    .number(M_segment_display_number),
    .decimal(M_segment_display_decimal),
    .seg_out1(M_segment_display_seg_out1),
    .seg_out2(M_segment_display_seg_out2),
    .seg_out3(M_segment_display_seg_out3),
    .seg_out4(M_segment_display_seg_out4)
  );
  
  reg [15:0] minput;
  
  reg pause;
  
  wire [8-1:0] M_test_out;
  wire [16-1:0] M_test_display;
  wire [1-1:0] M_test_error_is_happening;
  wire [1-1:0] M_test_z;
  wire [1-1:0] M_test_v;
  wire [1-1:0] M_test_n;
  tester_5 test (
    .clk(clk),
    .rst(rst),
    .man_reset(M_manual_reset_button_out),
    .select(io_dip[16+0+1-:2]),
    .man_input(minput),
    .pause(pause),
    .write_enable(io_dip[16+3+0-:1]),
    .out(M_test_out),
    .display(M_test_display),
    .error_is_happening(M_test_error_is_happening),
    .z(M_test_z),
    .v(M_test_v),
    .n(M_test_n)
  );
  
  always @* begin
    pause = M_pause_button_out | M_pause_switch_out;
    M_btn_cond_in = io_button[4+0-:1];
    M_reset_cond_in = ~rst_n;
    rst = M_reset_cond_out | M_btn_cond_out;
    led[0+0-:1] = M_test_z;
    led[1+0-:1] = M_test_v;
    led[2+0-:1] = M_test_n;
    led[3+4-:5] = 1'h0;
    minput[0+7-:8] = io_dip[0+7-:8];
    minput[8+7-:8] = io_dip[8+7-:8];
    io_led[0+7-:8] = M_test_display[0+7-:8];
    io_led[8+7-:8] = M_test_display[8+7-:8];
    io_led[16+7-:8] = M_test_out;
    usb_tx = usb_rx;
    M_segment_display_number = M_test_display;
    io_sel = 4'hf;
    io_seg = 8'hff;
    if (M_test_error_is_happening) begin
      M_segment_display_decimal = 4'hf;
    end else begin
      M_segment_display_decimal = 4'h0;
    end
    
    case (M_segment_counter_value)
      2'h0: begin
        io_sel = 4'he;
        io_seg = M_segment_display_seg_out1;
      end
      2'h1: begin
        io_sel = 4'hd;
        io_seg = M_segment_display_seg_out2;
      end
      2'h2: begin
        io_sel = 4'hb;
        io_seg = M_segment_display_seg_out3;
      end
      2'h3: begin
        io_sel = 4'h7;
        io_seg = M_segment_display_seg_out4;
      end
    endcase
  end
endmodule
