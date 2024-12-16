import sys
import os
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class SpriteSheetGenerator:
    def __init__(self, cell_width=128, cell_height=128, rows=8, cols=8):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.rows = rows
        self.cols = cols

    def generate(self, gif_path, output_file):
        try:
            gif = Image.open(gif_path)
            frames = []

            # 解码所有帧
            for frame_idx in range(gif.n_frames):
                gif.seek(frame_idx)
                frames.append(gif.copy())

            total_frames = len(frames)
            if total_frames > self.rows * self.cols:
                messagebox.showwarning("帧数超限", f"GIF 包含 {total_frames} 帧，仅处理前 {self.rows * self.cols} 帧。")

            # 创建 Sprite Sheet
            spritesheet = Image.new("RGBA", (self.cols * self.cell_width, self.rows * self.cell_height), (255, 255, 255, 0))
            for idx, frame in enumerate(frames[:self.rows * self.cols]):
                frame.thumbnail((self.cell_width, self.cell_height), Image.Resampling.LANCZOS)
                x = (idx % self.cols) * self.cell_width + (self.cell_width - frame.width) // 2
                y = (idx // self.cols) * self.cell_height + (self.cell_height - frame.height) // 2
                spritesheet.paste(frame, (x, y))

            spritesheet.save(output_file)
        except Exception as e:
            raise RuntimeError(f"生成 Sprite Sheet 错误: {e}")

class SpriteSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRChar Dynamic Emoji Generator")
        self.root.iconphoto(False, self.load_icon('icon.ico'))

        # 固定窗口大小
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.generator = SpriteSheetGenerator()
        self.setup_theme()
        self.setup_ui()

    def load_icon(self, icon_path):
        try:
            path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), icon_path)
            return ImageTk.PhotoImage(Image.open(path))
        except:
            return None

    def setup_theme(self):
        style = ttk.Style(self.root)
        self.root.tk_setPalette(background="#2b2b2b", foreground="#ffffff")
        style.theme_use("clam")
        style.configure("TButton", background="#444", foreground="#fff", font=("Arial", 10))
        style.map("TButton", background=[("active", "#666")])
        style.configure("TLabel", background="#2b2b2b", foreground="#fff")

    def setup_ui(self):
        ttk.Label(self.root, text="选择一个 GIF 文件:").pack(pady=5)
        ttk.Label(root, text="Github: mmyo456/VRChar Dynamic Emoji Generator").pack(pady=10)
        ttk.Button(self.root, text="选择文件", command=self.select_file).pack(pady=5)

        # 参数输入框
        self.vars = {k: tk.IntVar(value=v) for k, v in {"宽度": 128, "高度": 128, "行数": 8, "列数": 8}.items()}
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        for idx, (label, var) in enumerate(self.vars.items()):
            ttk.Label(frame, text=label).grid(row=idx//2, column=2*(idx%2))
            ttk.Entry(frame, textvariable=var, width=10).grid(row=idx//2, column=2*(idx%2)+1)

        self.generate_btn = ttk.Button(self.root, text="生成 Sprite Sheet", command=self.generate_spritesheet, state=tk.DISABLED)
        self.generate_btn.pack(pady=10)

    def select_file(self):
        self.gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if self.gif_path:
            self.generate_btn.config(state=tk.NORMAL)
            messagebox.showinfo("文件已选择", f"已选择文件: {self.gif_path}")

    def generate_spritesheet(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not output_file: return

        try:
            # 更新参数
            self.generator.cell_width = self.vars["宽度"].get()
            self.generator.cell_height = self.vars["高度"].get()
            self.generator.rows = self.vars["行数"].get()
            self.generator.cols = self.vars["列数"].get()
            self.generator.generate(self.gif_path, output_file)
            messagebox.showinfo("成功", f"Sprite Sheet 已保存到: {output_file}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteSheetApp(root)
    root.mainloop()
