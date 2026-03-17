from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTableWidget, QTableWidgetItem,
    QFrame, QPushButton, QSpinBox, QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt, QDate

from app.services.student_service import StudentService
from app.services.activity_service import ActivityService
from app.core.database import get_connection
from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import QStringListModel
from mysql.connector import Error
from datetime import datetime


class RegistroView(QWidget):
    def __init__(self):
        super().__init__()

        self.temp_records = []  # Lista temporal de registros del día
        self.all_students = []  # 🔥 lista base para filtrado

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # ==========================
        # CARDS KPI
        # ==========================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_students = self.create_card("Estudiantes del Día", 0)
        self.card_activities = self.create_card("Actividades del Día", 0)
        self.card_hours = self.create_card("Horas Totales", 0)

        cards_layout.addWidget(self.card_students)
        cards_layout.addWidget(self.card_activities)
        cards_layout.addWidget(self.card_hours)
        main_layout.addLayout(cards_layout)

        # ==========================
        # CONTENEDOR PRINCIPAL
        # ==========================
        container = QFrame()
        container.setObjectName("container")
        container.setStyleSheet("QFrame#container { background-color: transparent; border: none; }")

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(20)

        # ==========================
        # FORMULARIO
        # ==========================
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        # 🔥 NUEVO: ALUMNOS (MULTI SELECT + SEARCH)
        from PySide6.QtWidgets import QLineEdit, QListWidget

        self.alumno_input = QLineEdit()
        self.alumno_input.setPlaceholderText("Buscar alumno por nombre o número de control...")

        self.alumno_list = QListWidget()
        self.alumno_list.setSelectionMode(QListWidget.MultiSelection)

        self.alumno_input.setMinimumWidth(250)
        self.alumno_list.setMinimumWidth(250)
        self.alumno_list.setMaximumHeight(120)

        self.alumno_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                padding: 6px 10px;
                color: #111827;
            }
        """)

        self.alumno_list.setStyleSheet("""
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e3a8a;
            }
        """)

        alumno_layout = QVBoxLayout()
        alumno_layout.addWidget(self.alumno_input)
        alumno_layout.addWidget(self.alumno_list)

        # 🔹 Actividades (se mantiene igual)
        self.actividad_combo = QComboBox()
        self.actividad_combo.setMinimumWidth(250)

        combo_style = """
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 10px;
            padding: 6px 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            selection-background-color: #dbeafe;
            selection-color: #1e3a8a;
        }
        """
        self.actividad_combo.setStyleSheet(combo_style)

        # 🔹 Horas
        self.horas_spin = QSpinBox()
        self.horas_spin.setRange(1, 24)
        self.horas_spin.setValue(1)

        # Layout form
        form_layout.addWidget(QLabel("Alumno"))
        form_layout.addLayout(alumno_layout)
        form_layout.addWidget(QLabel("Actividad"))
        form_layout.addWidget(self.actividad_combo)
        form_layout.addWidget(QLabel("Horas"))
        form_layout.addWidget(self.horas_spin)

        container_layout.addLayout(form_layout)

        # ==========================
        # BOTONES
        # ==========================
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar")
        self.delete_button = QPushButton("Eliminar")
        self.clear_button = QPushButton("Limpiar Tabla")
        self.finalize_button = QPushButton("Finalizar Día")

        self.add_button.clicked.connect(self.add_temp_record)
        self.delete_button.clicked.connect(self.delete_temp_record)
        self.clear_button.clicked.connect(self.clear_all_records)
        self.finalize_button.clicked.connect(self.save_records)

        self.add_button.setStyleSheet("""
            QPushButton { background-color: #4f46e5; color: white; border-radius: 10px; padding: 8px 16px; }
            QPushButton:hover { background-color: #4338ca; }
        """)
        self.delete_button.setStyleSheet("""
            QPushButton { background-color: #ef4444; color: white; border-radius: 10px; padding: 8px 16px; }
            QPushButton:hover { background-color: #dc2626; }
        """)
        self.clear_button.setStyleSheet("""
            QPushButton { background-color: #f59e0b; color: white; border-radius: 10px; padding: 8px 16px; }
            QPushButton:hover { background-color: #d97706; }
        """)
        self.finalize_button.setStyleSheet("""
            QPushButton { background-color: #10b981; color: white; border-radius: 10px; padding: 8px 16px; }
            QPushButton:hover { background-color: #059669; }
        """)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(self.finalize_button)

        container_layout.addLayout(button_layout)

        # ==========================
        # TABLA
        # ==========================
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Alumno", "Actividad", "Horas"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #f4f6f9; border: 1px solid #cfd6df; border-radius: 18px; gridline-color: transparent; }
            QHeaderView::section { background-color: #dde3ea; padding: 10px; border: none; font-weight: 600; color: #2f3437; }
            QTableWidget::item:selected { background-color: #dbeafe; color: #1e3a8a; }
        """)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        container_layout.addWidget(self.table)

        container.setLayout(container_layout)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # 🔥 conexión del filtro
        self.alumno_input.textChanged.connect(self.filter_students)

        # Cargar datos iniciales
        self.refresh_all()

    def filter_students(self):
        text = self.alumno_input.text().lower()
        self.alumno_list.clear()

        for student in self.all_students:
            if text in student.lower():
                self.alumno_list.addItem(student)
    # ==========================
    # CARDS
    # ==========================
    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #f7f8fa; border-radius: 16px; border: 1px solid #d6dde6; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title)
        title_label.setStyleSheet("color:#6b7280; font-size:13px;")

        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size:28px; font-weight:600; color:#111827;")
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        return card

    # ==========================
    # REFRESH
    # ==========================
    def refresh_students(self):
        students = StudentService.list_students()

        # Guardamos lista base para filtro
        self.all_students = [f"{s[0]} - {s[1]}" for s in students]

        # Llenamos la lista visual
        self.alumno_list.clear()
        for s in self.all_students:
            self.alumno_list.addItem(s)
    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_students()
        self.refresh_activities()

    def refresh_activities(self):
        activities = ActivityService.get_all_activities()
        # Mostrar: "ID - Nombre actividad"
        activity_list = [f"{a[0]} - {a[1]}" for a in activities]

        self.setup_searchable_combobox(self.actividad_combo, activity_list)

    def refresh_all(self):
        self.refresh_table()
        self.update_cards()
        self.refresh_students()
        self.refresh_activities()

    def update_cards(self):
        # Contador de estudiantes únicos en la tabla
        unique_students = {r[0] for r in self.temp_records}
        self.card_students.findChild(QLabel, "value_label").setText(str(len(unique_students)))

        self.card_activities.findChild(QLabel, "value_label").setText(str(len(self.temp_records)))
        total_hours = sum(r[2] for r in self.temp_records)
        self.card_hours.findChild(QLabel, "value_label").setText(str(total_hours))

    # ==========================
    # TABLA
    # ==========================
    def refresh_table(self):
        self.table.setRowCount(len(self.temp_records))
        for i, record in enumerate(self.temp_records):
            for j, val in enumerate(record):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    # ==========================
    # CRUD TEMPORAL
    # ==========================
    def add_temp_record(self):
        selected_items = self.alumno_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Atención", "Selecciona al menos un alumno.")
            return

        actividad = self.actividad_combo.currentText()
        horas = self.horas_spin.value()

        for item in selected_items:
            alumno = item.text()

            # Buscar si ya existe ese alumno con esa actividad
            for i, record in enumerate(self.temp_records):
                if record[0] == alumno and record[1] == actividad:
                    # Si existe, sumamos horas
                    self.temp_records[i] = (alumno, actividad, record[2] + horas)
                    break
            else:
                # Si no existe, lo agregamos
                self.temp_records.append((alumno, actividad, horas))

        self.refresh_all()

    def setup_searchable_combobox(self, combo, items):

        combo.setEditable(True)
        combo.clear()
        combo.addItems(items)

        # Estilo para que NO se vea negro
        combo.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                padding: 6px 10px;
                color: #111827;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #dbeafe;
                selection-color: #1e3a8a;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: none;
            }
        """)

        #COMPLETER CORRECTO
        completer = QCompleter(items, combo)
        completer.setFilterMode(Qt.MatchContains)  # Busca dentro del texto
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        popup = completer.popup()
        popup.setStyleSheet("""
            QListView {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #e1e4e8;
            }
            QListView::item:selected {
                background-color: #dbeafe;
                color: #1e3a8a;
            }
        """)
        combo.setCompleter(completer)
    def edit_temp_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atención", "Selecciona un registro para modificar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar modificación",
            "¿Modificar este registro con los valores actuales?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            alumno = self.alumno_combo.currentText()
            actividad = self.actividad_combo.currentText()
            horas = self.horas_spin.value()
            self.temp_records[row] = (alumno, actividad, horas)
            self.refresh_all()

    def delete_temp_record(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atención", "Selecciona un registro para eliminar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.temp_records.pop(row)
            self.refresh_all()

    def clear_all_records(self):
        if not self.temp_records:
            QMessageBox.information(self, "Información", "No hay registros para eliminar.")
            return

        confirm = QMessageBox.question(
            self, "Confirmar limpieza",
            "¿Eliminar TODOS los registros de la tabla?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.temp_records.clear()
            self.refresh_all()

    def save_records(self):

        if not self.temp_records:
            QMessageBox.information(self, "Información", "No hay registros para guardar.")
            return

        try:
            with get_connection() as connection:

                if not connection:
                    QMessageBox.critical(self, "Error", "No hay conexión a la base de datos.")
                    return

                cursor = connection.cursor()
                confirm = QMessageBox.question(
                    self,
                    "Confirmar acción",
                    "¿Estás seguro de finalizar el día y guardar todos los registros?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm != QMessageBox.Yes:
                    return
    
                for alumno_texto, actividad_texto, horas in self.temp_records:

                    # Extraer valores desde "ID - Nombre"
                    numero_control = alumno_texto.split(" - ")[0]
                    id_actividad = actividad_texto.split(" - ")[0]

                    fecha_actual = datetime.now().date()

                    query = """
                        INSERT INTO registro_actividades
                        (numero_control, id_actividad, fecha, horas)
                        VALUES (%s, %s, %s, %s)
                    """

                    cursor.execute(query, (numero_control, id_actividad,fecha_actual, horas))

                connection.commit()

                QMessageBox.information(self, "Éxito", "Registros guardados correctamente.")

                self.temp_records.clear()
                self.refresh_all()

        except Error as e:
            QMessageBox.critical(self, "Error BD", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", str(e))