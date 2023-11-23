from neo4j import GraphDatabase

class RedeSocial:
  def __init__(self, uri, user, password):
      self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def fechar(self):
      self.driver.close()

  def criar_pessoa(self, id, nome, idade, localizacao):
      with self.driver.session() as session:
          session.run("CREATE (a:Pessoa {id: $id, nome: $nome, idade: $idade, localizacao: $localizacao})",
                    id=id, nome=nome, idade=idade, localizacao=localizacao)

  def criar_amizade(self, id1, id2):
      with self.driver.session() as session:
          session.run("MATCH (a:Pessoa), (b:Pessoa) WHERE a.id = $id1 AND b.id = $id2 "
                    "CREATE (a)-[r:AMIGO_DE]->(b)",
                    id1=id1, id2=id2)

  def obter_todas_pessoas(self):
      with self.driver.session() as session:
          result = session.run("MATCH (a:Pessoa) RETURN a.id, a.nome")
          return result.data()

  def obter_amigos(self, id):
      with self.driver.session() as session:
          result = session.run("MATCH (a:Pessoa)-[:AMIGO_DE]->(b:Pessoa) WHERE a.id = $id "
                             "RETURN b.id, b.nome",
                             id=id)
          return result.data()

  def remover_pessoa(self, id):
      with self.driver.session() as session:
          session.run("MATCH (a:Pessoa {id: $id}) DETACH DELETE a", id=id)

def menu():
   print("1. Inserir pessoa")
   print("2. Listar pessoas")
   print("3. Adicionar amizade")
   print("4. Visualizar amigos")
   print("5. Remover pessoa")
   print("6. Sair")
   opcao = int(input("Escolha uma opção: "))
   return opcao

def main():
   rede_social = RedeSocial("bolt://localhost:7687", "neo4j", "12345678")
   while True:
       opcao = menu()
       if opcao == 1:
           id = input("Insira o ID da pessoa: ")
           nome = input("Insira o nome da pessoa: ")
           idade = input("Insira a idade da pessoa: ")
           localizacao = input("Insira a localização da pessoa: ")
           rede_social.criar_pessoa(id, nome, idade, localizacao)
       elif opcao == 2:
           pessoas = rede_social.obter_todas_pessoas()
           for pessoa in pessoas:
               print(f"ID: {pessoa['a.id']}, Nome: {pessoa['a.nome']}")
       elif opcao == 3:
           id1 = input("Insira o ID da primeira pessoa: ")
           id2 = input("Insira o ID da segunda pessoa: ")
           rede_social.criar_amizade(id1, id2)
       elif opcao == 4:
           id = input("Insira o ID da pessoa: ")
           amigos = rede_social.obter_amigos(id)
           for amigo in amigos:
               print(f"ID: {amigo['b.id']}, Nome: {amigo['b.nome']}")
       elif opcao == 5:
           id = input("Insira o ID da pessoa a ser removida: ")
           rede_social.remover_pessoa(id)
       elif opcao == 6:
           rede_social.fechar()
           break

if __name__ == "__main__":
   main()
