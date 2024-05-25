import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QSizePolicy)

from app import db, app
from gruppi_manager import GruppiManager
from models.db_items import GruppoItem
from spider import scrape_groups


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_actions()

        # Configurazioni iniziali della finestra principale
        self.setWindowTitle('Facebook Scraper')
        self.setGeometry(100, 100, 800, 600)

        # Layout principale
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        # Barra laterale
        self.sidebar = QListWidget()
        #self.sidebar.addItems(["Progetti", "Gruppi"])
        self.sidebar.addItems(["Gruppi"])
        self.sidebar.currentItemChanged.connect(self.display_page)
        self.mainLayout.addWidget(self.sidebar)

        # Area di visualizzazione principale
        self.stack = QStackedWidget(self)
        #self.stack.addWidget(ProjectManager())
        self.stack.addWidget(GruppiManager())
        self.mainLayout.addWidget(self.stack, 4)

        self.sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Menu principale
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        #self.export_menu = self.menu_bar.addMenu("Esporta")
        self.help_menu = self.menu_bar.addMenu("Aiuto")

        # Azioni del menu
        exit_action = QAction("Esci", self)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        #export_action = QAction("Esporta Report in Excel", self)
        #self.export_menu.addAction(export_action)

        help_action = QAction("Aiuto", self)
        self.help_menu.addAction(help_action)

        # Barra degli strumenti
        self.toolbar = self.addToolBar("Toolbar")
        #self.toolbar.addAction("Aggiungi Progetto")
        #self.toolbar.addAction("Aggiungi Gruppo")
        #self.toolbar.addAction("Esporta Report")
        self.toolbar.addAction(self.run_bot_action)

    def create_actions(self):
        # azione per avviare il bot
        self.run_bot_action = QAction("Run", self)
        self.run_bot_action.triggered.connect(self.run_bot)

    @staticmethod
    def run_bot():
        with app.app_context():
            groups = GruppoItem.query.all()
        links = [group.link for group in groups]
        scrape_groups(links)

    def display_page(self, current, previous):
        if current:
            self.stack.setCurrentIndex(self.sidebar.row(current))


def main():
    with app.app_context():
        db.create_all()
    app_ = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app_.exec_())


if __name__ == '__main__':
    main()
