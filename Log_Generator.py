import os
import sys
import random
import datetime
import markovify
import json
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    elif os.path.exists(relative_path):
        return os.path.abspath(relative_path)
    else:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
# Create the GUI window
window = tk.Tk()
window.title("CsLog Generator")
window.geometry("300x120")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (400 / 2))
y_coordinate = int((screen_height / 2) - (300 / 2))
window.geometry("+{}+{}".format(x_coordinate, y_coordinate))
window.resizable(False, False)


icon = tk.PhotoImage(file=resource_path("icon.png"))
window.tk.call('wm', 'iconphoto', window._w, icon)

cs_label = tk.Label(window, text="CsLog Generator®. CsTech.2023")
cs_label.config(font=("MS Sans Serif",5))
cs_label.place(x=0, y=102)

logo = tk.PhotoImage(file=resource_path("logo.png"))

# Create a label with the image
img_label = tk.Label(window, image=logo)
img_label.place(x=220, y=99)

formats_arr = ["Format:", "log", "json", "4j2"]

format_var = tk.StringVar(window)
format_var.set(formats_arr[0])

# Create the OptionMenu widget
dropbox = tk.OptionMenu(window, format_var, *formats_arr)
dropbox.config(width=10)

# Set the "Format:" option as disabled
dropbox["menu"].entryconfigure(0, state="disabled")
dropbox.pack()

def loading_window():
    wait_window = tk.Toplevel()
    wait_window.title("CsLog Generator")
    wait_window.geometry("300x120")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (400 / 2))
    y_coordinate = int((screen_height / 2) - (300 / 2))
    wait_window.geometry("+{}+{}".format(x_coordinate, y_coordinate))
    
    icon = tk.PhotoImage(file=resource_path("icon.png"))
    wait_window.tk.call('wm', 'iconphoto', wait_window._w, icon)

    wait_label = tk.Label(wait_window, text="Please Wait ☺")
    wait_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    return wait_window


global num_logs_entry
global generate_button
global format_entry

def commands(ext):
    global num_logs_entry
    int_entry_ok = True
    try:
        value = int(num_logs_entry.get())
        if value <= 0 :
            int_entry_ok = False
            num_logs_entry.delete(0, tk.END)
    except ValueError:
        int_entry_ok = False
        num_logs_entry.delete(0, tk.END)

    if int_entry_ok:
        wait_window = loading_window()
        window.after(50, lambda: generate_logs(ext, wait_window))
    else:
        if not int_entry_ok:
            messagebox.showerror("Error", "Please enter a positive integer.")


# Define the function to generate logs
def generate_logs(ext, wait_window = None):
    if wait_window:
        wait_window.lift()
        
    global num_logs_entry
    global generate_button
    
    # Disable the input fields and the generate button
    num_logs_entry.configure(state='disabled')
    generate_button.configure(state='disabled')

    # Load the text corpus to use for generating sentences
    with open(resource_path("logs.txt"), encoding="utf8") as f:
        text = f.read()

    # Build the Markov model for the text
    model = markovify.Text(text)

    # Get the current date and time
    now = datetime.datetime.now()

    # Create a new directory if it doesn't exist
    if not os.path.exists("logs"):
        os.mkdir("logs")

    if ext == "log":
        # List of values to use for generating random logs
        system_names = ['System1', 'System2', 'System3', 'System4', 'System5']
        subsystem_names = ['Subsys1', 'Subsys2', 'Subsys3', 'Subsys4', 'Subsys5']
        sources = ['Source1', 'Source2', 'Source3', 'Source4', 'Source5']
        levels = ['Information', 'Warning', 'Error']
        users = ['User1', 'User2', 'User3', 'User4', 'User5', 'Aselsan Designer', 'Test', 'Aselsan Tasarimci']

        
        # Open a file to write the logs to
        filename = os.path.join("logs", f"log-{now.strftime('%y%m%d%H%M')}-000.log")
        with open(filename, 'w') as file:

            # Write the header line
            header = 'Date/Time\tSystem Name\tSubsystem Name\tSource\tCode\tLevel\tUser\tText\n'
            file.write(header)

            # Generate N random logs
            i = 0
            num_sentences = int(num_logs_entry.get())
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%d.%m.%y %H:%M:%S')
            while i < num_sentences:
                system_name = random.choice(system_names)
                subsystem_name = random.choice(subsystem_names)
                source = random.choice(sources)
                code = random.randint(0, 10)
                level = random.choice(levels)
                user = random.choice(users)
                sentence = model.make_sentence()
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:100] # Generating a random sentence that does not exceed 100 chars
                    log = f'{date_time_str}\t{system_name}\t{subsystem_name}\t{source}\t{code}\t{level}\t{user}\t{text}'
                    file.write(log)
                    i += 1
                    if i != num_sentences:
                        file.write('\n')
                        
                random_seconds = random.randint(0, 3)
                date_time += datetime.timedelta(seconds=random_seconds)
                date_time_str = date_time.strftime('%d.%m.%y %H:%M:%S')
      

    elif ext == "json":
        # List of values to use for generating random logs
        sources = ['REHIS', 'JETHA', 'FESOM', 'PODRI', 'BACOL', 'NIRLU', 'LOJEM', 'ZELGA', 'QOVIX', 'DUNIK']
        levels = ['INFO', 'WARN', 'ERROR']
        first_names = ['Aylin', 'Berk', 'Cemre', 'Deniz', 'Elif', 'Firat', 'Gul', 'Hakan', 'Irem', 'Jale']
        last_names = ['Yilmaz', 'Kaya', 'Celik', 'Ozturk', 'Demir', 'Sahin', 'Yildirim', 'Acar', 'Turan', 'Gunes']
        usernames = ['admin', 'uretici', 'tester', 'sistemci', 'muhendis', 'musteri']
        loggers = ['tr.com.aselsan.scope.common.business.logging.thread.WriteToConsoleThread',
                       'com.example.project.module.utility.logging.thread.WriteToDatabaseThread',
                       'tr.com.aselsan.scope.common.business.logging.thread.ReadFromConsoleThread',
                       'org.acme.application.service.mail.sendgrid.SendGridMailerService',
                       'com.company.project.util.logging.handler.LogFileHandler',
                       'io.github.user.project.database.repository.PostgreSQLRepository',
                       'net.example.app.module.security.authentication.JwtAuthenticationProvider']
        log_types = ['BUSINESS_LOG', 'Aselsan', 'TEST_LOG']
        services = ['GPY', 'VYX', 'KUZ', 'JAS', 'ZEN', 'FIZ', 'NOX', 'HUV', 'PYT', 'QEV', 'LOK']
        categories = ['GPY', 'TEST','ABC', 'XYZ', 'DEV', 'PROD', 'QA', 'UI', 'BACKEND', 'FRONTEND', 'MOBILE', 'DATABASE']

        filename = os.path.join("logs", f"logjson-{now.strftime('%y%m%d%H%M')}-000.json")
        with open(filename, 'w') as file:

            # Generate N random logs
            i = 0
            num_sentences = int(num_logs_entry.get())
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            while i < num_sentences:
                sentence = model.make_sentence()
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:100] # Generating a random sentence that does not exceed 100 chars
                    log = {
                    "time":date_time_str,
                    "logger":random.choice(loggers),
                    "level":random.choice(levels),
                    "thread":f'scheduling-{random.randint(1, 100)}',
                    "log.time":date_time_str,
                    "log.type":random.choice(log_types),
                    "user.name":random.choice(first_names),
                    "user.username":random.choice(usernames),
                    "user.surname":random.choice(last_names),
                    "source":random.choice(sources),
                    "service":random.choice(services),
                    "category":random.choice(categories),
                    "message":text
                    }
                    json.dump(log, file, separators=(",", ":"))
                    i += 1
                    if i != num_sentences:
                        file.write('\n')

                random_seconds = random.randint(0, 3)   
                random_microseconds = random.randint(0, 999)
                date_time += datetime.timedelta(seconds=random_seconds, microseconds=random_microseconds)
                date_time_str = date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    elif ext == "4j2":
        # Generate a unique integer for each run
        unique_id = random.randint(0, 1000)

        # Open a file to write the logs to
        filename = os.path.join("logs", f"log4j2-{now.strftime('%d-%m-%Y')}-{unique_id}.log")
        with open(filename, 'w') as file:

            # Generate N random logs
            i = 0
            num_sentences = int(num_logs_entry.get())
            generated_sentences = set()
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            while i < num_sentences:
                sentence = model.make_sentence()
                if sentence and sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    text = sentence[:99] # Generating a random sentence that does not exceed 100 chars
                    log = f'{date_time_str} \t {text}'
                    file.write(log)
                    i += 1
                    if i != num_sentences:
                        file.write('\n')

                random_seconds = random.randint(0, 3)
                random_microseconds = random.randint(0, 999)
                date_time += datetime.timedelta(seconds=random_seconds, microseconds=random_microseconds)
                date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            

    if wait_window:
            wait_window.destroy()
            
    # Display "Logs generated successfully"
    messagebox.showinfo("Information","Logs generated successfully!")

    # Re-enable the input fields and the generate button
    num_logs_entry.configure(state='normal')
    generate_button.configure(state='normal')
    num_logs_entry.delete(0, tk.END)

# Define a function to check if all entry fields are filled and enable/disable the Generate button accordingly
def check_fields(*args):
    if not num_logs_entry.get():
        generate_button.configure(state='disabled')
    else:
        generate_button.configure(state='normal')
        
def on_option_select(*args):
    
    # Get the selected option from the StringVar
    selected_format = format_var.get()
    check_format(selected_format)

def check_format(selected_format):
    
    # Do some action based on the selected format
    global num_logs_entry
    global generate_button

    # Destroy all the widgets that have been created in the window
    for widget in window.winfo_children():
        if isinstance(widget, tk.OptionMenu) or widget == img_label or widget == cs_label:
            continue
        widget.destroy()

    # Create the input field for the number of logs to generate
    num_logs_label = tk.Label(window, text="Number of logs to generate:")
    num_logs_label.pack()
    num_logs_entry = tk.Entry(window)
    num_logs_entry.pack()

    # Bind the check_fields() function to the contents of the entry fields
    num_logs_entry.bind("<KeyRelease>", check_fields)
    
    if selected_format == "log":
        generate_button = tk.Button(window, text="Generate", command=lambda: commands("log"), state='disabled')
    elif selected_format == "4j2":
        generate_button = tk.Button(window, text="Generate", command=lambda: commands("4j2"), state='disabled')
    elif selected_format == "json":
        generate_button = tk.Button(window, text="Generate", command=lambda: commands("json"), state='disabled')

    generate_button.pack()

    check_fields()


# Bind the on_option_select function to the formats StringVar
format_var.trace("w", on_option_select)

window.mainloop()

