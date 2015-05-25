import numpy as np
from scikits import audiolab as al
#import matplotlib.pyplot as plt


NOTES = {
	'C5': 523.25,
	'Db5': 554.37,
	'D5': 587.33,
	'Eb5': 622.25,
	'E5': 659.25,
	'F5': 698.46,
	'Gb5': 739.99,
	'G5': 783.99,
	'Ab5': 830.61,
	'A5': 880.00,
	'Bb5': 932.33,
	'B5': 987.77,
	'C6': 1046.50
}

melody = [
'C5',
'D5',
'E5',
'F5',
'G5',
'A5',
'B5',
'C6',
'B5',
'A5',
'G5',
'F5',
'E5',
'D5',
'C5'
]

amplitude = 0.3
f_sample = 48000
duration = 0.5
samples = f_sample * duration

pause = 0.001
break_samples = int(round(f_sample*pause))
break_sig = np.zeros(break_samples)

value_ids = np.arange(samples)

attack_length = 0.002
attack_end_sample = int(round(samples*attack_length))
attack_mod = np.linspace(0,1,attack_end_sample,True)

decay_length = 0.8
decay_start_sample = samples - int(round(samples*decay_length))
decay_mod = np.linspace(1,0,samples - decay_start_sample,True)

tone_shape = np.ones(samples)
tone_shape[0:attack_end_sample] = attack_mod
tone_shape[decay_start_sample:] = decay_mod

overtones = [2,3,4,5,6,7,8]
overamps = [0.08,0.05,0.01,0.005,0.001,0.0001,0.00001]

tune = np.zeros((2,len(melody)*(samples)))

for j in range(len(melody)):
	tone = melody[j]
	f_sin = NOTES[tone]
	ground = np.sin(f_sin/f_sample*np.arange(samples))
	sig = ground
	for i in np.arange(len(overtones)):
		n = overtones[i]
		relamp = overamps[i]
		overtone = relamp*np.sin(f_sin*n/f_sample*np.arange(samples))
		sig = np.add(sig,overtone)
	sig = amplitude*np.multiply(sig,tone_shape)

	tstart = j*samples
	tstop = (j+1)*samples
	tune[0,tstart:tstop] = sig
	tune[1,tstart:tstop] = sig

print f_sample
print len(tune[0])/len(melody)

#plt.plot(tune[0])
#plt.show()

al.play(tune[0],f_sample)
