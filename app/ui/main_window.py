from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont

from app.ui.dashboard_view import DashboardView
from app.ui.student_view import StudentView
from app.ui.activity_view import ActividadView
from app.ui.registro_view import RegistroView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ==========================
        # Configuración principal
        # ==========================
        self.setWindowTitle("Sistema Control de Horas")
        self.resize(1350, 850)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        # ==========================
        # SIDEBAR
        # ==========================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QFrame { background-color: #f9f9f9; border-right: 1px solid #e0e0e0; }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Título del software
        logo_label = QLabel("Control de Horas")
        logo_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedHeight(60)
        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addSpacing(10)

        # BOTONES DEL SIDEBAR
        self.btn_dashboard = QPushButton("  Dashboard")
        self.btn_estudiantes = QPushButton("  Estudiantes")
        self.btn_actividades = QPushButton("  Actividades")
        self.btn_registro = QPushButton("  Registro Diario")

        self.sidebar_buttons = [
            self.btn_dashboard,
            self.btn_estudiantes,
            self.btn_actividades,
            self.btn_registro
        ]

        for btn in self.sidebar_buttons:
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        # INDICADOR LATERAL
        self.indicator = QFrame(self.sidebar)
        self.indicator.setGeometry(0, 70, 5, 50)
        self.indicator.setStyleSheet("background-color: #4f46e5; border-radius: 2px;")

        # ==========================
        # PANEL PRINCIPAL
        # ==========================
        self.content = QFrame()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # HEADER con título y subtítulo
        self.header_title = QLabel("Sistema Control de Horas")
        self.header_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.header_subtitle = QLabel("Dashboard")
        self.header_subtitle.setFont(QFont("Segoe UI", 12))
        self.header_subtitle.setStyleSheet("color: #6b7280;")
        content_layout.addWidget(self.header_title)
        content_layout.addWidget(self.header_subtitle)

        # STACK DE VISTAS
        self.stack = QStackedWidget()
        self.dashboard_view = DashboardView()
        self.estudiante_view = StudentView()
        self.actividad_view = ActividadView()
        self.registro_view = RegistroView()
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.estudiante_view)
        self.stack.addWidget(self.actividad_view)
        self.stack.addWidget(self.registro_view)
        content_layout.addWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

        # ==========================
        # CONEXIONES BOTONES
        # ==========================
        self.btn_dashboard.clicked.connect(
            lambda: self.set_active_panel(self.dashboard_view, self.btn_dashboard, "Dashboard")
        )
        self.btn_estudiantes.clicked.connect(
            lambda: self.set_active_panel(self.estudiante_view, self.btn_estudiantes, "Estudiantes")
        )
        self.btn_actividades.clicked.connect(
            lambda: self.set_active_panel(self.actividad_view, self.btn_actividades, "Actividades")
        )
        self.btn_registro.clicked.connect(
            lambda: self.set_active_panel(self.registro_view, self.btn_registro, "Registro Diario")
        )

        # VISTA INICIAL
        self.set_active_panel(self.dashboard_view, self.btn_dashboard, "Dashboard", initial=True)

    def set_active_panel(self, widget, button, subtitle, initial=False):
        """Cambia la vista, mueve indicador y actualiza estilos del sidebar y header."""
        self.stack.setCurrentWidget(widget)
        self.header_subtitle.setText(subtitle)

        for btn in self.sidebar_buttons:
            if btn == button:
                btn.setStyleSheet(self.active_button_style())
            else:
                btn.setStyleSheet(self.inactive_button_style())

        if not initial:
            anim = QPropertyAnimation(self.indicator, b"geometry")
            anim.setDuration(250)
            anim.setStartValue(self.indicator.geometry())
            anim.setEndValue(QRect(0, button.y(), 5, button.height()))
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.start()
            self.anim = anim  # evitar garbage collection

    def active_button_style(self):
        return """
            QPushButton {
                background-color: #eaeaff;
                color: #4f46e5;
                font-weight: bold;
                padding-left: 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #dbeafe;
            }
        """

    def inactive_button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #6b6f72;
                font-weight: normal;
                padding-left: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #2f3437;
            }
        """