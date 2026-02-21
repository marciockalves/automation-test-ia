import flet as ft
import os

from src.bdd_generator import BDDGenerator
from src.components.test_card import TestCard
from src.components.add_card import AddFeatureCard
from src.components.wizard_dialog import BDDWizard




class BDDDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "QA Dashboard"
        # self.page.bgcolor = "#F0F2F5" # Hexadecimal continua string
        self.page.bgcolor =ft.Colors.BLUE_GREY_200
        self.grid = ft.GridView(expand=True, runs_count=5, max_extent=250, spacing=20)
        title =  ft.Text("Dashboard de Automação", align=ft.Alignment.CENTER, weight="bold", color= ft.Colors.BLACK_87)

        self.page.add(
           title,
            self.grid
        )

             
        self.refresh()

    def refresh(self):
        self.grid.controls.clear()
        self.grid.controls.append(AddFeatureCard(on_click=self.open_wizard))
        
        if os.path.exists("features"):
            files = sorted([f for f in os.listdir("features") if f.endswith(".feature")])
            for file in files:
                if file.endswith(".feature"):
                     self.grid.controls.append(TestCard(file, file, self.show_details))
                   
        self.page.update()

    def open_wizard(self, e):
        def handle_save(name, steps):
            # Lógica de geração
            gen = BDDGenerator(name, steps)
            gen.create_structure()
            gen.generate_all()
            
            # FECHAMENTO SEGURO
            wizard.open = False
            self.page.update()
            self.refresh()

        # Instancia o Wizard
        wizard = BDDWizard(on_save_callback=handle_save)
        
        # O SEGREDO: Adicionar ao overlay antes de abrir
        self.page.overlay.append(wizard)
        wizard.open = True
        self.page.update()

    def show_details(self, filename):
        pass
