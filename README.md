# Python逆向工程工具集 (PyRE Tool)

PyRE Tool是一个集成调用了多个Python逆向工程工具的图形化界面程序，旨在简化Python打包文件（如PyInstaller生成的exe）的解包、反编译和反汇编过程，适合像作者这样的懒狗qwq。

## 功能亮点

- **一站式解决方案**：集成调用多个Python逆向工程工具于单个应用程序
- **用户友好界面**：所有功能通过直观的图形界面操作
- **跨工具工作流**：支持从解包到反编译/反汇编的完整工作流程
- **文件拖放支持**：简化文件选择过程

## 包含工具(仅对工具的调用)

1. **PyInstaller打包工具** (`my_pyinstaller.py`)
   - 将Python脚本打包为可执行文件
   - 自定义打包选项
   - 单文件或多文件打包支持
2. **PyInstaller解包工具** (`my_pyinstxtractor.py`)
   - 解包PyInstaller生成的exe文件
   - 提取原始Python字节码(.pyc)文件
   - 自动组织解包文件结构
3. **pycdc反编译工具** (`my_pycdc.py`)
   - 将Python字节码(.pyc)反编译为可读的Python源代码
   - 支持多种Python版本
   - 输出到文件或查看结果
4. **pycdas反汇编工具** (`my_pycdas.py`)
   - 将Python字节码(.pyc)反汇编为字节码指令
   - 查看Python字节码的底层实现
   - 输出到文本文件
5. **uncompyle6反编译工具** (`my_uncompyle6.py`)
   - 替代反编译引擎
   - 支持不同Python版本
   - 与pycdc互补使用

## 下载与安装

### 预编译版本（推荐）

1. 前往[Release页面](https://github.com/X1uSi/py_re_tools/releases)下载最新版的`py_re_tool.exe`
2. 解压双击运行即可使用，无需安装

## 使用指南

### 基本工作流程

1. **解包PyInstaller打包的exe文件**
   - 使用PyInstaller解包工具打开exe文件
   - 工具会生成一个`<exe文件名>_extracted`的文件夹
2. **反编译.pyc文件**
   - 在解包目录中找到.pyc文件（通常在`PYZ-00.pyz_extracted`子目录中）
   - 使用pycdc或uncompyle6工具打开.pyc文件
   - 查看或保存反编译结果
3. **反汇编.pyc文件**
   - 使用pycdas工具打开.pyc文件
   - 查看Python字节码指令

### 首次使用配置

首次运行时，程序需配置所需工具路径：

1. 点击"配置"按钮
2. 设置正确的工具路径（如pycdc.exe、pycdas.exe等）
3. 程序会记住您的设置，下次启动无需重新配置

------
