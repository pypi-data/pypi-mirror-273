from PySide6.QtWidgets import QDialog, QTableView, QLabel, QVBoxLayout, QAbstractItemView

from qtlink.table.table_controller import TableController


class DialogTableDisplay(QDialog):
    """可以显示表格数据的对话框"""

    def __init__(self, text: str,
                 table_data: list[dict],
                 parent=None,
                 title: str = '提示',
                 *args, **kwargs):
        """
        :param text: 对话框的文本消息
        :param table_data: 表格数据
        :param parent: 对话框所属的父类
        :param args: 表格控制器可能使用的其他参数
        :param kwargs: 表格控制器可能使用的其他参数
        """
        super().__init__(parent=parent)
        self.v_layout = QVBoxLayout()
        label = QLabel(text, self)
        label.setWordWrap(True)
        self.tableview = QTableView(self)
        self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.v_layout.addWidget(label)
        self.v_layout.addWidget(self.tableview)

        self.setWindowTitle(title)
        self.setLayout(self.v_layout)
        self.table_controller = TableController(tableview=self.tableview)
        self.table_controller.update_table_data(table_data=table_data, *args, **kwargs)
