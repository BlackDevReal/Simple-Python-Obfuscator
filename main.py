import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
import random
import string
import os


def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def obfuscate_variable_names(code):
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
    obfuscated_names = {}

    def replace_name(match):
        original_name = match.group(0)
        if original_name in dir(__builtins__) or original_name in ['def', 'return', 'import', 'for', 'while', 'if', 'else', 'class']:
            return original_name
        if original_name not in obfuscated_names:
            obfuscated_names[original_name] = random_string()
        return obfuscated_names[original_name]

    obfuscated_code = re.sub(pattern, replace_name, code)
    return obfuscated_code


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if filepath:
        with open(filepath, 'r') as file:
            code = file.read()
            code_input.delete("1.0", tk.END)
            code_input.insert(tk.END, code)
        status_label.config(text=f"Loaded: {os.path.basename(filepath)}")
    else:
        status_label.config(text="No file selected")


def save_file():
    obfuscated_code = code_output.get("1.0", tk.END)
    if not obfuscated_code.strip():
        messagebox.showwarning("No Code", "There is no obfuscated code to save.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if filepath:
        with open(filepath, 'w') as file:
            file.write(obfuscated_code)
        status_label.config(text=f"Saved: {os.path.basename(filepath)}")
    else:
        status_label.config(text="Save canceled")

def obfuscate_code():
    original_code = code_input.get("1.0", tk.END)
    if not original_code.strip():
        messagebox.showwarning("Empty Code", "Please provide code to obfuscate.")
        return
    obfuscated_code = obfuscate_variable_names(original_code)
    code_output.delete("1.0", tk.END)
    code_output.insert(tk.END, obfuscated_code)
    status_label.config(text="Obfuscation complete")


root = tk.Tk()
root.title("Python Code Obfuscator")


root.geometry("800x600")
root.config(padx=10, pady=10)


menubar = tk.Menu(root)
root.config(menu=menubar)


file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save Obfuscated Code", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


obfuscate_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Obfuscate", menu=obfuscate_menu)
obfuscate_menu.add_command(label="Obfuscate Code", command=obfuscate_code)


input_label = tk.Label(root, text="Python Code Input:", font=("Arial", 12))
input_label.pack(pady=5)


code_input = scrolledtext.ScrolledText(root, width=90, height=15)
code_input.pack(pady=10)


output_label = tk.Label(root, text="Obfuscated Code Output:", font=("Arial", 12))
output_label.pack(pady=5)


code_output = scrolledtext.ScrolledText(root, width=90, height=15)
code_output.pack(pady=10)


status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
status_label.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)


root.mainloop()
