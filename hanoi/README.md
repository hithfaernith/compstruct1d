![alt text](https://github.com/hithfaernith/compstruct1d/blob/master/hanoi/gameplay.gif?raw=true)

The purpose of the python emulator was to verify the validity of our state transition diagram and clear any bugs that might occur,
and so that our resulting pytrhon FSM can be translated practically 1-to-1 to lucid in the hopes that we wont have any bugs that mihght otherwise occur when coding on lucid directly.  

Developed on python3.8, though 3.7 / 3.9 should work as well. To run the emulator do `pip install requirements.txt` first to get pygame and the other dependencies, then run `python3 emulator.py`. (Actually I just realised the python state machine here on this commit isnt technically the one we translated to lucid, cause the OG single-level FSM that we translated to lucid was from a [couple of commits ago](https://github.com/hithfaernith/compstruct1d/commit/f196fa6afea4a72e8157930ba2aa29ddaee55d6f), whereas the one now has the multiple levels as a result of me getting kinda carried away / paranoid about the rubrics)

Interesting files:  
BitNumber.py: jsim/lucid style fixed width binary numbers with reverse indexing support  
bit_test.py: BitNumber and ALU sanity tests  
ALU.py: python based ALU intended to mirror the lucid one  
emulator.py: FSM to fake LED matrix game emulator  
GameMachine.py: default registers and their values for the FSM. Also has a simple FSM for player movement  
HanoiMachine: FSM for the full game  
