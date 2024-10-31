from tkinter import *
from tkinter import messagebox
import tkinter.font as font

class HoverButton(Button):
    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self["state"] != "disabled":
            self["background"] = self.bright_color(self.defaultBackground)
            self.config(relief=RAISED)

    def on_leave(self, e):
        self["background"] = self.defaultBackground
        self.config(relief=FLAT)

    def bright_color(self, color):
        if color.startswith("#"):
            if color == "#121212":
                return "#2A2A2A"
            elif color == "#1E1E1E":
                return "#2D2D2D"
            return "#4A4A4A"
        return color

cal = Tk()
cal.geometry("312x394")
cal.resizable(True, True)  # Enable resizing
cal.title("Modern Calculator")

def about():
    messagebox.showinfo('About', "\n Created by Mumtaz Ali \n \n  linkedin :\n  https://www.linkedin.com/in/mumtazali12/")

def click_button(item):
    current = inputText.get()
    inputText.set(current + str(item))

def clear_button():
    current = inputText.get()
    if current:
        inputText.set(current[:-1])

def clear_all():
    inputText.set("")

def equal_button():
    try:
        result = eval(inputText.get())
        inputText.set(result)
    except:
        inputText.set("ERROR")

# Theme colors and fonts
DARK_GRAY = "#1E1E1E"
DARKER_GRAY = "#121212"
ACCENT_COLOR = "#007ACC"
TEXT_COLOR = "#FFFFFF"
OPERATOR_COLOR = "#FF4081"
button_font = font.Font(family="Helvetica", size=10, weight="bold")
display_font = font.Font(family="Helvetica", size=20, weight="bold")

# Menu
menubar = Menu(cal, bg=DARK_GRAY, fg=TEXT_COLOR)
filemenu = Menu(menubar, tearoff=0, bg=DARK_GRAY, fg=TEXT_COLOR)
filemenu.add_command(label="Cut", accelerator="Ctrl+X")
filemenu.add_command(label="Copy", accelerator="Ctrl+C")
filemenu.add_command(label="Paste", accelerator="Ctrl+V")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=cal.quit)
menubar.add_cascade(label="Edit", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0, bg=DARK_GRAY, fg=TEXT_COLOR)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

cal.config(bg=DARK_GRAY, menu=menubar)

# Input setup
inputText = StringVar()

inputFrame = Frame(cal, width=312, height=50, bg=DARK_GRAY)
inputFrame.pack(side=TOP, pady=10)

inputField = Entry(inputFrame, font=display_font, textvariable=inputText, width=20, fg=TEXT_COLOR, bg=DARKER_GRAY, bd=0, justify=RIGHT)
inputField.pack(ipady=10, ipadx=10, pady=5)

button_frame = Frame(cal, width=312, height=272.5, bg=DARK_GRAY)
button_frame.pack(padx=5, pady=5)

button_configs = {
    'width': 8,
    'height': 2,
    'bd': 0,
    'fg': TEXT_COLOR,
    'font': button_font,
    'cursor': 'hand2',
    'relief': FLAT
}

# Buttons setup
HoverButton(button_frame, text="C", bg=ACCENT_COLOR, command=clear_all, **button_configs).grid(row=1, column=0, padx=2, pady=2)
HoverButton(button_frame, text="(", bg=DARK_GRAY, command=lambda: click_button("("), **button_configs).grid(row=1, column=1, padx=2, pady=2)
HoverButton(button_frame, text=")", bg=DARK_GRAY, command=lambda: click_button(")"), **button_configs).grid(row=1, column=2, padx=2, pady=2)
HoverButton(button_frame, text="⌫", bg=ACCENT_COLOR, command=clear_button, **button_configs).grid(row=1, column=3, padx=2, pady=2)

# Other rows
HoverButton(button_frame, text="^", bg=DARK_GRAY, command=lambda: click_button("**"), **button_configs).grid(row=2, column=0, padx=2, pady=2)
HoverButton(button_frame, text="π", bg=DARK_GRAY, command=lambda: click_button(3.1415), **button_configs).grid(row=2, column=1, padx=2, pady=2)
HoverButton(button_frame, text="e", bg=DARK_GRAY, command=lambda: click_button(2.7182), **button_configs).grid(row=2, column=2, padx=2, pady=2)
HoverButton(button_frame, text="÷", bg=OPERATOR_COLOR, command=lambda: click_button("/"), **button_configs).grid(row=2, column=3, padx=2, pady=2)

HoverButton(button_frame, text="7", bg=DARKER_GRAY, command=lambda: click_button(7), **button_configs).grid(row=3, column=0, padx=2, pady=2)
HoverButton(button_frame, text="8", bg=DARKER_GRAY, command=lambda: click_button(8), **button_configs).grid(row=3, column=1, padx=2, pady=2)
HoverButton(button_frame, text="9", bg=DARKER_GRAY, command=lambda: click_button(9), **button_configs).grid(row=3, column=2, padx=2, pady=2)
HoverButton(button_frame, text="×", bg=OPERATOR_COLOR, command=lambda: click_button("*"), **button_configs).grid(row=3, column=3, padx=2, pady=2)

HoverButton(button_frame, text="4", bg=DARKER_GRAY, command=lambda: click_button(4), **button_configs).grid(row=4, column=0, padx=2, pady=2)
HoverButton(button_frame, text="5", bg=DARKER_GRAY, command=lambda: click_button(5), **button_configs).grid(row=4, column=1, padx=2, pady=2)
HoverButton(button_frame, text="6", bg=DARKER_GRAY, command=lambda: click_button(6), **button_configs).grid(row=4, column=2, padx=2, pady=2)
HoverButton(button_frame, text="-", bg=OPERATOR_COLOR, command=lambda: click_button("-"), **button_configs).grid(row=4, column=3, padx=2, pady=2)

HoverButton(button_frame, text="1", bg=DARKER_GRAY, command=lambda: click_button(1), **button_configs).grid(row=5, column=0, padx=2, pady=2)
HoverButton(button_frame, text="2", bg=DARKER_GRAY, command=lambda: click_button(2), **button_configs).grid(row=5, column=1, padx=2, pady=2)
HoverButton(button_frame, text="3", bg=DARKER_GRAY, command=lambda: click_button(3), **button_configs).grid(row=5, column=2, padx=2, pady=2)
HoverButton(button_frame, text="+", bg=OPERATOR_COLOR, command=lambda: click_button("+"), **button_configs).grid(row=5, column=3, padx=2, pady=2)

HoverButton(button_frame, text=".", bg=DARK_GRAY, command=lambda: click_button("."), **button_configs).grid(row=6, column=0, padx=2, pady=2)
HoverButton(button_frame, text="0", bg=DARKER_GRAY, command=lambda: click_button(0), **button_configs).grid(row=6, column=1, padx=2, pady=2)

equals_button = HoverButton(button_frame, 
                          text="=",
                          bg=ACCENT_COLOR,
                          fg=TEXT_COLOR,
                          command=equal_button,
                          width=17,
                          height=2,
                          bd=0,
                          cursor="hand2",
                          font=button_font)
equals_button.grid(row=6, column=2, columnspan=2, padx=2, pady=2)

# Footer Frame with Signature
footer_frame = Frame(cal, width=312, height=30, bg=DARK_GRAY)
footer_frame.pack(side=BOTTOM, pady=5)

footer_label = Label(
    footer_frame,
    text="Made by Mumtaz Ali",
    font=("Helvetica", 8, "italic"),
    fg=TEXT_COLOR,
    bg=DARK_GRAY
)
footer_label.pack()

cal.mainloop()
