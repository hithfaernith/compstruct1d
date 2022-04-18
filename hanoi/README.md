![alt text](https://github.com/hithfaernith/compstruct1d/blob/master/hanoi/gameplay.gif?raw=true)

The purpose of the python emulator was to verify the validity of our state transition diagram and clear any bugs that might occur,
and so that our resulting pytrhon FSM can be translated practically 1-to-1 to lucid in the hopes that we wont have any bugs that mihght otherwise occur when
coding on lucid directly.  
  
Interesting files:  
BitNumber.py: jsim/lucid style fixed width binary numbers with reverse indexing support  
bit_test.py: BitNumber and ALU sanity tests  
ALU.py: python based ALU intended to mirror the lucid one  
emulator.py: FSM to fake LED matrix game emulator  
GameMachine.py: default registers and their values for the FSM. Also has a simple FSM for player movement  
HanoiMachine: FSM for the full game  
