"""
8-Bit Keyboard Synthesizer
Generates chiptune tones mapped to keyboard keys with recording capability
"""

import numpy as np
import pyaudio
import threading
import time
from collections import deque
from scipy import signal


class ChiptuneKeyboard:
    """Interactive 8-bit keyboard synthesizer"""
    
    # Musical note frequencies (in Hz) for a chromatic scale
    NOTE_FREQUENCIES = {
        # 低音区（左手）
        'v': 130.81,  # C3
        'f': 146.83,  # D3
        'd': 164.81,  # E3
        's': 174.61,  # F3
        'a': 196.00,  # G3
        'r': 220.00,  # A3
        'e': 246.94,  # B3
        'w': 261.63,  # C4
        'q': 293.66,  # D4
        # 高音区（右手）
        'n': 329.63,  # E4
        'j': 349.23,  # F4
        'k': 392.00,  # G4
        'l': 440.00,  # A4
        ';': 493.88, # B4
        'u': 523.25, # C5
        'i': 587.33, # D5
        'o': 659.25, # E5
        'p': 698.46, # F5
    }
    
    def __init__(self, sample_rate=22050, volume=0.3):
        """
        Initialize the keyboard synthesizer
        
        Args:
            sample_rate: Sample rate for audio generation
            volume: Default volume (0-1)
        """
        self.sample_rate = sample_rate
        self.volume = volume
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False
        self.recording = []
        self.is_recording = False
        self.play_queue = deque()
        
    def generate_square_wave(self, frequency, duration, duty_cycle=0.5):
        """
        Generate a square wave (classic 8-bit sound)
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            duty_cycle: Duty cycle (0.5 = perfect square)
            
        Returns:
            numpy array of samples
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = signal.square(2 * np.pi * frequency * t, duty=duty_cycle)
        return wave
    
    def generate_triangle_wave(self, frequency, duration):
        """
        Generate a triangle wave (softer 8-bit sound)
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            
        Returns:
            numpy array of samples
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = signal.sawtooth(2 * np.pi * frequency * t, width=0.5)
        return wave
    
    def generate_pulse_wave(self, frequency, duration):
        """
        Generate a pulse wave (narrow square wave)
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            
        Returns:
            numpy array of samples
        """
        return self.generate_square_wave(frequency, duration, duty_cycle=0.25)
    
    def generate_chiptune_note(self, frequency, duration, wave_type='square'):
        """
        Generate a note with envelope and effects
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            wave_type: 'square', 'triangle', or 'pulse'
            
        Returns:
            numpy array of samples
        """
        # Generate base waveform
        if wave_type == 'triangle':
            wave = self.generate_triangle_wave(frequency, duration)
        elif wave_type == 'pulse':
            wave = self.generate_pulse_wave(frequency, duration)
        else:  # square (default)
            wave = self.generate_square_wave(frequency, duration)
        
        # Apply ADSR envelope for more natural sound
        wave = self.apply_envelope(wave)
        
        # Apply volume
        wave = wave * self.volume
        
        return wave.astype(np.float32)
    
    def apply_envelope(self, wave):
        """
        Apply ADSR envelope to the wave
        
        Args:
            wave: numpy array of samples
            
        Returns:
            Modified wave with envelope
        """
        length = len(wave)
        envelope = np.ones(length)
        
        # Attack (first 5%)
        attack_samples = int(length * 0.05)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay (next 10%)
        decay_samples = int(length * 0.10)
        envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, 0.7, decay_samples)
        
        # Sustain (middle portion stays at 0.7)
        
        # Release (last 15%)
        release_samples = int(length * 0.15)
        envelope[-release_samples:] = np.linspace(0.7, 0, release_samples)
        
        return wave * envelope
    
    def play_note(self, frequency, duration=0.3, wave_type='square'):
        """
        Play a single note
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            wave_type: Type of waveform
        """
        wave = self.generate_chiptune_note(frequency, duration, wave_type)
        
        # Open stream if not already open
        if self.stream is None or not self.stream.is_active():
            self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                output=True
            )
        
        # Play the wave
        self.stream.write(wave.tobytes())
        
        # Record if recording is active
        if self.is_recording:
            self.recording.append({
                'frequency': frequency,
                'duration': duration,
                'wave_type': wave_type,
                'timestamp': time.time()
            })
    
    def play_key(self, key, duration=0.3):
        """
        Play a note based on keyboard key
        
        Args:
            key: Keyboard key character
            duration: Duration in seconds
        """
        key = key.lower()
        if key in self.NOTE_FREQUENCIES:
            frequency = self.NOTE_FREQUENCIES[key]
            self.play_note(frequency, duration)
            return True
        return False
    
    def start_recording(self):
        """Start recording key presses"""
        self.recording = []
        self.is_recording = True
        self.record_start_time = time.time()
        print("🔴 Recording started...")
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        print(f"⏹️  Recording stopped. Captured {len(self.recording)} notes.")
        return self.recording
    
    def playback_recording(self, recording=None):
        """
        Play back recorded notes
        
        Args:
            recording: List of note dictionaries (uses self.recording if None)
        """
        if recording is None:
            recording = self.recording
        
        if not recording:
            print("No recording to play back.")
            return
        
        print(f"▶️  Playing back {len(recording)} notes...")
        
        # Calculate relative timings
        start_time = recording[0]['timestamp']
        
        for note in recording:
            # Wait for the right time
            relative_time = note['timestamp'] - start_time
            time.sleep(max(0, relative_time - (time.time() - start_time)))
            
            # Play the note
            self.play_note(
                note['frequency'],
                note['duration'],
                note['wave_type']
            )
        
        print("✓ Playback complete!")
    
    def export_recording_to_wav(self, filename, recording=None):
        """
        Export recording to WAV file
        
        Args:
            filename: Output filename
            recording: List of note dictionaries (uses self.recording if None)
        """
        if recording is None:
            recording = self.recording
        
        if not recording:
            print("No recording to export.")
            return
        
        print(f"Exporting recording to {filename}...")
        
        # Calculate total duration
        start_time = recording[0]['timestamp']
        end_time = recording[-1]['timestamp'] + recording[-1]['duration']
        total_duration = end_time - start_time
        
        # Create empty audio buffer
        total_samples = int(self.sample_rate * total_duration)
        audio_buffer = np.zeros(total_samples, dtype=np.float32)
        
        # Add each note to the buffer
        for note in recording:
            # Calculate position in buffer
            relative_time = note['timestamp'] - start_time
            start_sample = int(relative_time * self.sample_rate)
            
            # Generate note
            wave = self.generate_chiptune_note(
                note['frequency'],
                note['duration'],
                note['wave_type']
            )
            
            # Add to buffer
            end_sample = min(start_sample + len(wave), total_samples)
            audio_buffer[start_sample:end_sample] += wave[:end_sample-start_sample]
        
        # Normalize
        max_val = np.abs(audio_buffer).max()
        if max_val > 0:
            audio_buffer = audio_buffer / max_val * 0.8
        
        # Export using scipy
        from scipy.io import wavfile
        wavfile.write(filename, self.sample_rate, audio_buffer)
        
        print(f"✓ Exported to {filename}")
    
    def close(self):
        """Clean up resources"""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    
    def print_keyboard_layout(self):
        """Print the keyboard layout guide"""
        print("\n" + "="*60)
        print("🎹 8-BIT CHIPTUNE KEYBOARD")
        print("="*60)
        print("\nLower Octave (Bass):")
        print("  Z  S  X  D  C  V  G  B  H  N  J  M")
        print("  C3 C# D3 D# E3 F3 F# G3 G# A3 A# B3")
        print("\nMiddle Octave:")
        print("  Q  2  W  3  E  R  5  T  6  Y  7  U")
        print("  C4 C# D4 D# E4 F4 F# G4 G# A4 A# B4")
        print("\nUpper Octave (Treble):")
        print("  I  9  O  0  P")
        print("  C5 C# D5 D# E5")
        print("\nControls:")
        print("  [SPACE] - Start/Stop Recording")
        print("  [ENTER] - Playback Recording")
        print("  [ESC]   - Exit")
        print("="*60 + "\n")


def main():
    """Demo of the keyboard synthesizer"""
    keyboard = ChiptuneKeyboard()
    keyboard.print_keyboard_layout()
    
    print("Press keys to play notes!")
    print("This demo plays a quick melody...\n")
    
    # Play a simple melody
    melody = ['q', 'e', 'g', 'g', 'e', 'q']  # C-E-G-G-E-C
    
    for key in melody:
        keyboard.play_key(key, duration=0.4)
        time.sleep(0.1)
    
    print("\n✓ Demo complete!")
    keyboard.close()


if __name__ == "__main__":
    main()
