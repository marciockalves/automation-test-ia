from behave import given, when, then
import tagui as t

@then('abre a página do teste')
def step_abre_a_página_do_teste(context):
    t.echo('Ação pendente: abre a página do teste')
    t.wait(1)
