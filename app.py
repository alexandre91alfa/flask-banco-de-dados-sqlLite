import sqlalchemy
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from json import loads
import utils
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USUARIOS = {
#     'root': 'admin',
#     'admin': 'root'
# }
#
#
# @auth.verify_password
# def verificacao(login, senha):
#     if not (login, senha):
#         return False
#
#     return USUARIOS.get(login) == senha


@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False

    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, id):
        try:
            pessoa = utils.consulta_id(id)
        except TypeError:
            pessoa = {
                'status': 'erro',
                'messagem': 'pessoa não encontrada',
            }

        return pessoa

    @auth.login_required
    def put(self, id):
        pessoa = Pessoas.query.filter_by(id=id).first()
        dados = loads(request.data)
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        Pessoas.save(pessoa)
        return dados

    @auth.login_required
    def delete(self, id):
        try:
            utils.exclui_pessoa(id)
            status = {'Status': 'success'}
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            status = {'Status': 'error', 'messagem': 'Id não localizado'}

        return status


class ListPessoa(Resource):
    @auth.login_required
    def get(self):
        try:
            dados = utils.consulta()
        except TypeError:
            dados = {'status': 'Erro pesquisa'}
        return dados

    @auth.login_required
    def post(self):
        try:
            dados = loads(request.data)
            nome = dados['nome']
            idade = dados['idade']
            utils.insere_pessoa(nome, idade)
            result = {'status': 'success'}
        except TypeError:
            result = {'status': 'error'}

        return result


class AtividadeList(Resource):

    @auth.login_required
    def get(self):
        try:
            dados = utils.consultaAtividade()
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            dados = {'Status': 'erro'}
        return dados


class Atividade(Resource):

    @auth.login_required
    def get(self, id):
        try:
            atividade = utils.consultaA_id(id)
        except AttributeError:
            atividade = {
                'status': 'erro',
                'messagem': 'pessoa não encontrada',
            }

        return atividade

    @auth.login_required
    def put(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        dados = loads(request.data)
        if 'nome' in dados:
            atividade.nome = dados['nome']
        Atividades.save(atividade)
        return dados

    @auth.login_required
    def post(self, id):
        try:
            people = Pessoas.query.filter_by(id=id).first()
            try:
                if people:
                    dados = loads(request.data)
                    nome = dados['nome']
                    utils.insere_atividade(nome, people)
                    result = {'status': 'success'}
                else:
                    raise UnboundLocalError
            except UnboundLocalError:
                result = {'status': 'error', 'messagem': 'pessoa não exites'}
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            result = {'status': 'error', 'messagem': 'Atividade não exites'}

        return result

    @auth.login_required
    def delete(self, id):
        try:
            utils.exclui_atividade(id)
            status = {'Status': 'success'}
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            status = {'Status': 'error', 'messagem': 'Id não localizado'}

        return status


api.add_resource(AtividadeList, '/atv')
api.add_resource(Atividade, '/atv/<int:id>')
api.add_resource(Pessoa, '/people/<int:id>')
api.add_resource(ListPessoa, '/people')

if __name__ == "__main__":
    # app.run(debug=True, host='192.168.100.103')
    app.run(debug=True, )
