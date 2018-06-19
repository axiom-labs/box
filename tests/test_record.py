#!/usr/bin/env python3

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

THRESHOLD = 500
CHUNK_SIZE = 2048
FORMAT = pyaudio.paInt16
RATE = 48000

def is_silent(sound_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(sound_data) < THRESHOLD

def normalize(sound_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in sound_data)

    r = array('h')
    for i in sound_data:
        r.append(int(i*times))
    return r

def trim(sound_data):
    "Trim the blank spots at the start and end"
    def _trim(sound_data):
        sound_started = False
        r = array('h')

        for i in sound_data:
            if not sound_started and abs(i) > THRESHOLD:
                sound_started = True
                r.append(i)
            elif sound_started:
                r.append(i)
        return r

    # Trim to the left
    sound_data = _trim(sound_data)

    # Trim to the right
    sound_data.reverse()
    sound_data = _trim(sound_data)
    sound_data.reverse()

    return sound_data

def add_silence(sound_data, seconds):
    "Add silence to the strt and end of 'sound_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds * RATE))])
    r.extend(sound_data)
    r.extend([0 for i in range(int(seconds * RATE))])

    return r

def record():
    """
    Record a word or words from microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound.
    """

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    sound_started = False

    r = array('h')

    while 1:
        sound_data = array('h', stream.read(CHUNK_SIZE))

        if byteorder == 'big':
            sound_data.byteswap()
        r.extend(sound_data)

        silent = is_silent(sound_data)

        if silent and sound_started:
            num_silent += 1
        elif not silent and not sound_started:
            sound_started = True

        if sound_started and num_silent > 30:
            break
        
    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)

    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    print("Please speak a word into the microphone")

    record_to_file('demo.wav')

    print("Done - Result written to demo.wav")