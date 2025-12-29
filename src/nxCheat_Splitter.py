import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

# Drag-and-drop support for Windows 10 & 11
try:
    from tkdnd import DND_FILES
    dnd_available = True
except ImportError:
    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        dnd_available = True
    except ImportError:
        dnd_available = False

# ------------------------
# Version
# ------------------------
VERSION = "1.1.0"

# ------------------------
# Utility Functions
# ------------------------

def sanitize_name(name):
    invalid = r'<>:"/\|?*'
    for ch in invalid:
        name = name.replace(ch, "_")
    return name.strip()

def extract_build_id_from_filename(path):
    filename = os.path.basename(path)
    build_id, _ = os.path.splitext(filename)
    return build_id.strip()

def parse_cheats(cheat_text):
    pattern = r"\[([^\]]+)\]\s*([^[]*)"
    matches = re.findall(pattern, cheat_text, flags=re.MULTILINE)
    cleaned = []

    for name, body in matches:
        name = name.strip()
        body = body.strip()

        if not body or "SectionStart" in name or "SectionEnd" in name:
            continue

        cleaned.append((name, body))

    return cleaned

def create_eden_files(build_id, cheats, include_name):
    output_root = os.path.join(build_id)
    os.makedirs(output_root, exist_ok=True)
    created = []

    for cheat_name, cheat_body in cheats:
        safe_name = sanitize_name(cheat_name)
        cheat_folder = os.path.join(output_root, safe_name, "cheats")
        os.makedirs(cheat_folder, exist_ok=True)

        file_path = os.path.join(cheat_folder, f"{build_id}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            if include_name:
                f.write(f"[{cheat_name}]\n")
            f.write(cheat_body)

        created.append(file_path)

    return created

# ------------------------
# GUI Functions
# ------------------------

def main():

    # ------------------------
    # GUI Actions
    # ------------------------

    def load_file(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text_cheats.delete("1.0", tk.END)
                text_cheats.insert(tk.END, f.read())
                text_cheats.configure(fg="black")

            build_id = extract_build_id_from_filename(path)
            entry_buildid.delete(0, tk.END)
            entry_buildid.insert(0, build_id)

            messagebox.showinfo("Loaded", f"Loaded cheats from:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def browse_file():
        path = filedialog.askopenfilename(
            title="Select Cheat File",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            load_file(path)

    def drop_file(event):
        path = event.data.strip("{}")
        if os.path.isfile(path):
            load_file(path)

    def convert_now():
        build_id = entry_buildid.get().strip()
        cheats_text = text_cheats.get("1.0", tk.END).strip()

        if not build_id:
            messagebox.showerror("Error", "No Build ID detected or entered.")
            return

        if not cheats_text or cheats_text.startswith("Paste cheat list here"):
            messagebox.showerror("Error", "Cheat text is empty.")
            return

        cheats = parse_cheats(cheats_text)

        if not cheats:
            messagebox.showerror("Error", "No valid cheat blocks found.")
            return

        created = create_eden_files(
            build_id,
            cheats,
            include_name_var.get()
        )

        messagebox.showinfo(
            "Success",
            f"Created {len(created)} cheat files under:\n{build_id}/"
        )

    # ------------------------
    # Dark Mode Toggle
    # ------------------------

    dark_mode_on = False

    def toggle_dark_mode():
        nonlocal dark_mode_on
        dark_mode_on = not dark_mode_on

        bg = "#1e1e1e" if dark_mode_on else "#f0f0f0"
        fg = "#ffffff" if dark_mode_on else "#000000"
        txt_bg = "#2b2b2b" if dark_mode_on else "white"
        btn_bg = "#3c3c3c" if dark_mode_on else "SystemButtonFace"
        icon = "🌑" if dark_mode_on else "🔆"

        window.configure(bg=bg)
        label_buildid.configure(bg=bg, fg=fg)
        label_cheats.configure(bg=bg, fg=fg)
        checkbox_include_name.configure(bg=bg, fg=fg, selectcolor=bg)
        entry_buildid.configure(bg=txt_bg, fg=fg, insertbackground=fg)
        text_cheats.configure(bg=txt_bg, fg=fg, insertbackground=fg)
        convert_button.configure(bg=btn_bg, fg=fg)
        browse_button.configure(bg=btn_bg, fg=fg)
        darkmode_button.configure(bg=btn_bg, fg=fg, text=icon)

    # ------------------------
    # GUI Setup
    # ------------------------

    if dnd_available and "TkinterDnD" in globals():
        window = TkinterDnD.Tk()
    else:
        window = tk.Tk()

    window.title(f"nxCheat_Splitter v{VERSION}")
    window.geometry("820x650")

    include_name_var = tk.BooleanVar(value=True)

    darkmode_button = tk.Button(window, text="🔆", command=toggle_dark_mode)
    darkmode_button.place(x=770, y=10, width=40, height=30)

    label_buildid = tk.Label(window, text="Build ID:")
    label_buildid.pack(pady=5)

    entry_buildid = tk.Entry(window, width=50)
    entry_buildid.pack(pady=3)

    browse_button = tk.Button(window, text="Browse .txt File", command=browse_file)
    browse_button.pack(pady=5)

    label_cheats = tk.Label(window, text="Cheat Text:")
    label_cheats.pack(pady=5)

    text_cheats = scrolledtext.ScrolledText(window, width=100, height=25, fg="grey")
    text_cheats.pack(pady=5)

    placeholder = (
        "Instructions:\n"
        " • Paste cheat list here\n"
        " • Or drag and drop a cheat file\n"
        " • Or use 'Browse .txt File'\n\n"
        "⚠ Warning: The file must be named BUILDID.txt!"
    )

    text_cheats.insert(tk.END, placeholder)

    def on_focus_in(event):
        if text_cheats.get("1.0", tk.END).strip() == placeholder:
            text_cheats.delete("1.0", tk.END)
            text_cheats.configure(fg="black")

    def on_focus_out(event):
        if text_cheats.get("1.0", tk.END).strip() == "":
            text_cheats.insert(tk.END, placeholder)
            text_cheats.configure(fg="grey")

    text_cheats.bind("<FocusIn>", on_focus_in)
    text_cheats.bind("<FocusOut>", on_focus_out)

    checkbox_include_name = tk.Checkbutton(
        window,
        text="Include cheat name in output file (required for Yuzu-based emulators)",
        variable=include_name_var
    )
    checkbox_include_name.pack(pady=5)

    convert_button = tk.Button(
        window,
        text="Split Cheat File Into Folders",
        command=convert_now,
        height=2
    )
    convert_button.pack(pady=10)

    if dnd_available:
        text_cheats.drop_target_register(DND_FILES)
        text_cheats.dnd_bind("<<Drop>>", drop_file)

    window.mainloop()

if __name__ == "__main__":
    main()
