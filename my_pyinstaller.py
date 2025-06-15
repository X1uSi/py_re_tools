# my_pyinstaller.py - PyInstaller打包工具GUI
import os
import sys
import shlex
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QGroupBox, QCheckBox, QLineEdit, QPushButton, QLabel,
                             QTextEdit, QFileDialog, QMessageBox, QProgressBar, QDialog)
from PyQt5.QtCore import Qt, QUrl, QProcess, QMimeData
from PyQt5.QtGui import QFont, QDesktopServices, QTextCursor, QDragEnterEvent, QDropEvent


class DragDropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """接受拖拽事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """处理文件拖放"""
        urls = event.mimeData().urls()
        if urls:
            # 获取第一个文件的本地路径
            file_path = urls[0].toLocalFile()
            self.setText(file_path)
            event.acceptProposedAction()


class PyInstallerGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PyInstaller打包工具")
        self.setMinimumSize(800, 600)

        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 创建常用命令选项卡
        self.common_tab = QWidget()
        self.tab_widget.addTab(self.common_tab, "常用命令")
        self.setup_common_tab()

        # 创建自定义命令选项卡
        self.custom_tab = QWidget()
        self.tab_widget.addTab(self.custom_tab, "自定义命令")
        self.setup_custom_tab()

        # 添加执行按钮
        self.execute_btn = QPushButton("执行")
        self.execute_btn.setFont(QFont("Arial", 12))
        self.execute_btn.setFixedSize(120, 40)
        self.execute_btn.clicked.connect(self.execute_command)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.execute_btn)
        main_layout.addLayout(btn_layout)

        # 初始化进程
        self.process = None

    def setup_common_tab(self):
        """设置常用命令选项卡"""
        layout = QVBoxLayout(self.common_tab)
        layout.setSpacing(15)

        # 添加参数解释区域
        self.param_explanation = QTextEdit()
        self.param_explanation.setReadOnly(True)
        self.param_explanation.setFont(QFont("Arial", 9))
        self.param_explanation.setPlaceholderText("鼠标悬停在参数上查看详细解释...")
        self.param_explanation.setMaximumHeight(80)
        layout.addWidget(self.param_explanation)

        # 参数选择区
        param_layout = QHBoxLayout()

        # 基本选项
        basic_group = QGroupBox("基本选项")
        basic_layout = QVBoxLayout()

        self.help_cb = QCheckBox("-h, --help")
        self.help_cb.setToolTip("显示帮助信息并退出")
        # 添加悬停事件处理
        self.help_cb.enterEvent = lambda event: self.show_explanation("显示PyInstaller的帮助信息并退出")
        self.help_cb.leaveEvent = lambda event: self.clear_explanation()
        basic_layout.addWidget(self.help_cb)

        self.version_cb = QCheckBox("-v, --version")
        self.version_cb.setToolTip("显示程序版本信息并退出")
        # 添加悬停事件处理
        self.version_cb.enterEvent = lambda event: self.show_explanation("显示PyInstaller的版本信息并退出")
        self.version_cb.leaveEvent = lambda event: self.clear_explanation()
        basic_layout.addWidget(self.version_cb)

        basic_group.setLayout(basic_layout)
        param_layout.addWidget(basic_group)

        # 生成类型
        build_group = QGroupBox("生成类型")
        build_layout = QVBoxLayout()

        self.onefile_cb = QCheckBox("-F, --onefile")
        self.onefile_cb.setToolTip("创建一个单一的可执行文件包")
        # 添加悬停事件处理
        self.onefile_cb.enterEvent = lambda event: self.show_explanation("将所有文件打包成一个单独的可执行文件")
        self.onefile_cb.leaveEvent = lambda event: self.clear_explanation()
        build_layout.addWidget(self.onefile_cb)

        self.name_cb = QCheckBox("-n NAME, --name NAME")
        self.name_cb.setToolTip("指定打包应用和spec文件的名称")
        # 添加悬停事件处理
        self.name_cb.enterEvent = lambda event: self.show_explanation("为生成的可执行文件和spec文件指定名称")
        self.name_cb.leaveEvent = lambda event: self.clear_explanation()
        build_layout.addWidget(self.name_cb)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入应用名称")
        self.name_input.setEnabled(False)
        self.name_cb.stateChanged.connect(lambda state: self.name_input.setEnabled(state == Qt.Checked))
        build_layout.addWidget(self.name_input)

        build_group.setLayout(build_layout)
        param_layout.addWidget(build_group)

        # Windows与macOS特定选项
        os_group = QGroupBox("Windows与macOS特定选项")
        os_layout = QVBoxLayout()

        self.console_cb = QCheckBox("-c, --console, --nowindowed")
        self.console_cb.setToolTip("打开控制台窗口进行标准I/O")
        # 添加悬停事件处理
        self.console_cb.enterEvent = lambda event: self.show_explanation("为应用程序打开控制台窗口（Windows和macOS）")
        self.console_cb.leaveEvent = lambda event: self.clear_explanation()
        os_layout.addWidget(self.console_cb)

        self.windowed_cb = QCheckBox("-w, --windowed, --noconsole")
        self.windowed_cb.setToolTip("不提供控制台窗口进行标准I/O")
        # 添加悬停事件处理
        self.windowed_cb.enterEvent = lambda event: self.show_explanation("不显示控制台窗口（仅GUI应用程序）")
        self.windowed_cb.leaveEvent = lambda event: self.clear_explanation()
        os_layout.addWidget(self.windowed_cb)

        self.hide_console_cb = QCheckBox("--hide-console")
        self.hide_console_cb.setToolTip("自动隐藏或最小化控制台窗口")
        # 添加悬停事件处理
        self.hide_console_cb.enterEvent = lambda event: self.show_explanation("启动后自动隐藏或最小化控制台窗口")
        self.hide_console_cb.leaveEvent = lambda event: self.clear_explanation()
        os_layout.addWidget(self.hide_console_cb)

        self.icon_cb = QCheckBox("-i <FILE>, --icon <FILE>")
        self.icon_cb.setToolTip("指定应用的图标文件")
        # 添加悬停事件处理
        self.icon_cb.enterEvent = lambda event: self.show_explanation("为可执行文件设置自定义图标（.ico或.icns）")
        self.icon_cb.leaveEvent = lambda event: self.clear_explanation()
        os_layout.addWidget(self.icon_cb)

        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText("选择图标文件")
        self.icon_input.setEnabled(False)
        self.icon_cb.stateChanged.connect(lambda state: self.icon_input.setEnabled(state == Qt.Checked))

        icon_btn = QPushButton("浏览...")
        icon_btn.setFixedWidth(80)
        icon_btn.clicked.connect(self.select_icon_file)
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(icon_btn)
        os_layout.addLayout(icon_layout)

        os_group.setLayout(os_layout)
        param_layout.addWidget(os_group)

        layout.addLayout(param_layout)

        # 文件选择区
        file_group = QGroupBox("选择Python文件")
        file_layout = QVBoxLayout()

        file_select_layout = QHBoxLayout()
        # 使用支持拖拽的输入框
        self.file_input = DragDropLineEdit()
        self.file_input.setPlaceholderText("拖放文件到此处或点击浏览按钮")
        self.file_input.textChanged.connect(self.update_command_display)
        file_select_layout.addWidget(self.file_input)

        browse_btn = QPushButton("浏览...")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.select_python_file)
        file_select_layout.addWidget(browse_btn)

        file_layout.addLayout(file_select_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # 预期命令框
        command_group = QGroupBox("预期命令")
        command_layout = QVBoxLayout()

        self.command_display = QTextEdit()
        self.command_display.setReadOnly(True)
        self.command_display.setFont(QFont("Courier New", 10))
        self.command_display.setPlaceholderText("生成的命令将显示在这里")
        command_layout.addWidget(self.command_display)

        command_group.setLayout(command_layout)
        layout.addWidget(command_group)

        # 连接信号以更新命令显示
        self.connect_signals()

    def setup_custom_tab(self):
        """设置自定义命令选项卡"""
        layout = QVBoxLayout(self.custom_tab)
        layout.setSpacing(15)

        # 自定义命令输入
        custom_group = QGroupBox("自定义命令")
        custom_layout = QVBoxLayout()

        self.custom_command_input = QTextEdit()
        self.custom_command_input.setPlaceholderText(
            "在此输入完整的PyInstaller命令...\n例如: pyinstaller --onefile --windowed --icon=app.ico myscript.py")
        self.custom_command_input.setFont(QFont("Courier New", 10))
        custom_layout.addWidget(self.custom_command_input)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # 文件选择区
        file_group = QGroupBox("选择Python文件 (可选)")
        file_layout = QVBoxLayout()

        file_select_layout = QHBoxLayout()
        # 使用支持拖拽的输入框
        self.custom_file_input = DragDropLineEdit()
        self.custom_file_input.setPlaceholderText("拖放文件到此处或点击浏览按钮")
        file_select_layout.addWidget(self.custom_file_input)

        browse_btn = QPushButton("浏览...")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.select_custom_python_file)
        file_select_layout.addWidget(browse_btn)

        file_layout.addLayout(file_select_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # 添加帮助链接
        help_layout = QHBoxLayout()
        help_layout.addStretch()

        help_label = QLabel("需要帮助? 查看")
        help_layout.addWidget(help_label)

        help_btn = QPushButton("PyInstaller文档")
        help_btn.setStyleSheet("color: blue; text-decoration: underline;")
        help_btn.setCursor(Qt.PointingHandCursor)
        help_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://pyinstaller.org/en/stable/usage.html")))
        help_layout.addWidget(help_btn)

        layout.addLayout(help_layout)

    def show_explanation(self, text):
        """显示参数解释"""
        self.param_explanation.setText(text)
        self.param_explanation.setStyleSheet("background-color: #f0f0f0; border: 1px solid #d0d0d0;")

    def clear_explanation(self):
        """清除参数解释"""
        self.param_explanation.clear()
        self.param_explanation.setStyleSheet("")

    def connect_signals(self):
        """连接所有信号以更新命令显示"""
        # 连接所有复选框
        for checkbox in self.common_tab.findChildren(QCheckBox):
            checkbox.stateChanged.connect(self.update_command_display)

        # 连接文本输入框
        self.name_input.textChanged.connect(self.update_command_display)
        self.icon_input.textChanged.connect(self.update_command_display)

    def update_command_display(self):
        """更新预期命令框的内容"""
        if not self.file_input.text():
            self.command_display.setText("请先选择Python文件")
            return

        command = "pyinstaller"

        # 添加基本选项
        if self.help_cb.isChecked():
            command += " -h"
        if self.version_cb.isChecked():
            command += " -v"

        # 添加生成类型选项
        if self.onefile_cb.isChecked():
            command += " -F"
        if self.name_cb.isChecked() and self.name_input.text():
            # 修复：只在名称包含空格时才添加引号
            name = self.name_input.text()
            if ' ' in name:
                command += f' -n "{name}"'
            else:
                command += f' -n {name}'

        # 添加操作系统特定选项
        if self.console_cb.isChecked():
            command += " -c"
        if self.windowed_cb.isChecked():
            command += " -w"
        if self.hide_console_cb.isChecked():
            command += " --hide-console"
        if self.icon_cb.isChecked() and self.icon_input.text():
            # 修复：只在图标路径包含空格时才添加引号
            icon_path = self.icon_input.text()
            if ' ' in icon_path:
                command += f' -i "{icon_path}"'
            else:
                command += f' -i {icon_path}'

        # 添加文件路径 - 关键修复：只在路径包含空格时才添加引号
        file_path = self.file_input.text()
        if ' ' in file_path:
            command += f' "{file_path}"'
        else:
            command += f' {file_path}'

        self.command_display.setText(command)

    def select_python_file(self):
        """选择Python文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Python文件", "",
            "Python文件 (*.py);;所有文件 (*)"
        )
        if file_path:
            self.file_input.setText(file_path)

    def select_custom_python_file(self):
        """为自定义命令选择Python文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Python文件", "",
            "Python文件 (*.py);;所有文件 (*)"
        )
        if file_path:
            self.custom_file_input.setText(file_path)

    def select_icon_file(self):
        """选择图标文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图标文件", "",
            "图标文件 (*.ico);;所有文件 (*)"
        )
        if file_path:
            self.icon_input.setText(file_path)

    def execute_command(self):
        """执行命令"""
        current_tab = self.tab_widget.currentIndex()

        if current_tab == 0:  # 常用命令
            command = self.command_display.toPlainText().strip()
            if not command or "pyinstaller" not in command:
                QMessageBox.warning(self, "无效命令", "请先生成有效的打包命令")
                return
        else:  # 自定义命令
            command = self.custom_command_input.toPlainText().strip()
            if not command:
                QMessageBox.warning(self, "无效命令", "请输入有效的打包命令")
                return

            # 如果自定义命令中没有指定文件，但文件输入框中有内容，则添加文件
            # 关键修复：只在路径包含空格时才添加引号
            if self.custom_file_input.text():
                file_path = self.custom_file_input.text()
                if ' ' in file_path:
                    command += f' "{file_path}"'
                else:
                    command += f' {file_path}'

        # 创建输出窗口
        self.output_dialog = QDialog(self)
        self.output_dialog.setWindowTitle("命令执行中...")
        self.output_dialog.setMinimumSize(700, 500)

        layout = QVBoxLayout(self.output_dialog)

        # 命令显示
        command_label = QLabel(f"执行命令: {command}")
        command_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(command_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度模式
        layout.addWidget(self.progress_bar)

        # 输出区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier New", 9))
        self.output_text.setPlaceholderText("命令输出将显示在这里...")
        layout.addWidget(self.output_text)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close_output_dialog)
        layout.addWidget(close_btn)

        self.output_dialog.show()

        # 清空输出区域
        self.output_text.clear()

        # 执行命令
        self.execute_command_with_qprocess(command)

    def execute_command_with_qprocess(self, command):
        """使用QProcess执行命令"""
        # 如果已有进程在运行，先停止
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process = None

        # 创建新进程
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        # 连接信号
        self.process.readyReadStandardOutput.connect(self.read_process_output)
        self.process.finished.connect(self.process_finished)

        # 关键修复：正确处理命令参数
        if sys.platform == "win32":
            # 在Windows上，我们直接执行命令字符串
            self.process.start("cmd.exe", ["/c", command])
        else:
            # 在Unix系统上，使用shlex正确分割参数
            args = shlex.split(command)
            if args:
                executable = args[0]
                arguments = args[1:]
                self.process.start(executable, arguments)
            else:
                QMessageBox.warning(self, "错误", "无效的命令")
                return

    def read_process_output(self):
        """读取进程输出"""
        if self.process:
            output = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")
            self.append_output(output)

    def append_output(self, text):
        """追加输出到文本区域"""
        self.output_text.append(text)
        # 滚动到底部
        self.output_text.moveCursor(QTextCursor.End)

    def process_finished(self, exit_code, exit_status):
        """进程执行完成处理"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)

        # 添加执行结果信息
        if exit_code == 0:
            self.append_output("\n✅ 命令执行成功!")
        else:
            self.append_output(f"\n❌ 命令执行失败! 退出码: {exit_code}")

    def close_output_dialog(self):
        """关闭输出对话框"""
        # 如果进程仍在运行，终止它
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()

        self.output_dialog.close()


if __name__ == "__main__":
    # 独立运行测试
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle("Fusion")

    # 创建并显示窗口
    window = PyInstallerGUI()
    window.show()

    sys.exit(app.exec_())
