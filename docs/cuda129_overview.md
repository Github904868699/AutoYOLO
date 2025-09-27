# LabelQuick CUDA 12.9 版简介

本说明面向希望在 NVIDIA RTX 50 系列（如 RTX 5060）上运行 LabelQuick 的用户，概述项目提供的核心功能、依赖要求以及推荐的工作流。

## 核心特性
- **SAM2 一键分割**：针对图像与视频帧预先缓存特征，左键点击即可生成前景掩膜并转换为 VOC/YOLO 标注框。
- **多格式导出**：同名 `.xml` 与 `.txt` 将同步写入，`classes.txt` 自动维护类别索引，方便直接迁移到 Ultralytics YOLO8/YOLO11 训练流程。
- **视频辅助标注**：提供帧抽取、播放控制与目标跟踪工具，显著提升视频标注效率。
- **自动设备识别**：程序启动时优先使用 GPU，并在检测到 CUDA 不可用时回退到 CPU，同时允许通过环境变量 `SAM_DEVICE` 手动指定。

## 环境要求
- 操作系统：Windows 10/11 64 位
- Python：3.10.18
- GPU：NVIDIA RTX 50 系列或任意支持 CUDA 12.9 的显卡
- 驱动：CUDA 12.9 对应驱动版本或更新

## 依赖安装
项目根目录提供了 `environment.yml` 与 `requirements.txt`：

```bash
# 方式一：使用 Conda 一键创建
conda env create -f environment.yml
conda activate labelquick

# 方式二：在现有环境中手动安装
pip install -r requirements.txt
```

`requirements.txt` 预设清华 PyPI 镜像，并额外指向 PyTorch 官方的 `cu129` 轮子仓库，可直接获得包含 `sm_120` 内核的 `torch==2.6.0+cu129`、`torchvision==0.21.0+cu129`、`torchaudio==2.6.0+cu129` 等依赖。

## 模型准备
从项目 README 提供的链接下载 `sam2.1_hiera_large.pt` 并放置于 `sampro/checkpoints/`。如需自定义路径，可设置环境变量：

```powershell
set SAM2_CHECKPOINT=D:\path\to\sam2.1_hiera_large.pt
```

程序将在启动时读取该变量。

## 启动流程
1. 准备待标注的图片或视频数据。
2. 双击 `Run.py` 或在命令行执行 `python Run.py`。
3. 通过右侧面板查看当前图像文件名，使用顶部下拉框切换保存格式（XML/YOLO）。
4. 左键点击进行正样本提示，右键添加负样本约束；按 `S` 保存结果。

## 常见问题
- **显卡未被识别**：确认已安装 CUDA 12.9 驱动，使用 `nvidia-smi` 检查版本；必要时重新安装官方驱动。
- **依赖安装缓慢**：可以临时加上 `-i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://download.pytorch.org/whl/cu129` 参数。
- **缺少 `pycocotools`**：Windows 需先安装 Visual C++ Build Tools，并在激活的环境中运行 `pip install cython` 后再执行 `pip install pycocotools>=2.0.8`。

如需更详细的操作指南，请参考主仓库 README 与演示视频。
