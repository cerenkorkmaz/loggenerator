import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from FormatLog import FormatLog
from FormatJson import FormatJson
from Format4j2 import Format4j2
from Model import Model

class NegativeException(Exception):
    pass

def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        elif os.path.exists(relative_path):
            return os.path.abspath(relative_path)
        else:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

class LogGenerationProgress:
    def loadGif(self, path):
        gif = Image.open(path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames
    
    def updateGif(self):
        if self.gif:
            self.gif_label.config(image=self.gif[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif)
            self.master.after(100, self.updateGif)

    def onClose(self):
        pass
    
    def __init__(self, master):
        self.master = master
        self.master.title("Please Wait")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = 300
        window_height = 120
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.resizable(False, False)

        self.icon = tk.PhotoImage(file=resource_path("icon.png"))
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)

        self.progress_label = tk.Label(self.master, text="Generating logs...")
        self.progress_label.config(font=("TkDefaultFont ",13))
        self.progress_label.place(relx=0.5, rely=0.25, anchor='center')

        self.gif = self.loadGif("waiting_icon.gif")
        self.gif_index = 0
        self.gif_label = tk.Label(self.master)
        self.gif_label.place(relx=0.5, rely=0.55, anchor='center')
        self.updateGif()  
    
        self.cs_label = tk.Label(self.master, text="CsLog Generator®. CsTech.2023")
        self.cs_label.config(font=("MS Sans Serif",5))
        self.cs_label.place(relx=0, rely=0.85)

        self.cs_logo = tk.PhotoImage(file=resource_path("logo.png"))
        self.logo_label = tk.Label(self.master, image=self.cs_logo)
        self.logo_label.place(relx=0.733, rely=0.83)  

        self.master.protocol("WM_DELETE_WINDOW", self.onClose)
        self.master.attributes('-topmost',True)
        self.master.focus_force()

class LogGenerator:
    def onClose(self):
        if self.generation_in_progress:
            pass
        else:
            self.logGenerator.destroy()

    def onSelect(self, *args):
        self.selected_format = self.format_var.get()
        if self.selected_format != "Format:":
            self.num_logs_label.pack()
            self.num_logs_entry.pack()
            self.generate_button.pack()
            
    def checkEntry(self, *args):
        if not self.num_logs_entry.get():
            self.generate_button.configure(state='disabled')
        else:
            self.generate_button.configure(state='normal')

    def disable_widgets(self):
        for widget in self.logGenerator.winfo_children():
            try:
                widget.configure(state='disabled')
            except:
                pass

    def enable_widgets(self):
        for widget in self.logGenerator.winfo_children():
            try:
                widget.configure(state='normal')  
            except:
                pass      

    def generate(self):
        if self.generation_in_progress:
            return
        try:
            if not os.path.exists("logs"):
                os.mkdir("logs")
        except Exception as e:
            print("Error creating directory:", e)

        self.num_logs = self.num_logs_entry.get()
        try:
            self.num_logs = int(self.num_logs)
            if self.num_logs <= 0:
                raise NegativeException()
        except ValueError:
            self.num_logs_entry.delete(0, tk.END)
            self.generate_button.configure(state='disabled')
            messagebox.showerror("Error", "Number of logs must be a valid integer.")
        except NegativeException:
            self.num_logs_entry.delete(0, tk.END)
            self.generate_button.configure(state='disabled')
            messagebox.showerror("Error", "Number of logs must be a positive integer.")
        else:
            self.generation_in_progress = True
            self.disable_widgets()
            progress_window = tk.Toplevel()
            progress = LogGenerationProgress(progress_window)
            threading.Thread(target=self.generate_async, args=(progress,)).start()

    def generate_async(self, progress):
        model_instance = Model()
        try:
            format = self.format_var.get()
            if format == "log":
                FormatLog.generateLog(self.num_logs, model_instance)
            elif format == "4j2":
                Format4j2.generate4j2(self.num_logs, model_instance)
            elif format == "json":
                FormatJson.generateJson(self.num_logs, model_instance)
            else:
                messagebox.showerror("Error", "Unsupported format")
            
            messagebox.showinfo("INFO","Logs generated successfully!")
            self.enable_widgets()
            self.num_logs_entry.delete(0, tk.END) 
            self.generate_button.configure(state='disabled')
        finally:
            self.logGenerator.after(0, progress.master.destroy)
            self.generation_in_progress = False
            
        
    def __init__(self, logGenerator):
        self.logGenerator = logGenerator
        self.logGenerator.title("CsLog Generator")

        screen_width = self.logGenerator.winfo_screenwidth()
        screen_height = self.logGenerator.winfo_screenheight()

        window_width = 300
        window_height = 120
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.logGenerator.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.logGenerator.resizable(False, False)

        self.icon = tk.PhotoImage(file=resource_path("icon.png"))
        self.logGenerator.tk.call('wm', 'iconphoto', self.logGenerator._w, self.icon)

        self.cs_label = tk.Label(self.logGenerator, text="CsLog Generator®. CsTech.2023")
        self.cs_label.config(font=("MS Sans Serif",5))
        self.cs_label.place(relx=0, rely=0.85)

        self.cs_logo = tk.PhotoImage(file=resource_path("logo.png"))
        self.logo_label = tk.Label(self.logGenerator, image=self.cs_logo)
        self.logo_label.place(relx=0.733, rely=0.83)  

        self.formats_arr = ["Format:", "log", "json", "4j2"]
        self.format_var = tk.StringVar(self.logGenerator)
        self.format_var.set(self.formats_arr[0])
        self.dropbox = tk.OptionMenu(self.logGenerator, self.format_var, *self.formats_arr)
        self.dropbox.config(width=10)
        self.dropbox["menu"].entryconfigure(0, state="disabled")
        self.dropbox.pack()

        self.format_var.trace("w", self.onSelect)

        self.num_logs_label = tk.Label(self.logGenerator, text="Number of logs to generate:")
        self.num_logs_entry = tk.Entry(self.logGenerator)

        self.num_logs_entry.bind("<KeyRelease>", self.checkEntry)
        self.generate_button = tk.Button(self.logGenerator, text="Generate", command=self.generate, state='disabled')

        self.logGenerator.protocol("WM_DELETE_WINDOW", self.onClose)
        self.logGenerator.attributes('-topmost',True)
        self.logGenerator.focus_force()

        self.generation_in_progress = False