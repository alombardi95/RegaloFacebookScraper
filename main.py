import sys

from PyQt5.QtWidgets import QApplication

from app import app, db
from ui.main_window import MainWindow


def main():
    with app.app_context():
        db.create_all()
    app_ = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app_.exec_())


if __name__ == "__main__":
    main()
