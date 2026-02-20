import flet as ft

class AddFeatureCard(ft.Container):
    """Card fixo para a primeira posição do Dashboard para adicionar novos testes."""
    def __init__(self, on_click):
        super().__init__()
        # Estilo do Card (Claro e Moderno)
        self.width = 200
        self.height = 180
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.border.all(2, ft.Colors.BLUE_100)
        self.border_radius = 12
        self.padding = 20
        self.on_click = on_click
        self.ink = True  # Efeito visual de ondulação ao clicar (Material Design)
        self.cursor = ft.MouseCursor.CLICK
        
        # Borda tracejada para indicar "Adicionar"
        self.border = ft.Border(
            ft.BorderSide(2, ft.Colors.BLUE_200), # Topo
            ft.BorderSide(2, ft.Colors.BLUE_200), # Direita
            ft.BorderSide(2, ft.Colors.BLUE_200), # Baixo
            ft.BorderSide(2, ft.Colors.BLUE_200)  # Esquerda
        )
        # Nota: O Flet atualmente aplica bordas sólidas via ft.border.all. 
        # Para efeito tracejado puro, usamos uma estilização visual interna:
        
        self.content = ft.Column(
            controls=[
              
                ft.Icon(
                    name=ft.Icons.ADD_ROUNDED, 
                    color=ft.Colors.BLUE_ACCENT, 
                    size=50
                ),
                ft.Text(
                    "Criar Nova\nFeature", 
                    color=ft.Colors.BLUE_ACCENT, 
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def hover_animation(self, e):
        # Opcional: Efeito de destaque quando o mouse passa por cima
        self.bgcolor = ft.Colors.BLUE_50 if e.data == "true" else ft.Colors.WHITE
        self.update()