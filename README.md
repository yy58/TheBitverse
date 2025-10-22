# TheBitverse - 8-Bit Music & Game Universe# 🎮 The Bitverse - 8-Bit Chiptune Music Converter



## Project OverviewTransform your music into nostalgic 8-bit chiptune magic! The Bitverse lets you convert MP3 files into retro, pixelated audio and create your own chiptune melodies using an interactive keyboard synthesizer.

TheBitverse is a creative programming project that celebrates the nostalgic world of 8-bit chiptune music and retro-style games. This web application provides tools for converting modern music to 8-bit chiptune format, an online keyboard synthesizer, and a collection of browser-based retro-inspired games.

![Version](https://img.shields.io/badge/version-1.0.0-green)

## Features![Python](https://img.shields.io/badge/python-3.8%2B-blue)

![License](https://img.shields.io/badge/license-MIT-orange)

### Chiptune Converter

- **Desktop Application**: Convert MP3 files to 8-bit chiptune format (Available for download)## ✨ Features

- **Online Keyboard Synthesizer**: Create 8-bit music directly in your browser

- **Sound Customization**: Adjust waveforms, envelopes, and effects to create your unique 8-bit sound### 🎵 MP3 to 8-Bit Converter

- **Instant Conversion**: Upload any MP3, WAV, or audio file and watch it transform into a retro 8-bit masterpiece

### Retro Games- **Authentic Sound**: Uses square wave synthesis, bit-depth reduction, and sample rate downsampling for genuine chiptune character

- **Space Invaders**: Classic arcade shooting game- **Customizable Settings**: Adjust sample rates (11025Hz to 44100Hz) for different levels of "retro-ness"

- **Pixel Runner**: Endless runner with retro graphics - **Multiple Effects**: Automatic envelope shaping, dynamic range compression, and high-pass filtering

- **Bit Puzzler**: Brain-teasing puzzle game

### 🎹 Interactive Keyboard Synthesizer

## Technologies Used- **Real-time Playback**: 30+ keys mapped to musical notes across three octaves

- HTML5, CSS3, JavaScript- **Multiple Waveforms**: Choose from Square (classic), Triangle (soft), or Pulse (sharp) waves

- Web Audio API for sound synthesis- **Recording Capability**: Record your melodies and play them back

- Python/Tkinter for the desktop chiptune converter application- **Export功能**: Save your compositions as WAV files

- CSS animations for pixel art effects- **Visual Keyboard Layout**: On-screen guide shows note mappings



## Installation & Setup## 🚀 Installation



### Web Application### Prerequisites

1. Clone the repository- Python 3.8 or higher

```- FFmpeg (required for audio file conversion)

git clone https://github.com/yourusername/thebitverse.git

```### Step 1: Install FFmpeg

2. Open `index.html` in a modern web browser

**macOS:**

### Chiptune Converter Desktop App```bash

1. Navigate to the "chiptune converter" directorybrew install ffmpeg

2. Install required Python packages:```

```

pip install -r requirements.txt**Linux (Ubuntu/Debian):**

``````bash

3. Run the application:sudo apt-get update

```sudo apt-get install ffmpeg

python gui_app.py```

```

**Windows:**

## Project StructureDownload from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

```

TheBitverse/### Step 2: Clone the Repository

├── index.html              # Main web application page```bash

├── style.css               # CSS stylesgit clone https://github.com/yy58/TheBitverse.git

├── script.js               # Core JavaScript functionalitycd TheBitverse

├── chiptune-synth.html     # Online synthesizer page```

├── download.html           # Desktop app download page

├── chiptune converter/     # Desktop application folder### Step 3: Install Python Dependencies

│   ├── gui_app.py          # Main application file```bash

│   └── audio_processor.py  # Audio processing logicpip install -r requirements.txt

└── README.md               # Project documentation```

```

**Note for macOS users with M1/M2 chips:**

## DevelopmentIf you encounter issues with PyAudio, try:

This project was created as part of the SD5913 Creative Programming course at PolyU, combining technical skills with artistic expression.```bash

brew install portaudio

## Licensepip install pyaudio

This project is licensed under the MIT License - see the LICENSE file for details.```



## Acknowledgments## 🎮 Usage

- Classic 8-bit game developers for inspiration

- Open source audio libraries that make sound processing possible### Graphical User Interface (Recommended)

- PolyU SD5913 course instructors for guidance
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

## 🛠️ Technical Details

### Audio Processing Pipeline

1. **Loading**: Uses Pydub to load various audio formats
2. **Downsampling**: Reduces sample rate (default: 22050 Hz)
3. **Mono Conversion**: Converts stereo to mono for authentic chiptune feel
4. **Bit Depth Quantization**: Reduces to 8-bit (256 levels) for retro sound
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

## 🎯 Future Enhancements

- [ ] Add more waveform types (noise, sawtooth)
- [ ] Implement arpeggio and vibrato effects
- [ ] Add preset sound profiles (NES, Game Boy, C64)
- [ ] MIDI file import/export
- [ ] Visual waveform display
- [ ] Multi-track recording
- [ ] VST plugin version

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

## 🙏 Acknowledgments

- Inspired by classic 8-bit game consoles (NES, Game Boy, C64)
- Built with Python audio processing libraries
- Special thanks to the chiptune music community

## 📚 Resources

- [8-bit Music Theory](https://en.wikipedia.org/wiki/Chiptune)
- [Pydub Documentation](https://github.com/jiaaro/pydub)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)

---

**Made with ❤️ and nostalgia for SD5913 Creative Programming**

🎮 *Press START to continue...* 🎮