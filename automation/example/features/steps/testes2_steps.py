from behave import given, when, then
import tagui as t

# Inicialização automática do TagUI
def before_all(context):
    t.init()

@then('teste')
def step_teste(context):
    # TODO: Implementar lógica para: teste
    t.echo('Executando: teste')
    pass
