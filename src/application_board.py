import os
from PySide6.QtWidgets import (QMainWindow, QSplitter, QTreeView, 
                             QTextEdit, QVBoxLayout, QPushButton, QWidget, 
                             QFileSystemModel, QStackedWidget)
from PySide6.QtCore import Qt
from src.bbd_form import BDDForm


class ApplicationBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Feature Editor Pro")
        self.resize(1200, 800)

        # Widget Principal de Divisão
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.main_splitter)

        # 1. LADO ESQUERDO: Navegador de Arquivos
        self.setup_file_browser()

        # 2. CENTRO: Stack (Editor ou Formulário)
        self.setup_center_content()

        # 3. LADO DIREITO: Barra de Ações
        self.setup_right_sidebar()

        # Conectar Eventos do Formulário
        self.form_novo_cenario.cancel_clicked.connect(lambda: self.center_stack.setCurrentIndex(0))
        self.form_novo_cenario.file_saved.connect(self.refresh_and_show_editor)
        
        # Conectar Botão de Novo Cenário da Barra Lateral
        self.btn_novo.clicked.connect(lambda: self.center_stack.setCurrentIndex(1))

        # Ajuste de proporções (20% esquerda, 65% centro, 15% direita)
        self.main_splitter.setStretchFactor(0, 2)
        self.main_splitter.setStretchFactor(1, 7)
        self.main_splitter.setStretchFactor(2, 1)

    def setup_file_browser(self):
        self.file_model = QFileSystemModel()
        path = os.path.join(os.getcwd(), "automation")
        
        if not os.path.exists(path):
            os.makedirs(path)

        self.file_model.setRootPath(path)
        self.file_model.setNameFilters(["*.feature"])
        self.file_model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(path))
        
        for i in range(1, 4):
            self.tree.hideColumn(i)
        
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.load_file)
        self.main_splitter.addWidget(self.tree)

    def setup_center_content(self):
        # O QStackedWidget permite alternar entre o Editor e o Formulário
        self.center_stack = QStackedWidget()

        # Página 0: Editor de Texto original
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Selecione um arquivo .feature para visualizar ou clique em 'Novo Cenário'...")
        self.editor.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px; padding: 15px;")
        
        # Página 1: Formulário Novo Cenário
        self.form_novo_cenario = BDDForm()

        self.center_stack.addWidget(self.editor)            # Index 0
        self.center_stack.addWidget(self.form_novo_cenario) # Index 1

        self.main_splitter.addWidget(self.center_stack)

    def setup_right_sidebar(self):
        right_container = QWidget()
        layout = QVBoxLayout(right_container)
        layout.setAlignment(Qt.AlignTop)

        self.btn_novo = QPushButton("Novo Cenário")
        self.btn_editar = QPushButton("Editar Cenário Atual")
        self.btn_config = QPushButton("Configurações")

        for btn in [self.btn_novo, self.btn_editar, self.btn_config]:
            btn.setFixedHeight(45)
            layout.addWidget(btn)

        self.main_splitter.addWidget(right_container)

    def load_file(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            # Sempre que clicar num arquivo, volta para a visão do editor
            self.center_stack.setCurrentIndex(0)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                self.editor.setPlainText(f"Erro ao ler arquivo: {e}")

    def refresh_and_show_editor(self):
        """Atualiza a árvore e volta para o editor após salvar"""
        self.file_model.setRootPath("") 
        self.file_model.setRootPath(os.path.join(os.getcwd(), "automation"))
        self.center_stack.setCurrentIndex(0)