import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QDialogButtonBox, QLineEdit, QLabel,
                             QGridLayout, QDialog, QMessageBox)

from models.progetto import Progetto


class AddProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggiungi Progetto")
        self.setup_ui()

    def setup_ui(self):
        # Imposta il layout della finestra di dialogo
        layout = QGridLayout(self)

        # Aggiungi etichette e campi di testo
        layout.addWidget(QLabel("Nome del Progetto:"), 0, 0)
        self.project_name_input = QLineEdit(self)
        layout.addWidget(self.project_name_input, 0, 1)

        # Pulsanti per annullare o aggiungere il progetto
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 1, 0, 1, 2)

    def get_data(self):
        return self.project_name_input.text()


class ProjectManager(QWidget):
    def __init__(self):
        super().__init__()
        self.db_progetti = Progetto()
        self.initUI()

    def initUI(self):
        # Layout principale per il widget
        layout = QVBoxLayout()

        # Tabella per la visualizzazione dei progetti
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # ad esempio, ID e Nome del Progetto
        self.table.setHorizontalHeaderLabels(["ID", "Nome del Progetto"])
        self.populate_table()  # Funzione per popolare la tabella
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # Bottoni per le operazioni CRUD
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Aggiungi")
        add_btn.clicked.connect(self.add_project)
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
        projects = [(x.id, x.nome) for x in self.db_progetti.get_progetti()] #[(1, "Progetto 1"), (2, "Progetto 2"), (3, "Progetto 3")]
        self.table.setRowCount(len(projects))
        for i, (proj_id, proj_name) in enumerate(projects):
            self.table.setItem(i, 0, QTableWidgetItem(str(proj_id)))
            self.table.setItem(i, 1, QTableWidgetItem(proj_name))

    def add_project(self):
        dialog = AddProjectDialog()
        if dialog.exec() == QDialog.Accepted:
            new_project_name = dialog.get_data()
            if new_project_name:  # Controlla che il nome non sia vuoto
                self.db_progetti.add_progetto(new_project_name)
                row_count = self.table.rowCount()
                self.table.insertRow(row_count)
                self.table.setItem(row_count, 0, QTableWidgetItem(str(row_count + 1)))  # ID del progetto
                self.table.setItem(row_count, 1, QTableWidgetItem(new_project_name))
                print(f"Progetto aggiunto: {new_project_name}")
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
    ex = ProjectManager()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
