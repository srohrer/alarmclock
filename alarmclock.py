import tkinter as tk
from tkinter import ttk
import datetime
import time
from playsound import playsound
import threading
import sys
import os

class AlarmClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alarm Clock")
        self.root.geometry("300x200")
        
        # Create variables
        self.alarm_time = None
        self.alarm_active = False
        self.sound_playing = False
        
        # Create time options (5-minute intervals)
        self.times = []
        for hour in range(24):
            for minute in range(0, 60, 5):
                time_str = f"{hour:02d}:{minute:02d}"
                self.times.append(time_str)
        
        # Create GUI elements
        self.setup_gui()
        
        # Start the time update thread
        self.update_thread = threading.Thread(target=self.check_alarm, daemon=True)
        self.update_thread.start()
        
    def setup_gui(self):
        # Current time display
        self.time_label = tk.Label(self.root, text="", font=("Arial", 24))
        self.time_label.pack(pady=10)
        
        # Time selection dropdown
        self.time_var = tk.StringVar()
        self.time_dropdown = ttk.Combobox(self.root, textvariable=self.time_var, values=self.times)
        self.time_dropdown.pack(pady=10)
        
        # Set alarm button
        self.set_button = tk.Button(self.root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=5)
        
        # Stop alarm button
        self.stop_button = tk.Button(self.root, text="Stop Alarm", command=self.stop_alarm, state="disabled")
        self.stop_button.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="No alarm set")
        self.status_label.pack(pady=5)
        
        # Update current time
        self.update_current_time()
        
    def update_current_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_current_time)
    
    def set_alarm(self):
        selected_time = self.time_var.get()
        if selected_time in self.times:
            self.alarm_time = selected_time
            self.alarm_active = True
            self.set_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text=f"Alarm set for {selected_time}")
    
    def stop_alarm(self):
        self.alarm_active = False
        self.sound_playing = False
        self.set_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="No alarm set")
    
    def play_alarm_sound(self):
        try:
            while self.sound_playing:
                # Handle paths for both development and PyInstaller
                if getattr(sys, 'frozen', False):
                    # Running as compiled executable
                    application_path = sys._MEIPASS
                else:
                    # Running in development
                    application_path = os.path.dirname(os.path.abspath(__file__))
                
                sound_path = os.path.join(application_path, "alarm.mp3")
                playsound(sound_path)
                time.sleep(2)
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def check_alarm(self):
        while True:
            if self.alarm_active:
                current_time = datetime.datetime.now().strftime("%H:%M")
                if current_time == self.alarm_time:
                    self.sound_playing = True
                    self.play_alarm_sound()
                    self.alarm_active = False
            time.sleep(1)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    alarm = AlarmClock()
    alarm.run()
