import os
import subprocess
import tempfile
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal

class BDDForm(QWidget):
    file_saved = Signal()
    cancel_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # --- Seção Pasta ---
        layout.addWidget(QLabel("<b>Localização do Teste (Pasta):</b>"))
        folder_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setReadOnly(True)
        self.txt_path.setPlaceholderText("Selecione a pasta destino...")
        
        btn_browse = QPushButton("Escolher Pasta")
        # O ERRO ESTAVA AQUI: O método choose_folder precisa existir abaixo
        btn_browse.clicked.connect(self.choose_folder)
        
        folder_layout.addWidget(self.txt_path)
        folder_layout.addWidget(btn_browse)
        layout.addLayout(folder_layout)

        # --- Nome e Título ---
        layout.addWidget(QLabel("<b>Nome do Arquivo (.feature):</b>"))
        self.txt_filename = QLineEdit()
        layout.addWidget(self.txt_filename)

        layout.addWidget(QLabel("<b>Título do Cenário:</b>"))
        self.txt_title = QLineEdit()
        layout.addWidget(self.txt_title)

        # --- Conteúdo BDD ---
        layout.addWidget(QLabel("<b>Passos do Cenário (Documentação):</b>"))
        self.txt_content = QTextEdit()
        layout.addWidget(self.txt_content)

        # --- Botão de Gravação Playwright ---
        layout.addWidget(QLabel("<b>Automação Playwright:</b>"))
        self.btn_record = QPushButton("🔴 Gravar Teste (Playwright Codegen)")
        self.btn_record.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; height: 40px;")
        self.btn_record.clicked.connect(self.record_with_playwright)
        layout.addWidget(self.btn_record)

        self.generated_python_code = ""

        # --- Ações Finais ---
        actions_layout = QHBoxLayout()
        btn_save = QPushButton("Salvar Feature e Código")
        btn_save.setStyleSheet("background-color: #0e639c; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.save_all)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.clear_and_cancel)

        actions_layout.addStretch()
        actions_layout.addWidget(btn_cancel)
        actions_layout.addWidget(btn_save)
        layout.addLayout(actions_layout)

    # --- MÉTODOS QUE ESTAVAM FALTANDO ---

    def choose_folder(self):
        """Abre o diálogo para selecionar a pasta"""
        base_path = os.path.join(os.getcwd(), "automation")
        if not os.path.exists(base_path): 
            os.makedirs(base_path, exist_ok=True)
        
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", base_path)
        if folder:
            self.txt_path.setText(folder)

    def clear_and_cancel(self):
        """Limpa o formulário e emite sinal de cancelamento"""
        self.txt_path.clear()
        self.txt_filename.clear()
        self.txt_title.clear()
        self.txt_content.clear()
        self.generated_python_code = ""
        self.btn_record.setText("🔴 Gravar Teste (Playwright Codegen)")
        self.btn_record.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; height: 40px;")
        self.cancel_clicked.emit()

    def record_with_playwright(self):
        """Executa o codegen e captura o script"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                temp_path = tmp.name

            QMessageBox.information(self, "Gravação", "O Navegador abrirá. Execute as ações e FECHE-O para salvar.")
            
            # Chama o playwright instalado via UV
            subprocess.run(["uv", "run", "playwright", "codegen", "-o", temp_path], check=True)

            with open(temp_path, 'r', encoding='utf-8') as f:
                self.generated_python_code = f.read()

            if self.generated_python_code:
                self.btn_record.setText("✅ Teste Gravado!")
                self.btn_record.setStyleSheet("background-color: #388E3C; color: white; font-weight: bold; height: 40px;")
            
            os.remove(temp_path)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao iniciar gravador: {e}")

    def save_all(self):
        """Persiste os arquivos no disco"""
        filename = self.txt_filename.text().strip()
        path = self.txt_path.text()
        
        if not filename or not path or not self.generated_python_code:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos e grave o teste antes de salvar.")
            return

        try:
            # Salva .feature
            with open(os.path.join(path, f"{filename}.feature"), 'w') as f:
                f.write(f"Feature: {self.txt_title.text()}\n\n  Scenario: {self.txt_title.text()}\n")
                f.write(f"    {self.txt_content.toPlainText()}")

            # Salva o script python
            with open(os.path.join(path, f"test_{filename}.py"), 'w') as f:
                f.write(self.generated_python_code)

            QMessageBox.information(self, "Sucesso", "Arquivos gerados!")
            self.file_saved.emit()
            self.clear_and_cancel()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")