"""
8-Bit Chiptune Music Converter - GUI Application
Complete GUI with MP3 conversion, interactive keyboard, and enhanced visualizations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
import threading
import os
import time
import numpy as np
from chiptune_converter import ChiptuneConverter
from keyboard_synth import ChiptuneKeyboard
from enhanced_visualizer import EnhancedVisualizer


class ChiptuneApp:
    """Main GUI application for 8-bit chiptune converter"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("� The Bitverse - 8-Bit Chiptune Converter")
        self.root.geometry("980x800")  # Increased width for better fit
        self.root.resizable(True, True)  # Allow window resizing
        self.font_family = "Megamax Jonathan Too"
        
        # Initialize components
        self.converter = ChiptuneConverter(sample_rate=22050)
        self.keyboard = ChiptuneKeyboard(sample_rate=22050, volume=0.3)
        self.visualizer = None  # Will be initialized when needed
        
        # State variables
        self.input_file = None
        self.is_recording = False
        self.is_loop_recording = False
        self.wave_type = tk.StringVar(value="square")
        self.pressed_keys = set()  # Initialize before creating widgets
        
        # Voice recorder state
        self.is_voice_recording = False
        self.voice_recording_data = []
        self.voice_sample_rate = 44100
        self.recorded_voice_file = None
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        # Apply global font family to all widgets
        self.apply_global_font(self.font_family)
        
        # Bind keyboard events (piano-style)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
    def setup_styles(self):
        """Setup custom styles for retro look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors - retro 8-bit palette
        bg_color = "#2d2d2d"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        self.root.configure(bg=bg_color)

        # Base font for ttk widgets (overridden later by apply_global_font for all)
        try:
            style.configure('.', font=(self.font_family, 10))
            style.configure('TNotebook.Tab', font=(self.font_family, 10, 'bold'))
            style.configure('TButton', font=(self.font_family, 11, 'bold'))
            style.configure('TLabel', font=(self.font_family, 10))
        except Exception:
            # Safe ignore if font not available yet; will be handled in apply_global_font
            pass

    def apply_global_font(self, family: str):
        """Apply a global font family to all widgets and ttk styles, preserving sizes/styles.

        - If the requested font isn't installed, fall back to 'Courier New'.
        - Updates Tk named fonts (TkDefaultFont, etc.) and walks the widget tree to update explicit fonts.
        """
        try:
            available = set(tkfont.families(self.root))
        except Exception:
            available = set()

        if family not in available:
            fallback = 'Courier New'
            print(f"[Font] '{family}' not found on this system. Falling back to '{fallback}'.")
            family_to_use = fallback
        else:
            family_to_use = family

        # Update standard Tk named fonts so any widget using them inherits the family
        for name in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont", "TkFixedFont", "TkTooltipFont"):
            try:
                tkfont.nametofont(name).configure(family=family_to_use)
            except tk.TclError:
                pass

        # Update ttk base styles (tabs, labels, buttons, etc.)
        style = ttk.Style()
        try:
            style.configure('.', font=(family_to_use, 10))
            style.configure('TNotebook.Tab', font=(family_to_use, 10, 'bold'))
            style.configure('TButton', font=(family_to_use, 11, 'bold'))
            style.configure('TLabel', font=(family_to_use, 10))
            style.configure('TRadiobutton', font=(family_to_use, 10))
        except Exception:
            pass

        # Walk through all widgets and replace explicit fonts while keeping size/weight
        self._applied_fonts = []

        def _apply(widget: tk.Widget):
            try:
                if 'font' in widget.keys():
                    try:
                        current = tkfont.Font(root=self.root, font=widget['font'])
                        new_font = tkfont.Font(
                            root=self.root,
                            family=family_to_use,
                            size=current.cget('size'),
                            weight=current.cget('weight'),
                            slant=current.cget('slant'),
                            underline=current.cget('underline'),
                            overstrike=current.cget('overstrike'),
                        )
                        widget.configure(font=new_font)
                        # Keep a reference to prevent garbage collection
                        self._applied_fonts.append(new_font)
                    except Exception:
                        pass
            except Exception:
                pass
            for child in widget.winfo_children():
                _apply(child)

        _apply(self.root)
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2d2d2d")
        title_frame.pack(pady=20)
        
        title = tk.Label(
            title_frame,
            text="🎮 THE CHIPTUNE CONVERTER 🎮",
            font=("Courier", 28, "bold"),
            fg="#00ff00",
            bg="#2d2d2d"
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="8-Bit Chiptune Music Converter",
            font=("Courier", 12),
            fg="#00ffff",
            bg="#2d2d2d"
        )
        subtitle.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Tab 1: Keyboard Synthesizer
        keyboard_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(keyboard_frame, text="� Keyboard Synth")
        self.create_keyboard_tab(keyboard_frame)
        
        # Tab 2: MP3 Converter
        converter_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(converter_frame, text="🎵 MP3 Converter")
        self.create_converter_tab(converter_frame)
        
        # Tab 3: Voice Recorder
        recorder_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(recorder_frame, text="🎤 Voice to 8-bit")
        self.create_recorder_tab(recorder_frame)
        
    def create_converter_tab(self, parent):
        """Create the MP3 converter tab with integrated visualization"""
        # Create main layout: left side (controls) + right side (visualization)
        main_container = tk.Frame(parent, bg="#2d2d2d")
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - Controls (30% width)
        left_panel = tk.Frame(main_container, bg="#2d2d2d", width=300)
        left_panel.pack(side=tk.LEFT, fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)  # Maintain width
        
        # Right side - Visualization (70% width)
        right_panel = tk.Frame(main_container, bg="#000000")
        right_panel.pack(side=tk.LEFT, fill='both', expand=True)
        
        # === LEFT PANEL: CONTROLS ===
        
        # Instructions
        instructions = tk.Label(
            left_panel,
            text="8-Bit Converter",
            font=("Courier", 14, "bold"),
            fg="#ffff00",
            bg="#2d2d2d"
        )
        instructions.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(left_panel, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        file_frame.pack(pady=10, fill='x')
        
        tk.Label(
            file_frame,
            text="File:",
            font=("Courier", 9, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file",
            font=("Courier", 8),
            fg="#ffffff",
            bg="#1a1a1a",
            wraplength=250
        )
        self.file_label.pack(pady=3)
        
        # Browse button
        browse_btn = tk.Button(
            file_frame,
            text="📁 Browse",
            font=("Courier", 9, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            command=self.browse_file,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        browse_btn.pack(pady=5)
        
        # Conversion settings
        settings_frame = tk.Frame(left_panel, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        settings_frame.pack(pady=10, fill='x')
        
        tk.Label(
            settings_frame,
            text="Settings",
            font=("Courier", 9, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # Sample rate - 改用grid布局防止被挤出
        rate_frame = tk.Frame(settings_frame, bg="#1a1a1a")
        rate_frame.pack(pady=5, fill='x')
        
        tk.Label(
            rate_frame,
            text="Sample Rate:",
            font=("Courier", 9, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).pack(pady=2)
        
        self.sample_rate_var = tk.StringVar(value="22050")
        sample_rates = ["11025", "22050", "44100"]
        
        # 创建单独的frame用于radio buttons
        rate_buttons_frame = tk.Frame(rate_frame, bg="#1a1a1a")
        rate_buttons_frame.pack()
        
        for rate in sample_rates:
            tk.Radiobutton(
                rate_buttons_frame,
                text=f"{rate} Hz",
                variable=self.sample_rate_var,
                value=rate,
                font=("Courier", 9),
                fg="#ffff00",
                bg="#1a1a1a",
                selectcolor="#2d2d2d",
                activebackground="#1a1a1a",
                activeforeground="#ffff00"
            ).pack(anchor='w', padx=20)
        
        # Convert button
        self.convert_btn = tk.Button(
            left_panel,
            text="🎮 CONVERT!",
            font=("Courier", 11, "bold"),
            fg="#ffffff",
            bg="#ff00ff",
            command=self.convert_file,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=10,
            cursor="hand2"
        )
        self.convert_btn.pack(pady=15)
        
        # Playback controls
        playback_frame = tk.Frame(left_panel, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        playback_frame.pack(pady=10, fill='x')
        
        tk.Label(
            playback_frame,
            text="Playback",
            font=("Courier", 9, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # Store audio playback state
        self.is_playing = False
        self.is_paused = False
        self.converted_file = None
        
        # Play/Pause button (single button that toggles)
        self.play_pause_btn = tk.Button(
            playback_frame,
            text="▶️ Play / ⏸️ Pause",
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#00aa00",
            command=self.toggle_playback,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.play_pause_btn.pack(pady=10)
        
        # Progress/Status
        self.status_label = tk.Label(
            left_panel,
            text="Ready",
            font=("Courier", 8),
            fg="#00ffff",
            bg="#2d2d2d",
            wraplength=250
        )
        self.status_label.pack(pady=10)
        
        # === RIGHT PANEL: VISUALIZATION ===
        
        # Create canvas for kaomoji visualization
        self.vis_canvas = tk.Canvas(
            right_panel,
            bg="#000000",
            highlightthickness=0
        )
        self.vis_canvas.pack(fill='both', expand=True)
        
        # Welcome message
        self.vis_canvas.create_text(
            400, 300,
            text="🎵 TheBitverse Visualizer 🎵\n\nConvert a file to see the magic!",
            font=("Courier", 16, "bold"),
            fill="#00ffff",
            justify=tk.CENTER
        )
        
        # Initialize visualization variables
        self.vis_running = False
        self.vis_audio_data = None
        self.vis_sr = None
        
    def create_recorder_tab(self, parent):
        """Create the voice recorder tab for recording and converting voice to 8-bit"""
        # Main container
        main_container = tk.Frame(parent, bg="#2d2d2d")
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_container,
            text="🎤 Voice to 8-bit Converter",
            font=("Courier", 16, "bold"),
            fg="#ff00ff",
            bg="#2d2d2d"
        )
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            main_container,
            text="Record your voice or any sound through microphone,\nthen convert it to authentic 8-bit audio!",
            font=("Courier", 10),
            fg="#00ffff",
            bg="#2d2d2d",
            justify=tk.CENTER
        )
        instructions.pack(pady=10)
        
        # Recording controls frame
        controls_frame = tk.Frame(main_container, bg="#1a1a1a", relief=tk.RIDGE, bd=3)
        controls_frame.pack(pady=20, padx=20, fill='x')
        
        # Status display
        self.voice_status_label = tk.Label(
            controls_frame,
            text="Ready to record",
            font=("Courier", 12, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        self.voice_status_label.pack(pady=15)
        
        # Recording time label
        self.voice_time_label = tk.Label(
            controls_frame,
            text="Duration: 0.0s",
            font=("Courier", 10),
            fg="#ffff00",
            bg="#1a1a1a"
        )
        self.voice_time_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg="#1a1a1a")
        buttons_frame.pack(pady=15)
        
        # Record button
        self.voice_record_btn = tk.Button(
            buttons_frame,
            text="🔴 START RECORDING",
            font=("Courier", 12, "bold"),
            fg="#ffffff",
            bg="#ff0000",
            command=self.toggle_voice_recording,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.voice_record_btn.grid(row=0, column=0, padx=10, pady=5)
        
        # Playback original button
        self.voice_play_btn = tk.Button(
            buttons_frame,
            text="▶️ PLAY ORIGINAL",
            font=("Courier", 12, "bold"),
            fg="#ffffff",
            bg="#1a1a1a",
            command=self.play_original_voice,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.voice_play_btn.grid(row=0, column=1, padx=10, pady=5)
        
        # Sample rate selection
        rate_frame = tk.Frame(controls_frame, bg="#1a1a1a")
        rate_frame.pack(pady=10)
        
        tk.Label(
            rate_frame,
            text="8-bit Sample Rate:",
            font=("Courier", 10, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        self.voice_sample_rate_var = tk.StringVar(value="22050")
        
        rate_buttons_frame = tk.Frame(rate_frame, bg="#1a1a1a")
        rate_buttons_frame.pack()
        
        for rate in ["11025", "22050", "44100"]:
            tk.Radiobutton(
                rate_buttons_frame,
                text=f"{rate} Hz",
                variable=self.voice_sample_rate_var,
                value=rate,
                font=("Courier", 9),
                fg="#ffff00",
                bg="#1a1a1a",
                selectcolor="#2d2d2d",
                activebackground="#1a1a1a",
                activeforeground="#ffff00"
            ).pack(anchor='w', padx=20)
        
        # Convert button
        self.voice_convert_btn = tk.Button(
            controls_frame,
            text="🎮 CONVERT TO 8-BIT!",
            font=("Courier", 13, "bold"),
            fg="#ffffff",
            bg="#ff00ff",
            command=self.convert_voice_to_8bit,
            relief=tk.RAISED,
            bd=4,
            padx=25,
            pady=12,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.voice_convert_btn.pack(pady=15)
        
        # Play converted button
        self.voice_play_converted_btn = tk.Button(
            controls_frame,
            text="▶️ PLAY 8-BIT VERSION",
            font=("Courier", 12, "bold"),
            fg="#ffffff",
            bg="#00aa00",
            command=self.play_converted_voice,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.voice_play_converted_btn.pack(pady=10)
        
        # Save button
        self.voice_save_btn = tk.Button(
            controls_frame,
            text="💾 SAVE 8-BIT AUDIO",
            font=("Courier", 11, "bold"),
            fg="#ffff00",
            bg="#1a1a1a",
            command=self.save_converted_voice,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.voice_save_btn.pack(pady=10)
        
    def create_keyboard_tab(self, parent):
        """Create the keyboard synthesizer tab"""
        # Instructions
        instructions = tk.Label(
            parent,
            text="Play notes using your keyboard! Press keys to create chiptune music.",
            font=("Courier", 11),
            fg="#ffff00",
            bg="#2d2d2d"
        )
        instructions.pack(pady=20)
        
        # Top controls section - consolidated horizontally
        top_controls_frame = tk.Frame(parent, bg="#2d2d2d")
        top_controls_frame.pack(pady=5, padx=20, fill='x')
        
        # Create two side-by-side frames
        left_controls = tk.Frame(top_controls_frame, bg="#2d2d2d")
        left_controls.grid(row=0, column=0, padx=10, sticky="n")
        
        right_controls = tk.Frame(top_controls_frame, bg="#2d2d2d")
        right_controls.grid(row=0, column=1, padx=10, sticky="n")
        
        # Left side: Recording controls
        record_frame = tk.Frame(left_controls, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        record_frame.pack(pady=5, fill='x', expand=True)
        
        tk.Label(
            record_frame,
            text="🎵 RECORDING & EXPORT 🎵",
            font=("Courier", 10, "bold"),
            fg="#ff00ff",
            bg="#1a1a1a"
        ).pack(pady=3)
        
        # Recording buttons - horizontal row
        buttons_frame = tk.Frame(record_frame, bg="#1a1a1a")
        buttons_frame.pack(pady=5)
        
        self.record_btn = tk.Button(
            buttons_frame,
            text="🔴 REC",
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#ff0000",
            command=self.toggle_recording,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        self.record_btn.grid(row=0, column=0, padx=2)
        
        playback_btn = tk.Button(
            buttons_frame,
            text="▶️ PLAY",
            font=("Courier", 9, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            command=self.playback_recording,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        playback_btn.grid(row=0, column=1, padx=2)
        
        export_wav_btn = tk.Button(
            buttons_frame,
            text="💾 WAV",
            font=("Courier", 9, "bold"),
            fg="#ffff00",
            bg="#1a1a1a",
            command=self.export_recording_wav,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        export_wav_btn.grid(row=0, column=2, padx=2)
        
        export_midi_btn = tk.Button(
            buttons_frame,
            text="🎹 MIDI",
            font=("Courier", 9, "bold"),
            fg="#ff00ff",
            bg="#1a1a1a",
            command=self.export_recording_midi,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        export_midi_btn.grid(row=0, column=3, padx=2)
        
        # Right side: Loop controls and wave selection
        loop_wave_frame = tk.Frame(right_controls, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        loop_wave_frame.pack(pady=5, fill='x', expand=True)
        
        # Loop controls - horizontal
        loop_buttons_frame = tk.Frame(loop_wave_frame, bg="#1a1a1a")
        loop_buttons_frame.pack(pady=3)
        
        tk.Label(
            loop_buttons_frame,
            text="🔄 LOOP:",
            font=("Courier", 9, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).grid(row=0, column=0, padx=2)
        
        self.loop_record_btn = tk.Button(
            loop_buttons_frame,
            text="🔄 REC",
            font=("Courier", 9, "bold"),
            fg="#ffffff",
            bg="#0000ff",
            command=self.toggle_loop_recording,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        self.loop_record_btn.grid(row=0, column=1, padx=2)
        
        self.loop_play_btn = tk.Button(
            loop_buttons_frame,
            text="🔁 PLAY",
            font=("Courier", 9, "bold"),
            fg="#00ffff",
            bg="#1a1a1a",
            command=self.play_loop,
            relief=tk.RAISED,
            bd=2,
            padx=5,
            pady=3
        )
        self.loop_play_btn.grid(row=0, column=2, padx=2)
        
        # Wave type selection - horizontal
        wave_buttons_frame = tk.Frame(loop_wave_frame, bg="#1a1a1a")
        wave_buttons_frame.pack(pady=3)
        
        tk.Label(
            wave_buttons_frame,
            text="WAVE:",
            font=("Courier", 9, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).grid(row=0, column=0, padx=2)
        
        waves = [("Square", "square"), ("Triangle", "triangle"), ("Pulse", "pulse")]
        
        for i, (text, value) in enumerate(waves):
            tk.Radiobutton(
                wave_buttons_frame,
                text=text,
                variable=self.wave_type,
                value=value,
                font=("Courier", 9),
                fg="#00ff00",
                bg="#1a1a1a",
                selectcolor="#2d2d2d",
                activebackground="#1a1a1a",
                activeforeground="#00ff00"
            ).grid(row=0, column=i+1, padx=5)
        
        # Status indicator - centered below both controls
        self.recording_status = tk.Label(
            top_controls_frame,
            text="Press keys to play notes or start recording",
            font=("Courier", 9),
            fg="#ffffff",
            bg="#2d2d2d"
        )
        self.recording_status.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Keyboard layout display as a compact bar
        keyboard_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        keyboard_frame.pack(pady=5, padx=20, fill='x')
        
        # Create a horizontal layout with two rows side by side
        layout_container = tk.Frame(keyboard_frame, bg="#1a1a1a")
        layout_container.pack(pady=5)
        
        # Left side
        tk.Label(
            layout_container,
            text="🎹 LOW: ",
            font=("Courier", 10, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).grid(row=0, column=0, sticky="w", padx=2)
        
        # Low octave mapping
        tk.Label(
            layout_container,
            text="V=C3 F=D3 D=E3 S=F3 A=G3 T=A3 R=B3 E=C4 W=D4 Q=E4",
            font=("Courier", 10),
            fg="#00ffff",
            bg="#1a1a1a",
            justify=tk.LEFT
        ).grid(row=0, column=1, sticky="w", padx=2)
        
        # Right side
        tk.Label(
            layout_container,
            text="🎹 HIGH: ",
            font=("Courier", 10, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).grid(row=0, column=2, sticky="w", padx=(15, 2))
        
        # High octave mapping
        tk.Label(
            layout_container,
            text="B=F4 H=G4 J=A4 K=B4 L=C5 Y=D5 U=E5 I=F5 O=G5 P=A5",
            font=("Courier", 10),
            fg="#00ffff",
            bg="#1a1a1a",
            justify=tk.LEFT
        ).grid(row=0, column=3, sticky="w", padx=2)
        
        # ASCII Piano Visual Display - Made more prominent
        ascii_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=3)  # Increased border thickness
        ascii_frame.pack(pady=10, padx=20, fill='both', expand=True)  # Make it fill and expand
        
        # Title bar with gradient background
        title_bar = tk.Frame(ascii_frame, bg="#1a1a1a", height=30)
        title_bar.pack(fill='x', pady=0)
        
        tk.Label(
            title_bar,
            text="🎹 LIVE KEYBOARD DISPLAY 🎹",
            font=("Courier", 14, "bold"),  # Increased font size
            fg="#ff00ff",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # Main display container
        display_container = tk.Frame(ascii_frame, bg="#1a1a1a")
        display_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # ASCII keyboard display with monospace font
        # Increased height for more visibility
        self.ascii_display = tk.Text(
            display_container,
            width=58,
            height=16,  # Increased height
            font=("Courier", 14),  # Increased font size
            fg="#00ff00",
            bg="#000000",
            padx=10,
            pady=10,
            wrap=tk.NONE
        )
        self.ascii_display.insert(tk.END, self.get_ascii_keyboard())
        self.ascii_display.config(state=tk.DISABLED)
        self.ascii_display.pack(pady=5, fill='both', expand=True)
        
        # Controls bar at bottom
        controls_bar = tk.Frame(ascii_frame, bg="#1a1a1a")
        controls_bar.pack(fill='x', pady=5, padx=10)
        
        # Enhanced visualization button for keyboard - moved to side
        enhanced_keyboard_btn = tk.Button(
            controls_bar,
            text="🎮 SHOW ENHANCED VISUALIZER 🎮",
            font=("Courier", 11, "bold"),
            fg="#ffffff",
            bg="#ff00ff",
            activebackground="#ff00ff",
            activeforeground="#ffffff",
            command=self.show_keyboard_visualizer,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        enhanced_keyboard_btn.pack(pady=5)
        
        # Recording controls
        control_frame = tk.Frame(parent, bg="#2d2d2d")
        control_frame.pack(pady=10)
        
        self.record_btn = tk.Button(
            control_frame,
            text="🔴 START RECORDING",
            font=("Courier", 11, "bold"),
            fg="#ffffff",
            bg="#ff0000",
            activebackground="#ff0000",
            activeforeground="#ffffff",
            command=self.toggle_recording,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.record_btn.grid(row=0, column=0, padx=10)
        
        playback_btn = tk.Button(
            control_frame,
            text="▶️ PLAYBACK",
            font=("Courier", 11, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#00ff00",
            command=self.playback_recording,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        playback_btn.grid(row=0, column=1, padx=10)
        
        export_btn = tk.Button(
            control_frame,
            text="💾 EXPORT WAV",
            font=("Courier", 11, "bold"),
            fg="#ffff00",
            bg="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#ffff00",
            command=self.export_recording_wav,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        export_btn.grid(row=0, column=2, padx=10)
        
        export_midi_btn = tk.Button(
            control_frame,
            text="🎹 EXPORT MIDI",
            font=("Courier", 11, "bold"),
            fg="#ff00ff",
            bg="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#ff00ff",
            command=self.export_recording_midi,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        export_midi_btn.grid(row=0, column=3, padx=10)
        
        # Second row for loop controls
        loop_frame = tk.Frame(parent, bg="#2d2d2d")
        loop_frame.pack(pady=10)
        
        self.loop_record_btn = tk.Button(
            loop_frame,
            text="🔄 START LOOP REC",
            font=("Courier", 11, "bold"),
            fg="#ffffff",
            bg="#0000ff",
            activebackground="#0000ff",
            activeforeground="#ffffff",
            command=self.toggle_loop_recording,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.loop_record_btn.grid(row=0, column=0, padx=10)
        
        self.loop_play_btn = tk.Button(
            loop_frame,
            text="🔁 PLAY LOOP",
            font=("Courier", 11, "bold"),
            fg="#00ffff",
            bg="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#00ffff",
            command=self.play_loop,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.loop_play_btn.grid(row=0, column=1, padx=10)
        
        # Recording status
        self.recording_status = tk.Label(
            parent,
            text="Press any key to play a note!",
            font=("Courier", 10),
            fg="#00ffff",
            bg="#2d2d2d"
        )
        self.recording_status.pack(pady=10)
        
    def browse_file(self):
        """Open file browser to select MP3"""
        print("Opening file dialog...")
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.m4a *.ogg"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        print(f"Selected file: {filename}")
        if filename:
            self.input_file = filename
            print(f"Setting input_file to: {self.input_file}")
            self.file_label.config(text=os.path.basename(filename))
            self.status_label.config(text="File loaded! Ready to convert.")
            print("File label and status updated")
    
    def convert_file(self):
        """Convert the selected file to 8-bit"""
        print(f"Convert button clicked. Input file: {self.input_file}")
        if not self.input_file:
            messagebox.showwarning("No File", "Please select an audio file first!")
            return
        
        # Update converter settings
        sample_rate = int(self.sample_rate_var.get())
        self.converter.sample_rate = sample_rate
        print(f"Starting conversion with sample rate: {sample_rate}")
        
        # Disable button during conversion
        self.convert_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Converting... Please wait...")
        
        # Run conversion in separate thread
        def convert_thread():
            try:
                print("Conversion thread started...")
                output_file = self.converter.convert_file(self.input_file)
                print(f"Conversion complete. Output: {output_file}")
                
                # Update UI on completion
                self.root.after(0, lambda: self.conversion_complete(output_file))
            except Exception as e:
                print(f"Conversion error: {str(e)}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.conversion_error(str(e)))
        
        thread = threading.Thread(target=convert_thread)
        thread.start()
    
    def play_with_enhanced_visual(self, audio_path):
        """
        Play music with enhanced visual effects in a separate window
        """
        import librosa
        import pygame
        import time
        
        try:
            # Load audio for visualization
            y, sr = librosa.load(audio_path, sr=None, mono=True)
            
            # Initialize pygame mixer for audio playback
            try:
                pygame.mixer.quit()  # Ensure clean state
            except:
                pass
            pygame.mixer.init(frequency=sr, size=-16, channels=1, buffer=512)
            
            # Create enhanced visualizer in new window if not already created
            if self.visualizer is None or not hasattr(self.visualizer, 'root'):
                self.visualizer = EnhancedVisualizer(title=f"TheBitverse - {os.path.basename(audio_path)}")
                # Set visualization mode to ASCII art mode with kaomoji
                self.visualizer.vis_mode = 2  # Force ASCII art visualization
            else:
                # Show window if it exists but is hidden
                self.visualizer.show_window()
                # Ensure visualization mode is set correctly
                self.visualizer.vis_mode = 2  # Force ASCII art visualization
            
            # Play audio thread
            def play_audio():
                try:
                    # Load and play the audio file with pygame
                    pygame.mixer.music.load(audio_path)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    
                    # Update status when done
                    self.root.after(0, lambda: self.status_label.config(
                        text="✓ Playback complete!"
                    ))
                except Exception as e:
                    print(f"Playback error: {e}")
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"✗ Playback error: {str(e)}"
                    ))
            
            # Start visualization
            self.visualizer.visualize_audio(y, sr)
            
            # Start audio playback
            threading.Thread(target=play_audio, daemon=True).start()
            
            # Show basic visualization in the main app too
            threading.Thread(target=self.update_text_visual, args=(audio_path,), daemon=True).start()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Visualization Error", f"Could not start visualizer: {str(e)}")
    
    def update_text_visual(self, audio_path):
        """
        Update the text visualization in the main window
        """
        import librosa
        import time
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=None, mono=True)
            frame_size = int(sr * 0.3)  # Larger frames for less frequent updates
            total_frames = len(y) // frame_size
            
            # Update at a slower rate
            for i in range(min(total_frames, 100)):  # Limit number of updates
                frame = y[i*frame_size:(i+1)*frame_size]
                if len(frame) == 0:
                    continue
                    
                # Extract features
                features = self.converter.analyze_frame_features(frame, sr)
                
                # Generate ASCII art
                ascii_art = self.converter.features_to_ascii_art(features, width=60, height=24)
                
                # Update visualization display
                self.visualization_display.config(state=tk.NORMAL)
                self.visualization_display.delete('1.0', tk.END)
                self.visualization_display.insert(tk.END, ascii_art)
                self.visualization_display.config(state=tk.DISABLED)
                self.root.update_idletasks()
                
                # Slower update rate
                time.sleep(0.3)
                
        except Exception as e:
            print(f"Text visualization error: {e}")

    def conversion_complete(self, output_file):
        """Handle successful conversion"""
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✓ Complete!")
        
        # Store converted file
        self.converted_file = output_file
        
        # Enable playback button
        self.play_pause_btn.config(state=tk.NORMAL)
        
        # Load audio for visualization
        try:
            import librosa
            print(f"Loading audio from: {output_file}")
            y, sr = librosa.load(output_file, sr=None, mono=True)
            self.vis_audio_data = y
            self.vis_sr = sr
            print(f"Audio loaded: {len(y)} samples at {sr} Hz")
            
            # 确保visualization标志已设置
            self.vis_running = False  # 先重置
            
            # 启动音乐播放（这会同时启动visualization）
            print("Starting playback with visualization...")
            self.resume_or_start_playback()
            
        except Exception as e:
            print(f"Error loading audio for visualization: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.config(text="✓ Converted (visualization error)")
    
    def toggle_playback(self):
        """Toggle play/pause"""
        if self.is_playing and not self.is_paused:
            self.pause_playback()
        else:
            self.resume_or_start_playback()
    
    def resume_or_start_playback(self):
        """Resume paused playback or start from beginning"""
        if not self.converted_file:
            print("ERROR: No converted file to play")
            return
        
        try:
            import pygame
            
            if self.is_paused:
                # Resume from pause
                print("Resuming from pause...")
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.is_playing = True
                
                # Resume visualization if not running
                if not self.vis_running and self.vis_audio_data is not None:
                    print("Restarting visualization...")
                    self.vis_running = True
                    self.start_visualization()
            else:
                # Start from beginning
                print("Starting playback from beginning...")
                # Initialize pygame mixer
                try:
                    pygame.mixer.quit()
                except:
                    pass
                pygame.mixer.init()
                
                # Load and play
                pygame.mixer.music.load(self.converted_file)
                pygame.mixer.music.play()
                
                self.is_playing = True
                self.is_paused = False
                
                # Start visualization
                print("Starting visualization with playback...")
                if self.vis_audio_data is not None:
                    self.vis_running = True
                    self.start_visualization()
                else:
                    print("WARNING: No visualization data available")
            
            self.play_pause_btn.config(text="⏸️ Pause", bg="#ffaa00")
            self.status_label.config(text="▶️ Playing...")
            
        except Exception as e:
            print(f"Playback error: {e}")
            self.status_label.config(text=f"✗ Playback error")
    
    def pause_playback(self):
        """Pause audio playback and visualization"""
        try:
            import pygame
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
            self.play_pause_btn.config(text="▶️ Play", bg="#00aa00")
            self.status_label.config(text="⏸️ Paused")
            
            # Pause visualization
            self.vis_running = False
            
            # Clear canvas and show paused message
            self.vis_canvas.delete("all")
            width = self.vis_canvas.winfo_width()
            height = self.vis_canvas.winfo_height()
            if width < 10:
                width, height = 800, 600
            
            self.vis_canvas.create_text(
                width//2, height//2,
                text="⏸️ Paused\n\nPress Play to resume",
                font=("Courier", 18, "bold"),
                fill="#ffaa00",
                justify=tk.CENTER
            )
        except Exception as e:
            print(f"Pause error: {e}")
    
    # No longer needed - using pause instead
    # def stop_playback(self):
    #     """Stop audio playback and visualization"""
    #     try:
    #         import pygame
    #         pygame.mixer.music.stop()
    #         self.is_playing = False
    #         self.play_pause_btn.config(text="▶️ Play", bg="#00aa00")
    #         self.status_label.config(text="⏹️ Stopped")
    #         
    #         # Stop visualization
    #         self.vis_running = False
    #         
    #         # Clear canvas and show stopped message
    #         self.vis_canvas.delete("all")
    #         width = self.vis_canvas.winfo_width()
    #         height = self.vis_canvas.winfo_height()
    #         if width < 10:
    #             width, height = 800, 600
    #         
    #         self.vis_canvas.create_text(
    #             width//2, height//2,
    #             text="⏹️ Stopped\n\nPress Play to resume",
    #             font=("Courier", 18, "bold"),
    #             fill="#00ffff",
    #             justify=tk.CENTER
    #         )
    #     except Exception as e:
    #         print(f"Stop error: {e}")
    
    def start_visualization(self):
        """Start kaomoji visualization in canvas"""
        if self.vis_audio_data is None:
            print("ERROR: Cannot start visualization - no audio data")
            return
        
        if self.vis_running:
            print("Visualization already running, stopping old thread...")
            self.vis_running = False
            time.sleep(0.1)  # Give old thread time to stop
        
        print(f"Starting new visualization thread with {len(self.vis_audio_data)} samples")
        self.vis_running = True
        threading.Thread(target=self._run_canvas_visualization, daemon=True).start()
    
    def _run_canvas_visualization(self):
        """Run visualization loop on canvas"""
        import librosa
        import random
        import math
        import colorsys
        
        frame_size = int(self.vis_sr * 0.03)  # 0.03 second chunks (very fast)
        total_frames = len(self.vis_audio_data) // frame_size
        
        # Track centroid history for pitch jump detection
        centroid_history = []
        
        for i in range(total_frames):
            if not self.vis_running:
                break
            
            # Get current audio chunk
            frame = self.vis_audio_data[i*frame_size:(i+1)*frame_size]
            if len(frame) == 0:
                continue
            
            # Extract features
            rms = np.sqrt(np.mean(frame**2)) * 8
            
            try:
                spec = np.abs(librosa.stft(frame))
                if spec.size > 0:
                    centroid = np.mean(librosa.feature.spectral_centroid(S=spec)[0])
                else:
                    centroid = 2000
                    
                onset_env = librosa.onset.onset_strength(y=frame, sr=self.vis_sr)
                is_beat = np.mean(onset_env) > 0.2
            except:
                centroid = 2000
                is_beat = False
            
            # Track centroid history (keep last 10 frames)
            centroid_history.append(centroid)
            if len(centroid_history) > 10:
                centroid_history.pop(0)
            
            # Pattern triggering conditions (降低阈值，更容易触发):
            # 1. High pitch (降低到 >3000 Hz，原来是4000)
            very_high_pitch = centroid > 3000
            
            # 2. Pitch jump (降低到 >800 Hz，原来是1500)
            huge_pitch_jump = False
            if len(centroid_history) >= 2:
                pitch_change = centroid - centroid_history[-2]
                huge_pitch_jump = pitch_change > 800
            
            # 3. Strong beat (降低到 >0.3，原来是0.5)
            strong_beat = is_beat and rms > 0.3
            
            # Trigger pattern on any condition
            pattern_trigger = very_high_pitch or huge_pitch_jump or strong_beat
            
            # Normalize centroid for display (0-1 range)
            centroid_normalized = min(1.0, centroid / 8000)
            
            # High pitch flag for pattern selection (降低到2500)
            high_pitch = centroid > 2500
            
            features = {
                'rms': rms,
                'centroid': centroid,
                'is_beat': is_beat,
                'pattern_trigger': pattern_trigger,
                'high_pitch': high_pitch,
                'centroid_normalized': centroid_normalized
            }
            
            # Draw on canvas
            self.root.after(0, lambda f=features: self._draw_canvas_frame(f))
            
            time.sleep(0.025)  # Very fast frame rate (~40 FPS)
    
    def _draw_canvas_frame(self, features):
        """Draw visualization frame on canvas"""
        if not self.vis_running:
            return
        
        try:
            # 完全清除画布 - 无残影
            self.vis_canvas.delete("all")
            
            # Get canvas dimensions
            width = self.vis_canvas.winfo_width()
            height = self.vis_canvas.winfo_height()
            if width < 10:
                width, height = 800, 600
            
            # Extract features
            amplitude = features['rms']
            is_beat = features.get('is_beat', False)
            pattern_trigger = features.get('pattern_trigger', False)
            high_pitch = features.get('high_pitch', False)
            centroid_normalized = features.get('centroid_normalized', 0.5)
            
            import random
            import math
            import colorsys
            import time
            
            timestamp = time.time()
            
            # Kaomoji collection
            kaomoji = [
                "(^_^)", "(≧◡≦)", "ヽ(・∀・)ﾉ", "(●'◡'●)", "ヾ(≧▽≦*)o", "\\(★ω★)/",
                "(づ￣ ³￣)づ", "(｡♥‿♥｡)", "ლ(´ڡ`ლ)", "(╯°□°）╯︵ ┻━┻",
                "ಠ_ಠ", "¯\\_(ツ)_/¯", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "( ͡° ͜ʖ ͡°)", "ʕ•ᴥ•ʔ"
            ]
            
            # Music symbols
            symbol_chars = ["♪", "♫", "♬", "♩", "✧", "✦", "✩", "✪", "✫", "✬", "✭", "✮", "✯"]
            
            # Background ASCII - make it bigger and more visible
            light_chars = ['.', '·', ':', '+', '×', '*']
            medium_chars = ['=', '+', '*', 'o', 'O', '°']
            
            # Draw background with varying sizes (darker greys)
            cell_size = 12
            for y in range(0, height, cell_size):
                for x in range(0, width, cell_size):
                    if random.random() < 0.5:
                        continue
                    
                    # Vary character and size (darker colors for background)
                    if random.random() < 0.6:
                        char = random.choice(light_chars)
                        size = 12
                        color = "#333333"  # Darker grey
                    else:
                        char = random.choice(medium_chars)
                        size = 14
                        color = "#444444"  # Medium grey
                    
                    self.vis_canvas.create_text(
                        x, y,
                        text=char,
                        fill=color,
                        font=("Courier New", size),
                        anchor="nw"
                    )
            
            # Draw kaomoji - 网格位置 + 抖动效果（形成图案）
            center_x = width // 2
            center_y = height // 2
            
            # 网格设置
            cell_size = 60
            grid_cols = (width // cell_size) + 1
            grid_rows = (height // cell_size) + 1
            
            # 密度基于音乐状态
            if pattern_trigger:
                show_percentage = 0.85  # 触发时密集
            elif is_beat:
                show_percentage = 0.60  # 节拍时中等
            else:
                show_percentage = 0.40  # 正常时稀疏
            
            for row in range(grid_rows):
                for col in range(grid_cols):
                    if random.random() > show_percentage:
                        continue
                    
                    # 基础网格位置
                    base_x = col * cell_size
                    base_y = row * cell_size
                    
                    # 距离中心的距离和角度
                    dx = base_x - center_x
                    dy = base_y - center_y
                    dist = math.sqrt(dx*dx + dy*dy)
                    angle = math.atan2(dy, dx)
                    
                    # 抖动效果 - 基于音乐强度
                    jitter_base = 5 + (amplitude * 10)
                    if is_beat:
                        jitter_amount = jitter_base * 2.0  # 节拍时抖动更大
                    else:
                        jitter_amount = jitter_base
                    
                    if pattern_trigger:
                        # 触发时：向外爆炸
                        explosion_offset = 30 * (1 - min(dist / max(width, height), 1.0))
                        x = base_x + explosion_offset * math.cos(angle)
                        y = base_y + explosion_offset * math.sin(angle)
                        jitter_amount *= 3  # 更大的抖动
                    else:
                        # 正常：在网格位置附近抖动
                        x = base_x
                        y = base_y
                    
                    # 添加抖动
                    jitter_x = random.uniform(-jitter_amount, jitter_amount)
                    jitter_y = random.uniform(-jitter_amount, jitter_amount)
                    
                    x += jitter_x
                    y += jitter_y
                    
                    # Bounds check
                    if x < 10 or x > width - 10 or y < 10 or y > height - 10:
                        continue
                    
                    # 使用网格位置选择kaomoji（保持一致性）
                    kaomoji_index = (row * 7 + col * 13) % len(kaomoji)
                    face = kaomoji[kaomoji_index]
                    
                    # Size varies with beat and amplitude
                    base_size = 17
                    if pattern_trigger:
                        size = random.randint(20, 26)  # Bigger on trigger
                    elif is_beat:
                        size = random.randint(18, 24)  # Big on beat
                    else:
                        size = random.randint(14, 20)  # Normal range
                    
                    # Monochrome: brightness based on state
                    if pattern_trigger:
                        brightness = random.randint(230, 255)  # Very bright on trigger
                    elif is_beat:
                        brightness = random.randint(200, 230)  # Bright on beat
                    else:
                        brightness = random.randint(150, 190)  # Medium grey normally
                    
                    color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
                    
                    self.vis_canvas.create_text(
                        x, y,
                        text=face,
                        fill=color,
                        font=("Arial", size),
                        anchor="center"
                    )
            
            # Draw music symbols - 随机生成多种图案
            if amplitude > 0.15 or is_beat or pattern_trigger:
                # 音符数量基于音乐强度
                if pattern_trigger:
                    num_symbols = int(40 + amplitude * 30)
                elif is_beat:
                    num_symbols = int(25 + amplitude * 20)
                else:
                    num_symbols = int(10 + amplitude * 15)
                
                # 随机选择图案类型（触发时从多种图案中随机选择）
                if pattern_trigger:
                    # 触发时：从8种复杂图案中随机选择
                    pattern_types = ["spiral", "double_spiral", "star", "flower", 
                                   "lissajous", "heart", "infinity", "mandala"]
                    pattern_type = random.choice(pattern_types)
                elif is_beat:
                    # 节拍时：从简单图案中选择
                    pattern_types = ["circle", "square", "triangle", "hexagon"]
                    pattern_type = random.choice(pattern_types)
                else:
                    pattern_type = "scatter"  # 正常：散布
                
                for i in range(num_symbols):
                    if pattern_type == "spiral":
                        # 单螺旋
                        angle = (i / num_symbols) * 4 * math.pi
                        radius = (i / num_symbols) * min(width, height) * 0.4
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                    elif pattern_type == "double_spiral":
                        # 双螺旋
                        angle = (i / num_symbols) * 6 * math.pi
                        radius = (i / num_symbols) * min(width, height) * 0.35
                        offset_angle = math.pi if i % 2 == 0 else 0
                        x = int(center_x + radius * math.cos(angle + offset_angle))
                        y = int(center_y + radius * math.sin(angle + offset_angle))
                        
                    elif pattern_type == "star":
                        # 星形（5角或8角）
                        points = 8
                        angle = (i / num_symbols) * 2 * math.pi
                        # 交替长短半径
                        if (i * points // num_symbols) % 2 == 0:
                            radius = min(width, height) * 0.35
                        else:
                            radius = min(width, height) * 0.15
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                    elif pattern_type == "flower":
                        # 花瓣图案
                        angle = (i / num_symbols) * 2 * math.pi
                        petals = 6
                        radius = min(width, height) * 0.25 * (1 + 0.5 * math.sin(petals * angle))
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                    elif pattern_type == "lissajous":
                        # 利萨如图形
                        t = (i / num_symbols) * 2 * math.pi
                        a, b = 3, 4  # 频率比
                        radius_x = width * 0.3
                        radius_y = height * 0.3
                        x = int(center_x + radius_x * math.sin(a * t))
                        y = int(center_y + radius_y * math.sin(b * t))
                        
                    elif pattern_type == "heart":
                        # 心形
                        t = (i / num_symbols) * 2 * math.pi
                        scale = min(width, height) * 0.15
                        # 心形参数方程
                        x = int(center_x + scale * 16 * math.sin(t)**3)
                        y = int(center_y - scale * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)))
                        
                    elif pattern_type == "infinity":
                        # 无穷符号 (∞)
                        t = (i / num_symbols) * 2 * math.pi
                        scale = min(width, height) * 0.2
                        # 伯努利双纽线
                        x = int(center_x + scale * math.cos(t) / (1 + math.sin(t)**2))
                        y = int(center_y + scale * math.sin(t) * math.cos(t) / (1 + math.sin(t)**2))
                        
                    elif pattern_type == "mandala":
                        # 曼陀罗图案
                        angle = (i / num_symbols) * 2 * math.pi
                        layers = 3
                        layer = i % layers
                        radius = min(width, height) * (0.15 + layer * 0.1)
                        symmetry = 12
                        snap_angle = round(angle * symmetry / (2 * math.pi)) * (2 * math.pi / symmetry)
                        x = int(center_x + radius * math.cos(snap_angle))
                        y = int(center_y + radius * math.sin(snap_angle))
                        
                    elif pattern_type == "circle":
                        # 圆形 - 多个同心圆
                        angle = (i / num_symbols) * 2 * math.pi
                        ring = (i % 3) + 1
                        radius = ring * min(width, height) * 0.15
                        x = int(center_x + radius * math.cos(angle))
                        y = int(center_y + radius * math.sin(angle))
                        
                    elif pattern_type == "square":
                        # 方形
                        side = i % 4
                        progress = (i // 4) / (num_symbols // 4) if num_symbols > 4 else 0
                        size = min(width, height) * 0.3
                        if side == 0:  # 上边
                            x = int(center_x - size + progress * size * 2)
                            y = int(center_y - size)
                        elif side == 1:  # 右边
                            x = int(center_x + size)
                            y = int(center_y - size + progress * size * 2)
                        elif side == 2:  # 下边
                            x = int(center_x + size - progress * size * 2)
                            y = int(center_y + size)
                        else:  # 左边
                            x = int(center_x - size)
                            y = int(center_y + size - progress * size * 2)
                            
                    elif pattern_type == "triangle":
                        # 三角形
                        angle = (i / num_symbols) * 2 * math.pi
                        # 捕捉到最近的三角形顶点
                        snap_angle = round(angle * 3 / (2 * math.pi)) * (2 * math.pi / 3)
                        radius = min(width, height) * 0.3
                        x = int(center_x + radius * math.cos(snap_angle - math.pi/2))
                        y = int(center_y + radius * math.sin(snap_angle - math.pi/2))
                        
                    elif pattern_type == "hexagon":
                        # 六边形
                        angle = (i / num_symbols) * 2 * math.pi
                        snap_angle = round(angle * 6 / (2 * math.pi)) * (2 * math.pi / 6)
                        radius = min(width, height) * 0.3
                        x = int(center_x + radius * math.cos(snap_angle))
                        y = int(center_y + radius * math.sin(snap_angle))
                        angle = (i / num_symbols) * 2 * math.pi
                        # 多个同心圆
                        ring = (i % 3) + 1  # 3个环
                        y = int(center_y + radius * math.sin(snap_angle))
                        
                    else:  # scatter
                        # 散布 - 聚集在中心附近
                        cluster_x = random.gauss(center_x, width * 0.25)
                        cluster_y = random.gauss(center_y, height * 0.25)
                        x = int(max(20, min(width - 20, cluster_x)))
                        y = int(max(20, min(height - 20, cluster_y)))
                    
                    # 边界检查
                    if x < 10 or x > width - 10 or y < 10 or y > height - 10:
                        continue
                    
                    symbol = random.choice(symbol_chars)
                    
                    # 大小根据音调变化
                    if high_pitch:
                        size = random.choice([18, 20, 22])
                    else:
                        size = random.choice([14, 16, 18])
                    
                    # 亮度根据状态
                    if pattern_trigger:
                        color = "#FFFFFF"  # 触发时纯白
                    elif is_beat:
                        color = "#EEEEEE"  # 节拍时很亮
                    else:
                        color = "#CCCCCC"  # 正常时浅灰
                    
                    self.vis_canvas.create_text(
                        x, y,
                        text=symbol,
                        fill=color,
                        font=("Arial", size),
                        anchor="center"
                    )
        
        except Exception as e:
            print(f"Canvas draw error: {e}")
    
    def old_conversion_complete(self, output_file):
        """OLD VERSION - keeping for reference"""
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✓ Conversion complete! Opening enhanced visualization...")
        
        # Get cover.txt path
        base, ext = os.path.splitext(output_file)
        cover_path = f"{base}_cover.txt"
        
        try:
            # If there's a static ASCII cover, display it first in main window
            if os.path.exists(cover_path):
                with open(cover_path, 'r', encoding='utf-8') as f:
                    ascii_art = f.read()
                    self.visualization_display.config(state=tk.NORMAL)
                    self.visualization_display.delete('1.0', tk.END)
                    self.visualization_display.insert(tk.END, ascii_art)
                    self.visualization_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error loading ASCII cover: {e}")
        
        # Play with enhanced visualization in separate window
        audio_path = output_file
        threading.Thread(target=self.play_with_enhanced_visual, args=(audio_path,), daemon=True).start()
        
        # Show success message
        messagebox.showinfo(
            "Success!",
            f"Your 8-bit chiptune is ready!\n\nEnhanced visualization window has opened.\n\nSaved to:\n{output_file}"
        )
    
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="❌ Conversion failed!")
        
        messagebox.showerror(
            "Error",
            f"Conversion failed:\n{error_msg}"
        )
    
    def on_key_press(self, event):
        """Handle key press: play note immediately when pressed and update visualizations."""
        try:
            key = event.char.lower()
            if not key:
                return
            # Prevent retriggering if key is already pressed
            if key in self.pressed_keys:
                return
            if key in self.keyboard.NOTE_FREQUENCIES:
                self.pressed_keys.add(key)
                freq = self.keyboard.NOTE_FREQUENCIES[key]
                wave = self.wave_type.get()
                
                # Play the note
                threading.Thread(target=self.keyboard.play_note, args=(freq, 0.3, wave), daemon=True).start()
                self.recording_status.config(text=f"♪ Played: {key.upper()} ({freq:.2f} Hz) - {wave.capitalize()}")
                
                # Update ASCII keyboard display in main window
                self.update_ascii_display()
                
                # Show visualization for sustained key presses
                if len(self.pressed_keys) >= 3:  # Show visualizer when playing chords
                    self.show_keyboard_visualizer()
        except Exception as e:
            print(f"Key press error: {e}")
            
    def show_keyboard_visualizer(self):
        """Show ASCII art visualizer for keyboard playing"""
        if self.visualizer is None or not hasattr(self.visualizer, 'root'):
            # Create visualizer with kaomoji animation instead of waveforms
            self.visualizer = EnhancedVisualizer(title="TheBitverse - Kaomoji Visualizer", 
                                               width=960, height=640)
            
            # Set visualization mode to ASCII art mode
            self.visualizer.vis_mode = 2  # Force ASCII art visualization
        else:
            # If visualizer exists but hidden, show it
            self.visualizer.show_window()

    def on_key_release(self, event):
        """Handle key release: mark key as released (optional early stop can be added)."""
        try:
            key = event.char.lower()
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
                # Update ASCII keyboard display
                self.update_ascii_display()
        except Exception as e:
            print(f"Key release error: {e}")
    
    def get_ascii_keyboard(self):
        """Generate ASCII art representation of the keyboard."""
        # Define the two rows of keys
        row1_keys = ['v', 'f', 'd', 's', 'a', 't', 'r', 'e', 'w', 'q']
        row2_keys = ['b', 'h', 'j', 'k', 'l', 'y', 'u', 'i', 'o', 'p']
        
        # Build the ASCII keyboard with a more visible design
        lines = []
        lines.append("┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Row 1 - low octave keys with highlighting for pressed keys
        row1_display = "│"
        for key in row1_keys:
            if key in self.pressed_keys:
                row1_display += f" ▓{key.upper()}▓ │"  # Highlight pressed keys
            else:
                row1_display += f"  {key.upper()}  │"
        lines.append(row1_display)
        
        # Row for visual effect when key is pressed - make it flashy
        row1_visual = "│"
        for key in row1_keys:
            if key in self.pressed_keys:
                row1_visual += f" ♪♫♪ │"  # Musical notes when pressed
            else:
                row1_visual += f"     │"
        lines.append(row1_visual)
        
        # Notes row
        lines.append("├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        notes_display = "│"
        for note in ["C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]:
            notes_display += f"  {note}  │"
        lines.append(notes_display)
        lines.append("└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        
        # Add a spacer
        lines.append("")
        
        # High octave keyboard
        lines.append("┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Row 2 - high octave keys
        row2_display = "│"
        for key in row2_keys:
            if key in self.pressed_keys:
                row2_display += f" ▓{key.upper()}▓ │"  # Highlight pressed keys
            else:
                row2_display += f"  {key.upper()}  │"
        lines.append(row2_display)
        
        # Row for visual effect when key is pressed
        row2_visual = "│"
        for key in row2_keys:
            if key in self.pressed_keys:
                row2_visual += f" ♪♫♪ │"  # Musical notes when pressed
            else:
                row2_visual += f"     │"
        lines.append(row2_visual)
        
        # Notes row
        lines.append("├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
        notes_display = "│"
        for note in ["F4","G4","A4","B4","C5","D5","E5","F5","G5","A5"]:
            notes_display += f"  {note}  │"
        lines.append(notes_display)
        lines.append("└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        
        # Add status line if any key is pressed
        if self.pressed_keys:
            pressed_keys = ", ".join(k.upper() for k in self.pressed_keys)
            lines.append("")
            lines.append(f"Playing keys: {pressed_keys}")
        
        return "\n".join(lines)
    
    def update_ascii_display(self):
        """Update the ASCII keyboard display to show currently pressed keys."""
        if hasattr(self, 'ascii_display'):
            # For Text widget, we need to clear and insert the new content
            self.ascii_display.config(state=tk.NORMAL)
            self.ascii_display.delete(1.0, tk.END)
            self.ascii_display.insert(tk.END, self.get_ascii_keyboard())
            self.ascii_display.config(state=tk.DISABLED)
    
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            # Start recording
            self.keyboard.start_recording()
            self.is_recording = True
            self.record_btn.config(
                text="⏹️ STOP RECORDING",
                bg="#00ff00",
                activebackground="#00ff00"
            )
            self.recording_status.config(text="🔴 RECORDING... Play some notes!")
        else:
            # Stop recording
            self.keyboard.stop_recording()
            self.is_recording = False
            self.record_btn.config(
                text="🔴 START RECORDING",
                bg="#ff0000",
                activebackground="#ff0000"
            )
            num_notes = len(self.keyboard.recording)
            self.recording_status.config(
                text=f"⏹️ Recording stopped. Captured {num_notes} notes."
            )
    
    def playback_recording(self):
        """Play back the recorded notes"""
        if not self.keyboard.recording:
            messagebox.showinfo("No Recording", "No notes recorded yet! Record something first.")
            return
        
        self.recording_status.config(text="▶️ Playing back recording...")
        
        # Run playback in separate thread
        def playback_thread():
            self.keyboard.playback_recording()
            self.root.after(0, lambda: self.recording_status.config(
                text="✓ Playback complete!"
            ))
        
        thread = threading.Thread(target=playback_thread)
        thread.start()
    
    def export_recording_wav(self):
        """Export recorded notes to WAV file"""
        if not self.keyboard.recording:
            messagebox.showinfo("No Recording", "No notes recorded yet! Record something first.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Save Recording As WAV",
            defaultextension=".wav",
            filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.keyboard.export_recording_to_wav(filename)
                messagebox.showinfo("Success!", f"Recording exported to WAV:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export WAV:\n{str(e)}")
    
    def export_recording_midi(self):
        """Export recorded notes to MIDI file"""
        if not self.keyboard.recording:
            messagebox.showinfo("No Recording", "No notes recorded yet! Record something first.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Save Recording As MIDI",
            defaultextension=".mid",
            filetypes=[("MIDI Files", "*.mid"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                result = self.keyboard.export_recording_to_midi(filename)
                if result:
                    messagebox.showinfo("Success!", f"Recording exported to MIDI:\n{filename}")
                else:
                    messagebox.showwarning("Warning", "MIDI export failed. Make sure the mido library is installed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export MIDI:\n{str(e)}")
    
    def toggle_loop_recording(self):
        """Toggle loop recording on/off"""
        if not hasattr(self, 'is_loop_recording') or not self.is_loop_recording:
            # Start loop recording
            self.is_loop_recording = True
            self.loop_record_btn.config(text="⏹️ STOP LOOP REC", bg="#ff0000")
            self.recording_status.config(text="🔄 Loop recording started...")
            self.keyboard.start_loop_recording()
        else:
            # Stop loop recording
            self.is_loop_recording = False
            self.loop_record_btn.config(text="🔄 START LOOP REC", bg="#0000ff")
            
            # Stop with 4-second loop duration
            loop_result = self.keyboard.stop_loop_recording(loop_duration=4.0)
            
            if loop_result:
                self.recording_status.config(text=f"✓ Loop recording complete! {len(loop_result)} notes in loop")
            else:
                self.recording_status.config(text="⚠️ Loop recording stopped, but no notes were captured.")
    
    def play_loop(self):
        """Play the recorded loop"""
        if not hasattr(self.keyboard, 'loop_recording') or not self.keyboard.loop_recording:
            messagebox.showinfo("No Loop", "No loop recorded yet! Record a loop first.")
            return
        
        self.recording_status.config(text="🔁 Playing loop...")
        
        # Run loop playback in a separate thread
        def playback_thread():
            self.keyboard.play_loop(times=4)  # Play the loop 4 times
            self.root.after(0, lambda: self.recording_status.config(
                text="✓ Loop playback complete!"
            ))
        
        thread = threading.Thread(target=playback_thread)
        thread.start()
    
    def launch_visualizer(self):
        """Launch the enhanced visualizer with demo animation"""
        try:
            # Initialize visualizer if not exists
            if self.visualizer is None or not hasattr(self.visualizer, 'root'):
                self.visualizer = EnhancedVisualizer(title="TheBitverse - Music Visualizer")
                # Set visualization mode to ASCII art mode with kaomoji
                self.visualizer.vis_mode = 2  # Force ASCII art visualization
            else:
                # Show window if it exists but is hidden
                self.visualizer.show_window()
                # Ensure visualization mode is set correctly
                self.visualizer.vis_mode = 2  # Force ASCII art visualization
            
            # Generate a demo animation if no audio is playing
            import numpy as np
            
            # Create interesting demo waveform combining multiple frequencies
            sr = 12050
            duration = 15  # seconds
            t = np.linspace(0, duration, int(sr * duration))
            
            # Base frequencies for a harmonically pleasing sound
            freqs = [220, 277.18, 329.63, 440, 554.37, 659.26]
            
            # Combine waveforms
            audio = np.zeros_like(t)
            for i, freq in enumerate(freqs):
                # Different waveforms for variety
                if i % 3 == 0:
                    # Square wave
                    wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
                elif i % 3 == 1:
                    # Triangle wave
                    wave = 0.2 * 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
                else:
                    # Pulse wave
                    wave = 0.2 * ((np.sin(2 * np.pi * freq * t) > 0.3).astype(float) * 2 - 1)
                
                # Add amplitude modulation
                am = 0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t + i * 0.5)
                wave = wave * am
                
                # Add to mix
                audio += wave
            
            # Add some random noise bursts
            for i in range(5):
                start = int(sr * i * 3)
                end = start + int(sr * 0.1)
                if end < len(audio):
                    audio[start:end] += np.random.uniform(-0.3, 0.3, end-start)
            
            # Normalize
            if np.abs(audio).max() > 0:
                audio = audio / np.abs(audio).max() * 0.8
            
            # Start visualization
            self.visualizer.visualize_audio(audio, sr)
            
            # Show message
            messagebox.showinfo(
                "Visualizer Launched",
                "Enhanced visualizer window has opened.\n\nTry different visualization modes using the buttons at the bottom!"
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Visualizer Error", f"Could not launch visualizer: {str(e)}")
    
    def on_closing(self):
        """Clean up when closing the application"""
        self.keyboard.close()
        # Close visualizer if it's open
        if self.visualizer is not None and hasattr(self.visualizer, 'root'):
            try:
                self.visualizer.stop()
                self.visualizer.root.destroy()
            except Exception:
                pass
        self.root.destroy()
    
    # Voice Recorder Methods
    def toggle_voice_recording(self):
        """Toggle voice recording on/off"""
        if not self.is_voice_recording:
            self.start_voice_recording()
        else:
            self.stop_voice_recording()
    
    def start_voice_recording(self):
        """Start recording from microphone"""
        try:
            import sounddevice as sd
            
            self.is_voice_recording = True
            self.voice_recording_data = []
            self.recorded_voice_file = None
            
            # Update UI
            self.voice_record_btn.config(text="⏹️ STOP RECORDING", bg="#ff6600")
            self.voice_status_label.config(text="🔴 Recording...", fg="#ff0000")
            self.voice_play_btn.config(state=tk.DISABLED)
            self.voice_convert_btn.config(state=tk.DISABLED)
            self.voice_play_converted_btn.config(state=tk.DISABLED)
            self.voice_save_btn.config(state=tk.DISABLED)
            
            # Start recording in separate thread
            threading.Thread(target=self._record_voice_thread, daemon=True).start()
            
            print("Voice recording started...")
            
        except ImportError:
            messagebox.showerror(
                "Missing Library",
                "sounddevice library is required for recording.\n\nInstall it with:\npip install sounddevice"
            )
            print("ERROR: sounddevice library not found")
        except Exception as e:
            messagebox.showerror("Recording Error", f"Could not start recording:\n{e}")
            print(f"Recording error: {e}")
    
    def _record_voice_thread(self):
        """Recording thread function"""
        import sounddevice as sd
        
        recording_start = time.time()
        
        def callback(indata, frames, time_info, status):
            """This is called for each audio block"""
            if status:
                print(f"Recording status: {status}")
            if self.is_voice_recording:
                self.voice_recording_data.append(indata.copy())
                # Update time display
                duration = time.time() - recording_start
                self.root.after(0, lambda: self.voice_time_label.config(
                    text=f"Duration: {duration:.1f}s"
                ))
        
        try:
            with sd.InputStream(samplerate=self.voice_sample_rate, 
                               channels=1, 
                               callback=callback):
                while self.is_voice_recording:
                    sd.sleep(100)
        except Exception as e:
            print(f"Recording thread error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Recording Error", str(e)))
    
    def stop_voice_recording(self):
        """Stop voice recording"""
        self.is_voice_recording = False
        
        # Process recorded data
        if len(self.voice_recording_data) > 0:
            # Concatenate all chunks
            recording = np.concatenate(self.voice_recording_data, axis=0)
            
            # Convert float32 to int16 for proper WAV format
            # Normalize to [-1, 1] range first
            recording = np.clip(recording, -1.0, 1.0)
            # Convert to 16-bit PCM
            recording_int16 = (recording * 32767).astype(np.int16)
            
            # Save to temporary file
            import scipy.io.wavfile as wavfile
            temp_file = "temp_voice_recording.wav"
            wavfile.write(temp_file, self.voice_sample_rate, recording_int16)
            self.recorded_voice_file = temp_file
            
            duration = len(recording) / self.voice_sample_rate
            
            # Update UI
            self.voice_record_btn.config(text="🔴 START RECORDING", bg="#ff0000")
            self.voice_status_label.config(
                text=f"✓ Recorded {duration:.1f}s", 
                fg="#00ff00"
            )
            self.voice_play_btn.config(state=tk.NORMAL)
            self.voice_convert_btn.config(state=tk.NORMAL)
            
            print(f"Recording stopped. Duration: {duration:.1f}s")
        else:
            self.voice_status_label.config(text="No audio recorded", fg="#ff0000")
            self.voice_record_btn.config(text="🔴 START RECORDING", bg="#ff0000")
    
    def play_original_voice(self):
        """Play the original recorded voice"""
        if not self.recorded_voice_file or not os.path.exists(self.recorded_voice_file):
            messagebox.showwarning("No Recording", "Please record audio first")
            return
        
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(self.recorded_voice_file)
            pygame.mixer.music.play()
            self.voice_status_label.config(text="▶️ Playing original...", fg="#00ffff")
            print("Playing original recording...")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play audio:\n{e}")
            print(f"Playback error: {e}")
    
    def convert_voice_to_8bit(self):
        """Convert recorded voice to 8-bit"""
        if not self.recorded_voice_file or not os.path.exists(self.recorded_voice_file):
            messagebox.showwarning("No Recording", "Please record audio first")
            return
        
        self.voice_status_label.config(text="Converting to 8-bit...", fg="#ffff00")
        self.voice_convert_btn.config(state=tk.DISABLED)
        
        # Run conversion in thread
        threading.Thread(target=self._convert_voice_thread, daemon=True).start()
    
    def _convert_voice_thread(self):
        """Thread for voice conversion"""
        try:
            sample_rate = int(self.voice_sample_rate_var.get())
            self.converter.sample_rate = sample_rate
            
            output_file = "temp_voice_8bit.mp3"
            
            print(f"Converting voice to 8-bit at {sample_rate} Hz...")
            self.converter.convert_file(self.recorded_voice_file, output_file)
            
            self.converted_voice_file = output_file
            
            # Update UI
            self.root.after(0, lambda: self.voice_status_label.config(
                text="✓ Converted to 8-bit!",
                fg="#00ff00"
            ))
            self.root.after(0, lambda: self.voice_convert_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.voice_play_converted_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.voice_save_btn.config(state=tk.NORMAL))
            
            print("Voice conversion complete!")
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("Conversion Error", f"Conversion failed:\n{error_msg}"))
            self.root.after(0, lambda: self.voice_status_label.config(text="❌ Conversion failed", fg="#ff0000"))
            self.root.after(0, lambda: self.voice_convert_btn.config(state=tk.NORMAL))
            print(f"Conversion error: {e}")
            import traceback
            traceback.print_exc()
    
    def play_converted_voice(self):
        """Play the 8-bit converted voice"""
        if not hasattr(self, 'converted_voice_file') or not os.path.exists(self.converted_voice_file):
            messagebox.showwarning("No Conversion", "Please convert audio first")
            return
        
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(self.converted_voice_file)
            pygame.mixer.music.play()
            self.voice_status_label.config(text="▶️ Playing 8-bit version...", fg="#ff00ff")
            print("Playing 8-bit converted audio...")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play audio:\n{e}")
            print(f"Playback error: {e}")
    
    def save_converted_voice(self):
        """Save the 8-bit converted audio"""
        if not hasattr(self, 'converted_voice_file') or not os.path.exists(self.converted_voice_file):
            messagebox.showwarning("No Conversion", "Please convert audio first")
            return
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav"), ("All files", "*.*")],
            title="Save 8-bit Audio"
        )
        
        if save_path:
            try:
                import shutil
                shutil.copy(self.converted_voice_file, save_path)
                self.voice_status_label.config(text="✓ Saved!", fg="#00ff00")
                messagebox.showinfo("Success", f"8-bit audio saved to:\n{save_path}")
                print(f"Saved to: {save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{e}")
                print(f"Save error: {e}")


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = ChiptuneApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    print("Starting GUI...")
    main()
