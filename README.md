# LabelQuick
一种快速、轻松的AI辅助标注工具LabelQuick

<div> <img src="docs/image1.png"></div>

### 项目更新
🔥 V1.0 : 2024/7/8: 

- 我们更新了模型仓库的运行文件和配置文件，开源基础的UI跟标注功能，主要用于XML的数据标注。
- 保存标注时会在 XML 旁边自动生成符合 Ultralytics YOLOv8 要求的 `.txt` 标签文件，并在保存目录维护 `classes.txt` 以记录类别顺序。

🔥 V2.0 : 2025/1/20:
- 打标方式新增拉框标注，打标方式可切换。
- 新增模型仓库，模型仓库包含SAM2模型，用于快速标注。
- 支持视频物体追踪打标，选择物体后，自动追踪物体，并完成标注。
- 新增视频操作功能，包括开始播放，暂停，重新播放，抽帧操作。
- 优化了项目代码，修改了以知的BUG。


### 简介
LabelQuick_V2.0 是一款由 AI Horizon 团队设计并开发的快速图像标注工具，该版本在上一个版本的基础上进行了优化与改进。目前提供了直观易用的界面和强大的标注与分割功能，帮助您高效完成数据集的标注工作。当前版本仅支持 Windows 系统。

<div> <img src="docs/image2.png"></div>


### 快速开始
> 想在 RTX 50 系列或 CUDA 12.9 环境下极速部署？请参阅新增的《[LabelQuick CUDA 12.9 版简介](docs/cuda129_overview.md)》获取完整说明。
>⚠️显存最低需要`6G`⚠️
1. **拉取代码**
   ```bash
   git clone https://github.com/xaio6/LabelQuick
   ```

2. **模型下载**
下载[模型](https://pan.baidu.com/s/1dnfxBXaCYANRGcAxx7y0vg?pwd=ax58)到 `sampro/checkpoints` 里面。
-<div> <img src="docs/image3.png"></div>

   如果您希望将权重存放在其他目录，也可以在启动前设置环境变量 `SAM2_CHECKPOINT=/your/path/sam2.1_hiera_large.pt`（Windows 使用 `set` 命令），项目会自动读取该路径。

3. **环境配置**

   项目已针对 **Python 3.10.18** 与 **CUDA 12.9** 更新依赖，可直接驱动 RTX 5060（计算能力 `sm_120`）。

   - **方式一：使用 Conda 一键创建环境（推荐）**

     ```bash
     conda env create -f environment.yml
     conda activate labelquick
     ```

   - **方式二：在已有虚拟环境中手动安装**

     ```bash
     conda create -n labelquick python=3.10.18
     conda activate labelquick
     pip install -r requirements.txt
     ```

   说明：

   - `requirements.txt` 已包含 PyTorch 2.6.0 的 CUDA 12.9（`cu129`）官方轮子，能够原生支持 RTX 50 系列等 `sm_120` 架构显卡。请确保已安装 **CUDA 12.9 驱动** 或更新版本。
   - 若希望在 CPU 上运行，可在启动前通过设置 `SAM_DEVICE=cpu` 强制使用 CPU；项目仍会在检测到 GPU 不可用时自动回退。
   - `requirements.txt` 统一依赖 `pycocotools`。Windows 用户需要先安装 [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 并确保已安装 `cython`，随后执行 `pip install pycocotools>=2.0.8` 即可完成编译安装。
   - 如果在安装过程中 CUDA 扩展编译失败，可在安装前执行 `export SAM2_BUILD_CUDA=0`（Windows 使用 `set SAM2_BUILD_CUDA=0`）以跳过可选的 GPU 扩展构建。

   - **国内镜像加速（可选）**

     如果在国内网络环境下下载依赖较慢，可先配置 Conda 与 pip 的国内镜像：

     ```bash
     # Conda 镜像（如已配置可跳过）
     conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
     conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
     conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
     conda config --set show_channel_urls yes

     # pip 镜像（requirements.txt 已默认启用清华源和 PyTorch CUDA 轮子源）
     pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
     pip config set global.extra-index-url https://download.pytorch.org/whl/cu129
     ```

     如果不想修改全局配置，可在安装时临时指定：

     ```bash
     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
        --extra-index-url https://download.pytorch.org/whl/cu129
     ```

4. **项目运行**

- 运行 `Run.py` 打开 LabelQuick。
- 标注完成后，同名的 `.xml` 与 `.txt` 会同时保存，`classes.txt` 会持续收集出现过的标签，可直接拷贝到 YOLO 数据集的 `labels/` 目录中使用。


### 用户界面介绍
<div> <img src="docs/image4.png"></div>

- **顶部菜单栏**：包含文件、编辑、视图等常用功能。
- **左侧工具栏**：打开文件夹、选择标注数据储存位置、视频物体追踪标注。
- **中央工作区**：展示您的数据集，供您进行标注。
- **右侧属性面板**：显示当前数据集的标签。
- **进度条：** 可查看视频的播放进度，支持任意拖动播放位置。
- **按钮功能：** 包括开始播放，暂停，重新播放，抽帧操作。
- **自动抽帧：** 视频每秒自动抽取两帧图片。



### 功能详解
<div> <img src="docs/image5.png"></div>

- **快速标注**：2.0 版本快速打标，只需鼠标左键单击标注对象，软件将自动识别物品最大边缘的最小矩形框并进行快速自动标注。
- **视频物体追踪**：选择物体后，自动追踪物体，并完成标注。
- **视频操作**：支持视频播放、暂停、重新播放、抽帧操作。
- **自动抽帧**：视频每秒自动抽取两帧图片。


### **技术优势：**
我们引入了最新的 sam2 模型，在自动检测打标过程中实现了更高的准确率和效率。该模型能够快速对视频帧中的目标进行精准识别，减少人工干预，提高标注的质量。

### Demo
- 自动抽帧：

https://github.com/user-attachments/assets/66fef93a-18bc-4c6e-a91e-d90d63c33d89

- 视频物体追踪：


https://github.com/user-attachments/assets/59a824f8-1d48-4e73-ba34-28dea14a3bcc



- 更具体的操作可以参考[哔哩哔哩](https://www.bilibili.com/video/BV1kufJYyEhu/?spm_id_from=333.1387.homepage.video_card.click&vd_source=d9c1011fcda5afa76e9f5504f72e577f)视频教程：

### 常见问题解答（FAQ）
- **Q:** 如何撤销错误的标注？  
  **A:** 使用快捷键 (Q 或 Delete 键)。
- **Q:** 有哪些快捷键？  
  **A:** 上一张：A；下一张：D；保存标注数据：S。
- **Q:** 如何切换标注模式？  
  **A:** 使用快捷键 (W键)。


### 友情链接
- [SegmentAnything](https://github.com/facebookresearch/segment-anything) :分割任何模型 （SAM）

- [SAM2](https://github.com/facebookresearch/sam2): SAM2:分割图像和视频中的任何内容

### 许可协议
本项目遵循 MIT Licence。在使用本工具时，请遵守相关法律，包括版权法、数据保护法和隐私法。未经原作者和/或版权所有者许可，请勿使用本工具。未经原作者和/或版权所有者许可，请勿使用本工具。此外，请确保遵守您参考的模型和组件中的所有许可协议。

### 技术支持和联系方式
如果您在使用过程中遇到任何问题，请联系我们的技术支持团队：
- 公众号：AI Horizon

![5d2d299e21c40ef9bbe17b5b1e09fda](https://github.com/xaio6/LabelQuick/assets/118904918/17e51083-3abc-4812-9d32-8819f85cb3be)




感谢您选择 LabelQuick，我们希望这款工具能极大地提升您的工作效率。祝您标注愉快！
