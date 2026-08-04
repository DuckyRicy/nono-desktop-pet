# 嫑嫑 nono 桌宠

![嫑嫑 nono](assets/idle.png)

一只住在桌面上的小锅。嫑嫑的小名是「嫑嫑」，英文名是 `nono`。

这是由粉丝制作的非商业桌宠项目，与歌手周深、工作室及「周嫑嫑」官方账号无隶属或商业合作关系。

## 功能

- 透明背景、始终置顶
- 左键拖动移动嫑嫑
- 左键单击触发随机表情和台词
- 右键打开休息与退出菜单
- 无人操作时会从多种动作中随机发呆、挥手或玩耍
- 深色、浅色桌面均可辨认的细白描边

## 下载与使用

### 普通用户

1. 在 GitHub 项目右侧打开 `Releases`。
2. 下载对应系统的压缩包：
   - Windows：`nono-desktop-pet-vX.X.X-windows.zip`
   - macOS（Apple 芯片）：`nono-desktop-pet-vX.X.X-macos-arm64-native.zip`
3. 解压后运行：
   - Windows：双击 `nono-desktop-pet.exe`
   - macOS：打开 `nono-desktop-pet.app`

不需要安装 Python，也不要直接在压缩包内运行。

macOS 首次打开若提示无法验证开发者，可在 Finder 中按住 Control 点击应用，
选择“打开”，再确认一次。本项目暂未进行 Apple 开发者签名或公证。

目前发布的 macOS 原生版仅支持 M1、M2、M3、M4 等 Apple Silicon 芯片，
由朋友 **Road** 协助制作并在真实 Mac 设备上测试通过。Intel Mac 暂不支持。

## 版本说明

### v1.0.1

- 新增并修复 Apple Silicon 原生 macOS 版本
- macOS 原生版由 **Road** 协助制作与测试
- Windows 版本功能保持不变

### 从源码运行

先安装 Python 3，然后下载或克隆本项目。

Windows：

1. 安装 Python 时勾选 `Add Python to PATH`。
2. 双击 `启动嫑嫑.bat`。

Ubuntu/Linux：

1. 安装透明窗口组件：`sudo apt install python3-pyqt5`。
2. 在项目文件夹打开终端，首次运行时输入 `chmod +x 启动嫑嫑.sh`。
3. 输入 `./启动嫑嫑.sh` 启动桌宠。

若希望像普通应用一样启动、不保留终端窗口：

1. 输入 `chmod +x 安装Ubuntu应用图标.sh`。
2. 输入 `./安装Ubuntu应用图标.sh`，完成一次安装。
3. 在 Ubuntu 应用菜单搜索“嫑嫑 nono”，点击图标启动。

项目更新后，再运行一次安装脚本即可更新应用菜单中的版本。

Windows 和 macOS 版本不需要额外安装第三方 Python 包。

Linux 不支持直接运行 Windows 的 `.bat` 文件。Ubuntu 源码版使用 PyQt5 提供透明背景，
在 Wayland 会尝试通过系统自带的 XWayland 兼容层运行，以改善拖动和窗口置顶，
因此目前 Linux 版属于源码试用支持，暂不提供打包版。

### Ubuntu 已知问题

- 在部分 Ubuntu Wayland 桌面环境中，系统会忽略应用的“始终置顶”请求；点击其他应用后，嫑嫑仍可能被窗口覆盖。
- 程序已尝试使用置顶标记、定时维持置顶和 XWayland 兼容模式，但在已测试的环境中仍未完全解决。
- 在已测试的 Ubuntu 环境中，左键会被系统的窗口拖动机制接管，左键单击互动暂时无效；请右键点击嫑嫑，在菜单中选择“叫我一下”进行互动。
- 透明背景、右键互动和桌面拖动可以正常使用。
- 如必须使用稳定置顶，可在 Ubuntu 登录界面选择 `Ubuntu on Xorg` 后再运行；Wayland 下暂不保证置顶效果。

## 操作

- 左键拖动：移动
- 左键单击：互动
- 右键：休息或退出

Ubuntu Wayland 用户请以右键菜单操作为准，左键单击互动目前可能无效。

## 项目结构

- `nono.py`：桌宠程序
- `nono_linux.py`：Ubuntu/Linux 透明窗口版本
- `assets/`：处理后的透明桌宠素材
- `prepare_assets.py`：素材处理工具，仅供项目维护使用
- `启动嫑嫑.bat`：Windows 启动入口
- `启动嫑嫑.sh`：Linux 启动入口
- `安装Ubuntu应用图标.sh`：将 Linux 版添加到 Ubuntu 应用菜单

## 授权与声明

程序代码采用 [MIT License](LICENSE)。

角色形象和 `assets/` 内的美术素材不适用 MIT License。它们来自「周嫑嫑」官方小红书账号所发布形象的非商业粉丝二创，仅供学习、交流和非商业使用。详细规则见 [ASSETS_NOTICE.md](ASSETS_NOTICE.md)。

请勿将本项目或其中的角色素材用于付费软件、广告、商品、众筹、赞助回报或其他商业用途。若权利方提出调整或下架要求，项目维护者将配合处理。

## 致谢

- 角色/IP：周嫑嫑
- 官方发布来源：小红书账号「周嫑嫑」
- 桌宠整理与开发：社区贡献者
- macOS 原生版制作与真机测试：**Road**
