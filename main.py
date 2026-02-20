
import flet as ft

from src.dashboard import BDDDashboard



def main(page: ft.Page):
    BDDDashboard(page)

if __name__ == "__main__":
    # Mudança de ft.app para ft.run (para silenciar o aviso de Deprecation)
    ft.run(main)