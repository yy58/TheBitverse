"""
Enhanced Visualizer for Chiptune Music
Creates visually appealing patterns based on audio features
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import threading
import time
import random
import colorsys
import math
import librosa

class EnhancedVisualizer:
    """Advanced visualization window for chiptune music"""
    
    def __init__(self, title="Enhanced Audio Visualizer", width=800, height=600):
        """Initialize the enhanced visualizer with the specified dimensions"""
        # Create window
        self.root = tk.Toplevel()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg="black")
        
        # Setup canvas
        self.canvas = tk.Canvas(self.root, bg="black", width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Visualization state
        self.running = False
        self.paused = False
        self.audio_data = None
        self.sr = 44100  # Default sample rate
        self.vis_mode = 0  # Default visualization mode
        self.color_offset = 0.0  # For color cycling
        self.start_time = time.time()  # For timing animations
        
        # Remove control panel - we don't need it anymore
        # self.control_frame = tk.Frame(self.root, bg="#111111", height=40)
        # self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial draw
        self.draw_welcome()
    
    def set_mode(self, mode):
        """Change visualization mode"""
        self.vis_mode = mode
        self.patterns = []  # Reset patterns for new mode
    
    def draw_welcome(self):
        """Draw welcome screen"""
        self.canvas.delete("all")
        
        # Background
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width < 10:  # Not yet fully initialized
            width, height = 880, 680
        
        # Create pixel grid background
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                color = "#{:02x}{:02x}{:02x}".format(
                    random.randint(0, 40),
                    random.randint(0, 40),
                    random.randint(0, 40)
                )
                self.canvas.create_rectangle(x, y, x+18, y+18, fill=color, outline="")
        
        # Title
        self.canvas.create_text(
            width/2, height/3,
            text="TheBitverse",
            font=("Courier", 48, "bold"),
            fill="#00ffff"
        )
        
        # Subtitle
        self.canvas.create_text(
            width/2, height/3 + 60,
            text="Enhanced Music Visualizer",
            font=("Courier", 24),
            fill="#ff00ff"
        )
        
        # Instructions
        self.canvas.create_text(
            width/2, height/2 + 50,
            text="Music visualization will appear when audio plays",
            font=("Courier", 14),
            fill="#ffffff"
        )
        
        # Pixel art decorations
        self.draw_pixel_decoration(width/4, height*0.7, "#00ff00")
        self.draw_pixel_decoration(width*3/4, height*0.7, "#ff00ff")
    
    def draw_pixel_decoration(self, x, y, color):
        """Draw pixel art decoration"""
        size = 8
        for i in range(5):
            for j in range(5):
                if random.random() > 0.3:
                    self.canvas.create_rectangle(
                        x + i*size - 12, 
                        y + j*size - 12, 
                        x + i*size + size - 12, 
                        y + j*size + size - 12, 
                        fill=color, 
                        outline=""
                    )
    
    def visualize_audio(self, audio_data, sr):
        """Start visualization with audio data"""
        self.audio_data = audio_data
        self.sr = sr
        self.running = True
        self.patterns = []  # Reset patterns
        
        # Start visualization thread
        threading.Thread(target=self._run_visualization, daemon=True).start()
    
    def _run_visualization(self):
        """Run visualization loop"""
        # Analyze audio in chunks
        frame_size = int(self.sr * 0.1)  # 0.1 second chunks
        total_frames = len(self.audio_data) // frame_size
        
        # Begin drawing loop
        for i in range(total_frames):
            if not self.running:
                break
                
            if self.paused:
                time.sleep(0.1)
                continue
                
            # Get current audio chunk
            frame = self.audio_data[i*frame_size:(i+1)*frame_size]
            if len(frame) == 0:
                continue
                
            # Extract features for this frame
            features = self._extract_features(frame)
            
            # Draw the visualization
            self.root.after(0, lambda f=features: self._draw_frame(f))
            
            # Control timing
            time.sleep(0.09)  # Slightly faster than real-time for smooth visuals
    
    def _extract_features(self, frame):
        """Extract audio features from frame"""
        # Basic features
        rms = np.sqrt(np.mean(frame**2)) * 10
        
        # Handle potential errors in feature extraction
        try:
            # Spectral features
            spec = np.abs(librosa.stft(frame))
            if spec.size > 0:
                centroid = np.mean(librosa.feature.spectral_centroid(S=spec)[0])
                flatness = np.mean(librosa.feature.spectral_flatness(S=spec)[0])
                
                # Extract frequency data for waveform visualization
                n_fft = 1024
                hop_length = 512
                S = np.abs(librosa.stft(frame, n_fft=n_fft, hop_length=hop_length))
                
                # Get frequency bands (reduce size for performance)
                self.frequency_data = np.mean(S, axis=1)
                if len(self.frequency_data) > 128:
                    # Resample to 128 bands for visualization
                    indices = np.linspace(0, len(self.frequency_data) - 1, 128).astype(int)
                    self.frequency_data = self.frequency_data[indices]
                
                # Normalize
                if np.max(self.frequency_data) > 0:
                    self.frequency_data = self.frequency_data / np.max(self.frequency_data)
            else:
                centroid = 1000
                flatness = 0.1
                
            # Zero crossing rate (simplify for speed)
            zcr = np.mean(librosa.feature.zero_crossing_rate(frame))
            
            # Detect beats (simplified)
            onset_env = librosa.onset.onset_strength(y=frame, sr=self.sr)
            is_beat = np.mean(onset_env) > 0.2
            
            # Add some randomization for variety
            jitter = random.random() * 0.2
            
            # Output features
            return {
                'rms': rms, 
                'centroid': centroid,
                'flatness': flatness,
                'zcr': zcr,
                'is_beat': is_beat,
                'jitter': jitter,
                'frequency_data': self.frequency_data
            }
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            # Return fallback values
            return {
                'rms': 0.5,
                'centroid': 1000,
                'flatness': 0.1,
                'zcr': 0.1,
                'is_beat': False,
                'jitter': 0.1,
                'frequency_data': np.ones(64) * 0.1  # Fallback frequency data
            }
    
    def _generate_smoother_waveform(self, frame):
        """Generate a smoother, more realistic waveform for visualization"""
        try:
            # Get raw waveform data
            num_points = 500
            
            # For smoother appearance, interpolate the waveform
            import numpy as np
            
            # Normalize the frame
            if len(frame) > 0:
                max_val = np.max(np.abs(frame))
                if max_val > 0:
                    frame = frame / max_val
            
            # If frame is too large, resample
            if len(frame) > num_points:
                indices = np.linspace(0, len(frame)-1, num_points).astype(int)
                waveform = frame[indices]
            elif len(frame) < num_points:
                # Interpolate to desired size
                x_original = np.linspace(0, 1, len(frame))
                x_new = np.linspace(0, 1, num_points)
                waveform = np.interp(x_new, x_original, frame)
            else:
                waveform = frame.copy()
            
            # Ensure in 0-1 range for visualization
            waveform = (waveform + 1) / 2
            
            return waveform.tolist()
            
        except Exception as e:
            print(f"Error generating smooth waveform: {e}")
            return [0.5] * 300
    
    def _draw_frame(self, features):
        """Draw a visualization frame - kaomoji art only"""
        if not self.running:
            return
        
        # Check if canvas still exists to prevent errors after closing
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Get canvas dimensions
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width < 10:  # Not yet fully initialized
                width, height = 880, 680
        except Exception:
            # Canvas has been destroyed or is unavailable
            self.running = False
            return
        
        # Update color cycling
        self.color_offset = (self.color_offset + 0.005) % 1.0
        
        # Always use kaomoji visualization
        self._draw_ascii_art_animation(width, height, features)
    
    def _draw_pixel_waves(self, width, height, features):
        """Draw pixel-based waveform visualization"""
        # Extract relevant features
        amplitude = features['rms'] * 3
        frequency = features['centroid'] / 2000
        zcr = features['zcr'] * 10
        is_beat = features['is_beat']
        
        # Generate colors
        hue1 = (self.color_offset) % 1.0
        hue2 = (self.color_offset + 0.3) % 1.0
        r1, g1, b1 = [int(c * 255) for c in colorsys.hsv_to_rgb(hue1, 0.8, 1.0)]
        r2, g2, b2 = [int(c * 255) for c in colorsys.hsv_to_rgb(hue2, 0.8, 1.0)]
        color1 = f"#{r1:02x}{g1:02x}{b1:02x}"
        color2 = f"#{r2:02x}{g2:02x}{b2:02x}"
        
        # Create pixel grid background
        pixel_size = max(4, min(12, int(8 + amplitude * 4)))
        grid_width = width // pixel_size + 1
        grid_height = height // pixel_size + 1
        
        # Draw pixel grid with wave pattern
        for x in range(grid_width):
            for y in range(grid_height):
                # Create wave pattern
                wave_val = math.sin(x * 0.1 * frequency + self.color_offset * 10) * math.cos(y * 0.1 * zcr)
                if abs(wave_val) > 0.7 - amplitude * 0.5:
                    # Wave crest - bright color
                    pixel_color = color1 if wave_val > 0 else color2
                    fill_alpha = min(255, int(200 + abs(wave_val) * 55))
                else:
                    # Wave trough - dark background
                    r = int(r1 * 0.2)
                    g = int(g1 * 0.2)
                    b = int(b1 * 0.2)
                    pixel_color = f"#{r:02x}{g:02x}{b:02x}"
                    fill_alpha = 150
                
                # Add jitter on beats
                offset_x = offset_y = 0
                if is_beat:
                    offset_x = random.randint(-2, 2)
                    offset_y = random.randint(-2, 2)
                
                # Draw pixel
                self.canvas.create_rectangle(
                    x * pixel_size + offset_x, 
                    y * pixel_size + offset_y,
                    (x+1) * pixel_size + offset_x - 1, 
                    (y+1) * pixel_size + offset_y - 1,
                    fill=pixel_color,
                    outline=""
                )
    
    def _draw_fractal_tunnel(self, width, height, features):
        """Draw fractal tunnel visualization"""
        # Extract features
        amplitude = features['rms'] * 3
        complexity = features['flatness'] * 10
        is_beat = features['is_beat']
        
        # Center coordinates
        center_x = width / 2
        center_y = height / 2
        
        # Create a new pattern on beat
        if is_beat and time.time() - self.last_beat_time > 0.2:
            self.last_beat_time = time.time()
            # Add new fractal shape
            shape = {
                'size': 10,
                'angle': random.random() * 2 * math.pi,
                'sides': random.randint(3, 8),
                'hue': (self.color_offset + random.random() * 0.2) % 1.0
            }
            self.patterns.append(shape)
        
        # Limit number of patterns
        while len(self.patterns) > 20:
            self.patterns.pop(0)
        
        # Draw patterns
        for shape in self.patterns:
            # Update size
            shape['size'] += 5 + amplitude * 10
            shape['angle'] += 0.02 * complexity
            
            # Calculate vertices
            vertices = []
            for i in range(shape['sides']):
                angle = shape['angle'] + (2 * math.pi * i / shape['sides'])
                x = int(center_x + shape['size'] * math.cos(angle))
                y = int(center_y + shape['size'] * math.sin(angle))
                vertices.append(x)
                vertices.append(y)
            
            # Generate color
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(shape['hue'], 0.7, 0.8)]
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw polygon
            if len(vertices) >= 6:  # Need at least 3 points (6 coordinates)
                self.canvas.create_polygon(vertices, fill="", outline=color, width=2)
    
    def _draw_audio_particles(self, width, height, features):
        """Draw particle-based visualization"""
        # Extract features
        amplitude = features['rms'] * 3
        zcr = features['zcr'] * 10
        is_beat = features['is_beat']
        
        # Background
        self.canvas.create_rectangle(0, 0, width, height, fill="black", outline="")
        
        # Create new particles on beats
        if is_beat or len(self.patterns) < 50:
            # New particle burst
            num_new = random.randint(5, 15)
            for _ in range(num_new):
                particle = {
                    'x': width / 2,
                    'y': height / 2,
                    'vx': (random.random() - 0.5) * 10 * amplitude,
                    'vy': (random.random() - 0.5) * 10 * amplitude,
                    'size': random.randint(3, 12),
                    'life': 1.0,
                    'hue': (self.color_offset + random.random() * 0.3) % 1.0
                }
                self.patterns.append(particle)
        
        # Update and draw particles
        remaining_particles = []
        for p in self.patterns:
            # Update position
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.01 + 0.02 * zcr
            
            # Skip if off-screen or dead
            if p['life'] <= 0 or p['x'] < 0 or p['y'] < 0 or p['x'] > width or p['y'] > height:
                continue
                
            # Draw particle
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(p['hue'], 0.8, p['life'])]
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            size = p['size'] * p['life']
            self.canvas.create_rectangle(
                int(p['x'] - size/2), 
                int(p['y'] - size/2),
                int(p['x'] + size/2), 
                int(p['y'] + size/2),
                fill=color, 
                outline=""
            )
            
            # Keep alive particles
            remaining_particles.append(p)
        
        # Update particle list
        self.patterns = remaining_particles
    
    def _draw_spectrum_grid(self, width, height, features):
        """Draw spectrum grid visualization"""
        # Extract features
        amplitude = features['rms'] * 3
        centroid = features['centroid'] / 5000
        is_beat = features['is_beat']
        
        # Grid settings
        grid_cols = 16
        grid_rows = 12
        cell_width = width / grid_cols
        cell_height = height / grid_rows
        
        # Generate base hue from color offset
        base_hue = self.color_offset
        
        # Draw grid cells
        for col in range(grid_cols):
            for row in range(grid_rows):
                # Calculate cell position
                x = col * cell_width
                y = row * cell_height
                
                # Calculate cell value (based on position and audio features)
                cell_val = (
                    math.sin(col * 0.2 + self.color_offset * 10) * 
                    math.cos(row * 0.2 + amplitude * 5) * 
                    (0.5 + amplitude * 0.5)
                )
                
                # Determine cell brightness
                brightness = 0.3 + abs(cell_val) * 0.7
                
                # Calculate hue variation
                hue_offset = ((col / grid_cols) * 0.2 + (row / grid_rows) * 0.2) % 1.0
                hue = (base_hue + hue_offset) % 1.0
                
                # Convert to RGB
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, brightness)]
                cell_color = f"#{r:02x}{g:02x}{b:02x}"
                
                # Cell size variation based on audio
                size_factor = 0.85 + abs(cell_val) * 0.15
                if is_beat and random.random() > 0.7:
                    size_factor = 1.0  # Full size on beats
                
                # Calculate actual cell dimensions
                cell_w = cell_width * size_factor
                cell_h = cell_height * size_factor
                x_offset = (cell_width - cell_w) / 2
                y_offset = (cell_height - cell_h) / 2
                
                # Draw cell
                self.canvas.create_rectangle(
                    x + x_offset, 
                    y + y_offset,
                    x + x_offset + cell_w, 
                    y + y_offset + cell_h,
                    fill=cell_color,
                    outline="#000000",
                    width=1
                )
                
    def _draw_gradient_background(self, width, height, color1, color2, vertical=True):
        """Draw a gradient background"""
        # Convert hex colors to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Number of gradient steps
        steps = 100
        
        # Draw gradient rectangles
        for i in range(steps):
            # Calculate position and dimensions
            if vertical:
                x1, y1 = 0, int(i * height / steps)
                x2, y2 = width, int((i + 1) * height / steps)
            else:
                x1, y1 = int(i * width / steps), 0
                x2, y2 = int((i + 1) * width / steps), height
                
            # Calculate color for this step
            r = int(r1 + (r2 - r1) * i / steps)
            g = int(g1 + (g2 - g1) * i / steps)
            b = int(b1 + (b2 - b1) * i / steps)
            
            # Create color string
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw rectangle
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    
    def _draw_oscilloscope_grid(self, width, height):
        """Draw a professional oscilloscope grid"""
        # Horizontal major grid lines
        center_y = height / 2
        
        # Draw center line bolder
        self.canvas.create_line(
            0, int(center_y), width, int(center_y), 
            fill="#005500", width=2
        )
        
        # Draw horizontal grid lines
        for i in range(1, 6):
            # Lines above and below center
            offset = int(height * i / 10)
            
            # Major lines
            self.canvas.create_line(
                0, int(center_y - offset), width, int(center_y - offset),
                fill="#003300", width=1, dash=(3, 3)
            )
            self.canvas.create_line(
                0, int(center_y + offset), width, int(center_y + offset),
                fill="#003300", width=1, dash=(3, 3)
            )
            
        # Vertical grid lines - more divisions for time scale
        for i in range(0, width, int(width/20)):
            # Thicker lines for main divisions
            if i % (int(width/5)) == 0:
                self.canvas.create_line(
                    i, 0, i, height,
                    fill="#004400", width=1, dash=(3, 3)
                )
            else:
                self.canvas.create_line(
                    i, 0, i, height,
                    fill="#002200", width=1, dash=(1, 5)
                )
        
        # Add labels - voltage scale
        for i in range(-5, 6, 5):
            if i == 0:
                continue  # Skip center as we'll label it separately
                
            y = int(center_y - (i * height / 10))
            self.canvas.create_text(
                20, y, 
                text=f"{i/10:.1f}v", 
                fill="#00bb00", 
                font=("Courier", 8),
                anchor="w"
            )
        
        # Center label
        self.canvas.create_text(
            20, int(center_y - 10), 
            text="0.0v", 
            fill="#00ff00", 
            font=("Courier", 8, "bold"),
            anchor="w"
        )
        
        # Time labels at bottom
        for i in range(0, 6):
            x = int(i * width / 5)
            self.canvas.create_text(
                x, height - 10,
                text=f"{i*5}ms",
                fill="#00bb00",
                font=("Courier", 8)
            )
            
    def _draw_beat_indicators(self, width, height, color):
        """Draw beat indicators using animated ASCII art"""
        import random
        import math
        
        # Time-based animation
        timestamp = time.time()
        
        # ASCII symbol options for beat indicators
        beat_symbols = ["⚡", "✨", "★", "☆", "✺", "✸", "✹", "✷", "✶", "✵", "✴", "✳", "✲", "✱", "✯", "✮"]
        
        # Select random symbols for each corner
        symbol1 = random.choice(beat_symbols)
        symbol2 = random.choice(beat_symbols)
        symbol3 = random.choice(beat_symbols)
        symbol4 = random.choice(beat_symbols)
        
        # Create animated pulsing effect
        pulse = abs(math.sin(timestamp * 10)) * 0.5 + 0.5
        size_base = 18
        size = int(size_base + size_base * pulse * 0.5)
        
        # Calculate colors with subtle animation
        r = int(230 + 25 * math.sin(timestamp * 5))
        g = int(150 + 30 * math.sin(timestamp * 3))
        b = int(50 + 30 * math.sin(timestamp * 7))
        animated_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Draw animated beat indicators at corners
        self.canvas.create_text(
            20, 20,
            text=symbol1,
            fill=animated_color,
            font=("Arial", size),
            anchor="center"
        )
        
        self.canvas.create_text(
            width-20, 20,
            text=symbol2,
            fill=animated_color,
            font=("Arial", size),
            anchor="center"
        )
        
        self.canvas.create_text(
            20, height-20,
            text=symbol3,
            fill=animated_color,
            font=("Arial", size),
            anchor="center"
        )
        
        self.canvas.create_text(
            width-20, height-20,
            text=symbol4,
            fill=animated_color,
            font=("Arial", size),
            anchor="center"
        )
    
    def _draw_level_meter(self, width, height, amplitude):
        """Draw a VU meter style level indicator"""
        # Side meter parameters
        meter_width = 15
        meter_height = height * 0.8
        meter_x = width - meter_width - 10
        meter_y = height * 0.1
        
        # Draw meter background
        self.canvas.create_rectangle(
            int(meter_x), int(meter_y), 
            int(meter_x + meter_width), int(meter_y + meter_height),
            fill="#111111",
            outline="#333333"
        )
        
        # Calculate level based on amplitude (clamp between 0-1)
        level = min(1.0, max(0.0, amplitude * 1.2))
        level_height = meter_height * level
        
        # Determine color based on level
        if level > 0.8:
            meter_color = "#ff0000"  # Red for high levels
        elif level > 0.6:
            meter_color = "#ffff00"  # Yellow for medium levels
        else:
            meter_color = "#00ff00"  # Green for low levels
        
        # Draw the level indicator
        self.canvas.create_rectangle(
            int(meter_x), int(meter_y + meter_height - level_height),
            int(meter_x + meter_width), int(meter_y + meter_height),
            fill=meter_color,
            outline=""
        )
        
        # Add level markings
        for i in range(0, 11, 2):
            mark_y = int(meter_y + meter_height * (1 - i/10))
            mark_width = int(meter_width / 2) if i % 4 == 0 else int(meter_width / 4)
            
            self.canvas.create_line(
                int(meter_x), mark_y,
                int(meter_x + mark_width), mark_y,
                fill="#555555",
                width=1
            )
            
            if i % 4 == 0:
                self.canvas.create_text(
                    int(meter_x + meter_width + 5), mark_y,
                    text=f"{i*10}%",
                    fill="#aaaaaa",
                    font=("Courier", 7),
                    anchor="w"
                )
    
    def _draw_ascii_art_animation(self, width, height, features):
        """Draw animated ASCII art visualization with kaomoji patterns like the screenshot"""
        import math
        import random
        import colorsys
        
        # Extract features for ASCII generation
        amplitude = features['rms'] * 8
        centroid = features.get('centroid', 2000) / 5000
        is_beat = features.get('is_beat', False)
        
        # Background - plain black
        self.canvas.create_rectangle(0, 0, width, height, fill="#000000", outline="")
        
        # Character sets for background ASCII pattern
        light_chars = ['.', '·', ':', '˙', '˚', '⋅', '+', '×', '*']
        medium_chars = ['=', '+', '*', 'o', 'O', '°', '×', '⊕', '⊙', '◦']
        
        # Enhanced kaomoji collection
        kaomoji = [
            "(^_^)", "(≧◡≦)", "ヽ(・∀・)ﾉ", "(●'◡'●)", "ヾ(≧▽≦*)o", "\\(★ω★)/", "(-_-)", "(￣▽￣)",
            "(づ￣ ³￣)づ", "(｡♥‿♥｡)", "ლ(´ڡ`ლ)", "(╯°□°）╯︵ ┻━┻", "┬─┬ノ( º _ ºノ)",
            "ಠ_ಠ", "¯\\_(ツ)_/¯", "(っ˘̩╭╮˘̩)っ", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "◉_◉", "( ͡° ͜ʖ ͡°)", "(づ｡◕‿‿◕｡)づ",
            "(ノಠ益ಠ)ノ彡", "ʕ•ᴥ•ʔ", "(｡◕‿◕｡)", "(✿◠‿◠)", "(◡‿◡✿)", "(◕‿◕✿)", "(◠﹏◠)"
        ]
        
        # Music symbol characters
        symbol_chars = ["♪", "♫", "♬", "♩", "♭", "♮", "♯", "✧", "✦", "✩", "✪", "✫", "✬", "✭", "✮", "✯", "✰"]
        
        # Time-based animation
        timestamp = time.time()
        animation_speed = 0.5 + amplitude * 2
        
        # Create ASCII grid for background (denser grid)
        cell_size = 12
        grid_width = width // cell_size
        grid_height = height // cell_size
        
        # Draw background ASCII pattern with very small characters
        for y in range(grid_height):
            for x in range(grid_width):
                # More dense background
                if random.random() < 0.5:
                    continue
                
                pos_x = int(x * cell_size)
                pos_y = int(y * cell_size)
                
                # Wave pattern
                wave_val = math.sin(x * 0.2 + y * 0.1 + timestamp * animation_speed) * math.cos(y * 0.1 + x * 0.05 + timestamp * 0.7)
                
                # Choose character - BIGGER sizes for more visible background
                if abs(wave_val) < 0.3:
                    char = random.choice(light_chars)
                    size = int(10 + 2 * amplitude)  # Increased from 6+1 to 10+2
                    # Dark gray for background
                    color = "#555555"  # Slightly brighter
                else:
                    char = random.choice(medium_chars)
                    size = int(12 + 2 * amplitude)  # Increased from 7+1 to 12+2
                    color = "#666666"  # Brighter
                
                # Draw background ASCII
                self.canvas.create_text(
                    int(pos_x + cell_size/2),
                    int(pos_y + cell_size/2),
                    text=char,
                    fill=color,
                    font=("Courier New", size),
                    anchor="center"
                )
        
        # Add colorful music symbols - more symbols for richer effect
        # Show more symbols, distributed nicely
        if amplitude > 0.2 or is_beat:
            num_symbols = int(15 + amplitude * 25) if is_beat else int(8 + amplitude * 12)
            for i in range(num_symbols):
                # Position using wave equations
                x = int(width * (0.5 + 0.45 * math.sin(timestamp * (0.5 + i * 0.03) + i * 0.2)))
                y = int(height * (0.5 + 0.45 * math.cos(timestamp * (0.3 + i * 0.025) + i * 0.3)))
                
                # Ensure within bounds
                x = max(10, min(width - 10, x))
                y = max(10, min(height - 10, y))
                
                # Select symbol
                symbol = random.choice(symbol_chars)
                
                # Varied sizes for visual interest
                size = random.choice([12, 14, 16])
                
                # Vibrant colors like in the screenshot - fix color calculation
                hue = (timestamp * 0.2 + i / max(1, num_symbols)) % 1.0
                sat = 0.92 + 0.08 * math.sin(timestamp + i)
                val = 0.92 + 0.08 * amplitude
                r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                r = max(0, min(255, int(r * 255)))
                g = max(0, min(255, int(g * 255)))
                b = max(0, min(255, int(b * 255)))
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                # Draw with glow on beat
                if is_beat and random.random() < 0.4:
                    glow_size = 12  # Fixed glow size
                    glow_r = max(0, min(255, r // 2))
                    glow_g = max(0, min(255, g // 2))
                    glow_b = max(0, min(255, b // 2))
                    self.canvas.create_text(
                        x, y,
                        text=symbol,
                        fill=f"#{glow_r:02x}{glow_g:02x}{glow_b:02x}",
                        font=("Arial", glow_size),
                        anchor="center"
                    )
                
                self.canvas.create_text(
                    x, y,
                    text=symbol,
                    fill=color,
                    font=("Arial", size),
                    anchor="center"
                )
        
        # Add colorful kaomoji - dense but staggered layout
        # Create a grid-like pattern with randomness for "dense but orderly" effect
        cell_size_x = 60  # Horizontal spacing
        cell_size_y = 50  # Vertical spacing
        grid_cols = (width // cell_size_x) + 1
        grid_rows = (height // cell_size_y) + 1
        
        # Calculate how many kaomoji to show based on audio
        show_percentage = 0.4 + (amplitude * 0.4)  # 40% to 80% of grid filled
        if is_beat:
            show_percentage = min(0.9, show_percentage + 0.2)  # Up to 90% on beat
        
        for row in range(grid_rows):
            for col in range(grid_cols):
                # Random chance to show kaomoji in this cell
                if random.random() > show_percentage:
                    continue
                
                # Base position with random offset for "错落有致"
                base_x = col * cell_size_x
                base_y = row * cell_size_y
                
                # Add random offset within cell
                offset_x = random.randint(-15, 15)
                offset_y = random.randint(-15, 15)
                
                x = base_x + offset_x
                y = base_y + offset_y
                
                # Keep within bounds
                if x < 10 or x > width - 10 or y < 10 or y > height - 10:
                    continue
                
                face = random.choice(kaomoji)
                
                # Varied sizes for depth - slightly bigger
                size_variation = random.choice([14, 16, 18, 20])
                face_size = size_variation
                
                # Very vibrant colors with variation
                hue = (timestamp * 0.15 + col / grid_cols + row / grid_rows + random.random() * 0.1) % 1.0
                sat = 0.85 + random.random() * 0.15
                val = 0.85 + random.random() * 0.15
                r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
                r = max(0, min(255, int(r * 255)))
                g = max(0, min(255, int(g * 255)))
                b = max(0, min(255, int(b * 255)))
                face_color = f"#{r:02x}{g:02x}{b:02x}"
                
                self.canvas.create_text(
                    x, y,
                    text=face,
                    fill=face_color,
                    font=("Arial", face_size),
                    anchor="center"
                )
        
        # Add central pulsing effect - bigger and more prominent
        if is_beat or amplitude > 0.4:
            center_x = int(width / 2)
            center_y = int(height / 2)
            
            # Show rotating colorful symbols in center
            num_center_symbols = 5 if is_beat else 3
            for i in range(num_center_symbols):
                angle = (timestamp * 2 + i * (2 * math.pi / num_center_symbols)) % (2 * math.pi)
                radius = 60 + 20 * math.sin(timestamp * 3)  # Not affected by amplitude
                x = center_x + int(radius * math.cos(angle))
                y = center_y + int(radius * math.sin(angle))
                
                symbol = random.choice(symbol_chars)
                size = random.choice([16, 18, 20])  # Varied larger sizes
                
                hue = (timestamp * 0.3 + i / num_center_symbols) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.95, 0.98)
                r = max(0, min(255, int(r * 255)))
                g = max(0, min(255, int(g * 255)))
                b = max(0, min(255, int(b * 255)))
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                # Add glow effect
                glow_size = 14  # Fixed glow size
                glow_r = max(0, min(255, r // 3))
                glow_g = max(0, min(255, g // 3))
                glow_b = max(0, min(255, b // 3))
                self.canvas.create_text(
                    x, y,
                    text=symbol,
                    fill=f"#{glow_r:02x}{glow_g:02x}{glow_b:02x}",
                    font=("Arial", glow_size),
                    anchor="center"
                )
                
                self.canvas.create_text(
                    x, y,
                    text=symbol,
                    fill=color,
                    font=("Arial", size),
                    anchor="center"
                )
    
    def _draw_frequency_wave(self, width, height, features):
        """Draw pure kaomoji art animation - no waveforms"""
        # Background - plain black
        self.canvas.create_rectangle(0, 0, width, height, fill="#000000", outline="")
        
        # Only kaomoji art animation
        self._draw_ascii_art_animation(width, height, features)
    
    def _draw_mixed_visualization(self, width, height, features):
        """Kaomoji art only"""
        self._draw_ascii_art_animation(width, height, features)
    
    def stop(self):
        """Stop visualization"""
        self.running = False
        # Cancel any pending after callbacks to prevent errors
        if hasattr(self, 'after_id') and self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
    
    def pause(self):
        """Pause visualization"""
        self.paused = not self.paused
    
    def on_closing(self):
        """Handle window close"""
        self.stop()
        try:
            # Try to destroy the window properly
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
            self.root.destroy()
        except Exception:
            # Already destroyed or not available
            pass


if __name__ == "__main__":
    # Simple test
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    visualizer = EnhancedVisualizer()
    
    # Generate fake audio for testing
    duration = 10  # seconds
    sr = 22050
    t = np.linspace(0, duration, int(duration * sr))
    audio = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 880 * t)
    
    visualizer.visualize_audio(audio, sr)
    
    root.mainloop()