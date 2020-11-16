from models import Pessoas, Atividades, Usuarios


def insere_pessoas(nome, idade):
    pessoa = Pessoas(nome=nome, idade=idade)
    pessoa.save()
    print(pessoa)

def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas.idade)

def altera_pessoas(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    pessoa.idade = 28
    pessoa.save

def exclui_pessoa(nome):
    pessoa = Pessoas.query.filter_by(nome=nome).first()
    print(pessoa)
    pessoa.delete()

def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha, status=1)
    usuario.save()

def consulta_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

def deleta_usuario(login):
    usuario = Usuarios.query.filter_by(login=login).first()
    usuario.delete()

def consulta_atividades():
    atividades = Atividades.query.all()
    response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome}for i in atividades]
    print(response)

def nova_ativ():
    atividade = Atividades(nome="Limpar carro", estado='Pendente', pessoa='Adriano')
    print('dentro de nova atividade')
    atividade.save
    response = [{'id':atividade.id, 'nome':atividade.nome,'pessoa':atividade.pessoa}]
    print(response)

def deletar_atividade():
    atividade = Atividades.query.all()
    # print(atividade.id)
    atividade.id.delete()

if __name__ == '__main__':
    # consulta_atividades()
    # deletar_atividade()
    # nova_ativ()

    #insere_usuario('Adriano', '123')
    #insere_usuario('Admin', '123')
    #insere_usuario('Adriel', '789')
    #deleta_usuario('Larissa')
    consulta_usuarios()

    #insere_pessoas('Adriano', 28)
    #altera_pessoas('Adriano')
    # exclui_pessoa('Adrian')
    # consulta_pessoas()
