import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # ------------------------------
    # Estilos globales mejorados
    # ------------------------------
    app.setStyleSheet("""
        QMainWindow {
            background-color: #e6e9ef;
        }

        QWidget {
            font-family: "Segoe UI";
            font-size: 14px;
            color: #2f3437;
        }

        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 10px;
            padding: 8px 12px;
        }

        QLineEdit:focus {
            border: 1px solid #4f46e5;
        }

        QPushButton {
            background-color: #4f46e5;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 8px 16px;
        }

        QPushButton:hover {
            background-color: #4338ca;
        }
        QMessageBox {
            background-color: #ffffff;
        }

        QMessageBox QLabel {
            color: #2f3437;
        }

        QMessageBox QPushButton {
            background-color: #e7e7e5;
            color: #2f3437;
            border-radius: 6px;
            padding: 6px 14px;
        }

        QMessageBox QPushButton:hover {
            background-color: #dcdcdc;
        }
    """)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()