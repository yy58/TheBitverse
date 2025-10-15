# 🎮 The Bitverse - 8-Bit Chiptune Music Converter

Transform your music into nostalgic 8-bit chiptune magic! The Bitverse lets you convert MP3 files into retro, pixelated audio and create your own chiptune melodies using an interactive keyboard synthesizer.

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🎵 MP3 to 8-Bit Converter
- **Instant Conversion**: Upload any MP3, WAV, or audio file and watch it transform into a retro 8-bit masterpiece
- **Authentic Sound**: Uses square wave synthesis, bit-depth reduction, and sample rate downsampling for genuine chiptune character
- **Customizable Settings**: Adjust sample rates (11025Hz to 44100Hz) for different levels of "retro-ness"
- **Multiple Effects**: Automatic envelope shaping, dynamic range compression, and high-pass filtering

### 🎹 Interactive Keyboard Synthesizer
- **Real-time Playback**: 30+ keys mapped to musical notes across three octaves
- **Multiple Waveforms**: Choose from Square (classic), Triangle (soft), or Pulse (sharp) waves
- **Recording Capability**: Record your melodies and play them back
- **Export功能**: Save your compositions as WAV files
- **Visual Keyboard Layout**: On-screen guide shows note mappings

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (required for audio file conversion)

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
```
