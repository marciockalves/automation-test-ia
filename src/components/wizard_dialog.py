import flet as ft

class BDDWizard(ft.AlertDialog):
    def __init__(self, on_save_callback):
        super().__init__()
        self.on_save_callback = on_save_callback
        self.title = ft.Text("Novo Cenário BDD")
        self.modal = True
        # Inputs
        self.name_input = ft.TextField(label="Nome da Feature")
        self.steps_input = ft.TextField(label="Cenário", multiline=True, min_lines=5)
        
        # Páginas (Containers)
        self.page_1 = ft.Column([
            ft.Text("Bem-vindo! Este assistente gerará seu código de automação."),
            ft.Image(src="https://flet.dev/img/pages/home/flet-home.png", width=100) # Exemplo
        ])
        
        self.page_2 = ft.Column([self.name_input, self.steps_input], visible=False)
        
        self.content = ft.Container(content=ft.Column([self.page_1, self.page_2], tight=True), width=400)
        
        # Botões
        self.btn_next = ft.ElevatedButton("Próximo", on_click=self.next_step)
        self.btn_previous = ft.ElevatedButton("Cancelar", on_click=self.previous_step)
        
        self.actions = [self.btn_previous, self.btn_next]

    def previous_step(self, e):
        if self.page_1.visible:
            self.open = False
            self.update()
            
        if self.page_2.visible:
            self.page_1.visible = True
            self.page_2.visible = False
            self.btn_previous.content = "Cancelar"
            self.btn_next.content = "Próximo"
            self.update()   
        
    def next_step(self, e):
        if self.page_1.visible:
            self.page_1.visible = False
            self.page_2.visible = True
            self.btn_previous.content = "Anterior"
            self.btn_next.content = "Finalizar"
            self.update()
        else:
            # Ao finalizar, chama o callback passando os dados
            self.on_save_callback(self.name_input.value, self.steps_input.value)
            self.open = False
            self.update()