<h1>Instructions for finalsynth</h1>

<h2>Step 1: clone the github repository </h2>
Create a new local folder for the project then execute the code below in the command prompt.  

Example:  
`cd C:\Users\Laney\Documents\myfolder`  
`git init`  
`git clone https://github.com/vbreeden/music6202`  

<h2>Step 2: set up an environment</h2>
Example: set up a python environment called 'env'.

`python -m venv env`  

Activate the environment  
On macOS and Linux:
`source env/bin/activate`  

On Windows:
`.\env\Scripts\activate`

Install requirements.txt
`pip install -r FinalProject\requirements.txt`

If there are any missing package errors at this step, install them.

Example:  
`pip install music21`


<h2>Step 3: run the synth </h3>

<h3> Examples </h3>

 `python finalsynth.py -s additive sine -k melody2.krn -o low5000_16.wav -a 44100 -q 16 -l 500`

 `python finalsynth.py -s wavetable 5 static 0.25 -k melody3.krn -o sample0.wav -a 44100 -q 16 -v 200 1 -r big_hall 0.8 -l 2500`

`python finalsynth.py -s additive sine -k melody1.krn -o sample1.wav -a 44100 -q 16 -v 200 2 -r jazz_hall 0.8 -l 2500`

 `python finalsynth.py -s wavetable 1 sweep 1 -k melody1.krn -o sample2.wav -a 44100 -q 24 -c 200 1 -d 0.1 0.3 -r jazz_hall 0.8 -l 2500`

`python finalsynth.py -s additive square -k melody2.krn -o sample3.wav -a 44100 -q 16 -d 0.1 -r jazz_hall 0.9 -l 2500`

<h3> Required arguments </h3>

1. kern input file  
  * options are `melody1.krn`,...,`melody4.krn`  
  * example: `-k melody1.krn`  

2. synthesis method
  * `additive` + type (`sine` or `square`)
  * `wavetable` +
    + starting timbre from 1 to 10 (`1`=pure square, `10`=pure sine)
    + `sweep` or `static` (sweep across wavetable or remain on static + timbre)
   + time in seconds to complete a sweep cycle
 * examples:  
`-s additive sine`  
`-s wavetable 5 sweep 0.75`
3. down-sample rate
  * example: `-a 41000`
4. down-quantization bitrate
  * options are 8 16, or 24
  * example: `q 16`
5. output file name  
  * name of the output wav file in the 'audio' subfolder
  * example: `-o myoutput.wav`

<h3>Optional arguments (effects)</h3>

1. chorus
  * maximum delay samples  
  * frequency modulation
  * example: `-c 200 1.5`  
2. delay
  * length of delay in seconds
  * wet/dry mix percentage
  * example: `-d 0.25 0.5`
3. vibrato
  * max delay samples
  * frequency modulation
  * example: `-v 200 1`
4. bandpass filter
  * lower and upper bounds of band
  * example: `-b 400Hz 500Hz`
5. lowpass filter
  * frequency cutoff
  * example: `l 100Hz`
6. reverb
  * wav file to use for impulse response
  * Available options: `IR.wav`, `big_hall.wav`, `big_room.wav`, `box.wav`, `drum_plate.wav`, `jazz_hall.wav`, `wet_reverb.wav`
  * Dry/wet mix (`0`=dry `1`=wet)
  * Example: `-r IR.wav 0.4`
