"""
8-Bit Chiptune Music Converter
Converts MP3 files into nostalgic, retro 8-bit versions
"""

import numpy as np
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
from scipy import signal
import os
# Added audio feature analysis dependencies
import librosa
import librosa.display


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
    
    def analyze_features(self, audio_path):
        """
        Analyze audio file and extract key features
        """
        import librosa
        
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        # Extract key features
        # Pitch information (using piptrack to estimate overall pitch)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        avg_pitch = 0
        if pitches.any():
            avg_pitch = np.mean([
                pitch[mag == mag.max()]
                for pitch, mag in zip(pitches, magnitudes)
                if mag.any()
            ])
        
        # Tempo estimation
        tempo = 120  # Default value
        if hasattr(librosa.beat, 'tempo'):  # Check for new API
            tempo = librosa.beat.tempo(y=y, sr=sr)[0]
        
        # Spectral centroid (brightness)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        avg_centroid = np.mean(spectral_centroids)
        
        # Zero-crossing rate (noisiness/harshness)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        avg_zcr = np.mean(zcr)
        
        print(f"Audio analysis complete: pitch={avg_pitch:.2f}, tempo={tempo:.2f}, centroid={avg_centroid:.2f}")
        
        return {
            'avg_pitch': avg_pitch,
            'tempo': tempo,
            'avg_centroid': avg_centroid,
            'avg_zcr': avg_zcr
        }
        
    def analyze_frame_features(self, frame, sr):
        """
        Analyze a single audio frame for real-time visualization
        
        Args:
            frame: Audio samples
            sr: Sample rate
            
        Returns:
            Dictionary of audio features
        """
        import librosa
        import numpy as np
        
        try:
            # Pitch information (simplified for speed)
            pitches, magnitudes = librosa.piptrack(y=frame, sr=sr)
            avg_pitch = 0
            if pitches.any() and magnitudes.any():
                avg_pitch = np.mean(pitches[magnitudes > magnitudes.mean()])
                if np.isnan(avg_pitch):
                    avg_pitch = 200  # Default value
            else:
                avg_pitch = 200  # Default value
            
            # Tempo (simplified)
            tempo = 120  # Default value
            
            # Spectral centroid
            spectral_centroids = librosa.feature.spectral_centroid(y=frame, sr=sr)[0]
            avg_centroid = np.mean(spectral_centroids) if len(spectral_centroids) > 0 else 2000
            
            # Zero-crossing rate
            zcr = librosa.feature.zero_crossing_rate(frame)[0]
            avg_zcr = np.mean(zcr) if len(zcr) > 0 else 0.1
            
            return {
                'avg_pitch': avg_pitch,
                'tempo': tempo,
                'avg_centroid': avg_centroid,
                'avg_zcr': avg_zcr
            }
            
        except Exception as e:
            print(f"Frame analysis error: {e}")
            # Return default values
            return {
                'avg_pitch': 200,
                'tempo': 120,
                'avg_centroid': 2000,
                'avg_zcr': 0.1
            }

    def features_to_ascii_art(self, features, width=40, height=16):
        """
        Create pixel-style ASCII art based on audio features
        Pitch → character type, Spectral Centroid → brightness,
        Zero-Crossing Rate → edges/jitter, Tempo → horizontal block rhythm
        """
        import random
        import math
        
        # Get features
        pitch = features['avg_pitch']
        tempo = features['tempo']
        centroid = features['avg_centroid']
        zcr = features['avg_zcr']
        
        # Enhanced character set for more visual variety
        chars = [' ', '.', '·', ':', '*', '+', '=', '#', '%', '@', '█', '▓', '▒', '░']
        
        # Pitch to character mapping (expanded range)
        pitch_index = min(len(chars)-1, max(0, int(pitch / 100)))
        main_char = chars[pitch_index]
        
        # Secondary character based on centroid (brightness)
        cent_index = min(len(chars)-1, max(0, int(centroid / 500)))
        bright_char = chars[cent_index]
        
        # Edge character based on zero-crossing rate
        edge_index = min(len(chars)-2, max(0, int(zcr * 50)))
        edge_char = chars[edge_index + 2]  # Offset for visibility
        
        # Pattern variety based on tempo
        block_size = max(3, int(60/tempo * 2)) if tempo > 0 else 6
        
        # Generate more interesting patterns
        art = []
        for y in range(height):
            row = ''
            for x in range(width):
                # Base pattern selection
                pattern_val = (x % block_size) + (y % block_size)
                
                # Wave pattern overlay
                wave_val = math.sin(x * 0.2 + y * 0.1) * math.cos(y * 0.1 + x * 0.05)
                
                # Character selection logic with more interesting patterns
                if pattern_val <= block_size // 2:
                    # Main pattern
                    if wave_val > 0.3:
                        c = main_char
                    else:
                        c = bright_char
                else:
                    # Secondary pattern
                    if (x + y) % block_size == 0:
                        c = edge_char
                    elif wave_val < -0.3:
                        c = chars[min(len(chars)-1, abs(pitch_index - cent_index))]
                    else:
                        c = chars[min(len(chars)-1, abs(pitch_index + cent_index) % len(chars))]
                
                # Add occasional random pixels for texture
                if random.random() < 0.01 * zcr * 10:
                    c = random.choice(chars[8:])
                
                # Add to row
                row += c
            art.append(row)
        
        # Add a decorative border
        bordered_art = []
        border_top = '╔' + '═' * width + '╗'
        border_bottom = '╚' + '═' * width + '╝'
        bordered_art.append(border_top)
        
        for line in art:
            bordered_art.append('║' + line + '║')
        
        bordered_art.append(border_bottom)
        
        # Add a title
        title = " TheBitverse - 8-bit Chiptune "
        title_pos = max(0, (width - len(title)) // 2)
        if title_pos > 0:
            bordered_art[0] = '╔' + '═' * title_pos + title + '═' * (width - title_pos - len(title)) + '╗'
        
        return '\n'.join(bordered_art)

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
        # Generate output path
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_8bit_chiptune.mp3"
        # Save audio
        self.save_audio(audio, output_path)
        # Analyze audio features
        features = self.analyze_features(input_path)
        print("音频特征分析结果：")
        for k, v in features.items():
            print(f"  {k}: {v}")
        # 生成ASCII像素画
        ascii_art = self.features_to_ascii_art(features)
        cover_path = os.path.splitext(output_path)[0] + '_cover.txt'
        with open(cover_path, 'w', encoding='utf-8') as f:
            f.write(ascii_art)
        print(f"已生成像素风格ASCII封面: {cover_path}")
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
