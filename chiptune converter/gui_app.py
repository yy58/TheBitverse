"""
8-Bit Chiptune Music Converter - GUI Application
Complete GUI with MP3 conversion, interactive keyboard, and enhanced visualizations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
import threading
import os
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
        notebook.add(converter_frame, text="� MP3 Converter")
        self.create_converter_tab(converter_frame)
        
    def create_converter_tab(self, parent):
        """Create the MP3 converter tab"""
        # Instructions
        instructions = tk.Label(
            parent,
            text="A thing that reduces your emotions,\nmemories, or music into nostalgic 8-bit sound\n— because everything feels simpler in pixels.",
            font=("Courier", 16, "bold"),
            fg="#ffff00",
            bg="#2d2d2d",
            wraplength=750,
            justify=tk.CENTER
        )
        instructions.pack(pady=30)
        
        # File selection frame
        file_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        file_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            file_frame,
            text="Selected File:",
            font=("Courier", 10),
            fg="#00ff00",
            bg="#1a1a1a"
        ).pack(pady=10)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1a1a",
            wraplength=600
        )
        self.file_label.pack(pady=5)
        
        # Browse button
        browse_btn = tk.Button(
            file_frame,
            text="📁 Browse MP3 File",
            font=("Courier", 11, "bold"),
            fg="#00ff00",
            bg="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#00ff00",
            command=self.browse_file,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        browse_btn.pack(pady=10)
        
        # Conversion settings
        settings_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            settings_frame,
            text="Conversion Settings",
            font=("Courier", 10, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).pack(pady=10)
        
        # Sample rate
        rate_frame = tk.Frame(settings_frame, bg="#1a1a1a")
        rate_frame.pack(pady=5)
        
        tk.Label(
            rate_frame,
            text="Sample Rate:",
            font=("Courier", 9),
            fg="#ffffff",
            bg="#1a1a1a"
        ).pack(side=tk.LEFT, padx=10)
        
        self.sample_rate_var = tk.StringVar(value="22050")
        sample_rates = ["11025", "22050", "44100"]
        
        for rate in sample_rates:
            tk.Radiobutton(
                rate_frame,
                text=f"{rate} Hz",
                variable=self.sample_rate_var,
                value=rate,
                font=("Courier", 9),
                fg="#00ff00",
                bg="#1a1a1a",
                selectcolor="#2d2d2d",
                activebackground="#1a1a1a",
                activeforeground="#00ff00"
            ).pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_btn = tk.Button(
            parent,
            text="🎮 CONVERT TO 8-BIT! 🎮",
            font=("Courier", 14, "bold"),
            fg="#ffffff",
            bg="#ff00ff",
            activebackground="#ff00ff",
            activeforeground="#ffffff",
            command=self.convert_file,
            relief=tk.RAISED,
            bd=4,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.convert_btn.pack(pady=20)
        
        # Progress/Status
        self.status_label = tk.Label(
            parent,
            text="Ready to convert!",
            font=("Courier", 10),
            fg="#00ffff",
            bg="#2d2d2d"
        )
        self.status_label.pack(pady=10)
        
        # ASCII Visualization frame
        visualization_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        visualization_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            visualization_frame,
            text="🎵 REAL-TIME ASCII VISUALIZATION 🎵",
            font=("Courier", 12, "bold"),
            fg="#ff00ff",
            bg="#1a1a1a"
        ).pack(pady=5)
        
        # ASCII visualization display
        self.visualization_display = tk.Text(
            visualization_frame,
            width=60,
            height=24,
            font=("Courier", 12),
            fg="#00ff00",
            bg="#000000",
            padx=10,
            pady=10,
            wrap=tk.NONE
        )
        self.visualization_display.insert(tk.END, "转换完成后，ASCII视觉效果将在此处显示...")
        self.visualization_display.config(state=tk.DISABLED)
        self.visualization_display.pack(pady=10, fill='both', expand=True)
        
        # Enhanced visualization button
        enhanced_btn = tk.Button(
            visualization_frame,
            text="🎮 LAUNCH ENHANCED VISUALIZER 🎮",
            font=("Courier", 11, "bold"),
            fg="#ffffff",
            bg="#ff00ff",
            activebackground="#ff00ff",
            activeforeground="#ffffff",
            command=self.launch_visualizer,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        enhanced_btn.pack(pady=10)
        
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
        import sounddevice as sd
        import time
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=None, mono=True)
            
            # Create enhanced visualizer in new window if not already created
            if self.visualizer is None or not hasattr(self.visualizer, 'root'):
                self.visualizer = EnhancedVisualizer(title=f"TheBitverse - {os.path.basename(audio_path)}")
            
            # Play audio thread
            def play_audio():
                sd.play(y, sr)
                sd.wait()
                # Update status when done
                self.root.after(0, lambda: self.status_label.config(
                    text="✓ Playback complete!"
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
            self.visualizer = EnhancedVisualizer(title="TheBitverse - Kaomoji Visualizer 颜文字可视化", 
                                               width=960, height=640)
            
            # Set visualization mode to ASCII art mode
            self.visualizer.vis_mode = 2  # Force ASCII art visualization

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
            
            # Generate a demo animation if no audio is playing
            import numpy as np
            
            # Create interesting demo waveform combining multiple frequencies
            sr = 22050
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
                    wave = 0.2 * np.sign(np.sin(2 * np.pi * freq * t))
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


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = ChiptuneApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    print("Starting GUI...")
    main()
