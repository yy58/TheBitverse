"""
Birthday Candle Blower - 16-bit ASCII Style
Face recognition project that detects pout gesture to blow out candles on a cake
"""

import cv2
import numpy as np
import time
import os
from collections import deque

class CandleBlower:
    def __init__(self):
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Increased from 640
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Increased from 480
        
        # Game state: 'blowing' -> 'victory'
        self.game_state = 'blowing'  # Start directly in blowing mode
        self.candles = [True] * 5  # 5 candles, all lit
        self.pout_history = deque(maxlen=15)  # Track pout detection over time
        self.blow_cooldown = 0
        self.victory_time = None
        self.music_played = False
        
        # Dancing cats for victory animation
        self.cats = []
        self.cat_positions = []
        self.cat_frame = 0
        
        # ASCII filter toggle
        self.ascii_filter_enabled = True  # Toggle with 'A' key
        
        # ASCII art components
        self.colors = {
            'flame': (0, 140, 255),      # Orange
            'candle': (0, 255, 255),     # Yellow
            'cake': (147, 20, 255),      # Pink
            'text': (0, 255, 0),         # Green
            'accent': (255, 0, 255)      # Magenta
        }
        
        # ASCII characters for filter (from dark to bright)
        self.ascii_chars = ' .:-=+*#%@'
        
    def detect_pout(self, frame, face):
        """Detect if person is making a pout/blow gesture"""
        x, y, w, h = face
        roi_gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        
        # Detect mouth region with moderate parameters
        mouths = self.mouth_cascade.detectMultiScale(roi_gray, 1.3, 10, minSize=(25, 20))
        
        # Check mouth characteristics for pout
        is_pouting = False
        if len(mouths) > 0:
            mx, my, mw, mh = mouths[0]
            aspect_ratio = mh / mw if mw > 0 else 0
            mouth_area = mw * mh
            face_area = w * h
            mouth_ratio = mouth_area / face_area
            
            # Position check - mouth should be in lower part of face
            mouth_center_y = my + mh / 2
            relative_position = mouth_center_y / h
            
            # Pout characteristics (stricter):
            # - Small mouth area (not wide smile)
            # - More circular (aspect ratio closer to 1, not wide like smile)
            # - Lower part of face
            # - Exclude wide smiles
            if (mouth_ratio < 0.06 and  # Smaller mouth area (was 0.08)
                0.35 < aspect_ratio < 1.0 and  # More restricted range (was 0.3-1.2)
                relative_position > 0.4 and  # Lower position (was 0.35)
                mw < w * 0.4):  # Narrower mouth (was 0.5)
                is_pouting = True
        
        return is_pouting
    
    def init_dancing_cats(self, width, height):
        """Initialize random positions for dancing cats (avoiding center, evenly distributed)"""
        self.cat_positions = []
        center_x = width // 2
        center_y = height // 2
        center_radius = 200  # Radius to avoid around center
        
        # Divide screen into 8 regions for even distribution
        # 2 rows (top and bottom) × 4 columns
        regions = []
        cols = 4
        rows = 2
        
        margin = 50
        col_width = (width - 2 * margin) // cols
        row_height = (height - 350) // rows  # Avoid cake area (bottom 300px) and top margin
        
        for row in range(rows):
            for col in range(cols):
                region_x = margin + col * col_width
                region_y = 80 + row * row_height  # Start below title
                regions.append((region_x, region_y, col_width, row_height))
        
        # Shuffle regions and place one cat in each
        np.random.shuffle(regions)
        
        for i, (rx, ry, rw, rh) in enumerate(regions[:8]):
            attempts = 0
            while attempts < 20:
                # Random position within this region
                x = rx + np.random.randint(10, rw - 60)
                y = ry + np.random.randint(10, rh - 60)
                
                # Check if position is not in center area
                distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance_from_center > center_radius:
                    phase = np.random.random() * 2 * np.pi
                    self.cat_positions.append({'x': x, 'y': y, 'phase': phase})
                    break
                
                attempts += 1
    
    def apply_ascii_filter(self, frame):
        """Apply ASCII art filter to camera frame"""
        # Higher resolution for clearer image
        small_h, small_w = 120, 160  # Doubled resolution (was 60x80)
        small_frame = cv2.resize(frame, (small_w, small_h))
        
        # Convert to grayscale for ASCII mapping
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        
        # Create ASCII art frame
        ascii_frame = np.zeros_like(frame)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.25  # Smaller font for more detail
        char_width = int(frame.shape[1] / small_w)
        char_height = int(frame.shape[0] / small_h)
        
        for i in range(small_h):
            for j in range(small_w):
                # Get brightness value
                brightness = gray[i, j]
                
                # Map to ASCII character
                char_idx = int(brightness / 255 * (len(self.ascii_chars) - 1))
                char = self.ascii_chars[char_idx]
                
                # Get color from original frame
                color = tuple(int(c) for c in small_frame[i, j])
                
                # Draw character
                x = j * char_width
                y = i * char_height + char_height
                cv2.putText(ascii_frame, char, (x, y), 
                           font, font_scale, color, 1, cv2.LINE_AA)
        
        return ascii_frame
    
    def draw_dancing_cat(self, frame, x, y, frame_idx):
        """Draw an animated ASCII cat"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Cat animations (alternating frames)
        cat_frames = [
            # Frame 0 - arms up
            [
                " /\\_/\\  ",
                "( ^.^ )",
                " > ^ < "
            ],
            # Frame 1 - arms down
            [
                " /\\_/\\  ",
                "( ^.^ )",
                " v   v "
            ]
        ]
        
        cat = cat_frames[frame_idx % 2]
        
        # Draw each line of the cat
        for i, line in enumerate(cat):
            cv2.putText(frame, line, (x, y + i * 20), 
                       font, 0.5, (255, 255, 255), 2)  # White color
    
    def draw_ascii_cake(self, frame):
        """Draw 16-bit ASCII style cake with candles (bigger size)"""
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        
        # Cake position (higher and bigger)
        cake_x = width // 2
        cake_y = height - 250  # Moved up more to fit bigger cake
        
        # Draw candles (more spacing for bigger cake)
        candle_spacing = 80  # Increased from 60
        start_x = cake_x - (len(self.candles) - 1) * candle_spacing // 2
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        for i, lit in enumerate(self.candles):
            x = start_x + i * candle_spacing
            
            if lit:
                # Flame (animated, bigger)
                flame_offset = int(7 * np.sin(time.time() * 10 + i))
                cv2.putText(overlay, "^", (x-12, cake_y - 60 + flame_offset), 
                           font, 2.0, self.colors['flame'], 4)
                cv2.putText(overlay, "*", (x-12, cake_y - 80 + flame_offset), 
                           font, 1.6, self.colors['flame'], 3)
            
            # Candle stick (bigger)
            cv2.rectangle(overlay, (x-8, cake_y-55), (x+8, cake_y-15), 
                         self.colors['candle'], -1)
            cv2.rectangle(overlay, (x-8, cake_y-55), (x+8, cake_y-15), 
                         self.colors['accent'], 3)
        
        # Cake layers (bigger)
        layer_width = 400  # Increased from 280
        layer_height = 45  # Increased from 30
        
        # Top layer
        cv2.rectangle(overlay, 
                     (cake_x - layer_width//2, cake_y - 15),
                     (cake_x + layer_width//2, cake_y + layer_height),
                     self.colors['cake'], -1)
        cv2.rectangle(overlay, 
                     (cake_x - layer_width//2, cake_y - 15),
                     (cake_x + layer_width//2, cake_y + layer_height),
                     self.colors['accent'], 4)
        
        # Bottom layer
        bottom_width = layer_width + 60  # Increased from 40
        cv2.rectangle(overlay, 
                     (cake_x - bottom_width//2, cake_y + layer_height),
                     (cake_x + bottom_width//2, cake_y + layer_height*2),
                     self.colors['cake'], -1)
        cv2.rectangle(overlay, 
                     (cake_x - bottom_width//2, cake_y + layer_height),
                     (cake_x + bottom_width//2, cake_y + layer_height*2),
                     self.colors['accent'], 4)
        
        # ASCII decorations (bigger and more)
        deco_y = cake_y + 20
        for dx in range(-180, 190, 45):  # More decorations
            cv2.putText(overlay, "o", (cake_x + dx, deco_y), 
                       font, 0.8, self.colors['accent'], 3)
        
        # Blend overlay
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
    def draw_ui(self, frame):
        """Draw UI elements based on game state"""
        height, width = frame.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Exit instruction (top right corner, white text)
        exit_text = "Q: Exit | R: Restart | A: ASCII Filter"
        cv2.putText(frame, exit_text, (width - 380, 30), 
                   font, 0.5, (255, 255, 255), 2)  # White color
        
        # ASCII filter status indicator (top left)
        filter_status = f"ASCII Filter: {'ON' if self.ascii_filter_enabled else 'OFF'}"
        filter_color = self.colors['text'] if self.ascii_filter_enabled else (128, 128, 128)
        cv2.putText(frame, filter_status, (20, 30), 
                   font, 0.5, filter_color, 2)
        
        # Title (moved down a bit to avoid overlap)
        title = "=== BIRTHDAY CANDLE BLOWER ==="
        cv2.putText(frame, title, (width//2 - 250, 60), 
                   font, 0.8, self.colors['text'], 2)
        
        if self.game_state == 'blowing':
            # Bottom bar background (thin strip at bottom)
            bar_height = 35
            cv2.rectangle(frame, (0, height - bar_height, width, height),
                         (0, 0, 0), -1)
            
            # Blowing candles phase
            lit_count = sum(self.candles)
            counter = f"Candles lit: {lit_count}/{len(self.candles)}"
            cv2.putText(frame, counter, (20, height - 10), 
                       font, 0.6, self.colors['candle'], 2)
            
            instruction = "Pout to blow!"
            cv2.putText(frame, instruction, (width - 180, height - 10), 
                       font, 0.5, self.colors['text'], 2)
            
            # Show blow progress bar (inline in the bottom bar)
            pout_count = sum(self.pout_history)
            if pout_count > 0:
                bar_width = 120
                bar_x = width // 2 - bar_width // 2
                bar_y = height - 25
                
                # Progress bar
                progress = min(pout_count / 6.0, 1.0)
                cv2.rectangle(frame, (bar_x, bar_y, 
                                     bar_x + int(bar_width * progress), bar_y + 15),
                             self.colors['flame'], -1)
                
                # Border
                cv2.rectangle(frame, (bar_x, bar_y, bar_x + bar_width, bar_y + 15),
                             (255, 255, 255), 2)
                
                cv2.putText(frame, f"{int(progress*100)}%", 
                           (bar_x + bar_width + 10, bar_y + 12),
                           font, 0.4, self.colors['flame'], 1)
        
        elif self.game_state == 'victory':
            # Bottom bar background (thin strip at bottom)
            bar_height = 35
            cv2.rectangle(frame, (0, height - bar_height, width, height),
                         (0, 0, 0), -1)
            
            # Victory message in center
            victory = "HAPPY BIRTHDAY!"
            cv2.putText(frame, victory, (width//2 - 200, height//2 - 50), 
                       font, 1.5, self.colors['flame'], 3)
            
            # Restart instruction at bottom
            restart = "Press 'R' to restart"
            cv2.putText(frame, restart, (width//2 - 120, height - 10), 
                       font, 0.5, self.colors['text'], 2)
            
            # Draw dancing cats
            if len(self.cat_positions) == 0:
                self.init_dancing_cats(width, height)
            
            self.cat_frame += 1
            for cat_pos in self.cat_positions:
                # Add bouncing animation
                bounce = int(10 * np.sin(time.time() * 3 + cat_pos['phase']))
                self.draw_dancing_cat(frame, cat_pos['x'], cat_pos['y'] + bounce, 
                                    self.cat_frame // 10)
    
    def blow_out_candle(self):
        """Blow out the nearest lit candle"""
        for i in range(len(self.candles)):
            if self.candles[i]:
                self.candles[i] = False
                self.blow_cooldown = 30  # Cooldown frames
                print(f"Candle {i+1} blown out!")
                break
        
        # Check if all candles are out
        if not any(self.candles):
            self.game_state = 'victory'
            self.victory_time = time.time()
            print("All candles blown out! Victory!")
    
    def play_birthday_song(self):
        """Play birthday song"""
        try:
            import pygame
            pygame.mixer.init()
            
            # Look for music file in current directory
            music_files = ['happybirthdaysong.mp3', 'birthday.mp3', 'birthday.wav', 
                          'happy_birthday.mp3', 'happy_birthday.wav', 'song.mp3', 'song.wav']
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            for music_file in music_files:
                music_path = os.path.join(script_dir, music_file)
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play()
                    print(f"Playing {music_file}")
                    return True
            
            print("No music file found. Please add birthday.mp3 or birthday.wav")
            return False
        except Exception as e:
            print(f"Could not play music: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def reset_game(self):
        """Reset the game state"""
        # Stop music if playing
        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                print("Music stopped")
        except:
            pass
        
        self.candles = [True] * 5
        self.game_state = 'blowing'  # Start directly in blowing mode
        self.blow_cooldown = 0
        self.victory_time = None
        self.music_played = False
        self.pout_history.clear()
        self.cat_positions = []  # Clear cat positions
        self.cat_frame = 0
        print("Game reset!")
    
    def run(self):
        """Main game loop"""
        print("Starting Birthday Candle Blower...")
        print("Game started! Make a pout face to blow out candles!")
        print("Press 'Q' to quit, 'R' to restart, 'A' to toggle ASCII filter")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Mirror for natural interaction
            
            # Convert to grayscale for face detection (BEFORE applying filter)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces on original frame
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Process face detection on original frame
            is_pouting = False
            face_data = None  # Store face detection results
            
            if len(faces) > 0:
                face = faces[0]  # Use first detected face
                x, y, w, h = face
                face_data = (x, y, w, h)
                
                # Detect gestures based on game state (on original frame)
                if self.game_state == 'blowing':
                    is_pouting = self.detect_pout(frame, face)
            
            # Now apply ASCII filter if enabled (after detection)
            if self.ascii_filter_enabled:
                frame = self.apply_ascii_filter(frame)
            
            # Draw face indicators on filtered frame
            if face_data is not None:
                x, y, w, h = face_data
                
                # Draw face rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), self.colors['accent'], 2)
                
                # Draw pout indicator on face
                if self.game_state == 'blowing':
                    if is_pouting:
                        cv2.putText(frame, "BLOWING!", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['flame'], 2)
                    else:
                        cv2.putText(frame, "Pout lips!", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['text'], 1)
            
            # Track gesture history
            self.pout_history.append(is_pouting)
            
            # Game state logic
            if self.game_state == 'blowing':
                # Blow out candle if consistently pouting
                if self.blow_cooldown > 0:
                    self.blow_cooldown -= 1
                elif sum(self.pout_history) > 6:  # 6 out of 15 frames (very easy)
                    self.blow_out_candle()
            
            elif self.game_state == 'victory':
                # Play music once when entering victory state
                if not self.music_played:
                    success = self.play_birthday_song()
                    self.music_played = True
                    if success:
                        print("Music started playing!")
                    else:
                        print("Failed to play music")
            
            # Draw game elements
            self.draw_ascii_cake(frame)
            self.draw_ui(frame)
            
            # Add 16-bit style scanlines
            for i in range(0, frame.shape[0], 4):
                frame[i:i+2] = frame[i:i+2] * 0.95
            
            # Display
            cv2.imshow('Birthday Candle Blower', frame)
            
            # Handle input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.reset_game()
            elif key == ord('a'):
                self.ascii_filter_enabled = not self.ascii_filter_enabled
                print(f"ASCII filter: {'ON' if self.ascii_filter_enabled else 'OFF'}")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    game = CandleBlower()
    game.run()

if __name__ == "__main__":
    main()
