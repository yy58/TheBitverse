"""
8-Bit Chiptune Music Converter
Converts MP3 files into nostalgic, retro 8-bit versions
"""

import numpy as np
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
from scipy import signal
import os


class ChiptuneConverter:
    """Converts audio files to 8-bit chiptune style"""
    
    def __init__(self, sample_rate=22050):
        """
        Initialize the converter
        
        Args:
            sample_rate: Target sample rate (lower = more retro)
        """
        self.sample_rate = sample_rate
        self.bit_depth = 8  # 8-bit audio
        
    def load_audio(self, file_path):
        """
        Load an audio file (MP3, WAV, etc.)
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            AudioSegment object
        """
        print(f"Loading audio from: {file_path}")
        audio = AudioSegment.from_file(file_path)
        return audio
    
    def convert_to_8bit(self, audio):
        """
        Convert audio to crisp, classic 8-bit chiptune style (Mario/NES)
        """
        print("Converting to crisp 8-bit chiptune style...")
        # Mono
        audio = audio.set_channels(1)
        # Downsample
        audio = audio.set_frame_rate(self.sample_rate)
        # Get samples
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        max_val = np.abs(samples).max()
        if max_val > 0:
            samples = samples / max_val
        # Bitcrush (less aggressive)
        bit_depth_levels = 2 ** self.bit_depth
        samples = np.round(samples * (bit_depth_levels / 2)) / (bit_depth_levels / 2)
        # Pure square wave (no distortion, no vibrato)
        samples = np.sign(samples)
        # Normalize
        if np.abs(samples).max() > 0:
            samples = samples / np.abs(samples).max() * 0.9
        samples_int = (samples * 32767).astype(np.int16)
        audio = audio._spawn(samples_int.tobytes())
        # Gentle compression
        audio = compress_dynamic_range(audio, threshold=-18.0, ratio=2.0)
        return audio
    
    def apply_square_wave_distortion(self, samples, intensity=0.6):
        """
        Apply aggressive square wave distortion for authentic chiptune sound
        
        Args:
            samples: Normalized audio samples (-1 to 1)
            intensity: How much distortion to apply (0-1)
            
        Returns:
            Distorted samples
        """
        # Create square wave by using sign function
        square = np.sign(samples)
        
        # Mix original with square wave for authentic chiptune character
        distorted = (1 - intensity) * samples + intensity * square
        
        # Add harmonic distortion
        distorted = np.tanh(distorted * 2.0) * 0.8
        
        return distorted
    
    def apply_pwm_effect(self, samples, rate=0.1):
        """
        Apply pulse width modulation effect
        
        Args:
            samples: Audio samples
            rate: Modulation rate
            
        Returns:
            Modulated samples
        """
        # Create subtle PWM effect
        length = len(samples)
        t = np.arange(length) / self.sample_rate
        pwm = 0.5 + 0.3 * np.sin(2 * np.pi * rate * t)
        
        # Apply threshold based on PWM
        output = np.where(samples > 0, 
                         np.where(np.abs(samples) > pwm, samples, samples * 0.5),
                         np.where(np.abs(samples) > pwm, samples, samples * 0.5))
        
        return output
    
    def apply_vibrato(self, samples, rate=5.0, depth=0.003):
        """
        Apply vibrato effect (pitch modulation)
        
        Args:
            samples: Audio samples
            rate: Vibrato rate in Hz
            depth: Vibrato depth (0-1)
            
        Returns:
            Samples with vibrato
        """
        length = len(samples)
        t = np.arange(length) / self.sample_rate
        
        # Create vibrato modulation
        vibrato = depth * self.sample_rate * np.sin(2 * np.pi * rate * t)
        
        # Apply vibrato by modulating sample positions
        indices = np.arange(length) + vibrato
        indices = np.clip(indices, 0, length - 1).astype(int)
        
        return samples[indices]
    
    def add_retro_effects(self, audio):
        """
        Add additional retro effects for authentic 8-bit sound
        
        Args:
            audio: AudioSegment object
            
        Returns:
            Modified AudioSegment
        """
        # High-pass filter to remove deep bass (simulates hardware limitations)
        audio = audio.high_pass_filter(200)
        
        # Low-pass filter to remove high frequencies (authentic to 8-bit systems)
        audio = audio.low_pass_filter(8000)
        
        # Boost mid-range frequencies (typical of chiptune)
        audio = audio + 3
        
        # Add a tiny bit of noise for analog feel (optional)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        noise = np.random.normal(0, 10, len(samples))
        samples = samples + noise
        samples = np.clip(samples, -32768, 32767).astype(np.int16)
        audio = audio._spawn(samples.tobytes())
        
        return audio
    
    def save_audio(self, audio, output_path, format="mp3"):
        """
        Save the converted audio
        
        Args:
            audio: AudioSegment object
            output_path: Path to save the file
            format: Output format (mp3, wav, etc.)
        """
        print(f"Saving converted audio to: {output_path}")
        audio.export(output_path, format=format)
        print("Conversion complete!")
    
    def convert_file(self, input_path, output_path=None):
        """
        Complete conversion pipeline
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save output (auto-generated if None)
            
        Returns:
            Path to output file
        """
        # Load audio
        audio = self.load_audio(input_path)
        
        # Convert to 8-bit
        audio = self.convert_to_8bit(audio)
        
        # Add retro effects
        audio = self.add_retro_effects(audio)
        
        # Generate output path if not provided
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_8bit_chiptune.mp3"
        
        # Save
        self.save_audio(audio, output_path)
        
        return output_path


def main():
    """Demo usage of the converter"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python chiptune_converter.py <input_audio_file>")
        print("Example: python chiptune_converter.py song.mp3")
        return
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        return
    
    # Create converter and process file
    converter = ChiptuneConverter(sample_rate=22050)
    output_file = converter.convert_file(input_file)
    
    print(f"\n✓ Success! Your 8-bit chiptune is ready: {output_file}")


if __name__ == "__main__":
    main()
