from behave import given, when, then
import tagui as t

# Inicialização automática do TagUI
def before_all(context):
    t.init()

@when('is login')
def step_is_login(context):
    # TODO: Implementar lógica para: is login
    t.echo('Executando: is login')
    pass

@then('is complete')
def step_is_complete(context):
    # TODO: Implementar lógica para: is complete
    t.echo('Executando: is complete')
    pass
