import os
from PySide6.QtWidgets import (QMainWindow, QSplitter, QTreeView, 
                             QTextEdit, QVBoxLayout, QPushButton, QWidget, 
                             QFileSystemModel)
from PySide6.QtCore import Qt

class ApplicationBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Feature Editor Pro")
        self.resize(1100, 700)

        # Widget Principal e Layout de Divisão
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.main_splitter)

        # Componentes
        self.setup_file_browser()
        self.setup_editor()
        self.setup_right_sidebar()

        # Proporções: Esquerda (1), Centro (4), Direita (1)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 4)
        self.main_splitter.setStretchFactor(2, 1)

    def setup_file_browser(self):
        self.file_model = QFileSystemModel()
        # Define o caminho para a pasta 'automation' no diretório atual
        path = os.path.join(os.getcwd(), "automation")
        
        if not os.path.exists(path):
            os.makedirs(path)

        self.file_model.setRootPath(path)
        self.file_model.setNameFilters(["*.feature"])
        self.file_model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(path))
        
        # Oculta detalhes como tamanho e data
        for i in range(1, 4):
            self.tree.hideColumn(i)
        
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.load_file)
        self.main_splitter.addWidget(self.tree)

    def setup_editor(self):
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Selecione um arquivo .feature...")
        self.editor.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px;")
        self.main_splitter.addWidget(self.editor)

    def setup_right_sidebar(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)

        self.btn_novo = QPushButton("Novo Cenário")
        self.btn_editar = QPushButton("Editar Cenário Atual")
        self.btn_config = QPushButton("Configurações")

        for btn in [self.btn_novo, self.btn_editar, self.btn_config]:
            btn.setFixedHeight(40)
            layout.addWidget(btn)

        self.main_splitter.addWidget(container)

    def load_file(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                self.editor.setPlainText(f"Erro ao ler arquivo: {e}")