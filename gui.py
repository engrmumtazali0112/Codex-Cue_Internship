import tkinter as tk
from tkinter import messagebox

class VoiceAssistantGUI:
    def _init_(self, listener, command_executor):
        self.listener = listener
        self.command_executor = command_executor
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("300x200")
        
        self.label = tk.Label(self.root, text="Voice Assistant", font=("Arial", 16))
        self.label.pack(pady=20)
        
        self.start_button = tk.Button(self.root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=10)

    def start_listening(self):
        command = self.listener()
        if command != "None":
            self.command_executor(command)
    
    def run(self):
        self.root.mainloop()