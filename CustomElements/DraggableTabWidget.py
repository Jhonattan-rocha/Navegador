from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *


class DraggableTabWidget(QTabWidget):
    tabMovedToAnotherMainPage = Signal(QWidget, str, QIcon, name='tabMovedToAnotherMainPage')
    main_instances = []

    def __del__(self):
        self.__class__.main_instances.remove(self.parent().implementation)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tabBar = self.TabBar(self)
        self.tabBar.setMovable(True)
        self.tabBar.onDetachTabSignal.connect(self.detachTab)
        self.tabBar.onMoveTabSignal.connect(self.moveTab)
        self.tabBar.onAttchTabSignal.connect(self.attachTab)
        self.setTabBar(self.tabBar)
        self.__class__.main_instances.append(self.parent().implementation)

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

        detachedTab = self.DetachedTab(contentWidget, self.parentWidget(), name)
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
        # Setando a guia como filha do QTabWidget atual
        contentWidget.setParent(self)

        # Obtendo o índice onde a guia será inserida
        index = self.count()

        # Inserindo a guia no QTabWidget atual
        index = self.insertTab(index, contentWidget, icon, name)

        # Definindo a guia recém-inserida como a guia atual, se inserida com sucesso
        if index > -1:
            self.setCurrentIndex(index)

    class DetachedTab(QWidget):
        onCloseSignal = Signal(QWidget, str, QIcon, name='onCloseSignal')

        def __init__(self, contentWidget: QWidget, parent=None, name="Nova página"):
            super().__init__(parent)
            self.contentWidget = contentWidget

            from main import Main
            from Pages.Implementaion import Default, Historic, Download

            page = Main(new_tab=False)

            old_page = self.contentWidget.findChildren(QWebEngineView)
            if bool(old_page):
                url = old_page[0].url().toString()
                new_page = Default(parent=page, main_window=page)
                new_page.ui.webEngineView.load(url)
                self.contentWidget.deleteLater()
                self.update()
                page.ui.tabs.addTab(new_page.ui.page, name)
            elif 'download' in self.contentWidget.objectName():
                new_page = Download(parent=page, main_page=page)
                self.contentWidget.deleteLater()
                self.update()
                page.ui.tabs.addTab(new_page.ui.downloads, name)
            elif 'historic' in self.contentWidget.objectName():
                new_page = Historic(parent=page, main_page=page)
                self.contentWidget.deleteLater()
                self.update()
                page.ui.tabs.addTab(new_page.ui.historic, name)

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
        onAttchTabSignal = Signal(QWidget, str, QIcon)

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
            print(f"from: {fromIndex}, to: {toIndex}")
            print(self.dragStartPos.toTuple(), self.dragDropedPos.toTuple())
            if fromIndex != -1 and toIndex != -1 and fromIndex != toIndex:
                self.onMoveTabSignal.emit(fromIndex, toIndex)
                return

            if fromIndex == -1 or fromIndex == toIndex:
                for m in self.parent().__class__.main_instances:
                    print(m)
            super().dropEvent(event)
