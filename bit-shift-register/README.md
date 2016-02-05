## Fun with bit shift registers

Connecting up a bit shift register to play around with controlling 8 outputs with only 3 connections.

### The 74HC595N

A brief overview below. See the datasheets for more details.

			-------
		Q1	[1  16] Vcc
		Q2	[2  15] Q0
		Q3	[3  14] DS     "data in"
		Q4	[4  13] !OE    "blank"
		Q5	[5  12] ST_CP  "latch"
		Q6	[6  11] SH_CP  "clock"
		Q7	[7  10] !MR    "clear"
		GND	[8   9] Q7'    "data out"
			-------

- `Q0-Q7`: parallel data output
- `Q7'`: serial data outpt
- `!MR`: master reset (active low)
- `SH_CP`: shift register clock input
- `ST_CP`: storage register clock input
- `!OE`: output enable (active low)
- `DS`: serial data input


### Links

- [Tutorial med Raspberry Pi](http://www.instructables.com/id/Using-a-shift-register-with-Raspberry-Pi/?ALLSTEPS)
- [Video explaining how shift registers work](https://www.youtube.com/watch?v=6fVbJbNPrEU)
- [Video explaining the circuit of the previous video in more detail](https://www.youtube.com/watch?v=oB_pz18AinI)
