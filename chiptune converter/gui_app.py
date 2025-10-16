"""
8-Bit Chiptune Music Converter - GUI Application
Complete GUI with MP3 conversion and interactive keyboard
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from chiptune_converter import ChiptuneConverter
from keyboard_synth import ChiptuneKeyboard


class ChiptuneApp:
    """Main GUI application for 8-bit chiptune converter"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("🎮 The Bitverse - 8-Bit Chiptune Converter")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Initialize components
        self.converter = ChiptuneConverter(sample_rate=22050)
        self.keyboard = ChiptuneKeyboard(sample_rate=22050, volume=0.3)
        
        # State variables
        self.input_file = None
        self.is_recording = False
        self.wave_type = tk.StringVar(value="square")
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        
        # Bind keyboard events (piano-style)
        self.pressed_keys = set()
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
        
        # Tab 1: MP3 Converter
        converter_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(converter_frame, text="🎵 MP3 Converter")
        self.create_converter_tab(converter_frame)
        
        # Tab 2: Keyboard Synthesizer
        keyboard_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(keyboard_frame, text="🎹 Keyboard Synth")
        self.create_keyboard_tab(keyboard_frame)
        
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
        
        # Wave type selection
        wave_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        wave_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            wave_frame,
            text="Waveform Type:",
            font=("Courier", 10, "bold"),
            fg="#00ffff",
            bg="#1a1a1a"
        ).pack(pady=10)
        
        wave_buttons_frame = tk.Frame(wave_frame, bg="#1a1a1a")
        wave_buttons_frame.pack(pady=5)
        
        waves = [("Square (Classic)", "square"), ("Triangle (Soft)", "triangle"), ("Pulse (Sharp)", "pulse")]
        
        for text, value in waves:
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
            ).pack(anchor=tk.W, padx=20, pady=2)
        
        # Keyboard layout display
        keyboard_frame = tk.Frame(parent, bg="#1a1a1a", relief=tk.RIDGE, bd=2)
        keyboard_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            keyboard_frame,
            text="🎹 KEYBOARD LAYOUT 🎹",
            font=("Courier", 12, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        ).pack(pady=10)
        
        # Create keyboard layout
        layout_text = """
Left Hand (Low Octave):
    V   F   D   S   A   T   R   E   W   Q
    C3  D3  E3  F3  G3  A3  B3  C4  D4  E4

Right Hand (High Octave):
    B   H   J   K   L   Y   U   I   O   P
    F4  G4  A4  B4  C5  D5  E5  F5  G5  A5
                """
        
        layout_label = tk.Label(
            keyboard_frame,
            text=layout_text,
            font=("Courier", 10),
            fg="#00ffff",
            bg="#1a1a1a",
            justify=tk.LEFT
        )
        layout_label.pack(pady=10)
        
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
            command=self.export_recording,
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        export_btn.grid(row=0, column=2, padx=10)
        
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
    
    def conversion_complete(self, output_file):
        """Handle successful conversion"""
        self.convert_btn.config(state=tk.NORMAL)
        self.status_label.config(text="✓ Conversion complete!")
        
        messagebox.showinfo(
            "Success!",
            f"Your 8-bit chiptune is ready!\n\nSaved to:\n{output_file}"
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
        """Handle key press: play note immediately when pressed."""
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
                threading.Thread(target=self.keyboard.play_note, args=(freq,), daemon=True).start()
                self.recording_status.config(text=f"♪ Played: {key.upper()} ({freq:.2f} Hz)")
        except Exception as e:
            print(f"Key press error: {e}")

    def on_key_release(self, event):
        """Handle key release: mark key as released (optional early stop can be added)."""
        try:
            key = event.char.lower()
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except Exception as e:
            print(f"Key release error: {e}")
    
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
    
    def export_recording(self):
        """Export recorded notes to WAV file"""
        if not self.keyboard.recording:
            messagebox.showinfo("No Recording", "No notes recorded yet! Record something first.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Save Recording As",
            defaultextension=".wav",
            filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.keyboard.export_recording_to_wav(filename)
                messagebox.showinfo("Success!", f"Recording exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")
    
    def on_closing(self):
        """Clean up when closing the application"""
        self.keyboard.close()
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
