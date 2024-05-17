import os
import shutil
import json
from datetime import datetime
from icalendar import Calendar, Event
import tkinter as tk
from tkinter import filedialog, messagebox
from appdirs import user_data_dir

# Define application name and author for appdirs
APP_NAME = "cpimerge"
APP_AUTHOR = "Kirk Coombs"

# Get the path to the configuration directory
config_dir = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'config.json')

# Load iCalendar file
def load_ics(file_path):
    try:
        with open(file_path, 'rb') as f:
            return Calendar.from_ical(f.read())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load iCal file: {file_path}\n{e}")
        return None

# Get set of events from calendar
def get_event_set(cal):
    return {
        (str(component.get('summary')), component.get('dtstart').dt, component.get('dtend').dt)
        for component in cal.walk() if component.name == "VEVENT"
    }

# Load exclusions from file
def load_exclusions(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load exclusions file: {file_path}\n{e}")
        return []

# Filter events based on exclusions
def filter_exclusions(events, exclusions, output_text):
    filtered_events = set()
    if exclusions:
        output_text.insert(tk.END, "Excluding:\n")
    for event in events:
        if not any(excl.lower() in event[0].lower() for excl in exclusions):
            filtered_events.add(event)
        else:
            if exclusions:
                output_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
    if exclusions:
        output_text.insert(tk.END, "\n")
    return filtered_events

# Create all-day event
def create_all_day_event(event):
    new_event = Event()
    new_event.add('summary', event[0])
    new_event.add('dtstart', event[1].date())
    new_event.add('dtend', event[2].date())
    new_event.add('dtstamp', datetime.now())
    return new_event

# Create cancellation event
def create_cancel_event(event):
    cancel_event = Event()
    cancel_event.add('summary', event[0])
    cancel_event.add('dtstart', event[1].date())
    cancel_event.add('dtend', event[2].date())
    cancel_event.add('dtstamp', datetime.now())
    cancel_event.add('status', 'CANCELLED')
    return cancel_event

# Backup file
def backup_file(file_path):
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    shutil.copy2(file_path, backup_path)
    return backup_path

# Main function to merge calendars
def main(ics1_path, ics2_path, exclusions_path, output_path, output_text, rename_ics2):
    try:
        if os.path.exists(ics1_path):
            backup_ics1_path = backup_file(ics1_path)
            output_text.insert(tk.END, f"Backup of '{ics1_path}' created: {backup_ics1_path}\n")
            cal1 = load_ics(ics1_path)
        else:
            output_text.insert(tk.END, f"No ics1 provided. Using an empty iCal.\n")
            cal1 = Calendar()
        if os.path.exists(ics2_path):
            backup_ics2_path = backup_file(ics2_path)
            output_text.insert(tk.END, f"Backup of '{ics2_path}' created: {backup_ics2_path}\n")
            cal2 = load_ics(ics2_path)
               
        if cal1 is None and cal2 is None:
            return

        exclusions = load_exclusions(exclusions_path) if exclusions_path else []

        if exclusions:
            output_text.insert(tk.END, f"\nExclusions from '{exclusions_path}':\n")
            for excl in exclusions:
                output_text.insert(tk.END, f"  - '{excl}'\n")
            output_text.insert(tk.END, "\n")

        events1 = get_event_set(cal1) if cal1 else set()
        events2 = get_event_set(cal2)
        unique_events_ics2 = events2 - events1
        unique_events_ics1 = events1 - events2

        filtered_events = filter_exclusions(unique_events_ics2, exclusions, output_text)

        output_cal = Calendar()
        for event in filtered_events:
            output_cal.add_component(create_all_day_event(event))

        with open(output_path, 'wb') as f:
            f.write(output_cal.to_ical())

        if cal1:
            removals_cal = Calendar()
            for event in unique_events_ics1:
                removals_cal.add_component(create_cancel_event(event))

            output_text.insert(tk.END, f"Consider removing the following events from your calendar. They existed in '{ics1_path}' but are not in '{ics2_path}' and thus may no longer be relevant:\n")
            for event in sorted(unique_events_ics1, key=lambda x: x[1]):
                output_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")
        else:
            output_text.insert(tk.END, "First run detected. No removals suggested.\n")

        output_text.insert(tk.END, f"\n\nThere are {len(filtered_events)} event(s) in '{ics2_path}' that do not exist in '{ics1_path}'. They will be merged into '{output_path}':\n")
        for event in sorted(filtered_events, key=lambda x: x[1]):
            output_text.insert(tk.END, f"  - {event[0]} on {event[1].date()}\n")

        if rename_ics2:
            os.rename(ics2_path, ics1_path)
            output_text.insert(tk.END, f"Renamed {ics2_path} to {ics1_path} for the next run.\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the merge process: {e}")

#Function to set text color in the output_text widget
def insert_text_with_color(text_widget, text, color):
    text_widget.tag_configure(color, foreground=color)
    text_widget.insert(tk.END, text, color)

# Function to load files and display information
def load_files():
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()

    if ics1_path and not os.path.exists(ics1_path):
        messagebox.showerror("Error", f"File not found (ics1): {ics1_path}")
        return
    
    if not ics2_path:
        messagebox.showerror("Error", "ics2 file must be provided")
        return

    if not os.path.exists(ics2_path):
        messagebox.showerror("Error", f"File not found (ics2): {ics2_path}")
        return

    if exclusions_path and not os.path.exists(exclusions_path):
        messagebox.showerror("Error", f"File not found (exclusion): {exclusions_path}")
        return

    output_text.delete(1.0, tk.END)

    if ics1_path:
        cal1 = load_ics(ics1_path)
    else:
        output_text.insert(tk.END, f"No ics1 provided. Using an empty iCal.\n")
        cal1 = Calendar()
    cal2 = load_ics(ics2_path)
    exclusions = load_exclusions(exclusions_path) if exclusions_path else []

    if cal2 is None:
        return

    events1 = get_event_set(cal1) if cal1 else set()
    events2 = get_event_set(cal2)

    earliest_event_ics1 = (min(events1, key=lambda x: x[1])[1]).date() if events1 else None
    latest_event_ics1 = (max(events1, key=lambda x: x[1])[1]).date() if events1 else None
    earliest_event_ics2 = (min(events2, key=lambda x: x[1])[1]).date() if events2 else None
    latest_event_ics2 = (max(events2, key=lambda x: x[1])[1]).date() if events2 else None

    output_text.insert(tk.END, f"ics1: {len(events1)} events\n")
    if earliest_event_ics1 and latest_event_ics1:
        output_text.insert(tk.END, f"Earliest event in ics1: {earliest_event_ics1}\n")
        output_text.insert(tk.END, f"Latest event in ics1: {latest_event_ics1}\n")

    if cal2:
        output_text.insert(tk.END, f"\nics2: {len(events2)} events\n")
        if earliest_event_ics2 and latest_event_ics2:
            output_text.insert(tk.END, f"Earliest event in ics2: {earliest_event_ics2}\n")
            output_text.insert(tk.END, f"Latest event in ics2: {latest_event_ics2}\n")

        if earliest_event_ics2 and earliest_event_ics1 and earliest_event_ics2 < earliest_event_ics1:
            insert_text_with_color(output_text, "Warning: ics2 has events before the earliest event in ics1\n", "Red")
        if latest_event_ics2 and latest_event_ics1 and latest_event_ics1 > latest_event_ics2:
            insert_text_with_color(output_text, "Warning: ics1 has events after the latest event in ics2\n", "Red")

    if exclusions:
        output_text.insert(tk.END, f"\nExclusions:\n")
        for excl in exclusions:
            output_text.insert(tk.END, f"  - '{excl}'\n")

# File selection dialog
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Output file selection dialog
def select_output_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Show description in a new window
def show_description(description):
    description_window = tk.Toplevel(root)
    description_window.title("Description")
    description_window.geometry("400x300")
    description_window.resizable(False, False)
    description_window.transient(root)
    description_window.grab_set()
    description_window.overrideredirect(True)

    frame = tk.Frame(description_window, bd=2, relief=tk.RAISED)
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text=description, wraplength=380, justify=tk.LEFT)
    label.pack(padx=10, pady=10)

    close_button = tk.Button(frame, text="Close", command=description_window.destroy)
    close_button.pack(pady=10)

# Run merge process
def run_merge():
    ics1_path = ics1_entry.get()
    ics2_path = ics2_entry.get()
    exclusions_path = exclusions_entry.get()
    output_path = output_entry.get()
    rename_ics2 = rename_var.get()

    if not all([ics2_path, output_path]):
        messagebox.showerror("Error", "ics2 and output file fields must be filled out")
        return

    if ics1_path and not os.path.exists(ics1_path):
        messagebox.showerror("Error", f"File not found: {ics1_path}")
        return

    if not os.path.exists(ics2_path):
        messagebox.showerror("Error", f"File not found: {ics2_path}")
        return

    if exclusions_path and not os.path.exists(exclusions_path):
        messagebox.showerror("Error", f"File not found: {exclusions_path}")
        return

    output_text.delete(1.0, tk.END)
    main(ics1_path, ics2_path, exclusions_path if exclusions_path else None, output_path, output_text, rename_ics2)
    output_text.insert(tk.END, f"\nCalendars merged successfully.\n\n** You can now import the new events from {output_path} **")

    # Save the configuration
    config = {
        "ics1_path": ics1_path,
        "ics2_path": ics2_path,
        "exclusions_path": exclusions_path,
        "output_path": output_path
    }
    save_config(config)

# Load configuration from file
def load_config():
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load configuration file: {e}")
        return {}

# Save configuration to file
def save_config(config):
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save configuration file: {e}")

# Load initial configuration
config = load_config()

# Initialize GUI
root = tk.Tk()
root.title("CPI iCal Merger")

# GUI elements
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Previous iCal Export (ics1) (optional):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ics1_entry = tk.Entry(frame, width=50)
ics1_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
ics1_entry.insert(0, config.get("ics1_path", ""))
tk.Button(frame, text="Browse", command=lambda: select_file(ics1_entry)).grid(row=0, column=2, padx=10, pady=5)
tk.Button(frame, text="?", command=lambda: show_description("The iCal (.ics) file you used for the previous run of this tool.\n\nThis file will automatically be backed-up.\n\nIf no file, or an invalid file, is provided, an empty iCal with no events will be used. This useful for the first run of this program.")).grid(row=0, column=3, padx=10, pady=5)

tk.Label(frame, text="New iCal Export (ics2):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
ics2_entry = tk.Entry(frame, width=50)
ics2_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
ics2_entry.insert(0, config.get("ics2_path", ""))
tk.Button(frame, text="Browse", command=lambda: select_file(ics2_entry)).grid(row=1, column=2, padx=10, pady=5)
tk.Button(frame, text="?", command=lambda: show_description("The new iCal (.ics) file that you'd like to get events from.\n\nThis file will automatically be backed-up.\n\nIf 'Rename ics2 to ics1 after merging' is checked, the file provided in this field will be renamed to the name provided for the ics1 file (e.g., for use in the next run of this program).")).grid(row=1, column=3, padx=10, pady=5)

tk.Label(frame, text="Exclusions File (optional):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
exclusions_entry = tk.Entry(frame, width=50)
exclusions_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
exclusions_entry.insert(0, config.get("exclusions_path", ""))
tk.Button(frame, text="Browse", command=lambda: select_file(exclusions_entry)).grid(row=2, column=2, padx=10, pady=5)
tk.Button(frame, text="?", command=lambda: show_description("An optional file containing sub-strings, one per line. When matched, these sub-strings will cause an event to be excluded from the output.")).grid(row=2, column=3, padx=10, pady=5)

tk.Label(frame, text="Output File:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W+tk.E)
output_entry.insert(0, config.get("output_path", ""))
tk.Button(frame, text="Browse", command=lambda: select_output_file(output_entry)).grid(row=3, column=2, padx=10, pady=5)
tk.Button(frame, text="?", command=lambda: show_description("An output iCal (.ics) file, which will contain any new events. This can be imported into to your calendar.")).grid(row=3, column=3, padx=10, pady=5)

rename_var = tk.BooleanVar(value=False)
rename_checkbox = tk.Checkbutton(frame, text="Rename ics2 to ics1 after merging", variable=rename_var)
rename_checkbox.grid(row=4, column=0, columnspan=4, pady=5)

button_frame = tk.Frame(frame)
button_frame.grid(row=5, column=0, columnspan=4, pady=20)

tk.Button(button_frame, text="Load", command=load_files).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Merge", command=run_merge).pack(side=tk.LEFT, padx=10)

output_frame = tk.Frame(frame)
output_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

output_text = tk.Text(output_frame, height=30, width=100)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)

# Make the grid cells expand with window resizing
frame.grid_rowconfigure(6, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
