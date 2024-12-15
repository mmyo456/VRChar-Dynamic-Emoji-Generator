import sys
import os
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class SpriteSheetGenerator:
    def __init__(self, cell_width=128, cell_height=128, rows=8, cols=8):
        self.cell_width = cell_width  # 单元格宽度
        self.cell_height = cell_height  # 单元格高度
        self.rows = rows  # 行数
        self.cols = cols  # 列数

    def generate_spritesheet(self, gif_path, output_file):
        try:
            gif = Image.open(gif_path)
            frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
            total_frames = len(frames)

            if total_frames > self.rows * self.cols:
                messagebox.showwarning(
                    "帧数超限", f"GIF 包含 {total_frames} 帧，仅会处理前 {self.rows * self.cols} 帧。"
                )

            # 计算Sprite Sheet画布大小
            sheet_width = self.cols * self.cell_width
            sheet_height = self.rows * self.cell_height
            spritesheet = Image.new("RGBA", (sheet_width, sheet_height), (255, 255, 255, 0))

            for idx, frame in enumerate(frames[:self.rows * self.cols]):
                # 缩放帧到单元格大小（保持比例）
                frame.thumbnail((self.cell_width, self.cell_height), Image.Resampling.LANCZOS)

                # 计算居中偏移量
                x_offset = (self.cell_width - frame.width) // 2
                y_offset = (self.cell_height - frame.height) // 2

                # 计算单元格位置
                row = idx // self.cols
                col = idx % self.cols
                x = col * self.cell_width + x_offset
                y = row * self.cell_height + y_offset

                # 将帧粘贴到画布
                spritesheet.paste(frame, (x, y))

            spritesheet.save(output_file)
            print(f"Sprite Sheet 已保存为 {output_file}")
        except Exception as e:
            raise RuntimeError(f"生成Sprite Sheet时发生错误: {e}")


class SpriteSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRChar Dynamic Emoji Generator")

        # 设置应用图标，使用资源路径获取
        icon_path = self.resource_path('icon.ico')
        try:
            img = Image.open(icon_path)
            self.root.iconphoto(False, ImageTk.PhotoImage(img))  # 适用于跨平台
        except Exception as e:
            print(f"图标加载失败: {e}")  # 打印错误以便调试

        self.generator = SpriteSheetGenerator()
        self.gif_path = None

        # 应用 ttk 自定义样式
        self.apply_theme()

        # 界面布局
        ttk.Label(root, text="选择一个 GIF 文件:").pack(pady=10)
        ttk.Label(root, text="Github: mmyo456/VRChar Dynamic Emoji Generator").pack(pady=10)

        self.select_button = ttk.Button(root, text="选择文件", command=self.select_file)
        self.select_button.pack(pady=5)

        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="单元格宽度:").grid(row=0, column=0, padx=5)
        self.cell_width_var = tk.IntVar(value=128)
        ttk.Entry(frame, textvariable=self.cell_width_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="单元格高度:").grid(row=1, column=0, padx=5)
        self.cell_height_var = tk.IntVar(value=128)
        ttk.Entry(frame, textvariable=self.cell_height_var, width=10).grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="行数:").grid(row=0, column=2, padx=5)
        self.rows_var = tk.IntVar(value=8)
        ttk.Entry(frame, textvariable=self.rows_var, width=10).grid(row=0, column=3, padx=5)

        ttk.Label(frame, text="列数:").grid(row=1, column=2, padx=5)
        self.cols_var = tk.IntVar(value=8)
        ttk.Entry(frame, textvariable=self.cols_var, width=10).grid(row=1, column=3, padx=5)

        self.generate_button = ttk.Button(root, text="生成 Sprite Sheet", command=self.generate_spritesheet, state=tk.DISABLED)
        self.generate_button.pack(pady=10)

    def resource_path(self, relative_path):
        """获取打包后应用的资源文件路径"""
        try:
            # 如果是打包成 .exe 文件
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        except Exception as e:
            print(f"获取资源路径时出错: {e}")
            return relative_path

    def apply_theme(self):
        """应用自定义的暗色 ttk 样式"""
        style = ttk.Style(self.root)
        self.root.tk_setPalette(background="#2b2b2b", foreground="#ffffff")

        style.theme_use("clam")  # 使用 ttk 的基础主题
        style.configure(
            "TButton",
            background="#444444",
            foreground="#ffffff",
            font=("Arial", 10),
            borderwidth=1,
            focuscolor="#555555",
        )
        style.map(
            "TButton",
            background=[("active", "#666666")],
            foreground=[("disabled", "#888888")],
        )
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Arial", 10))

    def select_file(self):
        self.gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if self.gif_path:
            self.generate_button.config(state=tk.NORMAL)
            messagebox.showinfo("文件已选择", f"已选择文件: {self.gif_path}")

    def generate_spritesheet(self):
        if not self.gif_path:
            messagebox.showwarning("输入错误", "请选择一个有效的文件！")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not output_file:
            return

        try:
            self.generator.cell_width = self.cell_width_var.get()
            self.generator.cell_height = self.cell_height_var.get()
            self.generator.rows = self.rows_var.get()
            self.generator.cols = self.cols_var.get()

            self.generator.generate_spritesheet(self.gif_path, output_file)
            messagebox.showinfo("成功", f"Sprite Sheet 已保存到: {output_file}")
        except Exception as e:
            messagebox.showerror("错误", f"生成 Sprite Sheet 时出错: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteSheetApp(root)
    root.mainloop()
