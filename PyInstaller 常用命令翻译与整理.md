### PyInstaller 常用命令翻译与整理

#### 基本选项

- `-h, --help`
  - 显示帮助信息并退出。
- `-v, --version`
  - 显示程序版本信息并退出。

#### 输出路径与清理

- `--distpath DIR`
  - 指定打包应用的输出目录（默认：./dist）。
- `--workpath WORKPATH`
  - 指定存放所有临时工作文件的目录（默认：./build）。
- `-y, --noconfirm`
  - 不询问确认即替换输出目录。
- `--clean`
  - 在构建前清理PyInstaller缓存和临时文件。

#### 日志级别

- ```
  --log-level LEVEL
  ```

  - 设置构建时控制台消息的详细程度。LEVEL可以是TRACE, DEBUG, INFO, WARN, DEPRECATION, ERROR, FATAL（默认：INFO）。

#### 生成类型

- `-D, --onedir`
  - 创建一个包含可执行文件的一个文件夹包（默认）。
- `-F, --onefile`
  - 创建一个单一的可执行文件包。
- `--specpath DIR`
  - 指定存储生成的spec文件的文件夹（默认：当前目录）。
- `-n NAME, --name NAME`
  - 指定打包应用和spec文件的名称（默认：第一个脚本的基名）。

#### 打包内容与搜索路径

- `--add-data SOURCE:DEST`
  - 添加额外的数据文件或目录到应用中。格式为“源文件/目录:目标目录”。
- `--add-binary SOURCE:DEST`
  - 添加额外的二进制文件到可执行文件中。格式与`--add-data`相同。
- `-p DIR, --paths DIR`
  - 指定搜索导入的路径（类似于PYTHONPATH）。
- `--hidden-import MODULENAME`
  - 指定代码中未直接导入但需要的模块。
- `--collect-submodules MODULENAME`
  - 收集指定包或模块的所有子模块。
- `--collect-data MODULENAME`
  - 收集指定包或模块的所有数据文件。
- `--collect-binaries MODULENAME`
  - 收集指定包或模块的所有二进制文件。
- `--collect-all MODULENAME`
  - 收集指定包或模块的所有子模块、数据文件和二进制文件。

#### 调试与优化

- `-d {all,imports,bootloader,noarchive}, --debug {all,imports,bootloader,noarchive}`
  - 提供调试冻结应用的帮助。
- `--optimize LEVEL`
  - 设置收集的Python模块和脚本的字节码优化级别。
- `--python-option PYTHON_OPTION`
  - 指定传递给Python解释器的运行时命令行选项。
- `-s, --strip`
  - 对可执行文件和共享库应用符号表剥离（Windows不推荐）。

#### Windows与macOS特定选项

- `-c, --console, --nowindowed`
  - 打开控制台窗口进行标准I/O（Windows默认）。
- `-w, --windowed, --noconsole`
  - 不提供控制台窗口进行标准I/O（Windows和macOS）。
- `--hide-console {hide-late,minimize-early,hide-early,minimize-late}`
  - Windows专用：在控制台启用的可执行文件中，自动隐藏或最小化控制台窗口。
- `-i <FILE>, --icon <FILE>`
  - 指定应用的图标文件。

#### Windows特定选项

- `--version-file FILE`
  - 从FILE添加版本资源到exe中。
- `--manifest <FILE or XML>`
  - 添加manifest文件或XML到exe中。
- `-r RESOURCE`
  - 添加或更新Windows可执行文件的资源。
- `--uac-admin`
  - 创建请求应用程序启动时提升的Manifest。
- `--uac-uiaccess`
  - 允许提升的应用程序与远程桌面一起工作。

#### macOS特定选项

- `--argv-emulation`
  - 启用macOS应用包的argv仿真。
- `--osx-bundle-identifier BUNDLE_IDENTIFIER`
  - 设置macOS .app包标识符。
- `--target-architecture ARCH`
  - 设置目标架构（macOS专用；有效值：x86_64, arm64, universal2）。
- `--codesign-identity IDENTITY`
  - 设置代码签名身份（macOS专用）。
- `--osx-entitlements-file FILENAME`
  - 设置代码签名时使用的权限文件（macOS专用）。

#### 特殊选项

- `--runtime-tmpdir PATH`
  - 指定在`onefile`模式下提取库和支持文件的目录。
- `--bootloader-ignore-signals`
  - 告诉bootloader忽略信号，而不是将它们转发给子进程。