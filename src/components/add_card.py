import flet as ft

class AddFeatureCard(ft.Container):
    def __init__(self, on_click):
        super().__init__()
        self.width = 200
        self.height = 180
        self.bgcolor = ft.Colors.WHITE  
        self.border = ft.border.all(2, ft.Colors.BLUE_100)
        self.border_radius = 12
        self.padding = 20
        self.on_click = on_click
        self.ink = True 
        self.cursor = ft.MouseCursor.CLICK
        
        
        self.content = ft.Column(
            controls=[
                ft.Icon(ft.Icons.ADD_ROUNDED, color=ft.Colors.BLUE_ACCENT, size=50),
                ft.Text("Criar Nova\nFeature", color=ft.Colors.BLUE_ACCENT, 
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
    