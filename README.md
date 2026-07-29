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

1. 安装 Python 3，并确保安装时勾选 `Add Python to PATH`。
2. 下载或克隆本项目。
3. 双击 `启动嫑嫑.bat`。

运行桌宠不需要额外安装第三方 Python 包。

## 操作

- 左键拖动：移动
- 左键单击：互动
- 右键：休息或退出

## 项目结构

- `nono.py`：桌宠程序
- `assets/`：处理后的透明桌宠素材
- `prepare_assets.py`：素材处理工具，仅供项目维护使用
- `启动嫑嫑.bat`：Windows 启动入口

## 授权与声明

程序代码采用 [MIT License](LICENSE)。

角色形象和 `assets/` 内的美术素材不适用 MIT License。它们来自「周嫑嫑」官方小红书账号所发布形象的非商业粉丝二创，仅供学习、交流和非商业使用。详细规则见 [ASSETS_NOTICE.md](ASSETS_NOTICE.md)。

请勿将本项目或其中的角色素材用于付费软件、广告、商品、众筹、赞助回报或其他商业用途。若权利方提出调整或下架要求，项目维护者将配合处理。

## 致谢

- 角色/IP：周嫑嫑
- 官方发布来源：小红书账号「周嫑嫑」
- 桌宠整理与开发：社区贡献者
- macOS 原生版制作与真机测试：**Road**
