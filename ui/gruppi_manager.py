import sys
from typing import Optional

from PyQt5.QtCore import Qt, QRegExp

from database.create_app import db, app

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QDialogButtonBox, QLineEdit, QLabel,
                             QGridLayout, QDialog, QMessageBox)
from models.db_items import GruppoItem
from ui.LocationSelector import LocationSelector


class AddModifyGruppoDialog(QDialog):
    def __init__(self, record_to_modify: Optional[GruppoItem] = None):
        super().__init__()
        self.setWindowTitle("Aggiungi gruppo" if not record_to_modify else "Modifica gruppo")
        self.setGeometry(100, 100, 350, 200)
        self.is_modify_dialog = False
        if record_to_modify:
            self.is_modify_dialog = True
            self.record_to_modify = record_to_modify
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
        self.group_link_input.setReadOnly(self.is_modify_dialog)
        layout.addWidget(self.group_link_input)

        # Inserisce il widget di selezione della location
        self.location_selector = LocationSelector(self)
        layout.addWidget(self.location_selector)

        # Pulsanti per annullare o aggiungere il progetto
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if self.is_modify_dialog:
            self.populate_dialog()

    def get_data(self):
        result = {
            "nome": self.group_name_input.text(),
            "paese": self.location_selector.combo_nazione.currentText(),
            "regione": self.location_selector.combo_regione.currentText(),
            "provincia": self.location_selector.combo_provincia.currentText(),
            "citta": self.location_selector.combo_citta.currentText(),
        }
        if not self.is_modify_dialog:
            result["link"] = self.group_link_input.text()

        return result

    def populate_dialog(self):
        self.group_name_input.setText(self.record_to_modify.nome)
        self.group_link_input.setText(self.record_to_modify.link)
        self.location_selector.combo_nazione.setCurrentText(self.record_to_modify.paese)
        self.location_selector.combo_regione.setCurrentText(self.record_to_modify.regione)
        self.location_selector.combo_provincia.setCurrentText(self.record_to_modify.provincia)
        self.location_selector.combo_nazione.setCurrentText(self.record_to_modify.citta)


class GruppiManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout principale per il widget
        layout = QVBoxLayout()

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filter text...")
        self.filter_edit.textChanged.connect(self.filter_text_changed)
        layout.addWidget(self.filter_edit)

        # Tabella per la visualizzazione dei progetti
        self.table = QTableWidget()
        table_headers = ["Link", "Nome", "Paese", "Regione", "Provincia", "Citta"]
        self.table.setColumnCount(len(table_headers))  # ad esempio, ID e Nome del Progetto
        self.table.setHorizontalHeaderLabels(table_headers)

        # Configura la tabella per selezionare tutta la riga
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

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

    def add_non_editable_item(self, row, column, item):
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Rende la cella non modificabile
        self.table.setItem(row, column, item)

    def filter_text_changed(self, text):
        regex = QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(regex)

    def populate_table(self):
        # Qui dovresti caricare i dati dei progetti. Questo è solo un esempio.
        self.table.clearContents()
        with app.app_context():
            groups: list[GruppoItem] = GruppoItem.query.all() # [(1, "Gruppo 1"), (2, "Gruppo 2"), (3, "Gruppo 3")]
        self.table.setRowCount(len(groups))
        for i, group in enumerate(groups):
            self.add_non_editable_item(i, 0, QTableWidgetItem(group.link))
            self.add_non_editable_item(i, 1, QTableWidgetItem(group.nome))
            self.add_non_editable_item(i, 2, QTableWidgetItem(group.paese))
            self.add_non_editable_item(i, 3, QTableWidgetItem(group.regione))
            self.add_non_editable_item(i, 4, QTableWidgetItem(group.provincia))
            self.add_non_editable_item(i, 5, QTableWidgetItem(group.citta))

    def add_group(self):
        dialog = AddModifyGruppoDialog()
        if dialog.exec() == QDialog.Accepted:
            group_info = dialog.get_data()
            group_link = group_info.get("link")
            if group_info and group_link:  # Controlla che il nome non sia vuoto
                gruppo = GruppoItem(**group_info)
                with app.app_context():
                    existing_record = GruppoItem.query.filter_by(link=group_link)
                    if not existing_record.first():
                        db.session.add(gruppo)
                        db.session.commit()
                    else:
                        QMessageBox.warning(self, "Errore", "Il gruppo già esiste. Usa la funzione modifica.", QMessageBox.Ok)
                self.populate_table()
                print(f"Gruppo aggiunto.")
            else:
                QMessageBox.warning(self, "Errore", "Il link non può essere vuoto.", QMessageBox.Ok)

    def edit_project(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona un record da modificare.")
            return

        # Recuperare l'ID del record dalla prima colonna
        record_id = self.table.item(selected_row, 0).text()

        with app.app_context():
            record = GruppoItem.query.get(record_id)
            dialog = AddModifyGruppoDialog(record_to_modify=record)

        if dialog.exec() == QDialog.Accepted:
            edited_group_info = dialog.get_data()
            if edited_group_info:  # Controlla che il nome non sia vuoto
                with app.app_context():
                    #gruppo = GruppoItem.query.get(edited_group_info['link'])
                    record = GruppoItem.query.filter_by(link=record_id)

                    if record.first():
                        record.update(edited_group_info)
                        db.session.commit()
                self.populate_table()
            else:
                QMessageBox.warning(self, "Errore", "I campo non può essere vuoto", QMessageBox.Ok)

    def delete_project(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona un record da eliminare.")
            return

        # Recuperare l'ID del record dalla prima colonna
        record_id = self.table.item(selected_row, 0).text()

        # Confermare l'eliminazione
        confirm = QMessageBox.question(self, "Conferma Eliminazione",
                                       f"Sei sicuro di voler eliminare il record con ID {record_id}?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            with app.app_context():
                record = GruppoItem.query.get(record_id)
                db.session.delete(record)
                db.session.commit()

            self.populate_table()


def main():
    app = QApplication(sys.argv)
    ex = GruppiManager()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
