from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QMessageBox, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QFrame, QHeaderView
)
from PySide6.QtCore import Qt
from app.services.student_service import StudentService
from app.services.activity_service import ActivityService

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook


class StudentView(QWidget):

    def __init__(self):
        super().__init__()

        # 🔥 NUEVO ESTADO INTERNO
        self.selected_student_id = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # ==========================
        # CARDS KPI
        # ==========================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_students = self.create_card("Total Estudiantes", 0)
        self.card_activities = self.create_card("Total Actividades", 0)
        self.card_hours = self.create_card("Horas Registradas", 0)

        cards_layout.addWidget(self.card_students)
        cards_layout.addWidget(self.card_activities)
        cards_layout.addWidget(self.card_hours)

        main_layout.addLayout(cards_layout)

        # ==========================
        # CONTENEDOR PRINCIPAL
        # ==========================
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(20)

        # ==========================
        # FORMULARIO
        # ==========================
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        self.numero_control_input = QLineEdit()
        self.numero_control_input.setPlaceholderText("Número de control")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo")

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")

        form_layout.addWidget(self.numero_control_input)
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.correo_input)
        form_layout.addWidget(self.telefono_input)

        container_layout.addLayout(form_layout)

        # ==========================
        # BOTONES
        # ==========================
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Registrar")
        self.edit_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")
        
        # 🎨 ESTILOS ESPECÍFICOS POR TIPO DE ACCIÓN

        # Primario (Registrar)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)

        # Secundario (Editar)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #c7d2fe;
                color: #2f3437;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #a5b4fc;
            }
        """)

        # Destructivo (Eliminar)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)

        self.add_button.clicked.connect(self.register_student)
        self.edit_button.clicked.connect(self.modify_student)
        self.delete_button.clicked.connect(self.delete_student)
        #self.refresh_button.clicked.connect(self.refresh_all)
        #self.pdf_button.clicked.connect(self.generate_pdf)
        #self.excel_button.clicked.connect(self.export_excel)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        #button_layout.addWidget(self.pdf_button)
        #button_layout.addWidget(self.excel_button)
        #button_layout.addWidget(self.refresh_button)

        container_layout.addLayout(button_layout)

        # ==========================
        # TABLA
        # ==========================
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Número Control", "Nombre", "Correo", "Teléfono"]
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.viewport().setAutoFillBackground(False)

        self.table.setStyleSheet("""
        QTableWidget {
            background-color: #f4f6f9;
            border: 1px solid #cfd6df;
            border-radius: 18px;
            gridline-color: transparent;
        }

        QHeaderView::section {
            background-color: #dde3ea;
            padding: 10px;
            border: none;
            font-weight: 600;
            color: #2f3437;
        }

        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #e3e8ef;
        }

        QTableWidget::item:selected {
            background-color: #dbeafe;
            color: #1e3a8a;
        }
        """)

        self.table.setShowGrid(False)
        self.table.setAttribute(Qt.WA_StyledBackground, True)

        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setStretchLastSection(True)

        # 🔥 CONEXIÓN NUEVA
        self.table.itemSelectionChanged.connect(self.load_selected_student)

        container_layout.addWidget(self.table)
        container.setLayout(container_layout)
        main_layout.addWidget(container)

        self.setLayout(main_layout)

        self.refresh_all()

    # ==========================
    # CARGA AUTOMÁTICA
    # ==========================
    def load_selected_student(self):
        row = self.table.currentRow()

        if row < 0:
            self.selected_student_id = None
            return

        numero = self.table.item(row, 0)
        nombre = self.table.item(row, 1)
        correo = self.table.item(row, 2)
        telefono = self.table.item(row, 3)

        if numero and nombre and correo and telefono:
            self.selected_student_id = numero.text()
            self.numero_control_input.setText(numero.text())
            self.nombre_input.setText(nombre.text())
            self.correo_input.setText(correo.text())
            self.telefono_input.setText(telefono.text())

    # ==========================
    # CARDS
    # ==========================
    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f7f8fa;
                border-radius: 16px;
                border: 1px solid #d6dde6;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title)
        value_label = QLabel(str(value))
        value_label.setObjectName("value_label")
        value_label.setStyleSheet("font-size: 28px; font-weight: 600;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.setLayout(layout)
        return card

    # ==========================
    # REFRESH
    # ==========================
    def refresh_all(self):
        self.load_students()
        self.update_cards()

        # 🔥 RESET PROFESIONAL
        self.selected_student_id = None
        self.numero_control_input.clear()
        self.nombre_input.clear()
        self.correo_input.clear()
        self.telefono_input.clear()

    def update_cards(self):
        students = StudentService.list_students() or []
        activities = ActivityService.get_all_activities() or []

        total_hours = 0
        for a in activities:
            if isinstance(a, (list, tuple)) and len(a) >= 5:
                total_hours += a[4]

        self.card_students.findChild(QLabel, "value_label").setText(str(len(students)))
        self.card_activities.findChild(QLabel, "value_label").setText(str(len(activities)))
        self.card_hours.findChild(QLabel, "value_label").setText(str(total_hours))

    def load_students(self):
        students = StudentService.list_students() or []
        self.table.setRowCount(len(students))

        for row_index, student in enumerate(students):
            for col_index, value in enumerate(student):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    # ==========================
    # CRUD MEJORADO
    # ==========================

    def register_student(self):
        numero = self.numero_control_input.text().strip()
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        telefono = self.telefono_input.text().strip()

        if not numero or not nombre:
            QMessageBox.warning(self, "Validación", "Número y nombre son obligatorios.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar registro",
            "¿Estás seguro de registrar este estudiante?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        StudentService.add_student(numero, nombre, correo, telefono)
        self.refresh_all()

        QMessageBox.information(self, "Éxito", "Estudiante registrado correctamente.")

    def modify_student(self):
        if not self.selected_student_id:
            QMessageBox.warning(self, "Atención", "Selecciona un estudiante para editar.")
            return

        numero = self.numero_control_input.text().strip()
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        telefono = self.telefono_input.text().strip()

        if not numero or not nombre:
            QMessageBox.warning(self, "Validación", "Número y nombre son obligatorios.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar modificación",
            "¿Estás seguro de actualizar este estudiante?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        StudentService.update_student(numero, nombre, correo, telefono)
        self.refresh_all()

        QMessageBox.information(self, "Éxito", "Estudiante actualizado correctamente.")

    def delete_student(self):
        if not self.selected_student_id:
            QMessageBox.warning(self, "Atención", "Selecciona un estudiante para eliminar.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de eliminar este estudiante?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        StudentService.delete_student(self.selected_student_id)
        self.refresh_all()

        QMessageBox.information(self, "Éxito", "Estudiante eliminado correctamente.")

    # ==========================
    # PDF
    # ==========================
    def generate_pdf(self):
        students = StudentService.list_students()
        activities = ActivityService.get_all_activities()

        doc = SimpleDocTemplate("reporte_estudiantes.pdf", pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Reporte General de Estudiantes", styles["Title"]))
        elements.append(Spacer(1, 20))

        for student in students:
            numero = student[0]
            nombre = student[1]

            elements.append(Paragraph(f"<b>{nombre}</b> ({numero})", styles["Heading2"]))
            elements.append(Spacer(1, 10))

            student_activities = [a for a in activities if a[1] == numero]

            data = [["Actividad", "Fecha", "Horas"]]
            total_hours = 0

            for act in student_activities:
                data.append([act[2], str(act[3]), str(act[4])])
                total_hours += act[4]

            data.append(["", "Total Horas", str(total_hours)])

            table = Table(data, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

        doc.build(elements)

    # ==========================
    # EXCEL
    # ==========================
    def export_excel(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Estudiantes"

        students = StudentService.list_students() or []

        headers = ["Número Control", "Nombre", "Correo", "Teléfono"]
        sheet.append(headers)

        for student in students:
            sheet.append(student)

        workbook.save("reporte_estudiantes.xlsx")