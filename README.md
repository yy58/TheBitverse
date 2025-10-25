# TheBitverse 🎮🎵

A creative chiptune music converter and visualizer with real-time kaomoji animations, interactive keyboard synthesis, and voice-to-8bit conversion.

## Features

### 🎵 MP3 to 8-bit Chiptune Converter
- Convert any MP3 file to authentic 8-bit chiptune music
- Three sample rate options:
  - **11025 Hz** - Game Boy DMG style (lo-fi)
  - **22050 Hz** - NES/Game Boy Color style (balanced)
  - **44100 Hz** - SNES/PS1 style (high quality)
- Authentic 8-bit audio processing with extreme mechanical character

### 🎤 Voice to 8-bit Converter (NEW!)
- **Real-time Voice Recording**: Record your voice directly through microphone
- **Playback Original**: Listen to your raw recording before conversion
- **8-bit Voice Conversion**: Transform your voice into robotic 8-bit audio
- **Sample Rate Selection**: Choose between 11025 Hz, 22050 Hz, or 44100 Hz
- **Export Functionality**: Save converted audio as MP3 file
- **Perfect for**: Voice effects, game audio, creative sound design

### 🎨 Real-time Music Visualization
- **Kaomoji Animation Layer**: Expressive emoji faces in grid formation with music-reactive jitter
- **Music Symbol Layer**: Dynamic geometric patterns formed by music notes (♪♫♬♩✧)
- **12 Different Pattern Types**:
  
  **Complex Patterns (Triggered by high pitch/pitch jumps):**
  - Spiral 🌀
  - Double Spiral 🧬
  - 8-Point Star ⭐
  - Flower Petals 🌸
  - Lissajous Curves 🎵
  - Heart Shape ❤️
  - Infinity Symbol ∞
  - Mandala Pattern 🕉️

  **Simple Patterns (Triggered by beats):**
  - Concentric Circles ⭕
  - Square Grid ⬜
  - Triangle 🔺
  - Hexagon ⬡

- **Smart Trigger System**:
  - High pitch detection (>3000 Hz)
  - Pitch jump detection (>800 Hz change)
  - Strong beat detection
  - Automatic pattern selection based on music characteristics

### 🎹 Interactive Keyboard Synthesizer
- Live keyboard piano with ASCII art display
- Two octaves (C3-A5) mapped to QWERTY keys
- Real-time waveform visualization
- Recording and playback functionality
- Export recordings as WAV files
- Enhanced visualizer window option

### Prerequisites
```bash
# Python 3.7 or higher
python --version

# FFmpeg (required for audio processing)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Setup
```bash
# Clone the repository
git clone https://github.com/yy58/TheBitverse.git
cd TheBitverse

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- `pydub` - Audio processing
- `librosa` - Music analysis and feature extraction
- `numpy` - Numerical computations
- `pygame` - Audio playback
- `sounddevice` - Microphone recording
- `scipy` - WAV file operations
- `tkinter` - GUI (usually included with Python)

## Usage

### Launch the Application
```bash
cd "chiptune converter"
python gui_app.py
```

### MP3 Converter Tab
1. **Select Input File**: Click "📁 Select MP3 File" and choose your audio file
2. **Choose Sample Rate**: Select 11025 Hz, 22050 Hz, or 44100 Hz
3. **Convert**: Click "🎮 CONVERT!" button
4. **Auto-play**: Music will automatically start playing with visualization
5. **Playback Controls**: Use "▶️ Play / ⏸️ Pause" button to control playback

### Voice to 8-bit Tab (NEW!)
1. **Start Recording**: Click "🔴 START RECORDING" button
2. **Speak**: Record your voice (duration shown in real-time)
3. **Stop Recording**: Click "⏹️ STOP RECORDING" when finished
4. **Play Original**: Click "▶️ PLAY ORIGINAL" to hear raw recording
5. **Choose Sample Rate**: Select your desired output quality
6. **Convert**: Click "⚡ CONVERT TO 8-BIT" to apply robotic effect
7. **Play 8-bit**: Click "🎮 PLAY 8-BIT VERSION" to hear converted audio
8. **Save File**: Click "💾 SAVE 8-BIT AUDIO" to export as MP3

### Keyboard Synthesizer Tab
1. **Key Mapping**:
   - **Low Octave**: V=C3, F=D3, D=E3, S=F3, A=G3, T=A3, R=B3, E=C4, W=D4, Q=E4
   - **High Octave**: B=F4, H=G4, J=A4, K=B4, L=C5, Y=D5, U=E5, I=F5, O=G5, P=A5

2. **Recording**:
   - Click "🔴 START RECORDING" to begin
   - Play notes on keyboard
   - Click "⏹️ STOP RECORDING" to finish

3. **Playback & Export**:
   - Click "▶️ PLAYBACK" to listen to your recording
   - Click "💾 EXPORT WAV" to save as audio file

4. **Enhanced Visualizer**:
   - Click "🎮 SHOW ENHANCED VISUALIZER 🎮" for full-screen waveform display

## Technical Details

### Advanced 8-bit Audio Processing
**Extreme Mechanical Character with Hybrid Wave Synthesis**

#### Core Processing Pipeline:
1. **Mono Conversion**: Single channel for authentic chiptune
2. **Sample Rate Downsampling**: Adaptive to selected rate
3. **Extreme Bit Depth Reduction**: 6-bit quantization (64 levels) for maximum robotic crunch
4. **Aggressive Wave Shaping**: tanh(x * 3.5) for harsh harmonic distortion

#### Hybrid Waveform Synthesis:
- **45% Pulse Wave**: Dominant square wave for strong mechanical "buzz"
- **20% Triangle Wave**: Smooth melodic base for clarity
- **35% Original Signal**: Preserves intelligibility

#### Mechanical Modulation Effects:
- **Vibrato**: 6.5 Hz, 2.0% depth - pronounced robotic wobble
- **PWM (Pulse Width Modulation)**: 6 Hz, 15% depth - extreme mechanical character
- Creates distinctive Game Boy/NES robotic voice effect

#### Dynamic Processing:
- **Aggressive Compression**: Threshold -20dB, ratio 4.0:1
- **Volume Reduction**: -2dB for balanced output

#### Frequency Filtering (Hardware Simulation):
**High-Pass Filter**: 120 Hz (removes sub-bass)

**Adaptive Low-Pass Filtering**:
- **11025 Hz**: Cut at 2.5 kHz (extreme Game Boy DMG sound)
- **22050 Hz**: Cut at 4.0 kHz (harsh NES/retro arcade)
- **44100 Hz**: Cut at 6.0 kHz (mechanical but clear)

**Mid-Range Boost**: +2 to +4 dB for mechanical "tinny" speaker character

#### Echo/Delay Effects:
- **3 Echo Repeats**: 140ms delay intervals
- **Strong Decay**: 65% per repeat (quiet background ambience)
- **Decay Levels**: -13dB, -26dB, -45dB
- Subtle spatial depth without overpowering main voice

### Voice Recording System
- **Audio Input**: sounddevice library with real-time callback streaming
- **Format**: 16-bit PCM WAV (pygame-compatible)
- **Sample Rates**: Configurable 11025/22050/44100 Hz
- **Processing**: Full 8-bit conversion pipeline applied to voice
- **Output**: MP3 format for universal compatibility

### Visualization Engine
- **Frame Rate**: ~40 FPS (0.03s audio chunks, 0.025s sleep)
- **Feature Extraction**:
  - RMS amplitude for energy detection
  - Spectral centroid for pitch tracking
  - Onset strength for beat detection
- **Pattern Triggering**:
  - High pitch: >3000 Hz
  - Pitch jump: >800 Hz increase
  - Strong beat: detected + RMS >0.3
- **Rendering**: Tkinter Canvas with real-time text drawing

### Keyboard Synthesis
- **Waveform**: Pure sine wave generation
- **Sampling**: 44100 Hz (CD quality)
- **Volume**: 30% default (adjustable)
- **Polyphony**: Single note (monophonic)

## Project Structure
```
TheBitverse/
├── chiptune converter/
│   ├── gui_app.py              # Main GUI application (3 tabs)
│   ├── chiptune_converter.py   # Advanced 8-bit audio engine
│   ├── chiptune_keyboard.py    # Keyboard synthesizer
│   └── enhanced_visualizer.py  # Visualization system (reference)
├── README.md
└── requirements.txt
```

## Audio Effect Characteristics

### Mechanical Robot Voice Effect
The 8-bit converter creates an extreme robotic/mechanical character perfect for:
- 🤖 **Robot Voice Acting**: Game characters, AI voices, synthetic narration
- 🎮 **Retro Game Audio**: Authentic 1980s-90s game console sound
- 🎵 **Creative Music Production**: Vocoder-style effects, chiptune vocals
- 🔊 **Sound Design**: Sci-fi effects, mechanical sounds, retro aesthetics

### Key Sound Characteristics:
- **Harsh Digital Quantization**: 6-bit crushing for broken/pixelated sound
- **Dominant Square Wave**: 45% pulse wave creates strong "beep-boop" quality
- **Extreme Modulation**: Fast vibrato and PWM for robotic warble/flutter
- **Limited Frequency Range**: 120 Hz - 6 kHz mimics cheap 8-bit speakers
- **Aggressive Compression**: "Squashed" dynamic range typical of old hardware
- **Subtle Echo**: Light spatial ambience without overwhelming main signal

### Sample Rate Impact:
- **11025 Hz**: Most extreme/lo-fi - ultra Game Boy DMG sound
- **22050 Hz**: Balanced retro - classic NES/arcade quality  
- **44100 Hz**: Clear but mechanical - SNES/PS1 style with robotic edge

## Performance Notes
- Visualization is CPU-intensive; performance varies by system
- Recommended: Modern multi-core CPU, 8GB+ RAM
- Audio processing is done in separate thread to avoid UI blocking
- Pygame mixer handles real-time audio playback
- Voice recording requires working microphone input

## Known Issues
- Exit code 139 (segmentation fault) may occur on some macOS systems when closing - this is a known Tkinter/threading issue and doesn't affect functionality
- Large audio files (>10MB) may take longer to process
- Voice recording quality depends on microphone hardware

## Tips for Best Results
### Voice Recording:
- Use a decent microphone for clearer input
- Speak clearly and not too close to avoid distortion
- Lower sample rates (11025 Hz) give more extreme robot effect
- Higher sample rates (44100 Hz) maintain more clarity while still being robotic

### Music Conversion:
- Songs with clear melody work best for visualization patterns
- Lower sample rates emphasize retro character
- Instrumental tracks show pattern transitions more clearly


**Enjoy creating retro chiptune music and robotic voice effects! 🎮🎵🤖✨**
