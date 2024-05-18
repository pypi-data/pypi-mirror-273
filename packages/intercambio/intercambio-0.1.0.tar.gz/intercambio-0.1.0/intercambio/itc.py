class intercambio:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def apresentar(self):
        return f"Olá, meu nome é {self.nome} e eu tenho {self.idade} anos."

    def time_de_itc(self):
        print(f"time de itc {self.apresentar()}")

    def teste_de_classe(self):
        print("teste de classe")



# # Criando uma instância da classe Pessoa
# pessoa = intercambio("Alice", 30)

# # Usando o método apresentar
# print(pessoa.apresentar())  # Output: Olá, meu nome é Alice e eu tenho 30 anos.

# # Usando o método time_de_santos
# pessoa.time_de_itc()  # Output: time de santos

# # Usando o método teste_de_classe
# pessoa.teste_de_classe()  # Output: teste de classe
