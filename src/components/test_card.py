import flet as ft

class TestCard(ft.Container):
    def __init__(self, title, filename, on_details):
        super().__init__()
        self.content = ft.Column([
            ft.Text(title, weight="bold", size=16, max_lines=2),
            ft.Text("Cenário BDD", size=12, color=ft.Colors.GREY_700),
            
          
            ft.Container(expand=True), 
            
            ft.ElevatedButton(
                "Detalhes", 
                icon=ft.Icons.SEARCH, 
                on_click=lambda _: on_details(filename)
            )
        ])
        self.bgcolor = ft.Colors.WHITE
        self.padding = 20
        self.border_radius = 12
        self.shadow = ft.BoxShadow(
            blur_radius=10, 
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
        )
        self.width = 200
        self.height = 180
        