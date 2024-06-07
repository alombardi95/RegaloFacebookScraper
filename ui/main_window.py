import csv
import os

from PyQt5.QtWidgets import (QMainWindow, QAction, QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QSizePolicy, QFileDialog, QMessageBox)

from app import db, app, config
from models.db_items import GruppoItem
from spider import scrape_groups
from ui.gruppi_manager import GruppiManager


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
        self.sidebar.addItems(["Gruppi"])
        self.mainLayout.addWidget(self.sidebar)

        # Area di visualizzazione principale
        self.stack = QStackedWidget(self)
        #self.stack.addWidget(ProjectManager())
        self.gruppi_manager_widget = GruppiManager()
        self.stack.addWidget(self.gruppi_manager_widget)
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
        self.toolbar.addAction(self.importa_gruppi_action)
        self.toolbar.addAction(self.run_bot_action)

    def create_actions(self):
        # azione per avviare il bot
        self.run_bot_action = QAction("Run", self)
        self.run_bot_action.triggered.connect(self.run_bot)

        # azione per importare gruppi
        self.importa_gruppi_action = QAction("Importa", self)
        self.importa_gruppi_action.triggered.connect(self.importa_gruppi)

    def run_bot(self):
        with app.app_context():
            groups = GruppoItem.query.all()
        links = [group.link for group in groups]
        scrape_groups(links)
        QMessageBox.information(self, "Run Terminata", "Il processo di scraping è finito")

    @staticmethod
    def import_csv_to_db(filename: str):
        '''
        Funzione che mappa e importa i gruppi da un file CSV

        :param filename: percorso del file da importare
        '''
        if not os.path.exists(filename):
            return False

        exports = 0

        headers = config.CSV_HEADERS
        with open(filename, mode='r', newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            data = [GruppoItem(
                link=row[headers.Link],
                nome=row[headers.Nome],
                regione=row[headers.Regione],
                citta=row[headers.Citta]
            ) for row in reader]

        with app.app_context():
            for gruppo in data:
                if not GruppoItem.query.get(gruppo.link):
                    db.session.add(gruppo)
                    exports += 1
                else:
                    pass

            db.session.commit()

        return exports

    def importa_gruppi(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "CSV Files (*.csv);;All Files (*)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", file_filter, options=options)
        if file_name:
            result = self.import_csv_to_db(file_name)
            QMessageBox.information(self, "Importazione fatta", f"Importati {result} nuovi records.")
            self.gruppi_manager_widget.populate_table()
