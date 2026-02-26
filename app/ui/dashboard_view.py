from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from app.services.student_service import StudentService
from app.services.activity_service import ActivityService

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #f7f8fa;")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # ======================
        # DATOS NORMALIZADOS
        # ======================
        students_raw = StudentService.list_students() or []
        activities_raw = ActivityService.get_all_activities() or []

        # Normalizar estudiantes
        students = []
        for s in students_raw:
            if isinstance(s, dict):
                students.append({'numero': s.get('numero_control') or s.get('numero'), 'nombre': s.get('nombre')})
            elif isinstance(s, (list, tuple)) and len(s) >= 2:
                students.append({'numero': s[0], 'nombre': s[1]})

        # Normalizar actividades y sumar horas por estudiante
        hours_by_student = {}
        activities = []

        for a in activities_raw:
            numero = None
            horas = 0

            if isinstance(a, dict):
                numero = a.get('numero_control') or a.get('numero')
                horas = a.get('horas', 0)
            elif isinstance(a, (list, tuple)):
                if len(a) >= 5:
                    numero = a[1]  # numero_control
                    horas = a[4]   # horas
                elif len(a) >= 2:
                    numero = a[1]
                    horas = 0
                else:
                    continue
            else:
                continue

            if numero is not None:
                hours_by_student[numero] = hours_by_student.get(numero, 0) + horas
                activities.append({'numero': numero, 'horas': horas})

        total_students = len(students)
        total_activities = len(activities)
        total_hours = sum(a['horas'] for a in activities)

        # ======================
        # KPI CARDS
        # ======================
        self.card_students = self.create_kpi_card("👨‍🎓 Estudiantes", total_students)
        self.card_activities = self.create_kpi_card("📋 Actividades", total_activities)
        self.card_hours = self.create_kpi_card("⏰ Horas Totales", total_hours)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.addStretch()
        cards_layout.addWidget(self.card_students)
        cards_layout.addWidget(self.card_activities)
        cards_layout.addWidget(self.card_hours)
        cards_layout.addStretch()
        main_layout.addLayout(cards_layout, stretch=1)

        # ======================
        # TABLA
        # ======================
        table_card = QFrame()
        table_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e5e7eb;
                padding: 12px;
            }
        """)
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(12)

        table_title = QLabel("Resumen de horas por estudiante")
        table_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #374151; padding: 4px;")
        table_layout.addWidget(table_title)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Número Control", "Nombre", "Horas"])
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setFrameShape(QFrame.NoFrame)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        table.setMinimumHeight(250)
        table.setMaximumHeight(500)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        header.setMinimumHeight(40)

        table.setRowCount(len(students))
        for row, student in enumerate(students):
            numero = student['numero']
            nombre = student['nombre']
            horas = hours_by_student.get(numero, 0)

            table.setItem(row, 0, QTableWidgetItem(str(numero)))
            table.setItem(row, 1, QTableWidgetItem(nombre))
            table.setItem(row, 2, QTableWidgetItem(str(horas)))

            for col in range(3):
                table.item(row, col).setTextAlignment(Qt.AlignCenter)

        table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; border: none; }
            QHeaderView::section { background-color: #f3f4f6; font-weight: 600; color: #111827; padding: 8px; }
            QTableWidget::item { border-bottom: 1px solid #e5e7eb; padding: 6px 4px; }
            QTableWidget::item:hover { background-color: #f1f5f9; }
            QTableWidget::item:selected { background-color: #dbeafe; color: #1e3a8a; }
        """)

        table_layout.addWidget(table)
        main_layout.addWidget(table_card, stretch=3)

        # ======================
        # GRÁFICO DONUT
        # ======================
        chart_card = QFrame()
        chart_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e5e7eb;
                padding: 12px;
            }
        """)
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(16, 16, 16, 16)
        chart_layout.setSpacing(12)

        chart_title = QLabel("Horas acumuladas")
        chart_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #374151;")
        chart_layout.addWidget(chart_title)

        chart_canvas = self.create_chart(students, hours_by_student)
        chart_layout.addWidget(chart_canvas)
        main_layout.addWidget(chart_card, stretch=3)

        self.setLayout(main_layout)

    # ======================
    # FUNCIONES KPI
    # ======================
    def create_kpi_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f7f8fa;
                border-radius: 16px;
                border: 1px solid #d6dde6;
            }
        """)
        card.setFixedSize(200, 120)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        label = QLabel(f"{title}\n{value}")
        label.setFont(QFont("Segoe UI Emoji", 18, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #111827;")
        layout.addWidget(label)
        return card

    # ======================
    # FUNCION DONUT CHART
    # ======================
    def create_chart(self, students, hours_by_student):
        figure = Figure(figsize=(6, 4), dpi=100)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        labels, values = [], []
        for student in students:
            numero = student['numero']
            nombre = student['nombre']
            total = hours_by_student.get(numero, 0)
            if total > 0:
                labels.append(nombre)
                values.append(total)

        if not values:
            ax.text(0.5, 0.5, "No hay actividades",
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=12, color="#6b7280",
                    transform=ax.transAxes)
            ax.set_axis_off()
        else:
            figure.patch.set_facecolor("#ffffff")
            ax.set_facecolor("#ffffff")
            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                wedgeprops=dict(width=0.4, edgecolor='#f7f8fa'),
                startangle=90,
                autopct=lambda pct: f"{int(round(pct * sum(values)/100))}h",
                pctdistance=0.75
            )
            for t in autotexts:
                t.set_color("#111827")
                t.set_fontsize(10)
                t.set_fontweight("bold")
            ax.set_aspect('equal')
            ax.set_title("Distribución de horas", fontsize=12)

        figure.tight_layout()
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return canvas