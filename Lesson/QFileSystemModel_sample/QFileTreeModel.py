import os
import sys

from PySide2 import QtWidgets, QtCore, QtGui


class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super(FileSystemModel, self).__init__(*args, **kwargs)
        self.root_path = QtCore.QDir.currentPath()
        self.setRootPath(self.root_path)


class FileSystemTreeView(QtWidgets.QTreeView):
    def __init__(self, model: FileSystemModel, parent, *args, **kwargs):
        self.model = model
        super(FileSystemTreeView, self).__init__(parent, *args, **kwargs)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QtCore.QDir.currentPath()))
        self.clicked.connect(self.tree_click_action)

    def tree_click_action(self, index:QtCore.QModelIndex):
        print("tree clicked", index.row(), index.column())
        print(self.model.fileName(index))
        print(self.model.filePath(index))


class FileSystemListView(QtWidgets.QTreeView):
    def __init__(self, model: FileSystemModel, parent, *args, **kwargs):
        self.model = model
        super(FileSystemListView, self).__init__(parent, *args, **kwargs)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QtCore.QDir.currentPath()))
        self.clicked.connect(self.list_click_action)

    def list_click_action(self, index:QtCore.QModelIndex):
        print("list clicked", index.row(), index.column())
        print(self.model.fileName(index))
        print(self.model.filePath(index))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    splitter = QtWidgets.QSplitter()

    current_folder = QtCore.QDir.currentPath()

    model = FileSystemModel()

    tree = FileSystemTreeView(model, splitter)

    list = FileSystemListView(model, splitter)

    splitter.setWindowTitle("Two views onto the same file system model")
    splitter.show()
    sys.exit(app.exec_())
