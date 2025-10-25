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
        Convert audio to hybrid 8-bit chiptune style
        Blend of soft triangle wave melody with retro mechanical character
        """
        print("Converting to hybrid 8-bit chiptune style...")
        
        # Step 1: Convert to mono for authentic chiptune
        audio = audio.set_channels(1)
        
        # Step 2: Downsample to target rate
        audio = audio.set_frame_rate(self.sample_rate)
        
        # Step 3: Get samples as numpy array
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        
        # Step 4: Normalize with balanced headroom
        max_val = np.abs(samples).max()
        if max_val > 0:
            samples = samples / max_val * 0.68  # Balanced volume
        
        # Step 5: EXTREME bit depth for maximum robotic crunch (6-bit!)
        # Ultra-harsh quantization for strong mechanical voice
        bit_depth_levels = 2 ** 6  # Only 64 levels - very crushed!
        samples = np.round(samples * (bit_depth_levels / 2 - 1)) / (bit_depth_levels / 2 - 1)
        
        # Step 6: Very aggressive wave shaping for harsh mechanical edge
        samples = np.tanh(samples * 3.5) * 0.98
        
        # Step 7: MAXIMUM mechanical character - dominant pulse wave
        # Heavy pulse component for strong robotic voice effect
        triangle_mix = 0.20  # Only 20% smooth triangle
        pulse_mix = 0.45     # 45% mechanical pulse - dominant!
        
        triangle_wave = samples  # Smooth base
        pulse_wave = np.sign(samples) * 0.88  # Very strong mechanical accent
        
        samples = (samples * (1 - triangle_mix - pulse_mix) + 
                   triangle_wave * triangle_mix + 
                   pulse_wave * pulse_mix)
        
        # Step 8: Maximum vibrato for prominent robotic wobble
        vibrato_freq = 6.5  # Hz (much faster)
        vibrato_depth = 0.020  # Very pronounced
        t = np.arange(len(samples)) / self.sample_rate
        vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
        samples = samples * vibrato
        
        # Step 9: Very strong PWM for dominant mechanical buzz/robot voice
        pwm_freq = 6  # Hz (faster)
        pwm_amount = 0.15  # Very strong for extreme robotic character
        pwm = 1 + pwm_amount * np.sin(2 * np.pi * pwm_freq * t)
        samples = samples * pwm
        
        # Step 10: Convert back to audio
        samples_int = (samples * 32767).astype(np.int16)
        audio = audio._spawn(samples_int.tobytes())
        
        # Step 11: Aggressive compression for mechanical consistency
        audio = compress_dynamic_range(audio, threshold=-20.0, ratio=4.0)
        
        # Step 12: Slight volume reduction
        audio = audio - 2  # Reduce by 2dB
        
        return audio
    
    def add_retro_effects(self, audio):
        """
        Add aggressive retro effects for maximum mechanical character
        Harsh filtering and subtle echo for extreme 8-bit robot voice
        
        Args:
            audio: AudioSegment object
            
        Returns:
            Modified AudioSegment
        """
        # Higher high-pass for more mechanical "tinny" sound
        audio = audio.high_pass_filter(120)
        
        # Harsh low-pass filtering for extreme mechanical character
        # Very limited frequency range for robot voice effect
        if self.sample_rate <= 11025:
            # For 11kHz, harsh cut at 2.5kHz (extreme Game Boy DMG)
            audio = audio.low_pass_filter(2500)
            # Strong mid boost for mechanical presence
            audio = audio + 4
        elif self.sample_rate <= 22050:
            # For 22kHz, harsh cut at ~4kHz (extreme NES style)
            audio = audio.low_pass_filter(4000)
            audio = audio + 3
        else:
            # For 44kHz, limited cut at ~6kHz (mechanical but clear)
            audio = audio.low_pass_filter(6000)
            audio = audio + 2
        
        # Add subtle mid-range character for presence
        # Light boost for retro speaker simulation
        mid_boost = audio.high_pass_filter(600).low_pass_filter(3500)
        audio = audio.overlay(mid_boost - 12)  # Very subtle blend
        
        # Subtle delay/echo - present but quieter background
        # Create softer echo repeats that don't overpower main voice
        delay_time = 140  # milliseconds (balanced timing)
        decay_factor = 0.65  # Much stronger decay (echoes quieter)
        
        # First echo (quieter)
        echo1 = audio - (20 * decay_factor)  # ~13dB quieter
        combined = audio.overlay(echo1, position=delay_time)
        
        # Second echo (very soft)
        echo2 = audio - (20 * decay_factor * 2.0)  # ~26dB quieter
        combined = combined.overlay(echo2, position=delay_time * 2)
        
        # Third echo (barely audible, for subtle depth)
        echo3 = audio - (20 * decay_factor * 3.5)  # ~45dB quieter
        combined = combined.overlay(echo3, position=delay_time * 3)
        
        return combined
    
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
