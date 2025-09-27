# AutoYolo 全自动标注工作室

AutoYolo 是基于 Ultralytics YOLOv8 与 SAM 流程经验重新设计的桌面标注工具，专为 RTX 50 系列等全新 GPU 准备，默认集成了 DirectML 回退与现代化的深色界面。

![界面预览](../image/ui_preview.png)

## 功能亮点
- 🖼️ **极简工作流**：导入图片文件夹即可浏览与管理标注，实时展示文件名、进度与结果。
- ⚡ **自动标注**：一键调用 YOLOv8 预训练模型生成检测框，可批量处理整个数据集。
- 🧠 **智能设备选择**：优先使用 CUDA，如果遇到 RTX 5060 等暂未被官方 wheel 支持的 GPU，则自动切换到 `torch-directml`，仍可发挥显卡算力。
- 📦 **YOLO 原生格式**：生成的标签直接以 YOLO txt 形式保存，随时导入 Ultralytics 训练脚本。
- 🎨 **现代界面**：基于 PySide6 + 自定义深色主题，操作信息一目了然。

## 快速开始
```bash
# 1. 创建并激活 Conda 环境
conda env create -f environment.yml
conda activate autoyolo

# 2. 下载 YOLOv8n 权重（首次运行自动下载）
# 3. 启动应用
python -m AutoYolo.app
```

> 💡 **提示**：如果你使用 RTX 5060 等 Blackwell 架构显卡，请确保已经安装 [torch-directml](https://github.com/microsoft/torch-directml)。环境文件已经自动包含该依赖，PyTorch wheel 不支持的 GPU 将自动回退到 DirectML。

## 目录结构
```
AutoYolo/
├── AutoYolo/
│   ├── app.py              # 程序入口
│   ├── core/               # 设备检测与数据集管理
│   ├── models/             # YOLO 推理封装
│   └── ui/                 # PySide6 界面组件
├── environment.yml         # Conda 环境
└── requirements.txt        # pip 依赖
```

## 常见问题
### 1. 为什么第一次运行会卡在下载模型？
Ultralytics 会自动下载 `yolov8n.pt` 权重，请保持网络畅通或提前手动下载后放到 `~/.cache/ultralytics/`。

### 2. 如何自定义阈值或模型？
在右侧面板调整置信度即可；若希望替换模型，可在 `AutoYolo/ui/main_window.py` 的 `AutoLabeler` 初始化处更换权重文件路径。

### 3. 数据集保存在哪里？
标注会直接写在图片同级目录下的 `*.txt` 文件中，格式遵循 YOLO 标准。
