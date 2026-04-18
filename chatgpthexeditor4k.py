#!/usr/bin/env python3
# ============================================================
# Chatgpt's Hex Editor Tkinter
# Universal Binary Hex Editor
# ============================================================

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class HexEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatgpt's hex editor tkinter")
        self.root.geometry("900x600")

        self.data = bytearray()
        self.filepath = None

        self.text = scrolledtext.ScrolledText(
            root,
            font=("Consolas", 11),
            bg="#111",
            fg="#00ff99",
            insertbackground="white"
        )
        self.text.pack(fill="both", expand=True)

        bar = tk.Frame(root)
        bar.pack(fill="x")

        tk.Button(bar, text="Open", command=self.open_file).pack(side="left")
        tk.Button(bar, text="Save", command=self.save_file).pack(side="left")
        tk.Button(bar, text="Save As", command=self.save_as).pack(side="left")
        tk.Button(bar, text="Reload View", command=self.render).pack(side="left")

        self.status = tk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill="x")

        self.text.bind("<KeyRelease>", self.on_edit)

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        with open(path, "rb") as f:
            self.data = bytearray(f.read())

        self.filepath = path
        self.render()
        self.status.config(text=f"Loaded: {path}")

    def save_file(self):
        if not self.filepath:
            return self.save_as()
        self.write(self.filepath)
        self.status.config(text=f"Saved: {self.filepath}")

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if not path:
            return
        self.filepath = path
        self.write(path)
        self.status.config(text=f"Saved As: {path}")

    def write(self, path):
        try:
            with open(path, "wb") as f:
                f.write(self.data)
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def render(self):
        self.text.delete("1.0", tk.END)

        if not self.data:
            self.text.insert(tk.END, "No file loaded.\n")
            return

        for i in range(0, len(self.data), 16):
            chunk = self.data[i:i+16]
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            self.text.insert(tk.END, f"{i:08X}  {hex_part:<48}  {ascii_part}\n")

    def on_edit(self, event=None):
        # simple overwrite parser (basic)
        content = self.text.get("1.0", tk.END).splitlines()
        new_data = bytearray()

        try:
            for line in content:
                if len(line) < 10:
                    continue
                parts = line.split()
                hex_bytes = parts[1:17]
                for hb in hex_bytes:
                    new_data.append(int(hb, 16))

            self.data = new_data
            self.status.config(text="Edited (unsaved changes)")
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    HexEditor(root)
    root.mainloop()
