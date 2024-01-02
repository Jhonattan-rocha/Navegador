from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, QMimeData
from PySide6.QtGui import QAction, QIcon, QMouseEvent, QDrag, QPainter, QPixmap, QCursor, QColor
from PySide6.QtWidgets import QWidget, QTabWidget, QMenu, QTabBar, QApplication


class DraggableTabWidget(QTabWidget):
    tabMovedToAnotherMainPage = Signal(QWidget, str, QIcon, name='tabMovedToAnotherMainPage')
    main_instances = []

    def __del__(self):
        try:
            self.__class__.main_instances.remove(self.main_page)
        except Exception as e:
            print(e)

    def show_context_menu(self, event):
        menu = QMenu(self)
        join_action = QAction("Juntar abas", self)
        join_action.triggered.connect(self.join_tabs)
        close_action = QAction("Fechar aba", self)
        close_action.triggered.connect(self.close_tab)
        closes_action = QAction("Fechar abas", self)
        closes_action.triggered.connect(self.close_tabs)

        menu.addAction(close_action)
        menu.addAction(closes_action)
        menu.addAction(join_action)
        menu.exec(self.mapToGlobal(event))

    def join_tabs(self):

        main_instances = self.__class__.main_instances
        print(main_instances)
        # Verifica se há pelo menos duas instâncias
        if len(main_instances) >= 1:
            main_window_to_receive_tabs = self.main_page

            # Itera sobre as instâncias a partir da segunda
            for instance in main_instances:
                if instance != self.main_page:
                    tabs_to_transfer = instance.ui.tabs

                    # Transfere as abas para a primeira main_window
                    for index in range(tabs_to_transfer.count(), -1, -1):
                        widget = tabs_to_transfer.widget(index)
                        if widget:
                            tabs_to_transfer.removeTab(index)

                            widget.implementation.main_page = main_window_to_receive_tabs
                            widget.implementation.setParent(main_window_to_receive_tabs)
                            widget.setParent(widget.implementation)
                            main_window_to_receive_tabs.ui.tabs.addTab(widget,
                                                                       widget.implementation.windowTitle() or widget.implementation.ui.webEngineView.title())


                    self.update()
                    self.__class__.main_instances.remove(instance)
                    instance.close()
            main_window_to_receive_tabs.ui.tabs.setTabsClosable(True)

    def close_tab(self):
        current_index = self.currentIndex()
        tab = self.widget(current_index)
        self.removeTab(current_index)
        tab.implementation.deleteLater()
        tab.deleteLater()

    def close_tabs(self):
        cont = self.count()
        for i in range(cont):
            self.removeTab(i)
            tab = self.widget(i)
            tab.implementation.deleteLater()
            tab.deleteLater()

    def __init__(self, parent=None, main_page=None):
        super().__init__(parent)

        self.tabBar = self.TabBar(self)
        self.tabBar.setMovable(True)
        self.tabBar.onDetachTabSignal.connect(self.detachTab)
        self.tabBar.onMoveTabSignal.connect(self.moveTab)
        self.tabBar.onAttchTabSignal.connect(self.join_tabs)
        self.setTabBar(self.tabBar)
        self.__class__.main_instances.append(self.parent().implementation)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.main_page = main_page

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

        detachedTab = self.DetachedTab(contentWidget, self, name)
        detachedTab.setWindowModality(Qt.WindowModality.NonModal)
        detachedTab.setWindowTitle(name)
        detachedTab.setWindowIcon(icon)
        detachedTab.onCloseSignal.connect(self.attachTab)
        detachedTab.setObjectName(name)
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

            page = Main(new_tab=False)

            self.contentWidget.implementation.main_page = page
            self.contentWidget.implementation.setParent(page)
            self.contentWidget.setParent(self.contentWidget.implementation)
            page.ui.tabs.addTab(self.contentWidget,
                                self.contentWidget.implementation.windowTitle() or self.contentWidget.implementation.ui.webEngineView.title())
            self.update()
            page.show()

        def event(self, event):
            if event.type() == QEvent.Type.NonClientAreaMouseButtonDblClick:
                event.accept()
                self.close()

            return super().event(event)

        def closeEvent(self, event):
            self.onCloseSignal.emit(self.contentWidget, self.objectName(), self.windowIcon())
            event.accept()

    class TabBar(QTabBar):
        onDetachTabSignal = Signal(int, QPoint, name='onDetachTabSignal')
        onMoveTabSignal = Signal(int, int, name='onMoveTabSignal')
        onAttchTabSignal = Signal()

        def __init__(self, parent=None, main_page=None):
            super().__init__(parent)

            self.setAcceptDrops(True)
            self.setElideMode(Qt.TextElideMode.ElideRight)
            self.setSelectionBehaviorOnRemove(QTabBar.SelectionBehavior.SelectLeftTab)
            self.setMovable(True)
            self.dragStartPos = QPoint()
            self.dragDropedPos = QPoint()
            self.mouseCursor = QCursor()
            self.dragInitiated = False
            self.main_page = main_page

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

            if fromIndex == -1 or fromIndex == toIndex:
                self.onAttchTabSignal.emit()
                return

            super().dropEvent(event)
