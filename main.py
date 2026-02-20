import flet as ft
import os
import re
from src.bdd_generator import BDDGenerator
from src.components.test_card import TestCard
from src.components.add_card import AddFeatureCard # (Implementação similar ao card acima)
from src.components.wizard_dialog import BDDWizard

class BDDDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#F0F2F5"
        self.grid = ft.GridView(expand=True, runs_count=5, max_extent=250, spacing=20)
        
        self.page.add(
            ft.Text("Dashboard de Automação", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight="bold"),
            self.grid
        )
        self.refresh()

    def refresh(self, e=None):
        self.grid.controls.clear()
        
        # Adiciona o card de Novo (Componente)
        self.grid.controls.append(AddFeatureCard(on_click=self.open_wizard))
        
        # Adiciona os cards de Teste (Componentes)
        if os.path.exists("features"):
            for file in os.listdir("features"):
                if file.endswith(".feature"):
                    # Aqui você poderia extrair o título real do arquivo
                    self.grid.controls.append(TestCard(file, file, self.show_details))
        self.page.update()

    def open_wizard(self, e):
        # Instancia o componente Wizard e passa a lógica de salvamento
        def handle_save(name, steps):
            gen = BDDGenerator(name, steps)
            gen.create_structure()
            gen.generate_feature_file()
            gen.generate_steps_file()
            self.refresh()

        wizard = BDDWizard(on_save_callback=handle_save)
        self.page.dialog = wizard
        wizard.open = True
        self.page.update()

    def show_details(self, filename):
        # Lógica para mostrar detalhes...
        pass

if __name__ == "__main__":
    
    def main(page: ft.Page):
        BDDDashboard(page)

    ft.app(target=main)