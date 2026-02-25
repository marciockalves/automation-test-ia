from behave import given, when, then
import tagui as t

@when('entrar na página http://teste.com')
def step_entrar_na_página_httptestecom(context):
    t.echo('Ação pendente: entrar na página http://teste.com')
    t.wait(1)

@when('digitar no campo Email do usuário o email teste@gmail.com')
def step_digitar_no_campo_email_do_usuário_o_email_testegmailcom(context):
    t.echo('Ação pendente: digitar no campo Email do usuário o email teste@gmail.com')
    t.wait(1)

@when('digitar no campo Senha a senha do usuário 123')
def step_digitar_no_campo_senha_a_senha_do_usuário_123(context):
    t.echo('Ação pendente: digitar no campo Senha a senha do usuário 123')
    t.wait(1)

@then('abrirá a página principal')
def step_abrirá_a_página_principal(context):
    t.echo('Ação pendente: abrirá a página principal')
    t.wait(1)
