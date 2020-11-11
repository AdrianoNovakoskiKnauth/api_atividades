from models import Pessoas


def insere_pessoas():
    pessoa = Pessoas(nome='Adriel', idade=25)
    pessoa.save()
    print(pessoa)

def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)
    # pessoa = Pessoas.query.filter_by(nome='Samuel').first()
    # print(pessoa)

def altera_pessoas():
    pessoa = Pessoas.query.filter_by(nome='Samuel').first()
    pessoa.idade = 10
    pessoa.save

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Adriano').first()
    pessoa.delete()

if __name__ == '__main__':
    #insere_pessoas()
    altera_pessoas()
    # exclui_pessoa()
    consulta_pessoas()