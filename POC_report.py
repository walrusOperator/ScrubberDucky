from redlines import Redlines
import webbrowser
import os

# Define your strings
string1 = "This is the original string."
string2 = "This is the modified string."

# Compare strings using Redlines
redline = Redlines(string1, string2)

# Get the HTML representation of the differences
html_diff = redline.output_markdown

# Save the HTML to a file
html_file = 'diff_output.html'
with open(html_file, 'w') as file:
    file.write(html_diff)

# Open the HTML file in the default web browser
webbrowser.open(f'file://{os.path.realpath(html_file)}')
