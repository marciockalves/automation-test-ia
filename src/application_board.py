import os
import re
import sys
import subprocess
from PySide6.QtWidgets import (QMainWindow, QSplitter, QTreeView, 
                             QTextEdit, QVBoxLayout, QPushButton, QWidget, 
                             QFileSystemModel, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt
from src.bbd_form import BDDForm
from src.bdd_edit_form import BDDEditForm
from src.bdd_generator import BDDGenerator


class ApplicationBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Feature Editor Pro")
        self.resize(1200, 800)

        self.current_feature_path = None

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.main_splitter)

        self.setup_file_browser()
        self.setup_center_content()
        self.setup_right_sidebar()

        # --- Conexões ---
        self.form_novo_cenario.cancel_clicked.connect(lambda: self.center_stack.setCurrentIndex(0))
        self.form_novo_cenario.file_saved.connect(self.refresh_and_show_editor)
        
        self.btn_novo.clicked.connect(lambda: self.center_stack.setCurrentIndex(1))
        
        # Conexão do Botão Editar
        self.btn_editar.clicked.connect(self.prepare_edit_mode)
        self.form_edicao.btn_cancelar.clicked.connect(lambda: self.center_stack.setCurrentIndex(0))
        self.form_edicao.btn_atualizar.clicked.connect(self.update_existing_feature)

        self.btn_executar.clicked.connect(self.run_automation_test)

        self.main_splitter.setStretchFactor(0, 2)
        self.main_splitter.setStretchFactor(1, 7)
        self.main_splitter.setStretchFactor(2, 1)

    def setup_file_browser(self):
        self.file_model = QFileSystemModel()
        path = os.path.join(os.getcwd(), "automation")
        if not os.path.exists(path): os.makedirs(path)

        self.file_model.setRootPath(path)
        self.file_model.setNameFilters(["*.feature"])
        self.file_model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.setRootIndex(self.file_model.index(path))
        for i in range(1, 4): self.tree.hideColumn(i)
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.load_file)
        self.main_splitter.addWidget(self.tree)

    def setup_center_content(self):
        self.center_stack = QStackedWidget()

        self.editor = QTextEdit()
        self.editor.setReadOnly(True) # Editor principal como visualizador
        self.editor.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px; padding: 15px;")
        
        self.form_novo_cenario = BDDForm()
        self.form_edicao = BDDEditForm() # Instância do novo formulário

        self.center_stack.addWidget(self.editor)            # Index 0
        self.center_stack.addWidget(self.form_novo_cenario) # Index 1
        self.center_stack.addWidget(self.form_edicao)      # Index 2

        self.main_splitter.addWidget(self.center_stack)

    def setup_right_sidebar(self):
        right_container = QWidget()
        layout = QVBoxLayout(right_container)
        layout.setAlignment(Qt.AlignTop)

        self.btn_novo = QPushButton("Novo Cenário")
        self.btn_editar = QPushButton("Editar Cenário \n Atual")
        self.btn_config = QPushButton("Configurações")
        self.btn_executar = QPushButton("Executar Teste")
        
        for btn in [self.btn_novo, self.btn_editar, self.btn_config, self.btn_executar]:
            btn.setFixedHeight(45)
            btn.setMinimumWidth(120)
            layout.addWidget(btn)

        self.main_splitter.addWidget(right_container)

    def load_file(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            self.current_feature_path = path
            self.center_stack.setCurrentIndex(0)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                self.editor.setPlainText(f"Erro ao ler arquivo: {e}")

    def prepare_edit_mode(self):
        """Preenche o formulário de edição com os dados do arquivo atual"""
        if not self.current_feature_path:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo para editar.")
            return

        content = self.editor.toPlainText()
        
        # Tenta extrair o título da funcionalidade usando regex
        match = re.search(r"Funcionalidade:\s*(.*)", content)
        title = match.group(1) if match else os.path.basename(self.current_feature_path)

        # Remove as linhas de cabeçalho para deixar apenas o cenário no editor de texto
        lines = content.split('\n')
        scenario_lines = [l.strip() for l in lines if "language:" not in l and "Funcionalidade:" not in l and "Cenário:" not in l]
        
        self.form_edicao.txt_title.setText(title)
        self.form_edicao.txt_content.setPlainText("\n".join(scenario_lines).strip())
        
        self.center_stack.setCurrentIndex(2) # Muda para a tela de edição

    def update_existing_feature(self):
        """Salva as alterações e regera os steps via BDDGenerator"""
        if not self.current_feature_path: return

        # O BDDGenerator precisa do diretório pai da pasta 'features'
        # Estrutura: caminho/projeto/features/arquivo.feature -> alvo: caminho/projeto/
        project_dir = os.path.dirname(os.path.dirname(self.current_feature_path))
        
        new_title = self.form_edicao.txt_title.text()
        new_content = self.form_edicao.txt_content.toPlainText()

        try:
            # Reutiliza o BDDGenerator para sobrepor os arquivos
            generator = BDDGenerator(
                feature_name=new_title,
                scenario_text=new_content,
                target_directory=project_dir
            )
            generator.generate_all()

            # Se o título mudou, o nome do arquivo mudou. Removemos o antigo se for diferente.
            # (Opcional: implementar lógica de deleção se desejar que o arquivo antigo suma)

            QMessageBox.information(self, "Sucesso", "Cenário e testes atualizados reativamente!")
            self.refresh_and_show_editor()
        except Exception as e:
            QMessageBox.critical(self, "Erro na Atualização", f"Falha ao atualizar: {e}")

    def run_automation_test(self):
        if not self.current_feature_path:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo .feature antes de executar.")
            return

        # 1. Identifica o diretório e o nome base do arquivo
        folder_path = os.path.dirname(self.current_feature_path)
        filename = os.path.basename(self.current_feature_path).replace(".feature", "")
        
        # 2. Define o caminho do script de teste que o BDDForm gerou
        # O BDDForm salva como 'test_nome.py' na mesma pasta
        python_test_path = os.path.join(folder_path, f"test_{filename}.py")

        if not os.path.exists(python_test_path):
            QMessageBox.warning(self, "Aviso", f"Script de execução não encontrado:\n{python_test_path}")
            return

        # 3. Define o comando para rodar via UV (usando pytest que é melhor para Playwright)
        # Se quiser rodar via Behave no futuro, o comando mudaria, 
        # mas o Codegen gera scripts feitos para Pytest/Python puro.
        command = f'uv run pytest "{python_test_path}"'

        try:
            # Comando para Linux (Fedora)
            if sys.platform != "win32":
                # Tenta abrir o console do sistema para mostrar a execução
                # No Fedora, gnome-terminal é o padrão, mas xterm ou desktop-specific funcionam
                subprocess.Popen([
                    'gnome-terminal', '--', 'sh', '-c', 
                    f'cd "{folder_path}" && {command}; exec $SHELL'
                ])
            else:
                # Comando para Windows
                subprocess.Popen([
                    'start', 'cmd', '/k', 
                    f'cd /d "{folder_path}" && {command}'
                ], shell=True)
                
        except Exception as e:
            # Fallback caso não encontre um terminal específico (roda em background e loga erro)
            try:
                subprocess.Popen(f'cd "{folder_path}" && {command}', shell=True)
                QMessageBox.information(self, "Execução", "Teste iniciado em background.")
            except:
                QMessageBox.critical(self, "Erro de Execução", f"Não foi possível abrir o terminal: {e}")
    def refresh_and_show_editor(self):
        self.file_model.setRootPath("") 
        self.file_model.setRootPath(os.path.join(os.getcwd(), "automation"))
        self.center_stack.setCurrentIndex(0)