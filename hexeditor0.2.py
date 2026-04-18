#!/usr/bin/env python3
# ============================================================
# ChatGPT's Hex Editor
# ============================================================

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

BYTES_PER_LINE = 16


class HexEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT's Hex Editor")
        self.root.geometry("900x600")

        self.data = bytearray()

        top = tk.Frame(root)
        top.pack(fill="x")

        tk.Button(top, text="Open File", command=self.open_file).pack(side="left")
        tk.Button(top, text="Save File", command=self.save_file).pack(side="left")
        tk.Button(top, text="Reload", command=self.render).pack(side="left")

        self.text = scrolledtext.ScrolledText(
            root,
            font=("Consolas", 11),
            bg="#0a0a0a",
            fg="#00ff88",
            insertbackground="white"
        )
        self.text.pack(fill="both", expand=True)

        self.status = tk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill="x")

        self.render()

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        with open(path, "rb") as f:
            self.data = bytearray(f.read())

        self.root.title("ChatGPT's Hex Editor")
        self.status.config(text=f"Loaded {len(self.data)} bytes")
        self.render()

    def save_file(self):
        path = filedialog.asksaveasfilename()
        if not path:
            return

        try:
            with open(path, "wb") as f:
                f.write(self.data)
            self.status.config(text="File saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def render(self):
        self.text.delete("1.0", tk.END)

        for i in range(0, len(self.data), BYTES_PER_LINE):
            chunk = self.data[i:i + BYTES_PER_LINE]

            hex_part = " ".join(f"{b:02X}" for b in chunk)
            ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

            self.text.insert(tk.END, f"{i:08X}  {hex_part:<48}  {ascii_part}\n")

    def apply_edit(self):
        content = self.text.get("1.0", tk.END).splitlines()

        new_data = bytearray()

        for line in content:
            parts = line.split()
            if len(parts) < 2:
                continue

            for hb in parts[1:17]:
                try:
                    new_data.append(int(hb, 16))
                except:
                    pass

        self.data = new_data
        self.status.config(text=f"Edited buffer size: {len(self.data)} bytes")


if __name__ == "__main__":
    root = tk.Tk()
    app = HexEditor(root)

    root.bind("<Control-s>", lambda e: app.apply_edit())

    root.mainloop()
