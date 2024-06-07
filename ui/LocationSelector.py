import json
from PyQt5.QtWidgets import (QWidget, QComboBox, QLabel, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit)


class LocationSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = self.load_data()  # Carica i dati dal file JSON
        self.setup_ui()

    def load_data(self):
        with open("ui/locations.json", "r") as file:
            return json.load(file)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.combo_nazione = QComboBox()
        self.combo_regione = QComboBox()
        self.combo_provincia = QComboBox()
        self.entry_citta = QLineEdit()

        layout.addWidget(QLabel("Nazione:"))
        layout.addWidget(self.combo_nazione)
        layout.addWidget(QLabel("Regione:"))
        layout.addWidget(self.combo_regione)
        layout.addWidget(QLabel("Provincia:"))
        layout.addWidget(self.combo_provincia)
        layout.addWidget(QLabel("Città:"))
        layout.addWidget(self.entry_citta)

        self.combo_nazione.currentIndexChanged.connect(self.update_regioni)
        self.combo_regione.currentIndexChanged.connect(self.update_province)

        self.populate_nazioni()

    def populate_nazioni(self):
        self.combo_nazione.addItems(self.data.keys())

    def update_regioni(self):
        self.combo_regione.clear()
        nazione = self.combo_nazione.currentText()
        if nazione:
            self.combo_regione.addItems(self.data[nazione].keys())

    def update_province(self):
        self.combo_provincia.clear()
        nazione = self.combo_nazione.currentText()
        regione = self.combo_regione.currentText()
        if nazione and regione:
            self.combo_provincia.addItems(self.data[nazione][regione])


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Dialog')
        self.setGeometry(100, 100, 350, 200)

        layout = QVBoxLayout(self)

        # Inserisce il widget di selezione della location
        self.location_selector = LocationSelector(self)
        layout.addWidget(self.location_selector)

        # Aggiunge un pulsante per dimostrazione
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        layout.addWidget(submit_button)

    def submit(self):
        # Potresti voler fare qualcosa con i dati selezionati qui
        print("Nazione:", self.location_selector.combo_nazione.currentText())
        print("Regione:", self.location_selector.combo_regione.currentText())
        print("Provincia:", self.location_selector.combo_provincia.currentText())
        print("Città:", self.location_selector.entry_citta.currentText())


def main():
    app = QApplication([])
    dlg = MainDialog()
    dlg.exec_()


if __name__ == '__main__':
    main()
