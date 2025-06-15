# main.py - 主程序入口
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QHBoxLayout, QDialog, QLabel,
                            QDialogButtonBox, QGroupBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon, QFont

# 导入各个功能模块
from my_pyinstxtractor import PyInstxtractorGUI
from my_pyinstaller import PyInstallerGUI
from my_pycdc import PycdcGUI
from my_pycdas import PycdasGUI
from my_uncompyle6 import Uncompyle6GUI


class OnlineDecompilerDialog(QDialog):
    """在线反编译工具对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("在线pyc反汇编工具")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("推荐在线pyc反汇编工具:")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        # 工具列表
        tools = [
            ("Pylingual", "https://pylingual.io/", "支持多种Python版本的反编译"),
            ("Tool.lu", "https://tool.lu/pyc/", "中文界面，简单易用"),
            ("LDDGO", "https://www.lddgo.net/string/pyc-compile-decompile", "支持编译和解编译"),
            ("Decompiler.com", "https://www.decompiler.com/", "专业的反编译工具"),
            ("Python Decompiler", "https://python-decompiler.com/", "专注于Python反编译")
        ]

        for name, url, description in tools:
            # 使用水平布局而不是分组框
            tool_layout = QHBoxLayout()

            # 工具名称和描述
            tool_label = QLabel(f"{name}: {description}")
            tool_layout.addWidget(tool_label)

            # 添加弹性空间
            tool_layout.addStretch()

            # 链接按钮
            link_btn = QPushButton("访问网站")
            link_btn.setStyleSheet("color: blue; text-decoration: underline;")
            link_btn.setCursor(Qt.PointingHandCursor)
            link_btn.setProperty("url", url)  # 将URL存储为属性
            link_btn.clicked.connect(self.open_link)  # 连接到通用方法
            tool_layout.addWidget(link_btn)

            layout.addLayout(tool_layout)

        # 添加垂直间距
        layout.addSpacing(20)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def open_link(self):
        """打开浏览器访问链接"""
        # 获取发送信号的按钮
        button = self.sender()
        # 从按钮属性中获取URL
        url = button.property("url")
        if url:
            QDesktopServices.openUrl(QUrl(url))


class DecompilerChoiceDialog(QDialog):
    """反编译工具选择对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择pyc反编译工具")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # 标题
        title = QLabel("请选择反编译工具:")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        # 工具按钮
        self.tool_buttons = []

        # pycdc
        pycdc_btn = QPushButton("pycdc (支持Python 3.9及以下)")
        pycdc_btn.setToolTip("最强大的反编译工具之一，支持较新的Python版本")
        pycdc_btn.clicked.connect(lambda: self.select_tool("pycdc"))
        layout.addWidget(pycdc_btn)
        self.tool_buttons.append(pycdc_btn)

        # pycdas
        pycdas_btn = QPushButton("pycdas (反汇编器)")
        pycdas_btn.setToolTip("将pyc文件反汇编为字节码")
        pycdas_btn.clicked.connect(lambda: self.select_tool("pycdas"))
        layout.addWidget(pycdas_btn)
        self.tool_buttons.append(pycdas_btn)

        # uncompyle6
        uncompyle_btn = QPushButton("uncompyle6 (支持Python 3.8及以下)")
        uncompyle_btn.setToolTip("经典的反编译工具，支持较旧的Python版本")
        uncompyle_btn.clicked.connect(lambda: self.select_tool("uncompyle6"))
        layout.addWidget(uncompyle_btn)
        self.tool_buttons.append(uncompyle_btn)

        # 在线工具
        online_btn = QPushButton("在线pyc反汇编")
        online_btn.setToolTip("使用在线工具反编译pyc文件")
        online_btn.clicked.connect(lambda: self.select_tool("online"))
        layout.addWidget(online_btn)
        self.tool_buttons.append(online_btn)

        # 添加间距
        layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        self.selected_tool = None

    def select_tool(self, tool_name):
        """选择工具并关闭对话框"""
        self.selected_tool = tool_name
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python工具集")
        self.setGeometry(300, 300, 500, 300)

        # 设置应用图标
        if hasattr(sys, '_MEIPASS'):
            # 打包后的路径
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            # 开发环境路径
            icon_path = 'icon.ico'

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 创建主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 标题
        title = QLabel("Python逆向与打包工具集")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 添加间距
        layout.addSpacing(30)

        # 功能按钮
        self.unpack_btn = QPushButton("1. PyInstaller解包")
        self.unpack_btn.setFont(QFont("Arial", 12))
        self.unpack_btn.clicked.connect(self.open_pyinstxtractor)
        layout.addWidget(self.unpack_btn)

        self.pack_btn = QPushButton("2. Py程序打包")
        self.pack_btn.setFont(QFont("Arial", 12))
        self.pack_btn.clicked.connect(self.open_pyinstaller)
        layout.addWidget(self.pack_btn)

        self.decompile_btn = QPushButton("3. Pyc反编译")
        self.decompile_btn.setFont(QFont("Arial", 12))
        self.decompile_btn.clicked.connect(self.open_decompiler_choice)
        layout.addWidget(self.decompile_btn)

        # 添加底部信息
        layout.addStretch()
        footer = QLabel("© 2025 Python工具集 | 版本 1.0 | 作者: xiusi")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray;")
        layout.addWidget(footer)

    def open_pyinstxtractor(self):
        """打开PyInstaller解包工具"""
        self.pyinstxtractor_gui = PyInstxtractorGUI()
        self.pyinstxtractor_gui.show()

    def open_pyinstaller(self):
        """打开PyInstaller打包工具"""
        self.pyinstaller_gui = PyInstallerGUI()  # 使用导入的类
        self.pyinstaller_gui.show()  # 显示窗口

    def open_decompiler_choice(self):
        """打开反编译工具选择对话框"""
        dialog = DecompilerChoiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            tool = dialog.selected_tool
            if tool == "pycdc":
                self.pycdc_gui = PycdcGUI()
                self.pycdc_gui.show()
            elif tool == "pycdas":
                self.pycdas_gui = PycdasGUI()
                self.pycdas_gui.show()
            elif tool == "uncompyle6":
                self.uncompyle_gui = Uncompyle6GUI()
                self.uncompyle_gui.show()
            elif tool == "online":
                online_dialog = OnlineDecompilerDialog(self)
                online_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle("Fusion")

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())