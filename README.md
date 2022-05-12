# compstruct1d
For ISTD Computational Structures 1D Project 2022.  
[View our project on the 2022 ISTD virtual exhibit website](https://natalieagus.github.io/istd-1d-exhibition-2022/compstruct/Raiders-Of-Hanoi/)  

<p align="center" style="display=flex">
  <img style="height:360px" src="https://user-images.githubusercontent.com/11241733/168070005-2003b796-7540-4740-a67a-f3c097d378d2.gif"/> 
  <img style="height:360px" src="https://user-images.githubusercontent.com/11241733/168064779-f9909814-3eef-4ac7-9fc0-bca8ee2c2bdd.png"/>
</p>

Raiders of hanoi is a 2D arcade game where the player (green square) has to mvoe around using the joystick, to pick up disks (purple) and drop them onto the towers (blue) to solve the 4-disk towers of hanoi while avoiding the enemies that would spawn from the right edge and move left to attack the player. Created as a FPGA state machine that selects inputs to a single 16-bit ALU as part of the 50.002 1D project requirements.  

Team members:  
Acqquilaa Bathumalai  
Beverley Chee  
Christopher Lye Sze Kian  
Constance Chua Jie Ning  
[(Charles) Lim Thian Yew](https://github.com/milselarch)  
[Tham Jit](https://github.com/asdfash)  
[Wee Chun Hui](https://github.com/hithfaernith)  
[Yong Zheng Yew](https://github.com/snproj)  

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
