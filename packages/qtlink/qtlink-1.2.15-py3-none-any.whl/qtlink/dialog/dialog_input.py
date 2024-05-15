from PySide6.QtWidgets import QDialog, QLabel
from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from qtlink import create_signal


class DialogInput(QDialog):
    """带有单行输入框的对话框"""
    def __init__(self,
                 text='',
                 placeholder='',
                 place_text='',
                 title='提示',
                 parent=None):
        """
        :param text: 对话框的文本消息，为''时会自动隐藏
        :param placeholder: 输入框的提示语
        :param place_text: 输入框的默认文字
        :param title: 设置窗口标题
        :param parent: 所属的父类
        """
        super().__init__(parent=parent)
        # 数据信号，用于获取输入内容
        self.signal_data = create_signal(str)
        self.setWindowTitle(title)

        label = QLabel(text, self)
        label.setWordWrap(True)
        label.setText(text)

        # 创建 QLineEdit
        self.lineEdit = QLineEdit(self)

        # 创建确定按钮和取消按钮
        self.okButton = QPushButton("确定", self)
        self.cancelButton = QPushButton("取消", self)

        self.lineEdit.setPlaceholderText(placeholder)
        if place_text:
            self.lineEdit.setText(place_text)
        # 设置按钮点击事件处理函数
        self.okButton.clicked.connect(self.click_ok)
        self.cancelButton.clicked.connect(self.reject)

        # 按钮水平布局
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.okButton)
        h_layout.addWidget(self.cancelButton)

        # 总体垂直布局
        layout = QVBoxLayout(self)
        if text:
            layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        layout.addLayout(h_layout)  # 将水平布局加入垂直布局

        self.setLayout(layout)

    def click_ok(self):
        # 点击确定按钮的事件处理
        self.accept()
        self.signal_data.signal.emit(self.lineEdit.text())
