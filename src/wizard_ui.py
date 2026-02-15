from PySide6.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QTextEdit

class IntroPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Bem-vindo ao BDD Automation Wizard")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            "Este assistente guiará você na criação de um cenário de teste.\n\n"
            "1. Defina o nome da funcionalidade.\n"
            "2. Escreva os passos em Gherkin (Given, When, Then).\n"
            "3. O sistema gerará os arquivos Behave + TagUI automaticamente."
        ))
        self.setLayout(layout)

class ScenarioPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Configuração do Cenário")
        self.setSubTitle("Digite os detalhes da sua automação")
        
        layout = QVBoxLayout()
        
        self.feature_name_edit = QLineEdit()
        self.feature_name_edit.setPlaceholderText("Ex: Login no ERP")
        
        self.scenario_text_edit = QTextEdit()
        self.scenario_text_edit.setPlaceholderText(
            "Given que eu abra o site 'https://google.com'\n"
            "When eu digitar 'TagUI' no campo de busca\n"
            "Then eu pressiono enter"
        )
        
        layout.addWidget(QLabel("Nome da Feature (Funcionalidade):"))
        layout.addWidget(self.feature_name_edit)
        layout.addWidget(QLabel("Cenário BDD (Gherkin):"))
        layout.addWidget(self.scenario_text_edit)
        
        self.setLayout(layout)
        
        # O '*' torna o campo obrigatório para habilitar o botão Next/Finish
        self.registerField("feature_name*", self.feature_name_edit)
        self.registerField("scenario_text*", self.scenario_text_edit)

class BDDWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Testes BDD")
        self.setWizardStyle(QWizard.ModernStyle)
        
        # Adicionando as duas páginas originais
        self.addPage(IntroPage())
        self.addPage(ScenarioPage())
        
        self.resize(600, 500)