set projDir "C:/sutd/CompStruct/compstruct1d/ALU/work/vivado"
set projName "test_project"
set topName top
set device xc7a35tftg256-1
if {[file exists "$projDir/$projName"]} { file delete -force "$projDir/$projName" }
create_project $projName "$projDir/$projName" -part $device
set_property design_mode RTL [get_filesets sources_1]
set verilogSources [list "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/au_top_0.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/reset_conditioner_1.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/button_conditioner_2.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/counter_3.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/manual_alu_4.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/multi_segment_5.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/tester_6.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/pipeline_7.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/edge_detector_8.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/alu_full_9.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/segment_decoder_10.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/toggle_clock_11.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/adder_b16_12.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/multiply_13.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/divide_14.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/boolean_unit_15.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/shifter_16.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/compare_unit_17.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/counter_18.v" "C:/sutd/CompStruct/compstruct1d/ALU/work/verilog/full_adder_19.v" ]
import_files -fileset [get_filesets sources_1] -force -norecurse $verilogSources
set xdcSources [list "C:/sutd/CompStruct/compstruct1d/ALU/work/constraint/alchitry.xdc" "C:/sutd/CompStruct/compstruct1d/ALU/work/constraint/io.xdc" "C:/Program\ Files/Alchitry/Alchitry\ Labs/library/components/au.xdc" ]
read_xdc $xdcSources
set_property STEPS.WRITE_BITSTREAM.ARGS.BIN_FILE true [get_runs impl_1]
update_compile_order -fileset sources_1
launch_runs -runs synth_1 -jobs 12
wait_on_run synth_1
launch_runs impl_1 -to_step write_bitstream -jobs 12
wait_on_run impl_1
