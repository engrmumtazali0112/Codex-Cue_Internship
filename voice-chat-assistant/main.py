import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
import wikipediaapi
import webbrowser
import time
from datetime import datetime
import json
import os
import requests
import openai

class EnhancedVoiceAssistant:
    def __init__(self, openai_api_key):
        # Initialize OpenAI
        openai.api_key = openai_api_key
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("AI Voice Assistant with ChatGPT")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        # Initialize speech components
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Initialize chat history
        self.chat_history = []
        self.load_history()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main container
        main_container = tk.Frame(self.root, bg="#2C3E50")
        main_container.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_container, bg="#2C3E50")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="AI Voice Assistant with ChatGPT",
            font=("Helvetica", 24, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        title_label.pack()
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="● Idle",
            font=("Helvetica", 12),
            fg="#E74C3C",
            bg="#2C3E50"
        )
        self.status_label.pack(pady=(5, 0))
        
        # Create conversation display
        self.conversation_area = scrolledtext.ScrolledText(
            main_container,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg="#34495E",
            fg="#ECF0F1",
            height=15
        )
        self.conversation_area.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Control buttons frame
        button_frame = tk.Frame(main_container, bg="#2C3E50")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Microphone button
        self.mic_button = tk.Button(
            button_frame,
            text="Start Listening",
            command=self.toggle_listening,
            font=("Helvetica", 12, "bold"),
            bg="#2ECC71",
            fg="white",
            width=15,
            height=2
        )
        self.mic_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = tk.Button(
            button_frame,
            text="Clear History",
            command=self.clear_history,
            font=("Helvetica", 12),
            bg="#E74C3C",
            fg="white",
            width=15,
            height=2
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Command input frame
        input_frame = tk.Frame(main_container, bg="#2C3E50")
        input_frame.pack(fill=tk.X)
        
        self.command_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg="#34495E",
            fg="#ECF0F1",
            insertbackground="#ECF0F1"
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.handle_text_command,
            font=("Helvetica", 12),
            bg="#3498DB",
            fg="white",
            width=10
        )
        send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send command
        self.command_entry.bind("<Return>", lambda e: self.handle_text_command())
        
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.mic_button.configure(text="Stop Listening", bg="#E74C3C")
            self.status_label.configure(text="● Listening", fg="#2ECC71")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.mic_button.configure(text="Start Listening", bg="#2ECC71")
            self.status_label.configure(text="● Idle", fg="#E74C3C")
    
    def listen_loop(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio).lower()
                    self.process_command(command, "voice")
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                self.update_conversation("Sorry, there was an error with the speech recognition service.")
    
    def handle_text_command(self):
        command = self.command_entry.get().strip()
        if command:
            self.command_entry.delete(0, tk.END)
            self.process_command(command, "text")
    
    def process_command(self, command, source):
        # Update conversation with user's command
        self.update_conversation(f"You ({source}): {command}")
        
        # Check for specific commands first
        if any(keyword in command.lower() for keyword in ["open youtube", "search google", "wikipedia"]):
            response = self.execute_system_command(command)
        else:
            # Use ChatGPT for general conversation
            response = self.get_chatgpt_response(command)
        
        # Speak response if command was voice
        if source == "voice":
            self.speak(response)
        
        # Update conversation with assistant's response
        self.update_conversation(f"Assistant: {response}")
        
        # Save to history
        self.chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "command": command,
            "response": response
        })
        self.save_history()
    
    def execute_system_command(self, command):
        if "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube"
            
        elif "search google" in command:
            search_query = command.replace("search google", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return f"Searching Google for {search_query}"
            
        elif "wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page = wiki_wiki.page(search_query)
            
            if page.exists():
                return page.summary[:200] + "..."
            return "I couldn't find any information on that topic."
    
    def get_chatgpt_response(self, command):
        try:
            # Prepare the messages for the chat
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant that provides clear and concise responses."},
                {"role": "user", "content": command}
            ]
            
            # Get response from ChatGPT
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def update_conversation(self, text):
        self.conversation_area.insert(tk.END, f"{text}\n\n")
        self.conversation_area.see(tk.END)
    
    def clear_history(self):
        self.conversation_area.delete(1.0, tk.END)
        self.chat_history = []
        self.save_history()
    
    def load_history(self):
        try:
            if os.path.exists("chat_history.json"):
                with open("chat_history.json", "r") as f:
                    self.chat_history = json.load(f)
        except:
            self.chat_history = []
    
    def save_history(self):
        with open("chat_history.json", "w") as f:
            json.dump(self.chat_history, f, indent=4)
    
    def run(self):
        self.root.mainloop()

# Run the assistant
if __name__ == "__main__":
    # Replace with your OpenAI API key
    OPENAI_API_KEY = ""
    assistant = EnhancedVoiceAssistant(OPENAI_API_KEY)
    assistant.run()