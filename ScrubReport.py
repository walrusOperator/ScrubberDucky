import tkinter as tk
from tkinter import scrolledtext
from unidecode import unidecode
import pyperclip
import os
from redlines import Redlines
import webbrowser


basedir = os.path.dirname(__file__)
try:
    from ctypes import windll  # Only exists on Windows

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
except Exception as e:
    print(f"An error occurred setting AppUserModelID: {e}")

def scrub_text():
    try:
        origin_text = text_area.get("1.0", tk.END).strip()
        if origin_text and origin_text != placeholder:
            # Replace used here to replace any instances of £ with GBP before text is run through unidecode
            fixed_text = text_scrubber(origin_text.replace('£', 'GBP'))
            redlines = Redlines(origin_text, fixed_text)
            save_temp_html(redlines)
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", fixed_text)
            message_label.config(text="Text has been scrubbed and replaced in the text area", fg="green")
        else:
            message_label.config(text="Please enter some text to scrub", fg="red")
    except Exception as e:
        message_label.config(text=f"An error occurred: {e}", fg="red")


def save_temp_html(redline):
    try:
        html_diff = redline.output_markdown  # Retrieve the Markdown output from the redline object

        # HTML template with CSS to preserve whitespace
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                pre {{
                    white-space: pre-wrap; /* CSS to preserve whitespace */
                    font-family: monospace; /* Use a monospace font for better formatting */
                }}
            </style>
            <title>Text Difference Report</title>
        </head>
        <body>
            <pre>{html_diff}</pre>
        </body>
        </html>
        """

        html_file = 'diff_output.html'  # Define the filename
        with open(html_file, 'w', encoding='utf-8') as file:  # Open the file in write mode with UTF-8 encoding
            file.write(html_content)  # Write the HTML content to the file

        message_label.config(text="HTML file has been saved successfully", fg="green")
    except Exception as e:
        message_label.config(text=f"Error saving HTML file: {e}", fg="red")


def view_report():
    webbrowser.open(f'file://{os.path.realpath('diff_output.html')}')

def clear_text_area():
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", placeholder)
    text_area.config(fg="gray")

def text_scrubber(text):
    try:
        return unidecode(text)
    except Exception as e:
        message_label.config(text=f"Error in text_scrubber: {e}", fg="red")
        return text

# Method not currently implemented
def import_from_clipboard():
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        message_label.config(text=f"Error importing from clipboard: {e}", fg="red")
        return ""
    except Exception as e:
        message_label.config(text=f"Unexpected error importing from clipboard: {e}", fg="red")
        return ""

def save_to_clipboard():
    try:
        pyperclip.copy(text_area.get("1.0", tk.END).strip())
        message_label.config(text="Text has been copied to clipboard", fg="green")
    except pyperclip.PyperclipException as e:
        message_label.config(text=f"Error saving to clipboard: {e}", fg="red")
    except Exception as e:
        message_label.config(text=f"Unexpected error saving to clipboard: {e}", fg="red")

def close_app():
    root.destroy()

def on_focus_in(event):
    if text_area.get("1.0", tk.END).strip() == placeholder:
        text_area.delete("1.0", tk.END)
        text_area.config(fg="black")

def on_focus_out(event):
    if not text_area.get("1.0", tk.END).strip():
        text_area.insert("1.0", placeholder)
        text_area.config(fg="gray")

def on_key_press(event):
    if text_area.get("1.0", tk.END).strip() == placeholder:
        text_area.delete("1.0", tk.END)
        text_area.config(fg="black")
    text_area.unbind("<KeyPress>", on_key_press)

# Create the main window
root = tk.Tk()
root.title("TOPPAN MERRILL | Scrubber Ducky")
root.geometry("500x350")
root.resizable(False, False)  # Disable resizing of the window

try:
    root.iconbitmap(os.path.join(basedir, "rubberduck.ico"))
except Exception as e:
    print(f"An error occurred setting the icon: {e}")

placeholder = "Paste your text to scrub here"
# Create a scrolled text area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=15)
text_area.pack(pady=5)
text_area.insert("1.0", placeholder)
text_area.config(fg="gray")
text_area.bind("<FocusIn>", on_focus_in)
text_area.bind("<FocusOut>", on_focus_out)
text_area.bind("<KeyPress>", on_key_press)

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Create a button to scrub text and copy to clipboard
scrub_button = tk.Button(button_frame, text="Scrub Text", command=scrub_text)
scrub_button.pack(side=tk.LEFT, padx=5)

report_button = tk.Button(button_frame, text="View Report", command=view_report)
report_button.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=save_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5)

# Create a button to clear the text area
clear_button = tk.Button(button_frame, text="Clear", command=clear_text_area)
clear_button.pack(side=tk.LEFT, padx=5)

# Create a button to close the app
close_button = tk.Button(button_frame, text="Close", command=close_app)
close_button.pack(side=tk.LEFT, padx=5)

# Create a label to display messages
message_label = tk.Label(root, text="", wraplength=400)
message_label.pack(pady=5)

# Start the main loop
root.mainloop()
