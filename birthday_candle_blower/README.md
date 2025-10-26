# Birthday Candle Blower 🎂

A creative coding project that uses face recognition to detect pout gestures and blow out candles on a 16-bit ASCII style birthday cake.

## Features

- **Face Detection**: Real-time face tracking using OpenCV
- **Pout/Blow Gesture Recognition**: Detects when you purse your lips to blow
- **16-bit ASCII Aesthetic**: Retro-style cake with animated flame effects
- **ASCII Camera Filter**: Toggle-able ASCII art filter for full retro experience
- **Dancing ASCII Cats**: Cute white ASCII cats dance around the screen when you win
- **Victory Music**: Birthday song plays when all candles are blown out
- **Interactive Gameplay**: Blow out all 5 candles to win
- **Visual Feedback**: Dynamic UI with color-coded status indicators and progress bar
- **Smart Cat Distribution**: Cats appear evenly distributed across the screen, avoiding the center area

## Installation

1. Make sure you have Python 3.8+ installed

2. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Position your face in front of the camera

3. Make a pout gesture (purse your lips like you're blowing out candles) to blow out the candles one by one

4. Blow out all 5 candles to win!

## Controls

- **Pout gesture**: Blow out candles
- **R**: Restart game (stops music and resets all candles)
- **A**: Toggle ASCII filter (ON/OFF)
- **Q**: Quit

## Gameplay Tips

- **ASCII Filter**: The game starts with ASCII filter ON for a retro look. If you find the camera view too blurry, press **A** to toggle it off for a clearer view.
- **Pout Detection**: Purse your lips in a small, circular shape (not a wide smile) to blow out candles
- **Progress Bar**: Watch the progress bar at the bottom to see how close you are to blowing out the next candle
- **Victory**: When all candles are blown out, enjoy the dancing ASCII cats and birthday music!

## Technical Details

### Face Recognition
- Uses Haar Cascade classifiers for face and mouth detection
- Analyzes mouth characteristics: area ratio, aspect ratio, width, and position
- Distinguishes between pout gestures and smiles
- Tracks gesture consistency over 15 frames (needs 6 pout frames) to avoid false positives
- Face detection works even with ASCII filter enabled

### Visual Style
- 16-bit retro aesthetic with scanline effects
- Optional ASCII camera filter with 120x160 resolution
- ASCII-style decorations and flame animations
- Larger cake design (400px wide) for better visibility
- Color scheme: Orange flames, yellow candles, pink cake, green UI text
- White dancing ASCII cats with 2-frame animation
- Victory screen with thin bottom UI strip design

### Game Mechanics
- 5 candles to blow out sequentially
- 1280x720 HD camera resolution
- Cooldown system (30 frames) prevents accidental multiple blows
- Progress bar shows blow detection progress
- Victory music playback (searches for happybirthdaysong.mp3, birthday.mp3, etc.)
- Restart function stops music and resets all game states
- 8 dancing cats distributed evenly across screen in victory state

## Troubleshooting

**Camera not detected:**
- Make sure your webcam is connected and not being used by another application
- Grant camera permissions if prompted

**Face detection not working:**
- Ensure good lighting conditions
- Face the camera directly
- Keep your face within the camera frame

**Pout gesture not recognized:**
- Purse your lips into a small, circular shape (like blowing out a candle)
- Avoid wide smiles - they will not be detected as pouts
- Hold the gesture steady for 1-2 seconds
- Try adjusting the distance from the camera
- Check that your mouth is in the lower part of your face (keep chin down slightly)

**Camera view too blurry:**
- Press **A** to toggle off the ASCII filter for a clearer view
- The filter is purely visual - face detection works with it on or off

**Music not playing:**
- Make sure you have a music file named `happybirthdaysong.mp3` or `birthday.mp3` in the project folder
- Check that pygame is properly installed: `pip install pygame`

## Requirements

- Python 3.8+
- OpenCV 4.8.0+
- NumPy 1.24.0+
- Pygame 2.5.0+
- Webcam (HD resolution recommended)

## Project Structure

```
birthday_candle_blower/
├── main.py                    # Main game code with CandleBlower class
├── requirements.txt           # Python dependencies
├── happybirthdaysong.mp3     # Victory music (user-provided)
└── README.md                 # This file
```

## Key Features Explained

### ASCII Filter
The game includes a real-time ASCII art filter that converts your camera feed into ASCII characters (` .:-=+*#%@`). The filter creates a retro 16-bit aesthetic while maintaining face detection functionality. Toggle it on/off with the **A** key.

### Smart Pout Detection
The detection algorithm analyzes multiple mouth characteristics:
- Mouth area ratio (must be small, <6% of face area)
- Aspect ratio (should be circular, not horizontally stretched)
- Width constraint (must be narrow, <40% of face width)
- Position verification (must be in lower portion of face)

This prevents false positives from smiles or other facial expressions.

### Victory Animation
When you blow out all candles:
- Birthday music starts playing automatically
- "HAPPY BIRTHDAY!" message displays in the center
