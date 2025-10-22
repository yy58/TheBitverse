# 🎮 The Bitverse - 8-Bit Chiptune Music Converter

Transform your music into nostalgic 8-bit chiptune magic! The Bitverse lets you convert MP3 files into retro, pixelated audio and create your own chiptune melodies using an interactive keyboard synthesizer, now with enhanced visual effects!

![Version](https://img.shields.io/badge/version-2.0.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🌈 Enhanced Music Visualizations
- **Dedicated Visualization Window**: Immersive full-screen capable visualizations that react to audio in real-time
- **Multiple Visual Modes**: Choose between Pixel Waves, Fractal Tunnel, Audio Particles, and Spectrum Grid
- **Dynamic Patterns**: Visuals that respond to audio features like pitch, rhythm, and frequency content
- **Interactive Controls**: Switch visualization modes on the fly while music plays

### 🎵 MP3 to 8-Bit Converter
- **Instant Conversion**: Upload any MP3, WAV, or audio file and watch it transform into a retro 8-bit masterpiece
- **Authentic Sound**: Uses square wave synthesis, bit-depth reduction, and sample rate downsampling for genuine chiptune character
- **Customizable Settings**: Adjust sample rates (11025Hz to 44100Hz) for different levels of "retro-ness"
- **Multiple Effects**: Automatic envelope shaping, dynamic range compression, and high-pass filtering

### 🎹 Interactive Keyboard Synthesizer
- **Real-time Playback**: 30+ keys mapped to musical notes across three octaves
- **Multiple Waveforms**: Choose from Square (classic), Triangle (soft), or Pulse (sharp) waves
- **Recording Capability**: Record your melodies and play them back
- **Visual Feedback**: Enhanced visual effects that respond to your keyboard playing
- **Export功能**: Save your compositions as WAV files
- **Visual Keyboard Layout**: On-screen guide shows note mappings

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (required for audio file conversion)
- Required Python packages (for enhanced visualizations):
  - librosa
  - numpy
  - sounddevice
  - matplotlib

### Step 1: Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Step 2: Clone the Repository
```bash
git clone https://github.com/yy58/TheBitverse.git
cd TheBitverse
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note for macOS users with M1/M2 chips:**
If you encounter issues with PyAudio, try:
```bash
brew install portaudio
pip install pyaudio
```

## 🎮 Usage

### Graphical User Interface (Recommended)

Launch the GUI application:
```bash
python gui_app.py
```

#### MP3 Converter Tab:
1. Click **"📁 Browse MP3 File"** to select your audio file
2. Choose your preferred sample rate (lower = more retro)
3. Click **"🎮 CONVERT TO 8-BIT! 🎮"**
4. Your converted file will be saved in the same directory with `_8bit_chiptune` suffix

#### Keyboard Synth Tab:
1. Select your waveform type (Square, Triangle, or Pulse)
2. Press keyboard keys to play notes (see keyboard layout below)
3. Click **"🔴 START RECORDING"** to record your melody
4. Press keys to create your composition
5. Click **"⏹️ STOP RECORDING"** when done
6. Click **"▶️ PLAYBACK"** to hear your recording
7. Click **"💾 EXPORT WAV"** to save your creation

### 🎹 Keyboard Layout

```
Lower Octave (Bass):
  Z    S    X    D    C    V    G    B    H    N    J    M
  C3  C#3  D3  D#3  E3   F3  F#3  G3  G#3  A3  A#3  B3

Middle Octave:
  Q    2    W    3    E    R    5    T    6    Y    7    U
  C4  C#4  D4  D#4  E4   F4  F#4  G4  G#4  A4  A#4  B4

Upper Octave (Treble):
  I    9    O    0    P
  C5  C#5  D5  D#5  E5
```

### Command Line Interface

**Convert an MP3 file:**
```bash
python chiptune_converter.py song.mp3
```

**Play a melody with the keyboard synth:**
```bash
python keyboard_synth.py
```

### Enhanced Visualization

The enhanced visualization system features multiple visualization modes that you can switch between:

1. **Pixel Waves**: Colorful pixel-based patterns that respond to audio frequencies and amplitude
2. **Fractal Tunnel**: Geometric patterns that expand and rotate in response to audio features
3. **Audio Particles**: Dynamic particle system that bursts and flows with the rhythm and intensity of the music
4. **Spectrum Grid**: Color-coded grid visualization showing frequency spectrum as patterns

To access the enhanced visualization:
- Use the "LAUNCH ENHANCED VISUALIZER" button in the converter tab
- Click "SHOW ENHANCED VISUALIZER" in the keyboard tab when playing notes
- Visualizations automatically appear in a separate window when playing converted audio

**Note**: For the best visual experience, ensure your system meets the minimum requirements and has all dependencies installed.

## 🛠️ Technical Details

### Audio Processing Pipeline

1. **Loading**: Uses Pydub to load various audio formats
2. **Downsampling**: Reduces sample rate (default: 22050 Hz)
3. **Mono Conversion**: Converts stereo to mono for authentic chiptune feel
4. **Bit Depth Quantization**: Reduces to 8-bit (256 levels) for retro sound

### Audio Visualization System

1. **Feature Extraction**: Uses librosa to analyze audio features in real-time:
   - Spectral centroid (brightness of sound)
   - Zero-crossing rate (noisiness/harshness)
   - RMS amplitude (volume/energy)
   - Onset detection (beats/rhythm)

2. **Visualization Processing**:
   - Real-time audio frame processing
   - Feature mapping to visual parameters (color, size, position, etc.)
   - Multiple rendering algorithms for different visual styles

3. **Rendering**:
   - Tkinter Canvas for graphics rendering
   - Separate thread for visualization processing
   - Synchronized with audio playback
5. **Square Wave Processing**: Adds harmonic content typical of 8-bit systems
6. **Envelope Shaping**: Applies ADSR envelope for natural note decay
7. **Filtering**: High-pass filter removes sub-bass (hardware limitations simulation)
8. **Compression**: Dynamic range compression for consistent volume

### Synthesis Engine

- **Waveform Generation**: Square, Triangle, and Pulse waves using scipy.signal
- **ADSR Envelope**: Attack (5%), Decay (10%), Sustain (70%), Release (15%)
- **Real-time Audio**: PyAudio for low-latency playback
- **Recording System**: Timestamp-based recording for accurate playback

## 📁 Project Structure

```
TheBitverse/
├── gui_app.py              # Main GUI application
├── chiptune_converter.py   # MP3 to 8-bit converter
├── keyboard_synth.py       # Interactive keyboard synthesizer
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── index.html             # Web demo (if applicable)
├── script.js              # Web scripts
└── style.css              # Web styles
```

## 🎨 Customization

### Use the custom font (Megamax Jonathan Too)

To use the Megamax Jonathan Too font in the app and web demo, install it on your system:

macOS:
- Double-click the `.ttf` or `.otf` file and click "Install Font" in Font Book
- Restart the app if it was running

Windows:
- Right-click the font file → Install for all users

Linux:
- Copy the font file to `~/.local/share/fonts` (user) or `/usr/local/share/fonts` (system)
- Run `fc-cache -f -v`

If the font isn't installed, the app will fall back to Courier New.

### Modify Conversion Settings

Edit `chiptune_converter.py`:
```python
converter = ChiptuneConverter(
    sample_rate=22050  # Try 11025 for more retro, 44100 for cleaner
)
```

### Adjust Keyboard Volume

Edit `keyboard_synth.py`:
```python
keyboard = ChiptuneKeyboard(
    sample_rate=22050,
    volume=0.3  # Range: 0.0 to 1.0
)
```

### Change Waveform Mix

In `chiptune_converter.py`, adjust the square wave mix:
```python
audio = self.add_square_wave_effect(audio, mix=0.2)  # Range: 0.0 to 1.0
```

## 🐛 Troubleshooting

### "FFmpeg not found" error
Make sure FFmpeg is installed and accessible in your PATH. Test with:
```bash
ffmpeg -version
```

### PyAudio installation fails
On macOS with Apple Silicon:
```bash
brew install portaudio
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio
```

On Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### No sound from keyboard
- Check your system audio settings
- Ensure no other applications are using the audio device
- Try running with administrator/sudo privileges


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**YYG**
- GitHub: [@yy58](https://github.com/yy58)

## Acknowledgments

- Inspired by classic 8-bit game consoles (NES, Game Boy, C64)
- Built with Python audio processing libraries
- Special thanks to the chiptune music community

## 📚 Resources

- [8-bit Music Theory](https://en.wikipedia.org/wiki/Chiptune)
- [Pydub Documentation](https://github.com/jiaaro/pydub)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)

---

**Made with ❤️ and nostalgia**

🎮 *Press START to continue...* 🎮
