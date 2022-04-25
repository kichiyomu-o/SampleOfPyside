# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from varname import nameof

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt, QFile, Signal, Slot, QObject
from PySide6.QtUiTools import QUiLoader
# https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTreeWidget.html
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QTreeWidget.html

class QDictTreeWidget(QWidget):
    __value = None
    __varName = None
    ui = None

    # create signal
    valueSet = Signal(object)   # this signal emit when value is set

    def __init__(self, value=None, varName=None, ui=None, *args, **kwargs):
        super(QDictTreeWidget, self).__init__(*args, **kwargs)
        self.ui = ui
        self.__value = value
        self.__varName = varName
        self.__history = []
        self.load_ui()
        if value:
            self.appendHistory(value)

    def load_ui(self):
        if self.ui == None:
            # if
            loader = QUiLoader()
            path = os.fspath(Path(__file__).resolve().parent / "qDictTreeWidget.ui")
            ui_file = QFile(path)
            ui_file.open(QFile.ReadOnly)
            self.ui = loader.load(ui_file, self)
            ui_file.close()

        # set values of this widgets
        self.setUIvalue(self.__value)

        # connect sig to slot
        # https://wiki.qt.io/Signals_and_Slots_in_PySide/ja
        self.ui.pushButton_Save.clicked.connect(self.handle_save)
        self.ui.pushButton_Reset.clicked.connect(self.handle_clear)
        self.ui.pushButton_Expand.clicked.connect(self.handle_expand)
        self.ui.treeWidget.itemChanged.connect(self.handle_tree)
        self.ui.spinBox.valueChanged.connect(self.handle_spinbox)
        # self.valueSet.connect(self.handle_valueSet)

        # show this widget
        self.ui.treeWidget.show()

    def setUIvalue(self, value):
        if not self.__varName:
            self.__varName = "" # nameof(value)
        var_type = type(value)
        self.ui.label_name.setText(self.__varName)
        self.ui.label_type.setText(str(var_type))
        self.ui.treeWidget.setColumnCount(3)
        self.ui.treeWidget.setHeaderLabels(["Name", "Type", "Value"])
        self.addTreeItem(self.ui.treeWidget, value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.ui.treeWidget.clear()
        self.setUIvalue(self.__value)
        self.valueSet.emit(self.__value)

    @property
    def varName(self):
        return self.__varName

    @varName.setter
    def varName(self, varName):
        self.__varName = varName
        self.ui.label_name.setText(self.__varName)

    def handle_tree(self, item, column):
        self.setRootValue(item)
        self.__value = self.to_dict()

    def setRootValue(self, item):
        if item.parent() != None:
            parent = item.parent()
            value = {}
            for childindex in range(parent.childCount()):
                childitem = parent.child(childindex)
                print(f"child({childitem.text(0)}), childitem.text(2))")
                value[childitem.text(0)] = self.get_value(childitem)
            parent.setText(2, str(value))
            # self.setRootValue(parent)

    def handle_valueChanged(self, value):
        self.ui.treeWidget.clear()
        self.setUIvalue(value)

    def addTreeItem(self, tree, rootValue, rootItem=None):
        if type(rootValue) == dict:
            for key, value in rootValue.items():
                if rootItem == None:
                    currentItem = QTreeWidgetItem()
                else:
                    currentItem = QTreeWidgetItem(rootItem)
                currentItem.setFlags(currentItem.flags() | Qt.ItemIsEditable)
                currentItem._name = key
                currentItem.setText(0, currentItem._name)
                currentItem.setText(1, str(type(value)))
                if type(value) == str:
                    currentItem.setText(2, value)
                else:
                    currentItem.setText(2, str(value))
                if type(value) == dict:
                    self.addTreeItem(tree, value, currentItem)
                if rootItem == None:
                    tree.addTopLevelItem(currentItem)
                    flag = self.ui.pushButton_Expand.isChecked()
                    self.setExpandedAll(currentItem, flag)

    # set Expanded for all item
    def setExpandedAll(self, item, flag):
        item.setExpanded(flag)
        for childindex in range(item.childCount()):
            childitem = item.child(childindex)
            self.setExpandedAll(childitem, flag)

    def handle_save(self):
        self.__value = self.to_dict()
        self.appendHistory(self.__value)
        self.valueSet.emit(self.__value)

    def handle_clear(self):
        self.ui.treeWidget.clear()
        self.setUIvalue(self.__value)
        self.valueSet.emit(self.__value)

    def handle_expand(self):
        self.ui.treeWidget.clear()
        self.setUIvalue(self.__value)

    def handle_spinbox(self, int):
        ind = self.ui.spinBox.value()
        self.__value = self.__history[ind]
        self.ui.treeWidget.clear()
        self.setUIvalue(self.__value)

    def to_dict(self):
        value = {}
        for index in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(index)
            # print(item.text(0), item.text(2))
            if item.text(1) == "<class 'dict'>":
                value[item.text(0)] = {}
                self.add_dict(item, value[item.text(0)])
            else:
                value[item.text(0)] = self.get_value(item)
        return value

    def add_dict(self, item, value):
        for childindex in range(item.childCount()):
            childitem = item.child(childindex)
            # print(childitem.text(0), childitem.text(2))
            if childitem.text(1) == "<class 'dict'>":
                value[childitem.text(0)] = {}
                self.add_dict(childitem, value[childitem.text(0)])
            else:
                value[childitem.text(0)] = self.get_value(childitem)

    def get_value(self, item):
        varType = item.text(1)
        if varType == "<class 'int'>":
            return int(item.text(2))
        elif varType == "<class 'float'>":
            return float(item.text(2))
        else:
            return item.text(2)

    def appendHistory(self, value):
        if value not in self.__history:
            self.__history.append(value)
            self.ui.spinBox.setMaximum(len(self.__history)-1)


if __name__ == "__main__":
    app = QApplication([])
    val = {"a":0, "b":{"c":1, "d":{"e":3,"f":4}},"g":5, }
    widget = QDictTreeWidget(val)
    widget.show()
    sys.exit(app.exec())
