#!/usr/bin/env python3

"""Check that the voiceHAT audio input and output are both working."""

import fileinput
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import traceback
import aiy.audio
from aiy._drivers._hat import get_aiy_device_name

AXIOM_PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
STOP_DELAY = 1.0
TEST_SOUND_PATH = 'front_center.wav'
RECORD_DURATION_SECONDS = 3
CARDS_PATH = '/proc/asound/cards'
CARDS_ID = {
    "Voice Hat": "googlevoicehat",
    "Voice Bonnet": "aiy-voicebonnet",
}

def get_sound_cards():
    """Read a dictionary of ALSA cards from /proc, indexed by number."""
    cards = {}

    with open(CARDS_PATH) as f:
        for line in f.read().splitlines():
            try:
                index = int(line.strip().split()[0])
            except (IndexError, ValueError):
                continue
            
            cards[index] = line
    
    return cards