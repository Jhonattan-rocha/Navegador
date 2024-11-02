# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import sys, os

from PySide6.QtCore import (QByteArray, QDate, QDateTime, QDir, QEvent, QPoint,
                            QRect, QRegularExpression, QSettings, QSize, QTime,
                            QTimer, Qt, Slot)
from PySide6.QtGui import (QAction, QColor, QIcon, QIntValidator,
                           QDoubleValidator, QRegularExpressionValidator,
                           QValidator)
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QFileDialog, QHeaderView, QInputDialog,
                               QItemDelegate, QLineEdit, QTreeWidget, QTreeWidgetItem, QMainWindow,
                               QMessageBox, QStyle, QSpinBox, QStyleOptionViewItem)


class TypeChecker:
    def __init__(self, parent=None):
        self.bool_exp = QRegularExpression('^(true)|(false)$')
        assert self.bool_exp.isValid()
        self.bool_exp.setPatternOptions(QRegularExpression.CaseInsensitiveOption)

        self.byteArray_exp = QRegularExpression(r'^[\x00-\xff]*$')
        assert self.byteArray_exp.isValid()

        self.char_exp = QRegularExpression('^.$')
        assert self.char_exp.isValid()

        pattern = r'^[+-]?\d+$'
        self.int_exp = QRegularExpression(pattern)
        assert self.int_exp.isValid()

        pattern = r'^\(([0-9]*),([0-9]*),([0-9]*),([0-9]*)\)$'
        self.color_exp = QRegularExpression(pattern)
        assert self.color_exp.isValid()

        pattern = r'^\((-?[0-9]*),(-?[0-9]*)\)$'
        self.point_exp = QRegularExpression(pattern)
        assert self.point_exp.isValid()

        pattern = r'^\((-?[0-9]*),(-?[0-9]*),(-?[0-9]*),(-?[0-9]*)\)$'
        self.rect_exp = QRegularExpression(pattern)
        assert self.rect_exp.isValid()

        self.size_exp = QRegularExpression(self.point_exp)

        date_pattern = '([0-9]{,4})-([0-9]{,2})-([0-9]{,2})'
        self.date_exp = QRegularExpression(f'^{date_pattern}$')
        assert self.date_exp.isValid()

        time_pattern = '([0-9]{,2}):([0-9]{,2}):([0-9]{,2})'
        self.time_exp = QRegularExpression(f'^{time_pattern}$')
        assert self.time_exp.isValid()

        pattern = f'^{date_pattern}T{time_pattern}$'
        self.dateTime_exp = QRegularExpression(pattern)
        assert self.dateTime_exp.isValid()

    def type_from_text(self, text):
        if self.bool_exp.match(text).hasMatch():
            return bool
        if self.int_exp.match(text).hasMatch():
            return int
        return None

    def create_validator(self, value, parent):
        if isinstance(value, bool):
            return QRegularExpressionValidator(self.bool_exp, parent)
        if isinstance(value, float):
            return QDoubleValidator(parent)
        if isinstance(value, int):
            return QIntValidator(parent)
        if isinstance(value, QByteArray):
            return QRegularExpressionValidator(self.byteArray_exp, parent)
        if isinstance(value, QColor):
            return QRegularExpressionValidator(self.color_exp, parent)
        if isinstance(value, QDate):
            return QRegularExpressionValidator(self.date_exp, parent)
        if isinstance(value, QDateTime):
            return QRegularExpressionValidator(self.dateTime_exp, parent)
        if isinstance(value, QTime):
            return QRegularExpressionValidator(self.time_exp, parent)
        if isinstance(value, QPoint):
            return QRegularExpressionValidator(self.point_exp, parent)
        if isinstance(value, QRect):
            return QRegularExpressionValidator(self.rect_exp, parent)
        if isinstance(value, QSize):
            return QRegularExpressionValidator(self.size_exp, parent)
        return None

    def from_string(self, text, original_value):
        if isinstance(original_value, QColor):
            match = self.color_exp.match(text)
            return QColor(min(int(match.captured(1)), 255),
                          min(int(match.captured(2)), 255),
                          min(int(match.captured(3)), 255),
                          min(int(match.captured(4)), 255))
        if isinstance(original_value, QDate):
            value = QDate.fromString(text, Qt.ISODate)
            return value if value.isValid() else None
        if isinstance(original_value, QDateTime):
            value = QDateTime.fromString(text, Qt.ISODate)
            return value if value.isValid() else None
        if isinstance(original_value, QTime):
            value = QTime.fromString(text, Qt.ISODate)
            return value if value.isValid() else None
        if isinstance(original_value, QPoint):
            match = self.point_exp.match(text)
            return QPoint(int(match.captured(1)),
                          int(match.captured(2)))
        if isinstance(original_value, QRect):
            match = self.rect_exp.match(text)
            return QRect(int(match.captured(1)),
                         int(match.captured(2)),
                         int(match.captured(3)),
                         int(match.captured(4)))
        if isinstance(original_value, QSize):
            match = self.size_exp.match(text)
            return QSize(int(match.captured(1)),
                         int(match.captured(2)))
        if isinstance(original_value, list):
            return text.split(',')
        return type(original_value)(text)


class Configuracoes(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings_tree = SettingsTree()
        self.setCentralWidget(self.settings_tree)

        self.create_actions()
        self.create_menus()

        self.auto_refresh_action.setChecked(True)
        self.fallbacks_action.setChecked(True)

        self.setWindowTitle("Settings Editor")
        self.resize(500, 600)
        icon = QIcon()
        icon.addFile("./figs/config.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.default_path = os.path.join(".", "configs", "config.conf")

    @Slot()
    def open_inifile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open INI File",
                                                   '', "INI Files (*.ini *.conf)")

        if file_name:
            self.load_ini_file(file_name)

    def load_ini_file(self, file_name):
        settings = QSettings(file_name, QSettings.IniFormat)
        if settings.status() != QSettings.NoError:
            return
        self.set_settings_object(settings)
        self.fallbacks_action.setEnabled(False)

    @Slot()
    def open_registry_path(self):
        path, ok = QInputDialog.getText(self, "Open Registry Path",
                                        "Enter the path of config file:",
                                        QLineEdit.Normal, self.default_path)

        if ok and path != '':
            settings = QSettings(path, QSettings.NativeFormat)
            self.set_settings_object(settings)
            self.fallbacks_action.setEnabled(False)

    @Slot()
    def about(self):
        QMessageBox.about(self, "About Settings Editor",
                          "The <b>Settings Editor</b> my ethernet navigator "
                          "application using Qt."
                          "Settings credit: https://doc.qt.io/qtforpython-6/examples/example_corelib_settingseditor.html")

    def create_actions(self):
        self.open_ini_file_action = QAction("Open I&NI File...", self,
                                            shortcut="Ctrl+N", triggered=self.open_inifile)

        self.open_registry_path_action = QAction(
            "Open Windows &Registry Path...", self, shortcut="Ctrl+G",
            triggered=self.open_registry_path)

        self.refresh_action = QAction("&Refresh", self, shortcut="Ctrl+R",
                                      enabled=False, triggered=self.settings_tree.refresh)

        self.exit_action = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)

        self.auto_refresh_action = QAction("&Auto-Refresh", self,
                                           shortcut="Ctrl+A", checkable=True, enabled=False)
        self.auto_refresh_action.triggered[bool].connect(self.settings_tree.set_auto_refresh)
        self.auto_refresh_action.triggered[bool].connect(self.refresh_action.setDisabled)

        self.fallbacks_action = QAction("&Fallbacks", self,
                                        shortcut="Ctrl+F", checkable=True, enabled=False)
        self.fallbacks_action.triggered[bool].connect(self.settings_tree.set_fallbacks_enabled)

        self.about_action = QAction("&About", self, triggered=self.about)

        self.about_Qt_action = QAction("About &Qt", self,
                                       triggered=qApp.aboutQt)

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_ini_file_action)
        self.file_menu.addAction(self.open_registry_path_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.refresh_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.options_menu = self.menuBar().addMenu("&Options")
        self.options_menu.addAction(self.auto_refresh_action)
        self.options_menu.addAction(self.fallbacks_action)

        self.menuBar().addSeparator()

        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_action)
        self.help_menu.addAction(self.about_Qt_action)

    def set_settings_object(self, settings: QSettings):
        settings.setFallbacksEnabled(self.fallbacks_action.isChecked())
        self.settings_tree.set_settings_object(settings)

        self.refresh_action.setEnabled(True)
        self.auto_refresh_action.setEnabled(True)

        nice_name = QDir.fromNativeSeparators(settings.fileName())
        nice_name = nice_name.split('/')[-1]

        if not settings.isWritable():
            nice_name += " (read only)"

        self.setWindowTitle(f"{nice_name} - Settings Editor")

class SettingsTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._type_checker = TypeChecker()
        self.setItemDelegate(VariantDelegate(self._type_checker, self))

        self.setHeaderLabels(("Setting", "Type", "Value"))
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.Stretch)

        self.settings = None
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(2000)
        self.auto_refresh = False

        self.group_icon = QIcon()
        style = self.style()
        self.group_icon.addPixmap(style.standardPixmap(QStyle.StandardPixmap.SP_DirClosedIcon),
                                  QIcon.Normal, QIcon.Off)
        self.group_icon.addPixmap(style.standardPixmap(QStyle.StandardPixmap.SP_DirOpenIcon),
                                  QIcon.Normal, QIcon.On)
        self.key_icon = QIcon()
        self.key_icon.addPixmap(style.standardPixmap(QStyle.StandardPixmap.SP_FileDialogInfoView))

        self.refresh_timer.timeout.connect(self.maybe_refresh)

    def set_settings_object(self, settings):
        self.settings = settings
        self.clear()

        if self.settings is not None:
            self.settings.setParent(self)
            self.refresh()
            if self.auto_refresh:
                self.refresh_timer.start()
        else:
            self.refresh_timer.stop()

    def sizeHint(self):
        return QSize(800, 600)

    @Slot(bool)
    def set_auto_refresh(self, autoRefresh):
        self.auto_refresh = autoRefresh

        if self.settings is not None:
            if self.auto_refresh:
                self.maybe_refresh()
                self.refresh_timer.start()
            else:
                self.refresh_timer.stop()

    @Slot(bool)
    def set_fallbacks_enabled(self, enabled):
        if self.settings is not None:
            self.settings.setFallbacksEnabled(enabled)
            self.refresh()

    @Slot()
    def maybe_refresh(self):
        if self.state() != QAbstractItemView.EditingState:
            self.refresh()

    @Slot()
    def refresh(self):
        if self.settings is None:
            return

        # The signal might not be connected.
        try:
            self.itemChanged.disconnect(self.update_setting)
        except RuntimeError:
            pass
        except Exception:
            pass

        self.settings.sync()
        self.update_child_items(None)

        self.itemChanged.connect(self.update_setting)

    def event(self, event):
        if event.type() == QEvent.WindowActivate:
            if self.isActiveWindow() and self.auto_refresh:
                self.maybe_refresh()

        return super(SettingsTree, self).event(event)

    def update_setting(self, item):
        key = item.text(0)
        ancestor = item.parent()

        while ancestor:
            key = ancestor.text(0) + '/' + key
            ancestor = ancestor.parent()

        self.settings.setValue(key, item.data(2, Qt.UserRole))

        if self.auto_refresh:
            self.refresh()

    def update_child_items(self, parent):
        divider_index = 0

        for group in self.settings.childGroups():
            child_index = self.find_child(parent, group, divider_index)
            if child_index != -1:
                child = self.child_at(parent, child_index)
                child.setText(1, '')
                child.setText(2, '')
                child.setData(2, Qt.UserRole, None)
                self.move_item_forward(parent, child_index, divider_index)
            else:
                child = self.create_item(group, parent, divider_index)

            child.setIcon(0, self.group_icon)
            divider_index += 1

            self.settings.beginGroup(group)
            self.update_child_items(child)
            self.settings.endGroup()

        for key in self.settings.childKeys():
            child_index = self.find_child(parent, key, 0)
            if child_index == -1 or child_index >= divider_index:
                if child_index != -1:
                    child = self.child_at(parent, child_index)
                    for i in range(child.childCount()):
                        self.delete_item(child, i)
                    self.move_item_forward(parent, child_index, divider_index)
                else:
                    child = self.create_item(key, parent, divider_index)
                child.setIcon(0, self.key_icon)
                divider_index += 1
            else:
                child = self.child_at(parent, child_index)

            value = self.settings.value(key)
            if value is None:
                child.setText(1, 'Invalid')
            else:
                # Try to convert to type unless a QByteArray is received
                if isinstance(value, str):
                    value_type = self._type_checker.type_from_text(value)
                    if value_type:
                        value = self.settings.value(key, type=value_type)
                child.setText(1, value.__class__.__name__)
            child.setText(2, VariantDelegate.display_text(value))
            child.setData(2, Qt.UserRole, value)

        while divider_index < self.child_count(parent):
            self.delete_item(parent, divider_index)

    def create_item(self, text, parent, index):
        after = None

        if index != 0:
            after = self.child_at(parent, index - 1)

        if parent is not None:
            item = QTreeWidgetItem(parent, after)
        else:
            item = QTreeWidgetItem(self, after)

        item.setText(0, text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def delete_item(self, parent, index):
        if parent is not None:
            item = parent.takeChild(index)
        else:
            item = self.takeTopLevelItem(index)
        del item

    def child_at(self, parent, index):
        if parent is not None:
            return parent.child(index)
        else:
            return self.topLevelItem(index)

    def child_count(self, parent):
        if parent is not None:
            return parent.childCount()
        else:
            return self.topLevelItemCount()

    def find_child(self, parent, text, startIndex):
        for i in range(self.child_count(parent)):
            if self.child_at(parent, i).text(0) == text:
                return i
        return -1

    def move_item_forward(self, parent, oldIndex, newIndex):
        for int in range(oldIndex - newIndex):
            self.delete_item(parent, newIndex)


class VariantDelegate(QItemDelegate):
    def __init__(self, type_checker, parent=None):
        super().__init__(parent)
        self._type_checker = type_checker

    def paint(self, painter, option, index):
        if index.column() == 2:
            value = index.model().data(index, Qt.UserRole)
            if not self.is_supported_type(value):
                my_option = QStyleOptionViewItem(option)
                my_option.state &= ~QStyle.State_Enabled
                super(VariantDelegate, self).paint(painter, my_option, index)
                return

        super(VariantDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() != 2:
            return None

        original_value = index.model().data(index, Qt.UserRole)
        if not self.is_supported_type(original_value):
            return None

        editor = None
        if isinstance(original_value, bool):
            editor = QCheckBox(parent)
        elif isinstance(original_value, int):
            editor = QSpinBox(parent)
            editor.setRange(-32767, 32767)
        else:
            editor = QLineEdit(parent)
            editor.setFrame(False)
            validator = self._type_checker.create_validator(original_value, editor)
            if validator:
                editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        if not editor:
            return
        value = index.model().data(index, Qt.UserRole)
        if isinstance(editor, QCheckBox):
            editor.setCheckState(Qt.Checked if value else Qt.Unchecked)
        elif isinstance(editor, QSpinBox):
            editor.setValue(value)
        else:
            editor.setText(self.display_text(value))

    def value_from_lineedit(self, lineedit, model, index):
        if not lineedit.isModified():
            return None
        text = lineedit.text()
        validator = lineedit.validator()
        if validator is not None:
            state, text, _ = validator.validate(text, 0)
            if state != QValidator.Acceptable:
                return None
        original_value = index.model().data(index, Qt.UserRole)
        return self._type_checker.from_string(text, original_value)

    def setModelData(self, editor, model, index):
        value = None
        if isinstance(editor, QCheckBox):
            value = editor.checkState() == Qt.Checked
        elif isinstance(editor, QSpinBox):
            value = editor.value()
        else:
            value = self.value_from_lineedit(editor, model, index)
        if value is not None:
            model.setData(index, value, Qt.UserRole)
            model.setData(index, self.display_text(value), Qt.DisplayRole)

    @staticmethod
    def is_supported_type(value):
        return isinstance(value, (bool, float, int, QByteArray, str, QColor,
                                  QDate, QDateTime, QTime, QPoint, QRect,
                                  QSize, list))

    @staticmethod
    def display_text(value):
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return '✓' if value else 'x'
        if isinstance(value, (int, float, QByteArray)):
            return str(value)
        if isinstance(value, QColor):
            (r, g, b, a) = (value.red(), value.green(), value.blue(), value.alpha())
            return f'({r},{g},{b},{a})'
        if isinstance(value, (QDate, QDateTime, QTime)):
            return value.toString(Qt.ISODate)
        if isinstance(value, QPoint):
            x = value.x()
            y = value.y()
            return f'({x},{y})'
        if isinstance(value, QRect):
            x = value.x()
            y = value.y()
            w = value.width()
            h = value.height()
            return f'({x},{y},{w},{h})'
        if isinstance(value, QSize):
            w = value.width()
            h = value.height()
            return f'({w},{h})'
        if isinstance(value, list):
            return ','.join(map(repr, value))
        if value is None:
            return '<Invalid>'

        return f'<{value}>'
