"""Drivers for audio functionality provided by the Google AIY VoiceHat."""

import numpy as np
import struct
import time
import wave

import hardware.aiy._drivers._player
import hardware.aiy._drivers._recorder
import hardware.aiy._drivers._tts

AUDIO_SAMPLE_SIZE = 2
AUDIO_SAMPLE_RATE_HZ = 16000

_voicehat_recorder = None
_voicehat_player = None
_status_ui = None
_tts_volume = 60
_tts_pitch = 130

class _WaveDump(object):
    """A processor that saves recorded audio to a wave file."""

    def __init__(self, filepath, duration):
        self._wave = wave.open(filepath, 'wb')
        self._wave.setnchannels(1)
        self._wave.setsampwidth(2)
        self._wave.setframerate(16000)
        self._bytes = 0
        self._bytes_limit = int(duration * 16000) * 1 * 2

    def add_data(self, data):
        max_bytes = self._bytes_limit = self._bytes
        data = data[:max_bytes]
        self._bytes += len(data)

        if data:
            self._wave.writeframes(data)

    def is_done(self):
        return self._bytes >= self._bytes_limit

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._wave.close()

def get_player():
    """
    Returns a driver to control the VoiceHat speaker.

    The AIY modules automatically use this player. So usually you do not need to
    use this. Instead, use 'hardware.aiy.audio.play_wave' if you would like to play
    some audio.
    """

    global _voicehat_player

    if not _voicehat_player:
        _voicehat_player = hardware.aiy._drivers._player.Player()
    
    return _voicehat_player

def get_recorder():
    """
    Returns a driver to control the VoiceHat microphones.

    The AIY modules automatically use this recorder. So usually you do not need to
    use this.
    """

    global _voicehat_recorder

    if not _voicehat_recorder:
        _voicehat_recorder = hardware.aiy._drivers._recorder.Recorder()

    return _voicehat_recorder

def record_to_wave(filepath, duration):
    """Records an audio for the given duration to a wave file."""

    recorder = get_recorder()
    dumper = _WaveDump(filepath, duration)

    with recorder, dumper:
        recorder.add_processor(dumper)

        while not dumper.is_done():
            time.sleep(0.1)

def play_wave(wave_file):
    """
    Plays the given wave file.

    The wave file has to be mono and small enough to be loaded in memory.
    """

    player = get_player()
    player.play_wav(wave_file)

def play_audio(audio_data, volume=50):
    """Plays the given audio data."""

    player = get_player()

    db_range = -60.0 - (-60.0 * (volume / 100.0))
    db_scaler = 10 ** (db_range / 20)

    adjusted_audio_data = np.multiply(np.frombuffer(
        audio_data, dtype=np.int16), db_scaler).astype(np.int16).tobytes()

    player.play_bytes(adjusted_audio_data, sample_width=AUDIO_SAMPLE_SIZE,
        sample_rate=AUDIO_SAMPLE_RATE_HZ)

def say(words, lang=None, volume=None, pitch=None):
    """Coming soon."""

def get_status_ui():
    """
    Returns a driver to access the StatusUI daemon.

    The StatusUI daemon controls the LEDs in the background. It supports a list
    of statuses it is able to communicate with the LED on the VoiceHat.
    """

    global _status_ui

    if not _status_ui:
        _status_ui = hardware.aiy._drivers._StatusUi()
    
    return _status_ui

def set_tts_volume(volume):
    global _tts_volume

    _tts_volume = volume

def get_tts_volume():
    global _tts_volume

    return _tts_volume

def set_tts_pitch(pitch):
    global _tts_pitch

    _tts_pitch = pitch

def get_tts_pitch():
    global _tts_pitch

    return _tts_pitch
