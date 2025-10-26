# TheBitverse 🎮🎵

A creative chiptune music converter and visualizer with real-time kaomoji animations, interactive keyboard synthesis, and voice-to-8bit conversion.



###  MP3 to 8-bit Chiptune Converter
- Convert any MP3 file to authentic 8-bit chiptune music
- Three sample rate options:
  - **11025 Hz** - Game Boy DMG style (lo-fi)
  - **22050 Hz** - NES/Game Boy Color style (balanced)
  - **44100 Hz** - SNES/PS1 style (high quality)
- Authentic 8-bit audio processing with extreme mechanical character

###  Voice to 8-bit Converter 
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
cd TheBitverse/chiptune\ converter

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source ../.venv/bin/activate
# Windows:
..\.venv\Scripts\activate

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

## 🎮 Usage

### Launch the Application
### Launch the Application
```bash
python gui_app.py
```

The application has **3 tabs**:

### 1️⃣ MP3 Converter Tab
1. **Select Input File**: Click "📁 Select MP3 File" and choose your audio file
2. **Choose Sample Rate**: Select 11025 Hz, 22050 Hz, or 44100 Hz
3. **Convert**: Click "🎮 CONVERT!" button
4. **Auto-play**: Music will automatically start playing with visualization
5. **Playback Controls**: Use "▶️ Play / ⏸️ Pause" button to control playback

### 2️⃣ Voice to 8-bit Tab (NEW!)
1. **Start Recording**: Click "🔴 START RECORDING" button
2. **Speak**: Record your voice (duration shown in real-time)
3. **Stop Recording**: Click "⏹️ STOP RECORDING" when finished
4. **Play Original**: Click "▶️ PLAY ORIGINAL" to hear raw recording
5. **Choose Sample Rate**: Select your desired output quality
6. **Convert**: Click "⚡ CONVERT TO 8-BIT" to apply robotic effect
7. **Play 8-bit**: Click "🎮 PLAY 8-BIT VERSION" to hear converted audio
8. **Save File**: Click "💾 SAVE 8-BIT AUDIO" to export as MP3

### 3️⃣ Keyboard Synthesizer Tab
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

## 🛠️ Technical Details

### Advanced 8-bit Audio Processing
**Extreme Mechanical Character with Hybrid Wave Synthesis**
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

## 📁 Project Structure & Required Files

### ✅ Essential Files (Required to Run):
```
chiptune converter/
├── gui_app.py              # ✅ Main GUI application (REQUIRED)
├── chiptune_converter.py   # ✅ Audio conversion engine (REQUIRED)
├── enhanced_visualizer.py  # ✅ Visualization system (REQUIRED)
├── requirements.txt        # ✅ Python dependencies (REQUIRED)
└── __pycache__/           # Auto-generated, can be deleted
```

### ❌ Optional/Unused Files (NOT Required to Run App):
```
├── keyboard_synth.py     # ⚠️  Legacy standalone version (now integrated into GUI)
├── index.html            # ❌ Web landing page (NOT NEEDED for Python app)
├── style.css            # ❌ Web styling (NOT NEEDED for Python app)
└── README.md            # 📖 Documentation (helpful but not required)
```

### 🗑️ Root Directory Cleanup:
```
TheBitverse/ (root)
├── index.html           # ❌ Web landing page (NOT NEEDED)
├── script.js           # ❌ Web JavaScript (NOT NEEDED)
├── style.css           # ❌ Web styling (NOT NEEDED)
├── temp_*.wav          # 🗑️  Temporary audio files (safe to delete)
├── temp_*.mp3          # 🗑️  Temporary audio files (safe to delete)
├── temp_*_cover.txt    # 🗑️  Generated ASCII art (safe to delete)
├── .venv/              # ✅ Virtual environment (recommended to keep)
└── venv/               # ⚠️  Duplicate virtual env (delete if you use .venv)
```

**Important Note**: The HTML/CSS/JS files (`index.html`, `script.js`, `style.css`) are web-based documentation or landing pages. **They are completely unnecessary for running the Python application**, which uses Tkinter for its GUI interface. You can safely delete all web files if you only want the working desktop application.

### Minimal Working Setup:
To run the app, you only need:
1. Python 3.7+
2. FFmpeg installed
3. Files in `chiptune converter/` folder:
   - `gui_app.py`
   - `chiptune_converter.py`  
   - `enhanced_visualizer.py`
   - `requirements.txt` (+ installed dependencies)

## 🎨 Customization

### Modify Audio Effect Intensity

Edit `chiptune_converter.py` to adjust the robotic character:

```python
# Line ~65: Adjust bit depth (lower = more crushed)
bit_depth_levels = 2 ** 6  # Try 5 for ultra-harsh, 7 for smoother

# Line ~75: Adjust pulse wave mix (higher = more robotic)
pulse_mix = 0.45  # Try 0.3 for softer, 0.6 for extreme robot

# Line ~85: Adjust modulation intensity
vibrato_depth = 0.020  # Try 0.010 for subtle, 0.030 for extreme
pwm_amount = 0.15      # Try 0.08 for light, 0.20 for heavy
```

### Change Sample Rate Defaults

In `gui_app.py`, modify the default sample rate:
```python
self.sample_rate_var = tk.StringVar(value="22050")  # Change to 11025 or 44100
```

### Adjust Visualization Sensitivity

In `gui_app.py`, adjust pattern trigger thresholds:
```python
# Line ~1700: Adjust trigger sensitivity
high_pitch_threshold = 3000  # Lower for more triggers
pitch_jump_threshold = 800   # Lower for more pattern changes
strong_beat_threshold = 0.3  # Lower for more beat detection
```

## 💡 Tips for Best Results

### Voice Recording:
- Use a decent microphone for clearer input
- Speak clearly and not too close to avoid distortion
- Lower sample rates (11025 Hz) give more extreme robot effect
- Higher sample rates (44100 Hz) maintain more clarity while still being robotic
- Record in a quiet environment to minimize background noise

### Music Conversion:
- Songs with clear melody work best for visualization patterns
- Lower sample rates emphasize retro character
- Instrumental tracks show pattern transitions more clearly
- Electronic music tends to trigger more dynamic patterns

## 🐛 Troubleshooting

### "FFmpeg not found" error
Make sure FFmpeg is installed and accessible in your PATH. Test with:
```bash
ffmpeg -version
```

### Voice recording not working
- Check microphone permissions in System Preferences/Settings
- Ensure sounddevice library is installed: `pip install sounddevice`
- Test your microphone with: `python -m sounddevice`

### Visualization not appearing
- Make sure librosa is installed: `pip install librosa`
- Check that audio file is valid and not corrupted
- Try restarting the application

### Audio playback issues
- Ensure pygame is installed: `pip install pygame`
- Check system audio settings
- Close other applications using audio device
- On Linux, try: `sudo apt-get install python3-pygame`

### Application crashes on macOS
- Exit code 139 is a known Tkinter/threading issue on macOS
- This occurs when closing the app and doesn't affect functionality
- Your work is saved before the crash

## ⚙️ Performance Notes
- Visualization is CPU-intensive; performance varies by system
- Recommended: Modern multi-core CPU, 8GB+ RAM
- Audio processing done in separate thread to avoid UI blocking
- Voice recording quality depends on microphone hardware




## 🎮 Acknowledgments

- Inspired by classic 8-bit game consoles (Game Boy, NES, Commodore 64)
- Built with Python audio processing libraries


---

**Enjoy creating retro chiptune music and robotic voice effects! 🎮🎵🤖✨**