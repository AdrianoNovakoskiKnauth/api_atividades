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
    else:
        return Usuarios.query.filter_by(login=login,senha=senha).first()

#Verifica se sessão pertence ao cadastro ou  atividade a ser acessado
def login_igual_nome(nome):
    if nome == str(auth.current_user()) or str(auth.current_user()) == 'Admin':
        usuario = Usuarios.query.filter_by(login=nome).first()
        if usuario.status == 0:
            response = {
                'status': 'error',
                'mensagem': 'Usuário inativo'
            }
            return response
        else:
            return True
    else:
        response = {
            'status': 'error',
            'mensagem': 'Acesso não autorizado'
        }
        return response

class Cadastro_pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            try:
                if nome == 'Admin':
                    pessoas = Pessoas.query.all()
                    response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
                    return response
                else:
                    pessoa = Pessoas.query.filter_by(nome=nome).first()
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
        if nome == 'Admin':
            dados = request.json
            if 'nome' in dados and 'idade' in dados:
                pessoa = Pessoas.query.filter_by(nome=dados['nome']).first()
                pessoa.idade = dados['idade']
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
                    'mensagem': 'Nome e idade deve ser informado'
                }
                return response
        else:
            response = login_igual_nome(nome)
            if response == True:
                pessoa = Pessoas.query.filter_by(nome=nome).first()
                try:
                    dados = request.json
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
            usuario = Usuarios.query.filter_by(login=nome).first()
            try:
                atividade = Atividades.query.all()
                for i in atividade:
                    if pessoa == i.pessoa:
                        i.delete()
                mensagem = '{} excluido com sucesso'.format(pessoa.nome)
                pessoa.delete()
                usuario.delete()
                return {'status':'sucesso','mensagem':mensagem}
            except AttributeError:
                return {'status': 'error', 'mensagem': 'Nome não encontrado'}
        else:
            return response

    @auth.login_required
    def post(self, nome):
        if nome == 'Admin':
            response = login_igual_nome(nome)
            if response == True:
                dados = request.json
                if "nome" in dados and "idade" in dados and "senha" in dados:
                    pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
                    usuario = Usuarios(login=dados['nome'],senha=dados['senha'], status=1)
                    pessoa.save()
                    usuario.save()
                    response = {
                        'id': pessoa.id,
                        'senha':usuario.senha,
                        'nome': pessoa.nome,
                        'idade': pessoa.idade
                    }
                    return response
                else:
                    response = {
                        'status': 'error',
                        'mensagem': [{
                            'nome': '????',
                            'senha': '????',
                            'idade': '????'}]
                    }
                    return response
            else:
                return response
        else:
            response = {
                'status': 'error',
                'mensagem': 'Função requer acesso de administrador '
            }
            return response

class Cadastros_delete_admin(Resource):
    @auth.login_required
    def delete(self, nome, id):
        if nome == "Admin":
            pessoa = Pessoas.query.filter_by(id=id).first()
            usuario = Usuarios.query.filter_by(login=pessoa.nome).first()
            try:
                atividade = Atividades.query.all()
                for i in atividade:
                    if pessoa == i.pessoa:
                        i.delete()
                mensagem = '{} excluído com sucesso'.format(pessoa.nome)
                pessoa.delete()
                usuario.delete()
                return {'status': 'sucesso', 'mensagem': mensagem}
            except AttributeError:
                return {'status': 'error', 'mensagem': 'Nome não encontrado'}
        else:
            response = {
                'status':'error',
                'mensagem':'Função requer acesso de administrador'
            }
            return response

class Usuarios_get_admin(Resource):
    @auth.login_required
    def get(self, nome):
        if nome == 'Admin':
            response = login_igual_nome(nome)
            if response == True:
                usuario = Usuarios.query.all()
                response = [{'login':i.login, 'status':i.status}for i in usuario]
                return response
            else:
                return response
        else:
            response = {
                'status': 'error',
                'mensagem': 'Função requer acesso de administrador'
            }
            return response

class Usuarios_put_admin(Resource):
    def put(self, nome, id):
        if nome == "Admin":
            pessoa = Pessoas.query.filter_by(id=id).first()
            usuario = Usuarios.query.filter_by(login=pessoa.nome).first()
            if usuario.status == 0:
                usuario.status = 1
                mensagem = 'Usuário {} ativo.'.format(usuario.login)
            else:
                usuario.status = 0
                mensagem = 'Usuário {} inativo.'.format(usuario.login)
            usuario.save()
            response = {
                'status':'sucesso',
                'mensagem':mensagem
            }
            return response

# ATIVIDADE - acesso de usuários
class Pessoa_get_post_atividades(Resource):
    @auth.login_required
    def get(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            if nome == 'Admin':
                atividade = Atividades.query.all()
                response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividade]
                return response
            else:
                pessoa = Pessoas.query.filter_by(nome=nome).first()
                atividades = Atividades.query.all()
                response = [{'pessoa':pessoa.nome}]
                descr = {'mensagem':'Não consta atividades'}
                cond = 0
                for i in atividades:
                    if pessoa == i.pessoa:
                        descr = {'id':i.id,'nome': i.nome, 'status':i.status}
                        cond = True
                        response.append(descr)
                if cond != True:
                    response.append(descr)
                return response
        else:
            return response

    @auth.login_required
    def post(self, nome):
        response = login_igual_nome(nome)
        if response == True:
            dados = request.json
            if nome == 'Admin':
                if 'nome' in dados and 'pessoa' in dados:
                    pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
                    atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status='pendente')
                    atividade.save()
                    response = {
                        'id': atividade.id,
                        'pessoa': atividade.pessoa.nome,
                        'descricao': atividade.nome,
                        'status': atividade.status
                        }
                    return response
                else:
                    response = {
                        'pessoa': '???????????',
                        'nome': '???????????'
                    }
                return response
            else:
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
                if atividade.pessoa.nome == nome or nome == 'Admin':
                    atividade.status = 'Conclúido'
                    atividade.save()
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

# ATIVIDADES - acessos de administador
class Admin_delete_atividade(Resource):
    def delete(self, id):
        response = login_igual_nome('Admin')
        if response == True:
            atividade = Atividades.query.filter_by(id=id).first()
            atividade.delete()
            return [{'status': 'ok', 'mensagem': 'Exclúido'}]
        else:
            return response

# CADASTRO - acessos de usuários
api.add_resource(Usuarios_get_admin, '/<string:nome>/usuario/')
api.add_resource(Usuarios_put_admin, '/<string:nome>/usuario/<int:id>/')
api.add_resource(Cadastro_pessoa, '/<string:nome>/cadastro/')
api.add_resource(Cadastros_delete_admin, '/<string:nome>/cadastro/<int:id>/')
api.add_resource(Pessoa_get_post_atividades, '/<string:nome>/atividade/')
api.add_resource(Pessoa_put_delete_atividades,'/<string:nome>/atividade/<int:id>/')
api.add_resource(Admin_delete_atividade, '/Admin/atividade/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)

