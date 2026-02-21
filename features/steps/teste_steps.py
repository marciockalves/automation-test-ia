from behave import given, when, then
import tagui as t

# Inicialização automática do TagUI
def before_all(context):
    t.init()
