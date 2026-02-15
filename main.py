import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.wizard_ui import BDDWizard
from src.bdd_generator import BDDGenerator

class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wizard = BDDWizard()
        
        # Conecta o sinal de finalização do Wizard
        self.wizard.accepted.connect(self.process_results)

    def process_results(self):
        # Captura os dados dos campos registrados no Wizard
        f_name = self.wizard.field("feature_name")
        s_text = self.wizard.field("scenario_text")
        
        # Instancia e executa o gerador
        generator = BDDGenerator(f_name, s_text)
        try:
            f_path, s_path = generator.generate()
            QMessageBox.information(
                self.wizard, 
                "Sucesso!", 
                f"Arquivos gerados com sucesso!\n\nFeature: {f_path}\nSteps: {s_path}"
            )
        except Exception as e:
            QMessageBox.critical(self.wizard, "Erro", f"Falha ao gerar arquivos: {e}")

    def run(self):
        self.wizard.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = MainController()
    controller.run()