from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()

#Verifica se sessão pertence ao cadastro a ser acessado
def login_igual_nome(nome):
    if nome == str(auth.current_user()):
        return True
    elif str(auth.current_user()) == 'Admin':   # Usuário Admin e senha 123 tem acesso a todos os dados
        return True
    else:
        response = {
            'status': 'error',
            'mensagem': 'Acesso não autorizado'
        }
        return response

#  CADASTRO - acessos de usuários
class Cadastro_pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            try:
                response = {
                    'nome':pessoa.nome,
                    'idade':pessoa.idade,
                    'id':pessoa.id
                }
            except AttributeError:
                response = {
                    'status':'error',
                    'mensagem':'Nome não encontrado'
                }
            return response
        else:
            return response

    @auth.login_required
    def put(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            print(pessoa)
            try:
                dados = request.json
                # if 'nome' in dados:
                #     pessoa.nome = dados['nome']
                if 'idade' in dados:
                    pessoa.idade = dados['idade']
                pessoa.save()
                response = {
                    'id':pessoa.id,
                    'nome':pessoa.nome,
                    'idade':pessoa.idade
                }
                return response
            except AttributeError:
                response = {
                    'status': 'error',
                    'mensagem': 'Nome não encontrado'
                }
                return response
        else:
            return response

    @auth.login_required
    def delete(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            try:
                atividade = Atividades.query.all()
                for i in atividade:
                    if pessoa == i.pessoa:
                        i.delete()
                mensagem = '{} excluido com sucesso'.format(pessoa.nome)
                pessoa.delete()
                return {'status':'sucesso','mensagem':mensagem}
            except AttributeError:
                return {'status': 'error', 'mensagem': 'Nome não encontrado'}
        else:
            return response

# ATIVIDADE - acesso de usuários
class Pessoa_get_post_atividades(Resource):
    @auth.login_required
    def get(self, nome):
        response = login_igual_nome(nome)
        print('1º passo')
        if response == True:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            atividades = Atividades.query.all()
            response = [{'pessoa':pessoa.nome}]
            for i in atividades:
                if pessoa == i.pessoa:
                    descr = {'id':i.id,'nome': i.nome, 'status':i.status}
                    response.append(descr)
            return response
        else:
            return response

    # Desenvolver POST
    @auth.login_required
    def post(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            dados = request.json
            if 'nome' in dados:
                pessoa = Pessoas.query.filter_by(nome=nome).first()
                atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status='Pendente')
                atividade.save()
                response = {
                    'id': atividade.id,
                    'pessoa': atividade.pessoa.nome,
                    'nome': atividade.nome,
                    'status': atividade.status
                }
                return response
            else:
                response = {
                    'nome': '????',
                    'status': 'informe a atividade'
                }
                return response
        else:
            return response


class Pessoa_put_delete_atividades(Resource):
    @auth.login_required
    def put(self,nome, id):
        response = login_igual_nome(nome)
        if response == True:
            try:
                atividade = Atividades.query.filter_by(id=id).first()
                if atividade.pessoa.nome == nome:
                    mensagem = {'status': 'Conclúido',
                                'mensagem': 'Status alterado com sucesso'.format(atividade.nome)}
                else:
                    mensagem = {'status': 'error', 'mensagem': 'Atividade {} e de outro usuário'.format(atividade.id)}
                return mensagem
            except AttributeError:
                return [{'status': 'error', 'mensagem': 'Erro ao ID da atividade'}]
        else:
            return response

    @auth.login_required
    def delete(self, nome, id):
        response = login_igual_nome(nome)
        if response == True:
            try:
                atividade = Atividades.query.filter_by(id=id).first()
                if atividade.pessoa.nome == nome:
                    mensagem = {'status': 'sucesso',
                                'mensagem': 'Atividade {} excluida com sucesso'.format(atividade.nome)}
                    atividade.delete()
                else:
                    mensagem = {'status': 'error', 'mensagem': 'Atividade {} e de outro usuário'.format(atividade.id)}
                return mensagem
            except AttributeError:
                return [{'status': 'error', 'mensagem': 'Erro ao ID da atividade'}]
        else:
            return response

class Pessoa_altera_atividades(Resource):
    pass

# CADASTRO - ATIVIDADES - acessos de administador
class Lista_cadastros_pessoa(Resource):
    @auth.login_required
    def get(self):
        response = login_igual_nome('Admin')
        if response == True:
            pessoas = Pessoas.query.all()
            response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
            return response
        else:
            return response

    @auth.login_required
    def post(self):
        response = login_igual_nome('Admin')
        if response == True:
            dados = request.json
            if "nome" in dados and "idade" in dados:
                pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
                pessoa.save()
                response = {
                    'id': pessoa.id,
                    'nome': pessoa.nome,
                    'idade': pessoa.idade
                }
                return response
            else:
                response = {
                    'status': 'error',
                    'mensagem': [{
                        'nome': '????',
                        'idade': '????'}]
                }
                return response
        else:
            return response

class Lista_cadastro_atividades(Resource):
    @auth.login_required
    def get(self):
        response = login_igual_nome('Admin')
        if response == True:
            atividade = Atividades.query.all()
            response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome, 'status':i.status}for i in atividade]
            return response
        else:
            return response

    @auth.login_required
    def post(self):
        response = login_igual_nome('Admin')
        if response == True:
            dados = request.json
            if 'nome' in dados and 'pessoa' in dados:
                pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
                atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status='pendente')
                atividade.save()
                response = {
                    'id': atividade.id,
                    'pessoa':atividade.pessoa.nome,
                    'descricao':atividade.nome,
                    'status':atividade.status
                }
                return response
            else:
                response = {
                    'pessoa': '???????????',
                    'nome': '???????????'
                }
                return response
        else:
            return response

class Admin_excluir_atividade(Resource):
    def delete(self, id):
        response = login_igual_nome('Admin')
        if response == True:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            return [{'status': 'ok', 'mensagem': 'Exclúido'}]
        else:
            return response

# CADASTRO - acessos de usuários
api.add_resource(Cadastro_pessoa, '/<string:nome>/cadastro/')

# ATIVIDADE - acesso de usuários
api.add_resource(Pessoa_get_post_atividades, '/<string:nome>/atividade/')
api.add_resource(Pessoa_put_delete_atividades,'/<string:nome>/atividade/<int:id>/')
api.add_resource(Pessoa_altera_atividades,'/<string:nome>/atividade/<int:id>/')


# CADASTRO - ATIVIDADES - acessos de administador
api.add_resource(Lista_cadastros_pessoa, '/Admin/cadastro/')
api.add_resource(Lista_cadastro_atividades, '/Admin/atividade/')
api.add_resource(Admin_excluir_atividade, '/Admin/atividades/<int:id>/')


if __name__ == '__main__':
    app.run(debug=True)


# OBSERVAÇÕES
    # Verificar excesso de código