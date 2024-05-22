import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenuBar,
                             QVBoxLayout, QWidget, QListWidget, QPushButton,
                             QStackedWidget, QLabel, QHBoxLayout, QSizePolicy)
from project_manager import ProjectManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurazioni iniziali della finestra principale
        self.setWindowTitle('Gestione Progetti e Gruppi')
        self.setGeometry(100, 100, 800, 600)

        # Layout principale
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        # Barra laterale
        self.sidebar = QListWidget()
        self.sidebar.addItems(["Progetti", "Gruppi"])
        self.sidebar.currentItemChanged.connect(self.display_page)
        self.mainLayout.addWidget(self.sidebar)

        # Area di visualizzazione principale
        self.stack = QStackedWidget(self)
        self.stack.addWidget(ProjectManager())
        self.stack.addWidget(self.create_page("Gruppi"))
        self.mainLayout.addWidget(self.stack, 4)

        self.sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Menu principale
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.export_menu = self.menu_bar.addMenu("Esporta")
        self.help_menu = self.menu_bar.addMenu("Aiuto")

        # Azioni del menu
        exit_action = QAction("Esci", self)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        export_action = QAction("Esporta Report in Excel", self)
        self.export_menu.addAction(export_action)

        help_action = QAction("Aiuto", self)
        self.help_menu.addAction(help_action)

        # Barra degli strumenti
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addAction("Aggiungi Progetto")
        self.toolbar.addAction("Aggiungi Gruppo")
        self.toolbar.addAction("Esporta Report")
        self.toolbar.addAction("Avvia Procedura")

    def create_page(self, text):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"Contenuto per {text}", page)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def display_page(self, current, previous):
        if current:
            self.stack.setCurrentIndex(self.sidebar.row(current))


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
