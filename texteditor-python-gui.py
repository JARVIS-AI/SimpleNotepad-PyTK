import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font, colorchooser
import re

def create_new_window():
    new_window = tk.Toplevel(app)
    new_window.title("Untitled - New Window")
    text_area = tk.Text(new_window, wrap="word", undo=True, font=current_font)
    text_area.pack(expand=True, fill="both", padx=2.5, pady=2.5)  # Added padding
    menu = tk.Menu(new_window)
    new_window.config(menu=menu)
    create_menus(menu, text_area)
    add_syntax_highlighting(text_area)
    highlight_current_line(text_area)

def create_menus(menu, text_area):
    file_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=create_new_window)
    file_menu.add_command(label="Open...", command=lambda: open_file(text_area))
    file_menu.add_command(label="Save", command=lambda: save_file(text_area))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)

    edit_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Undo", command=text_area.edit_undo)
    edit_menu.add_command(label="Redo", command=text_area.edit_redo)
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", command=lambda: cut_text(text_area))
    edit_menu.add_command(label="Copy", command=lambda: copy_text(text_area))
    edit_menu.add_command(label="Paste", command=lambda: paste_text(text_area))
    edit_menu.add_separator()
    edit_menu.add_command(label="Find and Replace", command=lambda: find_and_replace(text_area))

    font_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Font", menu=font_menu)
    font_menu.add_command(label="Change Font Size", command=lambda: change_font_size(text_area))
    font_menu.add_command(label="Change Font Family", command=lambda: change_font_family(text_area))
    font_menu.add_command(label="Change Font Color", command=lambda: change_font_color(text_area))

    statistics_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Statistics", menu=statistics_menu)
    statistics_menu.add_command(label="Count Letters, Words, and Lines", command=lambda: count_statistics(text_area))

    about_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="About", menu=about_menu)
    about_menu.add_command(label="About App", command=show_about)

def open_file(text_area):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)

def save_file(text_area):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            content = text_area.get(1.0, tk.END)
            file.write(content)
        messagebox.showinfo("Save", "File saved successfully!")

def cut_text(text_area):
    text_area.event_generate("<<Cut>>")

def copy_text(text_area):
    text_area.event_generate("<<Copy>>")

def paste_text(text_area):
    text_area.event_generate("<<Paste>>")

def find_and_replace(text_area):
    find_text = simpledialog.askstring("Find", "Enter text to find:")
    replace_text = simpledialog.askstring("Replace", "Enter text to replace with:")
    if find_text and replace_text:
        content = text_area.get(1.0, tk.END)
        new_content = content.replace(find_text, replace_text)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, new_content)
        messagebox.showinfo("Find and Replace", f"Replaced all occurrences of '{find_text}' with '{replace_text}'.")

def change_font_size(text_area):
    size = simpledialog.askinteger("Font Size", "Enter font size:")
    if size:
        current_font.configure(size=size)
        text_area.configure(font=current_font)

def change_font_family(text_area):
    family = simpledialog.askstring("Font Family", "Enter font family (e.g., Arial, Courier):")
    if family:
        current_font.configure(family=family)
        text_area.configure(font=current_font)

def change_font_color(text_area):
    color = colorchooser.askcolor()[1]
    if color:
        text_area.configure(fg=color)

def add_syntax_highlighting(text_area):
    keywords = ["def", "class", "if", "else", "try", "except", "import", "from", "return", "for", "while"]
    highlight_color = "#ff8800"
    text_area.tag_configure("keyword", foreground=highlight_color)

    def highlight_keywords(event=None):
        content = text_area.get("1.0", tk.END)
        for word in keywords:
            start_idx = "1.0"
            while True:
                start_idx = text_area.search(r"\b" + word + r"\b", start_idx, tk.END, regexp=True)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(word)}c"
                text_area.tag_add("keyword", start_idx, end_idx)
                start_idx = end_idx

    text_area.bind("<KeyRelease>", highlight_keywords)

def highlight_current_line(text_area):
    text_area.tag_configure("current_line", background="#e8e8e8")

    def update_current_line(event=None):
        text_area.tag_remove("current_line", "1.0", tk.END)
        current_line = text_area.index("insert").split(".")[0]
        text_area.tag_add("current_line", f"{current_line}.0", f"{current_line}.end")

    text_area.bind("<KeyRelease>", update_current_line)
    text_area.bind("<ButtonRelease-1>", update_current_line)

def count_statistics(text_area):
    content = text_area.get(1.0, tk.END)
    letter_count = len([char for char in content if char.isalpha()])
    word_count = len([word for word in content.split() if word.strip()])
    line_count = content.count('\n')

    messagebox.showinfo("Statistics", f"Letters: {letter_count}\nWords: {word_count}\nLines: {line_count}")

def show_about():
    messagebox.showinfo("About App", "Enhanced Text Editor\nDeveloped by Amir Mohammad Safari\n\n\nVersion 1.0.8\n")

app = tk.Tk()
app.title("Enhanced Text Editor")

current_font = font.Font(family="Helvetica", size=12)
text_area = tk.Text(app, wrap="word", undo=True, font=current_font)
text_area.pack(expand=True, fill="both", padx=2.5, pady=2.5)  # Added padding here
menu = tk.Menu(app)
app.config(menu=menu)
create_menus(menu, text_area)
add_syntax_highlighting(text_area)
highlight_current_line(text_area)

app.mainloop()
