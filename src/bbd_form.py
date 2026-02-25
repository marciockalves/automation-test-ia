import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal
from src.bdd_generator import BDDGenerator # Supondo que sua classe esteja neste arquivo

class BDDForm(QWidget):
    # Sinal para avisar a janela principal que o arquivo foi salvo e a árvore deve atualizar
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
        self.txt_path.setPlaceholderText("Selecione ou crie uma subpasta em 'automation'...")
        
        btn_browse = QPushButton("Escolher Pasta")
        btn_browse.clicked.connect(self.choose_folder)
        
        folder_layout.addWidget(self.txt_path)
        folder_layout.addWidget(btn_browse)
        layout.addLayout(folder_layout)

        layout.addWidget(QLabel("Nova Subpasta (Opcional):"))
        self.txt_new_subfolder = QLineEdit()
        self.txt_new_subfolder.setPlaceholderText("Ex: login_tests (deixe vazio para usar a pasta selecionada)")
        layout.addWidget(self.txt_new_subfolder)

        # --- Nome do Arquivo ---
        layout.addWidget(QLabel("<b>Nome do Arquivo (.feature):</b>"))
        self.txt_filename = QLineEdit()
        self.txt_filename.setPlaceholderText("ex: login_usuario")
        layout.addWidget(self.txt_filename)

        # --- Título do Cenário ---
        layout.addWidget(QLabel("<b>Título do Cenário:</b>"))
        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("Ex: Validar login com sucesso")
        layout.addWidget(self.txt_title)

        # --- Conteúdo BDD ---
        layout.addWidget(QLabel("<b>Cenário (Passos BDD):</b>"))
        self.txt_content = QTextEdit()
        self.txt_content.setPlaceholderText("Dado que estou na página...\nQuando digito...\nEntão vejo...")
        layout.addWidget(self.txt_content)

        # --- Botões de Ação ---
        actions_layout = QHBoxLayout()
        btn_save = QPushButton("Salvar e Gerar")
        btn_save.setStyleSheet("background-color: #0e639c; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.save_feature)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.clear_and_cancel)

        actions_layout.addStretch()
        actions_layout.addWidget(btn_cancel)
        actions_layout.addWidget(btn_save)
        layout.addLayout(actions_layout)

    def choose_folder(self):
        base_path = os.path.join(os.getcwd(), "automation")
        if not os.path.exists(base_path): os.makedirs(base_path)
        
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", base_path)
        if folder:
            self.txt_path.setText(folder)

    def clear_and_cancel(self):
        self.txt_path.clear()
        self.txt_new_subfolder.clear()
        self.txt_filename.clear()
        self.txt_title.clear()
        self.txt_content.clear()
        self.cancel_clicked.emit()

    def save_feature(self):
        # 1. Validação básica de campos obrigatórios
        filename = self.txt_filename.text().strip()
        scenario_content = self.txt_content.toPlainText().strip()
        title = self.txt_title.text().strip()

        if not filename or not scenario_content:
            QMessageBox.warning(self, "Campos Obrigatórios", "Por favor, preencha o Nome do Arquivo e o Cenário.")
            return

        # 2. Determinar o diretório base
        # Se o usuário não escolheu pasta, usamos a 'automation' padrão na raiz
        base_dir = self.txt_path.text() if self.txt_path.text() else os.path.join(os.getcwd(), "automation")
        
        # 3. Concatenar com a nova subpasta, se houver
        new_sub = self.txt_new_subfolder.text().strip()
        target_dir = os.path.join(base_dir, new_sub) if new_sub else base_dir

        try:
            # Certifica-se de que a pasta de destino existe
            os.makedirs(target_dir, exist_ok=True)

            # 4. Instanciar o BDDGenerator com o NOVO argumento target_directory
            generator = BDDGenerator(
                feature_name=title if title else filename,
                scenario_text=scenario_content,
                target_directory=target_dir  # Este é o argumento que estava faltando!
            )
            
            # 5. Gerar os arquivos
            feat_path, step_path = generator.generate_all()
            
            QMessageBox.information(
                self, 
                "Sucesso", 
                f"Arquivos gerados com sucesso!\n\nFeature: {os.path.basename(feat_path)}\nSteps: {os.path.basename(step_path)}"
            )
            
            # Notifica a tela principal para atualizar a árvore e limpa o form
            self.file_saved.emit()
            self.clear_and_cancel()

        except Exception as e:
            QMessageBox.critical(self, "Erro ao Gerar", f"Ocorreu um erro: {str(e)}")