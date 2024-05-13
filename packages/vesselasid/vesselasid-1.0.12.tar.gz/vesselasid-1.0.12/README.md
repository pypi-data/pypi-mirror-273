# vesselasid

vesselasid is a python client for the [Elektron ASID protocol](http://paulus.kapsi.fi/asid_protocol.txt), which allows programming SID registers remotely using MIDI Sysex (in an ASID receiver, such as a SidStation or [Vessel](https://github.com/anarkiwi/vessel) equipped C64 runing [VAP](https://github.com/anarkiwi/vap)).

It contains extensions that allow sending arbitrary data such as machine code over Sysex, and executing code remotely, and acknowledging commands with MIDI clock. Currently only VAP implements these extensions.

# installation

### linux

```
pip3 install vesselasid
```

### macosx

1. Install [MacPorts](https://www.macports.org/install.php).
2. Install portmidi and dependencies: ```sudo port install python310 py310-pip py310-mido portmidi```
3. Install VesselASID: ```/opt/local/bin/pip-3.10 install vesselasid```
4. Test your installation:
```
% /opt/local/bin/python3.10                 
Python 3.10.13 (main, Jan  8 2024, 11:42:08) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import vesselasid
>>> import mido
>>> mido.set_backend('mido.backends.portmidi')
>>> mido.get_output_names()
['IAC Driver Bus 1']
````

## programming SID registers

```
MIDI_DEV = "Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 16:0"
port = mido.open_output(MIDI_DEV)
asid = Asid(port)
asid.start()
asid.sid.voice[1].set_state(freq=2048, s=15)
asid.sid.set_state(vol=15)
asid.update() # sends all pending changes
```

## sending and running machine code

```
MIDI_DEV = "Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 16:0"
port = mido.open_output(MIDI_DEV)
in_port = mido.open_input(MIDI_DEV) # when in_port defined, receiver will acknowledge commands with MIDI clock.
asid = Asid(port, in_port=in_port)
asid.start()
code = xa(["lda #$0f", "sta $d418"]) # Asid adds rts automatically. Code origin currently fixed to $c000.
asid.load(code)
asid.run() # does jsr $c000 remotely, sends clock when done.
```

# buffer API

VesselASID supports remote memory operations on the C64 side, implemented by the VAP client.

All operations are related to the position of the VAP pointer, which is a 16 bit address pointer to the C64's memory.
In general, all operations do not modify the pointer (for example, repeated calls to load() will always begin at the
same position).

#### addr(addr)

Sets the VAP pointer to the value of ```addr```.

#### load(code)

Accepts a list of integers as ```code```, and writes them to the location beginning at the VAP pointer.

#### loaddiffs(self, addr, a, b, shuffle=True, overhead=9)

Minimize load operation by sending only diffs.  Accepts two lists of equal size of integers, ```a``` and ```b```,
relative to the location beginning at ```addr```. Sends load() commands to cause memory to be updated to ```b``` 
assuming original state ```a```. If ```shuffle``` is True, then the order that the diffs are sent is randomized. 
```overhead``` is the maxmium number of bytes between adjacent diffs to send a new diff.

#### fillbuff(val, count)

Writes ```val```, ```count``` times beginning at the VAP pointer.

#### copybuff(copyfrom, coumt)

Copies ```count``` bytes from ```copyfrom``` (a 16 bit address) to the location beginning at the VAP pointer.

#### run()

Causes the C64 to ```JSR``` to a program beginning at the VAP pointer (the program must ```RTS``` to return control).

#### addrrect(rowstart, rowsize, inc)

Define a rectangular region in memory, for subsequent rect calls. The rectangle's top left position is always
the current position of the VAP pointer. ```rowstart``` is the number of positions to skip to move to a new row (generally
40 for screen memory). ```rowsize``` is the size of each row in the rectangle. ```inc``` is the number of rows to
increment (for example 2, causes every other row to be skipped).

#### loadrect(code)

Accepts a list of integers as ```code```, and writes them to the location beginning at the VAP pointer, as a rectangle.
For example, if writing to the first location in screen memory, and addrrect(40, 4, 1) was previously called, calling
loadrect([32] * 16) would cause a 4 x 4 rectangle of spaces to be written.

#### fillrect(val, code)

Writes ```val```, ```count``` times beginning at the VAP pointer, as a rectangle. For example, if writing to the first
location in screen memory, and addrrect(40, 4, 1) was previously called, calling fillrect(32, 16) would cause a 
4 x 4 rectangle of spaces to be written.

#### copyrect(copyfrom, count)

Copies ```count``` bytes from ```copyfrom``` (a 16 bit address) to the location beginning at the VAP pointer,
as a rectangle.

#### stashbuff(reuaddr, count)

Stores ```count``` bytes from the location beginning at the VAP pointer to the address specified by ```reuaddr``` (a 24 bit address) in the REU.

#### fetchbuff(reuaddr, count)

Retrieves ```count``` bytes to the location beginning at the VAP pointer from the address specified by ```reuaddr``` (a 24 bit address) in the REU.

# MIDI rendering

VesselASID provides a framework for running code in response to MIDI commands. The user provides a python module incontaining subclasses of
```VesselAsidRenderer``` (an example is provided). Each class is provided a program number which can be selected with a program change message.
Each class can be controlled with the usual MIDI messages (e.g. a note on message might cause an animation to advance).

```
$ asidrenderer --asid-port "Scarlett 4i4 USB:Scarlett 4i4 USB MIDI 1 20:0" --renderers vesselasid.examplerender
2024-03-01 08:52:43,041 importing vesselasid.examplerender
2024-03-01 08:52:43,042 found ExampleAsidRenderer
2024-03-01 08:52:43,042 program 0 is ExampleAsidRenderer
2024-03-01 08:52:43,042 using Scarlett 4i4 USB:Scarlett 4i4 USB MIDI 1 20:0 for ASID
2024-03-01 08:52:43,042 using Midi Through:Midi Through Port-0 14:0 for control input
2024-03-01 08:52:43,044 starting renderer ExampleAsidRenderer
2024-03-01 08:52:49,049 note_off channel=0 note=90 velocity=0 time=0
```
