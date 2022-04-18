# compstruct1d
For ISTD Computational Structures 1D Project 2022

Team members:  
Acqquilaa Bathumalai  
Beverley Chee  
Christopher Lye Sze Kian  
Constance Chua Jie Ning  
Lim Thian Yew  
Tham Jit  
Wee Chun Hui  
Yong Zheng Yew  

Relevant folders:  
ALU - lucid code for 16-bit ALU checkoff submission   
GPU/led_render - lucid code for final raiders of hanoi game, and supporing LED matrix drivers  
hanoi - python game, ALU and state machine emulator
  
~~todo~~ feature wishlist:  
1. ~~change player color to indicate pick / drop state~~
2. ~~reorder state machine to avoid occasional flickering due to enemy being made visible before being repositioned to right edge~~
3. ~~create white border on the top of the second screen to denote floor of the game area~~
4. expand playable game area to both LED matrices
6. build 16-bit beta CPU and code the game using beta assembly
7. change the game display output to VGA
8. retarget vbcc for the 16-bit beta architecture and write the game in C
9. implement 2D rigid body dynamics for raiders of hanoi and turn it into a physics game
10. turn the game into 3D with 3D rigid body dyanmics
11. implement raytraced graphics and rebrand the FPGA as an ATX 4060TI
