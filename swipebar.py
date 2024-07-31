import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import tkinter as tk
import keyboard
from src.assist import ask_question_memory

class JarvisWindow(tk.Tk):
    def __init__(self):
        print("swipebar.py gestartet")
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(bg='#000033')

        self.frame = tk.Frame(self, bg='#000033')
        self.frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.input_frame = tk.Frame(self.frame, bg='white', bd=1)
        self.input_frame.pack(fill='x', pady=(0, 5))
        
        self.input_inner_frame = tk.Frame(self.input_frame, bg='#000066', bd=4)
        self.input_inner_frame.pack(fill='both', expand=True)

        self.input_entry = tk.Entry(self.input_inner_frame, bg='#000066', fg='white', insertbackground='white', bd=0)
        self.input_entry.pack(fill='x', pady=2, padx=2)
        self.input_entry.bind('<Return>', self.send_message)

        self.output_outer_frame = tk.Frame(self.frame, bg='white', bd=1)
        self.output_outer_frame.pack(fill='both', expand=True)

        self.output_frame = tk.Frame(self.output_outer_frame, bg='#000066', bd=4)
        self.output_frame.pack(fill='both', expand=True)

        self.output_text = tk.Text(self.output_frame, height=6, wrap='word', state='disabled', bg='#000066', fg='white', bd=0)
        self.output_text.pack(fill='both', expand=True)

        self.y_position = -300
        self.is_visible = False
        self.output_visible = False
        self.jarvis_response = ""
        self.user_message = ""

        self.bind('<Escape>', lambda e: self.toggle_visibility())

        self.minsize(567, 60)

    def send_message(self, event=None):
        user_input = self.input_entry.get()
        if user_input:
            self.clear_output()
            self.user_message = user_input
            self.input_entry.delete(0, 'end')

            self.jarvis_response = ask_question_memory(user_input, "swipebar")
            if not self.output_visible:
                self.show_output_frame()
            else:
                self.display_messages()

    def display_messages(self):
        self.append_text(f"Sie: {self.user_message}")
        self.animate_underline()

    def animate_underline(self):
        self.output_text.configure(state='normal')
        self.output_text.insert('end', "\n")
        self.output_text.configure(state='disabled')
        
        text_width = self.output_text.winfo_width() - 15
        underline_length = int(text_width // 8.2)
        
        def add_underline(index):
            if index <= underline_length:
                self.output_text.configure(state='normal')
                self.output_text.insert('end', "_", 'underline')
                self.output_text.tag_configure('underline', foreground='#1E90FF')
                self.output_text.configure(state='disabled')
                self.output_text.see('end')
                self.after(10, add_underline, index + 1)
            else:
                self.output_text.configure(state='normal')
                self.output_text.insert('end', "\n\n")
                self.output_text.configure(state='disabled')
                self.append_text(f"Jarvis: {self.jarvis_response}\n")

        self.after(500, add_underline, 1)

    def append_text(self, text):
        self.output_text.configure(state='normal')
        self.output_text.insert('end', text)
        self.output_text.see('end')
        self.output_text.configure(state='disabled')

    def clear_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.configure(state='disabled')

    def show_output_frame(self):
        if not self.output_visible:
            self.output_outer_frame.pack(fill='both', expand=True)
            self.output_visible = True
            self.update_idletasks()
            self.animate_output_down()

    def animate_output_down(self):
        current_height = self.winfo_height()
        target_height = current_height + self.output_outer_frame.winfo_reqheight() + 38
        
        def expand_step():
            nonlocal current_height
            if current_height < target_height:
                current_height += 2
                self.geometry(f'567x{current_height}')
                self.after(20, expand_step)
            else:
                self.geometry(f'567x{target_height}')
                self.display_messages()

        expand_step()

    def toggle_visibility(self):
        if self.is_visible:
            self.animate_up()
        else:
            self.animate_down()

    def animate_down(self):
        if self.y_position < 20:
            self.y_position += 10
            self.geometry(f'+{self.winfo_screenwidth()//2 - 283}+{self.y_position}')
            self.after(10, self.animate_down)
        else:
            self.y_position = 20
            self.geometry(f'+{self.winfo_screenwidth()//2 - 283}+{self.y_position}')
            self.is_visible = True
            self.input_entry.focus_set()  

    def animate_up(self):
        if self.y_position > -300:
            self.y_position -= 10
            self.geometry(f'+{self.winfo_screenwidth()//2 - 283}+{self.y_position}')
            self.after(10, self.animate_up)
        else:
            self.is_visible = False
            self.clear_window()

    def clear_window(self):
        self.clear_output()
        self.input_entry.delete(0, 'end')
        self.output_outer_frame.pack_forget()
        self.output_visible = False
        self.geometry('567x60')

def toggle_window():
    if window.is_visible:
        window.toggle_visibility()
    else:
        window.deiconify()
        window.geometry('567x60')
        window.toggle_visibility()
        window.focus_force()
        window.input_entry.focus_set()  

window = JarvisWindow()
keyboard.add_hotkey('f10', toggle_window)

window.withdraw()
window.mainloop()
