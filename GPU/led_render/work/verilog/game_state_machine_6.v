/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module game_state_machine_6 (
    input clk,
    input rst,
    input [3:0] pmove,
    input pick_or_drop,
    input reset_game,
    output reg [7:0] dump_player_pos,
    output reg [15:0] dump_player_counter,
    output reg [15:0] dump_enemy_no,
    output reg [15:0] dump_tower_no,
    output reg [15:0] dump_last_fire_wait,
    output reg [3:0] dump_active_disk,
    output reg [15:0] dump_game_state,
    output reg [63:0] dump_enemy_positions,
    output reg [15:0] dump_enemy_directions,
    output reg [127:0] dump_enemy_move_waits,
    output reg [23:0] dump_tower_positions,
    output reg [11:0] dump_tower_states,
    output reg [5:0] current_state
  );
  
  
  
  wire [16-1:0] M_alu_res;
  reg [16-1:0] M_alu_a;
  reg [16-1:0] M_alu_b;
  reg [6-1:0] M_alu_alufn;
  alu_unit_12 alu (
    .a(M_alu_a),
    .b(M_alu_b),
    .alufn(M_alu_alufn),
    .res(M_alu_res)
  );
  
  wire [16-1:0] M_regfile_aout;
  wire [16-1:0] M_regfile_bout;
  wire [8-1:0] M_regfile_dump_player_pos;
  wire [16-1:0] M_regfile_dump_player_counter;
  wire [16-1:0] M_regfile_dump_enemy_no;
  wire [16-1:0] M_regfile_dump_tower_no;
  wire [16-1:0] M_regfile_dump_last_fire_wait;
  wire [4-1:0] M_regfile_dump_active_disk;
  wire [16-1:0] M_regfile_dump_game_state;
  wire [64-1:0] M_regfile_dump_enemy_positions;
  wire [16-1:0] M_regfile_dump_enemy_directions;
  wire [128-1:0] M_regfile_dump_enemy_move_waits;
  wire [24-1:0] M_regfile_dump_tower_positions;
  wire [12-1:0] M_regfile_dump_tower_states;
  reg [16-1:0] M_regfile_asel;
  reg [1-1:0] M_regfile_aconst;
  reg [16-1:0] M_regfile_bsel;
  reg [1-1:0] M_regfile_bconst;
  reg [4-1:0] M_regfile_wsel;
  reg [1-1:0] M_regfile_we;
  regfile_unit_13 regfile (
    .clk(clk),
    .rst(rst),
    .wd(M_alu_res),
    .reset_game(reset_game),
    .asel(M_regfile_asel),
    .aconst(M_regfile_aconst),
    .bsel(M_regfile_bsel),
    .bconst(M_regfile_bconst),
    .wsel(M_regfile_wsel),
    .we(M_regfile_we),
    .aout(M_regfile_aout),
    .bout(M_regfile_bout),
    .dump_player_pos(M_regfile_dump_player_pos),
    .dump_player_counter(M_regfile_dump_player_counter),
    .dump_enemy_no(M_regfile_dump_enemy_no),
    .dump_tower_no(M_regfile_dump_tower_no),
    .dump_last_fire_wait(M_regfile_dump_last_fire_wait),
    .dump_active_disk(M_regfile_dump_active_disk),
    .dump_game_state(M_regfile_dump_game_state),
    .dump_enemy_positions(M_regfile_dump_enemy_positions),
    .dump_enemy_directions(M_regfile_dump_enemy_directions),
    .dump_enemy_move_waits(M_regfile_dump_enemy_move_waits),
    .dump_tower_positions(M_regfile_dump_tower_positions),
    .dump_tower_states(M_regfile_dump_tower_states)
  );
  localparam START_states = 6'd0;
  localparam PLAYER_INIT_states = 6'd1;
  localparam INC_PLAYER_POS_states = 6'd2;
  localparam CMP_PLAYER_WAIT_states = 6'd3;
  localparam PLAYER_MOVE_states = 6'd4;
  localparam INIT_ENEMY_POS_states = 6'd5;
  localparam INIT_ENEMY_NO_states = 6'd6;
  localparam INC_ENEMY_NO_states = 6'd7;
  localparam CHECK_ENEMY_NO_states = 6'd8;
  localparam IF_ENEMY_HIDDEN_states = 6'd9;
  localparam LAST_FIRE_CHECK_states = 6'd10;
  localparam INC_FIRE_WAIT_states = 6'd11;
  localparam ENEMY_WAIT_CHECK_states = 6'd12;
  localparam INC_ENEMY_WAIT_states = 6'd13;
  localparam RESET_ENEMY_WAIT_states = 6'd14;
  localparam FIRE_ENEMY_states = 6'd15;
  localparam RESET_FIRE_WAIT_states = 6'd16;
  localparam SET_ENEMY_POS_states = 6'd17;
  localparam CHECK_ENEMY_LEFT_states = 6'd18;
  localparam ENEMY_MOVE_LEFT_states = 6'd19;
  localparam ENEMY_HIDE_states = 6'd20;
  localparam COLLISION_CHECK_states = 6'd21;
  localparam DEATH_states = 6'd22;
  localparam RESET_TOWER_NO_states = 6'd23;
  localparam INC_TOWER_NO_states = 6'd24;
  localparam TOWER_NO_CMP_states = 6'd25;
  localparam CHECK_TOWER_POS_states = 6'd26;
  localparam IF_DROPPABLE_states = 6'd27;
  localparam DROP_DISK_states = 6'd28;
  localparam CLEAR_DISK_SEL_states = 6'd29;
  localparam IF_PICKABLE_states = 6'd30;
  localparam PICK_DISK_states = 6'd31;
  localparam RM_TOWER_DISK_states = 6'd32;
  localparam SET_LAST_TOWER_states = 6'd33;
  localparam WIN_CHECK_states = 6'd34;
  localparam WIN_states = 6'd35;
  localparam ERROR_states = 6'd36;
  
  reg [5:0] M_states_d, M_states_q = START_states;
  
  localparam PLAYER_WAIT = 5'h14;
  
  localparam ENEMY_MOVE_DELAY = 4'h8;
  
  localparam MIN_FIRE_DELAY = 8'ha0;
  
  always @* begin
    M_states_d = M_states_q;
    
    M_alu_a = M_regfile_aout;
    M_alu_b = M_regfile_bout;
    
    case (M_states_q)
      START_states: begin
        M_regfile_asel = pmove;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = START_states;
        end else begin
          M_states_d = PLAYER_INIT_states;
        end
      end
      PLAYER_INIT_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 1'h1;
        M_states_d = INC_PLAYER_POS_states;
      end
      INC_PLAYER_POS_states: begin
        M_regfile_asel = 1'h1;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h00;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 1'h1;
        M_states_d = CMP_PLAYER_WAIT_states;
      end
      CMP_PLAYER_WAIT_states: begin
        M_regfile_asel = 1'h1;
        M_regfile_bsel = 5'h14;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h35;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = INIT_ENEMY_NO_states;
        end else begin
          M_states_d = PLAYER_MOVE_states;
        end
      end
      PLAYER_MOVE_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = pmove;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h08;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 1'h0;
        M_states_d = PLAYER_INIT_states;
      end
      INIT_ENEMY_NO_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h01;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 2'h2;
        M_states_d = INC_ENEMY_NO_states;
      end
      INC_ENEMY_NO_states: begin
        M_regfile_asel = 2'h2;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h00;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 2'h2;
        M_states_d = CHECK_ENEMY_NO_states;
      end
      CHECK_ENEMY_NO_states: begin
        M_regfile_asel = 2'h2;
        M_regfile_bsel = 3'h7;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h35;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = IF_ENEMY_HIDDEN_states;
        end else begin
          M_states_d = RESET_TOWER_NO_states;
        end
      end
      IF_ENEMY_HIDDEN_states: begin
        M_regfile_asel = 4'h8;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = LAST_FIRE_CHECK_states;
        end else begin
          M_states_d = ENEMY_WAIT_CHECK_states;
        end
      end
      ENEMY_WAIT_CHECK_states: begin
        M_regfile_asel = 4'h9;
        M_regfile_bsel = 4'h8;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h35;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res != 1'h0) begin
          M_states_d = INC_ENEMY_WAIT_states;
        end else begin
          M_states_d = RESET_ENEMY_WAIT_states;
        end
      end
      LAST_FIRE_CHECK_states: begin
        M_regfile_asel = 3'h4;
        M_regfile_bsel = 8'ha0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h35;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = INC_FIRE_WAIT_states;
        end else begin
          M_states_d = FIRE_ENEMY_states;
        end
      end
      INC_FIRE_WAIT_states: begin
        M_regfile_asel = 3'h4;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h00;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h4;
        M_states_d = INC_ENEMY_NO_states;
      end
      FIRE_ENEMY_states: begin
        M_regfile_asel = 2'h2;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'h8;
        M_states_d = SET_ENEMY_POS_states;
      end
      SET_ENEMY_POS_states: begin
        M_regfile_asel = 8'h1f;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h1e;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h7;
        M_states_d = RESET_FIRE_WAIT_states;
      end
      RESET_FIRE_WAIT_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h4;
        M_states_d = INC_ENEMY_NO_states;
      end
      INC_ENEMY_WAIT_states: begin
        M_regfile_asel = 4'h9;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h00;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'h9;
        M_states_d = COLLISION_CHECK_states;
      end
      RESET_ENEMY_WAIT_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'h9;
        M_states_d = CHECK_ENEMY_LEFT_states;
      end
      CHECK_ENEMY_LEFT_states: begin
        M_regfile_asel = 3'h7;
        M_regfile_bsel = 8'h1f;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h18;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res != 1'h0) begin
          M_states_d = ENEMY_MOVE_LEFT_states;
        end else begin
          M_states_d = ENEMY_HIDE_states;
        end
      end
      ENEMY_HIDE_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'h8;
        M_states_d = INC_ENEMY_NO_states;
      end
      ENEMY_MOVE_LEFT_states: begin
        M_regfile_asel = 3'h7;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h09;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h7;
        M_states_d = COLLISION_CHECK_states;
      end
      COLLISION_CHECK_states: begin
        M_regfile_asel = 3'h7;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = DEATH_states;
        end else begin
          M_states_d = INC_ENEMY_NO_states;
        end
      end
      DEATH_states: begin
        M_regfile_asel = 2'h1;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h6;
        M_states_d = DEATH_states;
      end
      RESET_TOWER_NO_states: begin
        M_regfile_asel = 16'hffff;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 2'h3;
        M_states_d = INC_TOWER_NO_states;
      end
      INC_TOWER_NO_states: begin
        M_regfile_asel = 2'h3;
        M_regfile_bsel = 1'h1;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h00;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 2'h3;
        M_states_d = TOWER_NO_CMP_states;
      end
      TOWER_NO_CMP_states: begin
        M_regfile_asel = 2'h3;
        M_regfile_bsel = 2'h2;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h37;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = CHECK_TOWER_POS_states;
        end else begin
          M_states_d = SET_LAST_TOWER_states;
        end
      end
      CHECK_TOWER_POS_states: begin
        M_regfile_asel = 4'ha;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          if (pick_or_drop == 1'h1) begin
            M_states_d = IF_PICKABLE_states;
          end else begin
            M_states_d = IF_DROPPABLE_states;
          end
        end else begin
          M_states_d = INC_TOWER_NO_states;
        end
      end
      IF_DROPPABLE_states: begin
        M_regfile_asel = 4'hb;
        M_regfile_bsel = 3'h5;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h35;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = DROP_DISK_states;
        end else begin
          M_states_d = INC_TOWER_NO_states;
        end
      end
      DROP_DISK_states: begin
        M_regfile_asel = 4'hb;
        M_regfile_bsel = 3'h5;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h1e;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'hb;
        M_states_d = CLEAR_DISK_SEL_states;
      end
      CLEAR_DISK_SEL_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h5;
        M_states_d = INC_TOWER_NO_states;
      end
      IF_PICKABLE_states: begin
        M_regfile_asel = 3'h5;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = PICK_DISK_states;
        end else begin
          M_states_d = INC_TOWER_NO_states;
        end
      end
      PICK_DISK_states: begin
        M_regfile_asel = 4'hb;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h0a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h5;
        M_states_d = RM_TOWER_DISK_states;
      end
      RM_TOWER_DISK_states: begin
        M_regfile_asel = 4'hb;
        M_regfile_bsel = 3'h5;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h0;
        M_alu_alufn = 6'h16;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 4'hb;
        M_states_d = INC_TOWER_NO_states;
      end
      SET_LAST_TOWER_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 2'h3;
        M_states_d = WIN_CHECK_states;
      end
      WIN_CHECK_states: begin
        M_regfile_asel = 4'hb;
        M_regfile_bsel = 16'h000f;
        M_regfile_aconst = 1'h0;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h33;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        if (M_alu_res[0+0-:1] == 1'h1) begin
          M_states_d = WIN_states;
        end else begin
          M_states_d = INC_PLAYER_POS_states;
        end
      end
      WIN_states: begin
        M_regfile_asel = 2'h2;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h1;
        M_regfile_wsel = 3'h6;
        M_states_d = WIN_states;
      end
      ERROR_states: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        M_states_d = ERROR_states;
      end
      default: begin
        M_regfile_asel = 1'h0;
        M_regfile_bsel = 1'h0;
        M_regfile_aconst = 1'h1;
        M_regfile_bconst = 1'h1;
        M_alu_alufn = 6'h1a;
        M_regfile_we = 1'h0;
        M_regfile_wsel = 1'h0;
        M_states_d = ERROR_states;
      end
    endcase
    dump_player_pos = M_regfile_dump_player_pos;
    dump_player_counter = M_regfile_dump_player_counter;
    dump_enemy_no = M_regfile_dump_enemy_no;
    dump_tower_no = M_regfile_dump_tower_no;
    dump_last_fire_wait = M_regfile_dump_last_fire_wait;
    dump_active_disk = M_regfile_dump_active_disk;
    dump_game_state = M_regfile_dump_game_state;
    dump_enemy_positions = M_regfile_dump_enemy_positions;
    dump_enemy_directions = M_regfile_dump_enemy_directions;
    dump_enemy_move_waits = M_regfile_dump_enemy_move_waits;
    dump_tower_positions = M_regfile_dump_tower_positions;
    dump_tower_states = M_regfile_dump_tower_states;
    current_state = M_states_q;
    if (reset_game) begin
      M_states_d = START_states;
    end
  end
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_states_q <= 1'h0;
    end else begin
      M_states_q <= M_states_d;
    end
  end
  
endmodule
