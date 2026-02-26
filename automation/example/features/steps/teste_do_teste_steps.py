from behave import given, when, then
import tagui as t

@then('abre somente a página do teste')
def step_abre_somente_a_página_do_teste(context):
    t.echo('Ação pendente: abre somente a página do teste')
    t.wait(1)
