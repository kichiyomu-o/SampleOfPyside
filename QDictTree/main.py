# This Python file uses the following encoding: utf-8

# File: main.py
import json
import os
import sys
from varname import nameof

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QFile, QIODevice
from QDictTreeWidget import QDictTreeWidget

window = None
treeWidget = None


def jread():

    global treeWidget
    filepath = QFileDialog().getOpenFileName()[0]
    if os.path.splitext(filepath)[1] == ".json":
        print("json_read")
        json_open = open(filepath, "r")
        json_load = json.load(json_open)
        if "varName" in json_load.keys():
            treeWidget.varName = json_load["varName"]
        else:
            treeWidget.varName = ""
        if "value" in json_load.keys():
            treeWidget.value = json_load["value"]
        else:
            treeWidget.value = json_load


def jsave():
    global treeWidget
    jdata = {}
    jdata["varName"] = treeWidget.varName
    jdata["value"] = treeWidget.value
    filepath = QFileDialog().getSaveFileName()[0]
    with open(filepath, "w") as f:
        print("json_save")
        json.dump(jdata, f)


def add(a: int, b: int):
    return a + b


def sub(a: int, b: int):
    return a - b


def funcSelect(ind):
    global window
    global func_table
    global treeWidget
    func_name = window.comboBox_Function.itemText(ind)
    func = func_table[func_name]
    varlist = func.__code__.co_varnames[:func.__code__.co_argcount]
    value = {}
    for varName in varlist:
        value[varName] = 0
    if treeWidget:
        treeWidget.varName = f"{func_name}_var"
        treeWidget.value = value


def funcExec():
    global window
    global func_table
    global treeWidget
    func_name = window.comboBox_Function.currentText()
    func = func_table[func_name]
    varName = func_name + "_var"
    args = list(treeWidget.value.values())
    answer =func(*args)
    if type(answer) is not str:
        answer = str(answer)
    window.lineEdit_Answer.clear()
    window.lineEdit_Answer.insert(answer)


def mainWindow():
    global func_table
    global window
    global treeWidget

    ui_file_name = "mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")[0]
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    window.actionREAD.triggered.connect(jread)
    window.actionSAVE.triggered.connect(jsave)
    window.pushButton_Exec.clicked.connect(funcExec)
    window.comboBox_Function.currentIndexChanged.connect(funcSelect)

    func_table = {"Add": add, "Sub": sub}

    # set func_table_name to combobox
    for key in func_table.keys():
        window.comboBox_Function.addItem(key)

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    val = {"a": 0, "b": {"c": 1, "d": {"e": 3,"f": 4}},"g": 5, "h": 6}
    treeWidget = QDictTreeWidget(val, nameof(val), ui=window)

    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow()

    sys.exit(app.exec())
