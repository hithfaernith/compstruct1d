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
  wire [2-1:0] M_segment_counter_value;
  counter_2 segment_counter (
    .clk(clk),
    .rst(rst),
    .value(M_segment_counter_value)
  );
  wire [1-1:0] M_slowclock_value;
  counter_3 slowclock (
    .clk(clk),
    .rst(rst),
    .value(M_slowclock_value)
  );
  wire [1-1:0] M_medclock_value;
  counter_4 medclock (
    .clk(clk),
    .rst(rst),
    .value(M_medclock_value)
  );
  
  reg [15:0] write_a;
  
  reg write_enable;
  
  reg [15:0] a_value;
  
  wire [16-1:0] M_reg_a_out;
  dff_b16_5 reg_a (
    .clk(M_medclock_value),
    .rst(rst),
    .write_val(write_a),
    .write_enable(1'h1),
    .out(M_reg_a_out)
  );
  
  wire [16-1:0] M_adder_s;
  wire [1-1:0] M_adder_cout;
  wire [1-1:0] M_adder_z;
  wire [1-1:0] M_adder_n;
  wire [1-1:0] M_adder_v;
  reg [16-1:0] M_adder_x;
  reg [16-1:0] M_adder_y;
  reg [1-1:0] M_adder_subtract;
  adder_b16_6 adder (
    .x(M_adder_x),
    .y(M_adder_y),
    .subtract(M_adder_subtract),
    .s(M_adder_s),
    .cout(M_adder_cout),
    .z(M_adder_z),
    .n(M_adder_n),
    .v(M_adder_v)
  );
  
  wire [8-1:0] M_segment_display_seg_out1;
  wire [8-1:0] M_segment_display_seg_out2;
  wire [8-1:0] M_segment_display_seg_out3;
  wire [8-1:0] M_segment_display_seg_out4;
  reg [16-1:0] M_segment_display_number;
  multi_segment_7 segment_display (
    .clk(clk),
    .rst(rst),
    .number(M_segment_display_number),
    .seg_out1(M_segment_display_seg_out1),
    .seg_out2(M_segment_display_seg_out2),
    .seg_out3(M_segment_display_seg_out3),
    .seg_out4(M_segment_display_seg_out4)
  );
  
  always @* begin
    M_reset_cond_in = ~rst_n;
    rst = M_reset_cond_out;
    a_value = M_reg_a_out;
    M_adder_x = M_reg_a_out;
    M_adder_y = 16'h0001;
    M_adder_subtract = 1'h1;
    write_a = M_adder_s;
    io_led[0+7-:8] = M_adder_s[0+7-:8];
    io_led[8+7-:8] = M_adder_s[8+7-:8];
    M_segment_display_number = M_adder_s;
    io_sel = 4'hf;
    io_seg = 8'hff;
    
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
    usb_tx = usb_rx;
    led = 8'haa;
  end
endmodule