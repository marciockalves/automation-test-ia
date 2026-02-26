from PySide6.QtWidgets import (QMainWindow, QSplitter, QTreeView, 
                             QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
                             QFileSystemModel, QStackedWidget, QMessageBox, QLabel, QLineEdit)
from PySide6.QtCore import Qt, Signal
from src.bbd_form import BDDForm
from src.bdd_generator import BDDGenerator # Import do seu gerador

# --- Nova Classe para o Formulário de Edição ---
class BDDEditForm(QWidget):
    updated = Signal()
    cancelled = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.label_info = QLabel("<b>Editando Cenário</b>")
        layout.addWidget(self.label_info)

        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("Título da Feature")
        layout.addWidget(QLabel("Título da Feature:"))
        layout.addWidget(self.txt_title)

        self.txt_content = QTextEdit()
        self.txt_content.setPlaceholderText("Conteúdo BDD...")
        layout.addWidget(QLabel("Conteúdo do Cenário:"))
        layout.addWidget(self.txt_content)

        btns = QHBoxLayout()
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_cancelar = QPushButton("Cancelar")
        
        self.btn_atualizar.setStyleSheet("background-color: #007acc; color: white;")
        
        btns.addStretch()
        btns.addWidget(self.btn_cancelar)
        btns.addWidget(self.btn_atualizar)
        layout.addLayout(btns)

