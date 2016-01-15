## Using:

- 3 LEDs (green, yellow, red)
- 3 resistors (210 ohms)
- 4 jumper wires
- Raspberry Pi
- Breadboard


## Steps:

GPIO-pins numbered after board, not BCM.

- Connect GPIO 13, 15, 16 to separate rows.
- Connect each row to the row beneath by one LED (anode in lower number).
- Connect resistor from cathode of each LED to `-` column.
- Connect `-` column to ground (pin 6)

