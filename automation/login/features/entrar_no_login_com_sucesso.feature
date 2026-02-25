# language: pt
Funcionalidade: Entrar no login com sucesso

  Cenário: Entrar no login com sucesso Automatizado
    Quando entrar na página http://teste.com
    E digitar no campo Email do usuário o email teste@gmail.com
    E digitar no campo Senha a senha do usuário 123
    Então abrirá a página principal
