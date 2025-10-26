# TheBitverse 🎮🎵🎂

A creative coding collection featuring retro-style interactive experiences: chiptune music conversion with real-time visualization, keyboard synthesis, voice-to-8bit transformation, and a face recognition birthday candle blowing game with ASCII art aesthetics.

## Projects Overview

### 1. 🎵 Chiptune Converter & Synthesizer
A comprehensive audio application with three powerful tools:
- **MP3 to 8-bit Converter**: Transform any music into authentic chiptune with real-time kaomoji visualization
- **Voice to 8-bit**: Record and convert your voice into robotic 8-bit effects
- **Keyboard Synthesizer**: Interactive piano with waveform visualization and recording

### 2. 🎂 Birthday Candle Blower
An interactive face recognition game where you blow out birthday candles using pout gestures, featuring:
- Real-time face and mouth detection
- ASCII art camera filter with retro aesthetics
- Dancing ASCII cats victory animation
- Birthday music celebration

---

## 🎵 Chiptune Converter & Synthesizer

### Features

#### MP3 to 8-bit Chiptune Converter
- Convert any MP3 file to authentic 8-bit chiptune music
- Three sample rate options:
  - **11025 Hz** - Game Boy DMG style (lo-fi)
  - **22050 Hz** - NES/Game Boy Color style (balanced)
  - **44100 Hz** - SNES/PS1 style (high quality)
- Extreme mechanical character with hybrid wave synthesis
- Real-time kaomoji and music symbol visualization with 12 dynamic patterns

#### Voice to 8-bit Converter 
- **Real-time Voice Recording**: Record through microphone
- **Playback Original**: Listen to raw recording before conversion
- **8-bit Voice Conversion**: Transform voice into robotic 8-bit audio
- **Export Functionality**: Save converted audio as MP3 file
- **Perfect for**: Voice effects, game audio, creative sound design

#### Interactive Keyboard Synthesizer
- Live keyboard piano
- Two octaves (C3-A5) mapped to QWERTY keys
- Real-time waveform visualization
- Recording and playback functionality
- Export recordings as MP3 files

### Installation

#### Prerequisites
```bash
# Python 3.8 - 3.11 recommended (tested and optimized)
# Python 3.12+ may have compatibility issues with some dependencies
python --version

# FFmpeg (required for audio processing)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows - Download from https://ffmpeg.org/download.html
```

#### Setup
```bash
cd TheBitverse

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Usage

Launch the application:
```bash
cd "chiptune converter"
python gui_app.py
```

**MP3 Converter Tab**: Select MP3 → Choose sample rate → Convert → Auto-play with visualization

**Voice to 8-bit Tab**: Record voice → Play original → Convert to 8-bit → Play result → Save as MP3

**Keyboard Synthesizer Tab**: Play keys → Record → Playback → Export WAV

---

## 🎂 Birthday Candle Blower

### Features

- **Face Detection**: Real-time face tracking using OpenCV Haar Cascades
- **Pout/Blow Gesture Recognition**: Detects mouth shape to blow out candles
- **16-bit ASCII Aesthetic**: Retro-style cake with animated flames
- **ASCII Camera Filter**: Toggle-able filter for full retro experience (120x160 resolution)
- **Dancing ASCII Cats**: 8 white cats with 2-frame animation appear on victory
- **Victory Music**: Birthday song plays when all candles are blown out
- **Interactive Gameplay**: Blow out 5 candles sequentially
- **Smart Detection**: Distinguishes pouts from smiles, tracks 15 frames for accuracy

### Installation

```bash
cd birthday_candle_blower
pip install -r requirements.txt
```

Requirements:
- Python 3.8+
- OpenCV 4.8.0+
- NumPy 1.24.0+
- Pygame 2.5.0+
- Webcam (HD resolution recommended)

### Usage

```bash
python main.py
```

**Controls**:
- **Pout gesture**: Blow out candles (purse lips in small circular shape)
- **R**: Restart game (stops music and resets)
- **A**: Toggle ASCII filter ON/OFF
- **Q**: Quit

**Gameplay Tips**:
- Press **A** to toggle ASCII filter for clearer camera view
- Watch progress bar at bottom to see blow detection progress
- Avoid wide smiles - only pout gestures are detected
- Hold pout gesture steady for 1-2 seconds

---

## Technical Highlights

### Chiptune Converter
- **8-bit Processing**: 6-bit quantization (64 levels) for robotic crunch
- **Hybrid Waveform**: 45% pulse wave, 20% triangle, 35% original signal
- **Modulation Effects**: 6.5 Hz vibrato, 6 Hz PWM for mechanical character
- **Visualization**: 12 pattern types (spirals, stars, flowers, mandalas) triggered by pitch/beat detection
- **Smart Pattern System**: High pitch (>3000 Hz) and pitch jumps (>800 Hz) trigger complex patterns

### Birthday Candle Blower
- **Face Detection**: Haar Cascade classifiers with mouth characteristic analysis
- **Pout Detection Algorithm**: 
  - Mouth area <6% of face area
  - Circular aspect ratio (0.35-1.0)
  - Width <40% of face width
  - Lower face position verification
- **ASCII Filter**: Converts camera to ASCII characters (` .:-=+*#%@`) while maintaining detection
- **Victory Animation**: 8 cats distributed in 2×4 grid, bouncing with sine wave motion
- **HD Resolution**: 1280×720 camera with 400px wide cake design

---

## Project Structure

```
TheBitverse/
├── chiptune converter/
│   ├── gui_app.py                 # Main GUI (3 tabs: MP3, Voice, Keyboard)
│   ├── chiptune_converter.py      # Advanced 8-bit audio engine
│   ├── chiptune_keyboard.py       # Keyboard synthesizer
│   └── enhanced_visualizer.py     # Visualization system
├── birthday_candle_blower/
│   ├── main.py                    # Face recognition game
│   ├── requirements.txt           # Python dependencies
│   ├── happybirthdaysong.mp3     # Victory music (user-provided)
│   └── README.md                  # Detailed documentation
├── index.html                     # Web interface (if any)
├── script.js
├── style.css
├── README.md                      # This file
└── requirements.txt               # Combined dependencies
```

---

## Dependencies

### Chiptune Converter
**Recommended Python Version**: 3.8 - 3.11 (Python 3.12+ may have issues with librosa and numba)

- `pydub` - Audio processing
- `librosa` - Music analysis (requires compatible numba version)
- `numpy` - Numerical computations
- `pygame` - Audio playback
- `sounddevice` - Microphone recording
- `scipy` - WAV operations
- `tkinter` - GUI (usually included with Python)

### Birthday Candle Blower
**Recommended Python Version**: 3.8+

- `opencv-python` - Face detection
- `numpy` - Array operations
- `pygame` - Music playback

---

## Audio Effect Characteristics

### Mechanical Robot Voice (Chiptune Converter)
Creates extreme robotic/mechanical character perfect for:
- 🤖 Robot voice acting and AI narration
- 🎮 Retro game audio (1980s-90s console sound)
- 🎵 Vocoder-style effects and chiptune vocals
- 🔊 Sci-fi sound design

**Key Characteristics**:
- Harsh 6-bit digital quantization
- Dominant square wave (45%) for "beep-boop" quality
- Fast vibrato and PWM for robotic warble
- Limited frequency: 120 Hz - 6 kHz
- Aggressive compression and subtle echo

**Sample Rate Impact**:
- **11025 Hz**: Ultra lo-fi Game Boy DMG sound
- **22050 Hz**: Classic NES/arcade quality
- **44100 Hz**: Clear but mechanical SNES/PS1 style

---

## Performance & Compatibility

- **Python**: 3.8 - 3.11 recommended for Chiptune Converter; 3.8+ for Birthday Candle Blower
- **CPU**: Modern multi-core recommended for smooth visualization
- **RAM**: 8GB+ for optimal performance
- **Camera**: HD webcam recommended for birthday game
- **OS**: macOS, Linux, Windows supported

### Known Issues
- **Python 3.12+**: May have compatibility issues with `librosa` and `numba` dependencies in Chiptune Converter
- macOS: Exit code 139 (segmentation fault) may occur on close - doesn't affect functionality
- Large audio files (>10MB) take longer to process
- Voice quality depends on microphone hardware

---

## Tips for Best Results

### Chiptune Converter
- Use clear melodies for better visualization patterns
- Lower sample rates emphasize retro character
- Speak clearly for voice recording, not too close to mic
- Instrumental tracks show pattern transitions more clearly

### Birthday Candle Blower
- Ensure good lighting for face detection
- Purse lips in small circular shape (not wide smile)
- Use ASCII filter toggle (A key) if camera view too blurry
- Add `happybirthdaysong.mp3` to project folder for victory music
- Position face directly toward camera at arm's length

---

## Quick Start

### Chiptune Converter
```bash
cd "chiptune converter"
python gui_app.py
```

### Birthday Candle Blower
```bash
cd birthday_candle_blower
python main.py
```

---

**Enjoy creating retro chiptune music, robotic voice effects, and blowing out virtual birthday candles! 🎮🎵🤖🎂✨**
