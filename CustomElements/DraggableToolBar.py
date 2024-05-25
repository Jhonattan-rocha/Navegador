from PySide6.QtWidgets import QToolBar, QMenu, QMessageBox, QLineEdit, QInputDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QMimeData, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QDrag, QAction
from DataOperations.register_recover import recover_favorities

class DraggableToolBar(QToolBar):
    def __init__(self, title, parent=None, webEngineView: QWebEngineView=None):
        super().__init__(title, parent)
        self.webEngineView = webEngineView
        self.setMovable(False) 
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.extra_menu = QMenu("Mais Favoritos", self)
        # Mais opção com um menu
        create_folder = self.extra_menu.addAction("Criar Pasta")
        create_folder.triggered.connect(self.create_folder)
        
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        
    def create_folder(self):
        folder, ok = QInputDialog.getText(self, "Criar Pasta", "Nome da pasta: ")
        print(folder)
        pass
        
    def showContextMenu(self, pos):
        self.extra_menu.exec(self.mapToGlobal(pos))
    
    def load_favorities(self):
        self.clear()
        historico = recover_favorities(20, True)
        cont = 0
        for site in historico:
            if cont < self.width() and site.folder == 'default':
                self.add_favorite(site.name, site.site)
                cont += 110
            
    def add_favorite(self, name, url):
        action = QAction((name[:75] + '...') if len(name) > 75 else name, self) 
        action.setData(QUrl(url))
        action.triggered.connect(lambda: self.webEngineView.load(QUrl(url)))
        self.addAction(action)

    def add_folder(self):
        pass

    def remove_action(self, action):
        pass
