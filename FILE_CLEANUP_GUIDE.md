# File Cleanup Guide 🗂️

## Which Files Are Necessary?

### ✅ **REQUIRED FILES** - Keep These!

#### In `chiptune converter/` folder:
```
✅ gui_app.py              - Main application (essential)
✅ chiptune_converter.py   - Audio processing engine (essential)
✅ enhanced_visualizer.py  - Visualization system (essential)
✅ requirements.txt        - Python dependencies (essential)
```

#### In root `TheBitverse/` folder:
```
✅ .venv/ or venv/         - Virtual environment (recommended, pick one)
✅ .git/                   - Git version control (if using git)
✅ .gitignore              - Git ignore rules (if using git)
✅ README.md               - Documentation (helpful)
```

---

### ❌ **NOT REQUIRED** - Safe to Delete!

#### Web Files (Python app doesn't use these):
```
❌ index.html              - Web landing page (root)
❌ script.js              - Web JavaScript (root)
❌ style.css              - Web CSS (root)
❌ chiptune converter/index.html - Duplicate web file
❌ chiptune converter/style.css  - Duplicate web file
```

**Why?** The application uses **Tkinter** for GUI, not web technologies. These HTML/CSS/JS files were probably for a web demo or documentation site that's separate from the Python app.

#### Legacy/Duplicate Files:
```
⚠️  keyboard_synth.py     - Old standalone version (now in gui_app.py)
```

**Why?** This functionality is now integrated into `gui_app.py` as the third tab.

#### Temporary Files:
```
🗑️  temp_voice_recording.wav  - Temporary recording
🗑️  temp_voice_8bit.mp3       - Temporary conversion
🗑️  temp_voice_8bit.wav       - Temporary conversion  
🗑️  temp_voice_8bit_cover.txt - Generated ASCII art
🗑️  __pycache__/              - Python bytecode cache
```

**Why?** These are auto-generated during runtime. They'll be recreated when you use the app.

---

## 📋 Cleanup Recommendations

### Option 1: Minimal Clean (Keep Everything Working)
**Delete only temporary files:**
```bash
cd TheBitverse
rm temp_*
rm -rf __pycache__
rm -rf "chiptune converter/__pycache__"
```

### Option 2: Medium Clean (Remove Web Files)
**Delete temp files + web files:**
```bash
cd TheBitverse
rm temp_*
rm index.html script.js style.css
rm "chiptune converter/index.html"
rm "chiptune converter/style.css"
rm -rf __pycache__
rm -rf "chiptune converter/__pycache__"
```

### Option 3: Deep Clean (Keep Only Essentials)
**Keep only what's needed to run the app:**
```bash
cd TheBitverse

# Keep these folders/files:
# - chiptune converter/ (entire folder)
# - .venv/ (or venv/)
# - .git/ and .gitignore (if using git)
# - README.md files

# Delete everything else:
rm temp_*
rm index.html script.js style.css
rm "chiptune converter/index.html"
rm "chiptune converter/style.css"
rm "chiptune converter/keyboard_synth.py"  # Optional if you don't use standalone version
rm -rf __pycache__
rm -rf "chiptune converter/__pycache__"
rm -rf venv/  # If you're using .venv instead
```

---

## 🎯 Final Structure After Cleanup

```
TheBitverse/
├── .git/                          # Git (if using)
├── .gitignore                     # Git (if using)
├── .venv/                         # Virtual environment
├── README.md                      # Main documentation
└── chiptune converter/
    ├── gui_app.py                 # ✅ MAIN APP
    ├── chiptune_converter.py      # ✅ REQUIRED
    ├── enhanced_visualizer.py     # ✅ REQUIRED
    ├── requirements.txt           # ✅ REQUIRED
    └── README.md                  # Documentation
```

---

## ⚡ Quick Test After Cleanup

To verify everything still works:

```bash
cd "TheBitverse/chiptune converter"
source ../.venv/bin/activate  # or: source ../venv/bin/activate
python gui_app.py
```

If the app launches successfully, your cleanup was successful! 🎉

---

## 📝 Notes

- **Don't delete** anything in `.venv/` or `venv/` - that's your Python environment
- **Temporary files** will be recreated automatically when you use recording/conversion features
- **Web files** are completely separate from the Python Tkinter application
- **keyboard_synth.py** can be kept if you want to run it standalone (not necessary for GUI app)
