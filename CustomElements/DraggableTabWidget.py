from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class DraggableTabWidget(QTabWidget):
    tabMovedToAnotherMainPage = Signal(QWidget, str, QIcon, name='tabMovedToAnotherMainPage')

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)

        self.tabBar = self.TabBar(self)
        self.tabBar.setMovable(True)
        self.tabBar.onDetachTabSignal.connect(self.detachTab)
        self.tabBar.onMoveTabSignal.connect(self.moveTab)
        self.main_page = main_page
        self.setTabBar(self.tabBar)

    @Slot(QWidget, str, QIcon, name='attachTabToMainPage')
    def attachTabToMainPage(self, contentWidget, name, icon):
        # Emitir o sinal para indicar que a guia está sendo movida para outra tela principal
        self.tabMovedToAnotherMainPage.emit(contentWidget, name, icon)

    @Slot(int, int, name='moveTab')
    def moveTab(self, fromIndex, toIndex):
        widget = self.widget(fromIndex)
        icon = self.tabIcon(fromIndex)
        text = self.tabText(fromIndex)

        self.removeTab(fromIndex)
        self.insertTab(toIndex, widget, icon, text)
        self.setCurrentIndex(toIndex)

    @Slot(int, QPoint, name='detachTab')
    def detachTab(self, index, point):
        name = self.tabText(index)
        icon = self.tabIcon(index)
        if icon.isNull():
            icon = self.windowIcon()
        contentWidget = self.widget(index)
        contentWidgetRect = contentWidget.frameGeometry()

        existing_detached_tabs = [w for w in self.parent().children() if isinstance(w, self.DetachedTab)]
        for detached_tab in existing_detached_tabs:
            if detached_tab.contentWidget == contentWidget:
                detached_tab.activateWindow()
                return

        detachedTab = self.DetachedTab(contentWidget, self.parentWidget(), self.main_page)
        detachedTab.setWindowModality(Qt.WindowModality.NonModal)
        detachedTab.setWindowTitle(name)
        detachedTab.setWindowIcon(icon)
        detachedTab.setObjectName(name)
        detachedTab.setGeometry(contentWidgetRect)
        detachedTab.onCloseSignal.connect(self.attachTab)
        detachedTab.move(point)
        detachedTab.show()

    @Slot(QWidget, str, QIcon, name='attachTab')
    def attachTab(self, contentWidget, name, icon):
        contentWidget.setParent(self)
        index = self.count()
        index = self.insertTab(index, contentWidget, icon, name)

        if index > -1:
            self.setCurrentIndex(index)

    class DetachedTab(QWidget):
        onCloseSignal = Signal(QWidget, str, QIcon, name='onCloseSignal')

        def __init__(self, contentWidget: QWidget, parent=None, main_page=None):
            super().__init__(parent)
            self.contentWidget = contentWidget
            layout = QVBoxLayout()
            layout.addWidget(self.contentWidget)
            self.setLayout(layout)

            from main import Main
            page = Main()
            page.ui.tabs.addTab(self, self.windowTitle())
            page.ui.tabs.removeTab(1)
            page.show()

        def event(self, event):
            if event.type() == QEvent.Type.NonClientAreaMouseButtonDblClick:
                event.accept()
                self.close()

            return super().event(event)

        def closeEvent(self, event):
            self.onCloseSignal.emit(self.contentWidget, self.objectName(), self.windowIcon())

    class TabBar(QTabBar):
        onDetachTabSignal = Signal(int, QPoint, name='onDetachTabSignal')
        onMoveTabSignal = Signal(int, int, name='onMoveTabSignal')

        def __init__(self, parent=None):
            super().__init__(parent)

            self.setAcceptDrops(True)
            self.setElideMode(Qt.TextElideMode.ElideRight)
            self.setSelectionBehaviorOnRemove(QTabBar.SelectionBehavior.SelectLeftTab)
            self.setMovable(True)
            self.dragStartPos = QPoint()
            self.dragDropedPos = QPoint()
            self.mouseCursor = QCursor()
            self.dragInitiated = False

        def mouseDoubleClickEvent(self, event):
            event.accept()
            self.onDetachTabSignal.emit(self.tabAt(event.pos()), self.mouseCursor.pos())

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.dragStartPos = event.pos()

            self.dragDropedPos.setX(0)
            self.dragDropedPos.setY(0)
            self.dragInitiated = False

            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            if not self.dragStartPos.isNull() and (
                    (event.pos() - self.dragStartPos).manhattanLength() > QApplication.startDragDistance()):
                self.dragInitiated = True

            if (event.buttons() & Qt.MouseButton.LeftButton) and self.dragInitiated:
                finishMoveEvent = QMouseEvent(
                    QMouseEvent.Type.MouseMove, event.position(), Qt.MouseButton.NoButton,
                    Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier
                )

                super().mouseMoveEvent(finishMoveEvent)

                drag = QDrag(self)
                mimeData = QMimeData()
                mimeData.setData('action', b'application/tab-detach')
                drag.setMimeData(mimeData)

                pixmap = self.parentWidget().grab()
                targetPixmap = QPixmap()
                targetPixmap.fill(QColor().black())
                painter = QPainter()
                painter.setOpacity(0.85)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()
                drag.setPixmap(targetPixmap)

                dropAction = drag.exec(Qt.DropAction.MoveAction, Qt.DropAction.CopyAction)

                if dropAction == Qt.DropAction.IgnoreAction:
                    event.accept()
                    self.onDetachTabSignal.emit(self.tabAt(self.dragStartPos), self.mouseCursor.pos())
                # elif dropAction == Qt.DropAction.MoveAction:
                #     if not self.dragDropedPos.isNull():
                #         event.accept()
                #         self.onMoveTabSignal.emit(self.tabAt(self.dragDropedPos), self.tabAt(self.dragStartPos))
            else:
                super().mouseMoveEvent(event)

        def dragEnterEvent(self, event):
            mimeData = event.mimeData()
            formats = mimeData.formats()

            if 'action' in formats and mimeData.data('action') == 'application/tab-detach':
                event.acceptProposedAction()

            super().dragMoveEvent(event)

        def dropEvent(self, event):
            self.dragDropedPos = event.pos()
            event.accept()

            fromIndex = self.tabAt(self.dragStartPos)
            toIndex = self.tabAt(self.dragDropedPos)

            if fromIndex != -1 and toIndex != -1 and fromIndex != toIndex:
                self.onMoveTabSignal.emit(fromIndex, toIndex)
                return
            super().dropEvent(event)
