set projDir "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/vivado"
set projName "test_project"
set topName top
set device xc7a35tftg256-1
if {[file exists "$projDir/$projName"]} { file delete -force "$projDir/$projName" }
create_project $projName "$projDir/$projName" -part $device
set_property design_mode RTL [get_filesets sources_1]
set verilogSources [list "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/verilog/au_top_0.v" "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/verilog/reset_conditioner_1.v" "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/verilog/counter_2.v" ]
import_files -fileset [get_filesets sources_1] -force -norecurse $verilogSources
set xdcSources [list "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/constraint/io.xdc" "/home/milselarch/SUTD/50-002/FPGA/1D/ALU/work/constraint/alchitry.xdc" "/home/milselarch/SUTD/50-002/FPGA/alcrity/library/components/au.xdc" ]
read_xdc $xdcSources
set_property STEPS.WRITE_BITSTREAM.ARGS.BIN_FILE true [get_runs impl_1]
update_compile_order -fileset sources_1
launch_runs -runs synth_1 -jobs 12
wait_on_run synth_1
launch_runs impl_1 -to_step write_bitstream -jobs 12
wait_on_run impl_1
