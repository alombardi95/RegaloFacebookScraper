import sys
from database.create_app import db, app

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QDialogButtonBox, QLineEdit, QLabel,
                             QGridLayout, QDialog, QMessageBox)
from models.db_items import GruppoItem
from ui.LocationSelector import LocationSelector


class AddGruppoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggiungi gruppo")
        self.setGeometry(100, 100, 350, 200)
        self.setup_ui()

    def setup_ui(self):
        # Imposta il layout della finestra di dialogo
        layout = QVBoxLayout(self)

        # Aggiungi etichette e campi di testo
        layout.addWidget(QLabel("Nome del Gruppo:"))
        self.group_name_input = QLineEdit(self)
        layout.addWidget(self.group_name_input)

        layout.addWidget(QLabel("Link al Gruppo:"))
        self.group_link_input = QLineEdit(self)
        layout.addWidget(self.group_link_input)

        # Inserisce il widget di selezione della location
        self.location_selector = LocationSelector(self)
        layout.addWidget(self.location_selector)

        # Pulsanti per annullare o aggiungere il progetto
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "link": self.group_link_input.text(),
            "nome": self.group_name_input.text(),
            "paese": self.location_selector.combo_nazione.currentText(),
            "regione": self.location_selector.combo_regione.currentText(),
            "provincia": self.location_selector.combo_provincia.currentText(),
            "citta": self.location_selector.combo_citta.currentText(),
        }


class GruppiManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout principale per il widget
        layout = QVBoxLayout()

        # Tabella per la visualizzazione dei progetti
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # ad esempio, ID e Nome del Progetto
        self.table.setHorizontalHeaderLabels(["Link", "Nome"])
        self.populate_table()  # Funzione per popolare la tabella
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # Bottoni per le operazioni CRUD
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Aggiungi")
        add_btn.clicked.connect(self.add_group)
        edit_btn = QPushButton("Modifica")
        edit_btn.clicked.connect(self.edit_project)
        delete_btn = QPushButton("Elimina")
        delete_btn.clicked.connect(self.delete_project)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def populate_table(self):
        # Qui dovresti caricare i dati dei progetti. Questo è solo un esempio.
        self.table.clear()
        with app.app_context():
            groups: list[GruppoItem] = GruppoItem.query.all() # [(1, "Gruppo 1"), (2, "Gruppo 2"), (3, "Gruppo 3")]
        self.table.setRowCount(len(groups))
        for i, group in enumerate(groups):
            self.table.setItem(i, 0, QTableWidgetItem(group.link))
            self.table.setItem(i, 1, QTableWidgetItem(group.nome))

    def add_group(self):
        dialog = AddGruppoDialog()
        if dialog.exec() == QDialog.Accepted:
            group_info = dialog.get_data()
            if group_info:  # Controlla che il nome non sia vuoto
                gruppo = GruppoItem(**group_info)
                with app.app_context():
                    db.session.add(gruppo)
                    db.session.commit()
                self.populate_table()
                print(f"Gruppo aggiunto.")
            else:
                QMessageBox.warning(self, "Errore", "Il nome del progetto non può essere vuoto.", QMessageBox.Ok)

    def edit_project(self):
        # Implementa una funzione per modificare un progetto esistente
        print("Modifica un progetto esistente")

    def delete_project(self):
        # Implementa una funzione per eliminare un progetto esistente
        print("Elimina un progetto esistente")


def main():
    app = QApplication(sys.argv)
    ex = GruppiManager()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
