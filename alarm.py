import os
import signal
import subprocess

class Alarm:
    def __init__(self, midi_file=None):
        self.driver = "alsa"
        self.gain = 1
        self.sample_rate = 44100
        self.midi_file = midi_file
        self.active = True
        self.pid = None

    def set_midi_file(self, midi_file):
        self.midi_file = midifile

    def reset(self):
        self.active = True

    def play_midi(self):
        if not self.pid and self.active and self.midi_file:
            cmd = 'fluidsynth -i -g {} -a {} -r {} {}'.format(str(self.gain), self.driver,  str(self.sample_rate), self.midi_file)
            midi = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            self.pid = midi.pid

    def stop_midi(self):
        if self.pid:
            self.active = False
            os.killpg(os.getpgid(self.pid), signal.SIGTERM)
            self.pid = None
