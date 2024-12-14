# VRChat-GIF-to-Sprite-Sheet
## 项目简介
**VRChat-GIF-to-Sprite-Sheet** 是一个简单易用的工具，能够将 GIF 动画拆分为多帧，并将这些帧整齐排列到一个固定网格中，生成 **精灵表 (Sprite Sheet)**方便您上传到VRChat自定义表情
## 功能特点
- **从 GIF 动画中提取帧**：自动解析 GIF 动画，提取其中的帧图像。
- **网格布局固定**：生成的精灵表固定为 **8 行 8 列**，共 64 个单元格。
- **支持透明背景**：单元格未使用的部分会保持透明。
- **用户友好的图形界面 (GUI)**：通过图形化界面操作，无需代码编辑。

---

## 运行环境
- **Python 版本**：Python 3.8 及以上  
- **依赖库**：
  - `Pillow`：用于图像处理。
  - `tkinter`：用于构建图形用户界面。

### 安装依赖
运行以下命令安装所需依赖：
```bash
pip install pillow
```
---

### 上传教程
**[VRChat Emoji上传页面](https://vrchat.com/home/gallery/emoji)**
点击**Upload a New Emoji**并勾选**Enable Sprite Sheet Mode**然后选择你刚导出的Sprite Sheet
- **Frames**：请结合自身上传的Sprite Sheet有多少帧动画填写
- **FPS**：按自身需求调节动画速度
当调节到自己满意的状态时即可点击**Next**上传

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=mmyo456/VRChat-GIF-to-Sprite-Sheet&type=Date)](https://star-history.com/#mmyo456/VRChat-GIF-to-Sprite-Sheet&Date)
