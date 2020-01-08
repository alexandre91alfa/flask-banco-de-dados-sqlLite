from models import Pessoas, Atividades

# Pessoas


def insere_pessoa(nome, idade):
    pessoa = Pessoas(nome=nome, idade=idade)
    Pessoas.save(pessoa)


def consulta():
    pessoa = Pessoas.query.all()
    np = [p.__dict__ for p in pessoa]
    nPessoa = []
    for p in np:
        del p['_sa_instance_state']
        nPessoa.append(p)
    return nPessoa

def consulta_id(id):
    p = Pessoas.query.filter_by(id=id).first()
    return {
        "id": p.id,
        "nome": p.nome,
        "idade": p.idade,
    }


def altera_pessoa(id, nome, idade):
    pessoa = Pessoas.query.filter_by(id=id)
    pessoa.nome = nome
    pessoa.idade = idade
    Pessoas.save(pessoa)


def exclui_pessoa(id):
    pessoa = Pessoas.query.filter_by(id=id).first()
    Pessoas.delele(pessoa)

# Atividades


def consultaAtividade():
    atividade = Atividades.query.all()
    na = [a.__dict__ for a in atividade]
    nAtividade = []
    for a in na:
        del a['_sa_instance_state']
        pessoa = Pessoas.query.filter_by(id=a['id']).first()
        a = {**a, 'pessoa': pessoa.nome}
        nAtividade.append(a)
    return nAtividade


def consultaA_id(id):
    a = Atividades.query.filter_by(id=id).first()
    p = Pessoas.query.filter_by(id=a.id).first()
    return {
        "id": a.id,
        "nome": a.nome,
        "id_pessoa": a.pessoa_id,
        "pessoa": p.nome
    }


def altera_atividade(id, nome):
    pessoa = Pessoas.query.filter_by(id=id)
    pessoa.nome = nome
    Pessoas.save(pessoa)


def insere_atividade(nome, pessoa):
    atividade = Atividades(nome=nome, pessoa=pessoa)
    Atividades.save(atividade)


def exclui_atividade(id):
    atividade = Atividades.query.filter_by(id=id).first()
    Atividades.delele(atividade)


if __name__ == "__main__":
    print(pessoa_referencia(1))
