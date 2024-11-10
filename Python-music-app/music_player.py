"""
Enhanced Music Player Application with Modern UI
Requirements:
pip install pygame
pip install tk
pip install mutagen
pip install ttkthemes
"""

import os
import time
from tkinter import *
from tkinter import filedialog, ttk
import pygame
from mutagen.mp3 import MP3
import threading
from pathlib import Path
from ttkthemes import ThemedStyle

class ModernMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Music Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        
        # Apply modern theme
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")
        
        # Configure custom styles
        self.configure_styles()
        
        # Initialize Pygame Mixer
        pygame.mixer.init()
        
        # Create the music directory
        self.music_dir = Path("music_library")
        self.music_dir.mkdir(exist_ok=True)
        
        # Initialize variables
        self.current_directory = str(self.music_dir)
        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.played = False
        self.current_song_length = 0
        
        # Create GUI
        self.create_gui()
        
        # Load initial music library
        self.load_music_library()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Custom colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#1db954',
            'secondary': '#282828',
            'hover': '#2a2a2a'
        }

        # Configure ttk styles
        self.style.configure(
            "Custom.TButton",
            padding=10,
            background=self.colors['accent'],
            foreground=self.colors['fg']
        )

        self.style.configure(
            "Custom.Horizontal.TScale",
            background=self.colors['bg'],
            troughcolor=self.colors['secondary'],
            slidercolor=self.colors['accent']
        )

    def create_gui(self):
        # Main container
        self.main_container = Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Header Frame
        self.header_frame = Frame(self.main_container, bg=self.colors['bg'])
        self.header_frame.pack(fill=X, pady=(0, 20))

        self.title_label = Label(
            self.header_frame,
            text="Modern Music Player",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.title_label.pack(side=LEFT)

        # Add Music Button
        self.add_button = ttk.Button(
            self.header_frame,
            text="Add Music",
            style="Custom.TButton",
            command=self.add_music_files
        )
        self.add_button.pack(side=RIGHT, padx=10)

        # Create Playlist Frame
        self.playlist_frame = Frame(self.main_container, bg=self.colors['bg'])
        self.playlist_frame.pack(fill=BOTH, expand=True)

        # Playlist
        self.playlist_box = Listbox(
            self.playlist_frame,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['fg'],
            font=("Helvetica", 11),
            borderwidth=0,
            highlightthickness=0
        )
        self.playlist_box.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.playlist_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configure scrollbar
        self.playlist_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.playlist_box.yview)

        # Control Frame
        self.control_frame = Frame(self.main_container, bg=self.colors['bg'])
        self.control_frame.pack(fill=X, pady=20)

        # Progress Bar Frame
        self.progress_frame = Frame(self.control_frame, bg=self.colors['bg'])
        self.progress_frame.pack(fill=X)

        # Time Labels
        self.current_time = Label(
            self.progress_frame,
            text="00:00",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Helvetica", 10)
        )
        self.current_time.pack(side=LEFT)

        self.total_time = Label(
            self.progress_frame,
            text="00:00",
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            font=("Helvetica", 10)
        )
        self.total_time.pack(side=RIGHT)

        # Progress Bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Scale(
            self.progress_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            variable=self.progress_var,
            style="Custom.Horizontal.TScale",
            command=self.slide
        )
        self.progress_bar.pack(fill=X, padx=10)

        # Buttons Frame
        self.buttons_frame = Frame(self.control_frame, bg=self.colors['bg'])
        self.buttons_frame.pack(pady=20)

        # Control Buttons
        button_data = [
            ("⏮", self.previous_track),
            ("⏯", self.play_music),
            ("⏹", self.stop_music),
            ("⏭", self.next_track)
        ]

        for text, command in button_data:
            btn = Button(
                self.buttons_frame,
                text=text,
                font=("Helvetica", 16),
                command=command,
                bg=self.colors['secondary'],
                fg=self.colors['fg'],
                activebackground=self.colors['hover'],
                activeforeground=self.colors['fg'],
                borderwidth=0,
                width=5,
                height=2
            )
            btn.pack(side=LEFT, padx=10)

        # Volume Frame
        self.volume_frame = Frame(self.control_frame, bg=self.colors['bg'])
        self.volume_frame.pack(fill=X, pady=(10, 0))

        # Volume Icon
        self.volume_label = Label(
            self.volume_frame,
            text="🔊",
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.volume_label.pack(side=LEFT, padx=(0, 10))

        # Volume Slider
        self.volume_var = DoubleVar(value=0.7)
        self.volume_slider = ttk.Scale(
            self.volume_frame,
            from_=0,
            to=1,
            orient=HORIZONTAL,
            variable=self.volume_var,
            command=self.volume,
            style="Custom.Horizontal.TScale"
        )
        self.volume_slider.pack(fill=X)

        # Status Bar
        self.status_bar = Label(
            self.main_container,
            text="Ready to Play",
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=("Helvetica", 10),
            pady=5
        )
        self.status_bar.pack(fill=X, side=BOTTOM)

        # Bind Events
        self.playlist_box.bind('<Double-1>', self.play_selected)
        self.bind_hover_events()

        # Initialize Timer
        self.timer_thread = None
        self.timer_running = False

    def bind_hover_events(self):
        """Bind hover events for buttons"""
        for widget in self.buttons_frame.winfo_children():
            widget.bind('<Enter>', lambda e, w=widget: self.on_hover(e, w))
            widget.bind('<Leave>', lambda e, w=widget: self.on_leave(e, w))

    def on_hover(self, event, widget):
        """Handle hover enter event"""
        widget.configure(bg=self.colors['hover'])

    def on_leave(self, event, widget):
        """Handle hover leave event"""
        widget.configure(bg=self.colors['secondary'])

    def add_music_files(self):
        """Add music files to the library"""
        files = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=(
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav")
            )
        )
        
        if files:
            for file in files:
                # Copy file to music library
                dest = self.music_dir / Path(file).name
                if not dest.exists():
                    with open(file, 'rb') as src_file, open(dest, 'wb') as dst_file:
                        dst_file.write(src_file.read())
            
            # Reload the music library
            self.load_music_library()
            self.status_bar.config(text="Music files added successfully!")

    def load_music_library(self):
        """Load all music files from the music directory"""
        self.playlist = []
        self.playlist_box.delete(0, END)
        
        for file in self.music_dir.glob('*'):
            if file.suffix.lower() in ('.mp3', '.wav'):
                self.playlist.append(file)
                self.playlist_box.insert(END, file.name)

    def play_music(self):
        """Play the selected music"""
        try:
            if not self.played:
                if not self.playlist_box.curselection():
                    if self.playlist_box.size() > 0:
                        self.playlist_box.selection_set(0)
                    else:
                        self.status_bar.config(text="Please add some music files first!")
                        return
                
                current_selection = self.playlist_box.curselection()[0]
                selected_song = self.playlist[current_selection]
                
                pygame.mixer.music.load(str(selected_song))
                pygame.mixer.music.play()
                self.played = True
                self.update_song_length(selected_song)
                self.status_bar.config(text=f"Playing: {selected_song.name}")
                self.start_timer()
            else:
                if self.paused:
                    pygame.mixer.music.unpause()
                    self.paused = False
                    self.status_bar.config(text="Resumed")
                else:
                    pygame.mixer.music.pause()
                    self.paused = True
                    self.status_bar.config(text="Paused")
        except pygame.error as e:
            self.status_bar.config(text=f"Error playing file: {str(e)}")

    def update_song_length(self, song_path):
        """Update the total length of the current song"""
        try:
            audio = MP3(str(song_path))
            self.current_song_length = audio.info.length
            mins, secs = divmod(self.current_song_length, 60)
            mins = round(mins)
            secs = round(secs)
            self.total_time.config(text=f"{mins:02d}:{secs:02d}")
            self.progress_bar.config(to=self.current_song_length)
        except:
            self.current_song_length = 0
            self.total_time.config(text="00:00")

    def stop_music(self):
        """Stop the current playing music"""
        pygame.mixer.music.stop()
        self.played = False
        self.paused = False
        self.timer_running = False
        self.progress_var.set(0)
        self.current_time.config(text="00:00")
        self.status_bar.config(text="Stopped")

    def next_track(self):
        """Play the next track"""
        if self.playlist_box.size() > 0:
            next_index = (self.playlist_box.curselection()[0] + 1) % self.playlist_box.size()
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.selection_set(next_index)
            self.playlist_box.activate(next_index)
            self.playlist_box.see(next_index)
            self.played = False
            self.play_music()

    def previous_track(self):
        """Play the previous track"""
        if self.playlist_box.size() > 0:
            prev_index = (self.playlist_box.curselection()[0] - 1) % self.playlist_box.size()
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.selection_set(prev_index)
            self.playlist_box.activate(prev_index)
            self.playlist_box.see(prev_index)
            self.played = False
            self.play_music()

    def play_selected(self, event):
        """Play the selected track on double click"""
        self.played = False
        self.play_music()

    def start_timer(self):
        """Start the timer thread"""
        self.timer_running = True
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def update_timer(self):
        """Update the timer display"""
        while self.timer_running:
            if not self.paused and self.played:
                current_time = pygame.mixer.music.get_pos() / 1000
                if current_time >= 0:  # Only update if we have a valid position
                    mins, secs = divmod(current_time, 60)
                    mins = round(mins)
                    secs = round(secs)
                    self.current_time.config(text=f"{mins:02d}:{secs:02d}")
                    self.progress_var.set(current_time)
            time.sleep(0.1)

    def slide(self, value):
        """Handle slider movement"""
        try:
            if self.played and not self.paused:
                current_time = float(value)
                # Stop and restart the music at the new position
                pygame.mixer.music.stop()
                pygame.mixer.music.play(start=current_time)
        except pygame.error:
            pass  # Handle the error silently

    def volume(self, value):
        """Handle volume changes"""
        try:
            pygame.mixer.music.set_volume(float(value))
            # Update volume icon based on level
            if float(value) == 0:
                self.volume_label.config(text="🔇")
            elif float(value) < 0.5:
                self.volume_label.config(text="🔉")
            else:
                self.volume_label.config(text="🔊")
        except pygame.error:
            pass

if __name__ == "__main__":
    root = Tk()
    app = ModernMusicPlayer(root)
    root.mainloop()