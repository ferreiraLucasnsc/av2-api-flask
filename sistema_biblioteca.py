from datetime import datetime, timedelta
import os
from os import system

PRAZO_DEVOLUCAO = 7 
VALOR_MULTA_DIARIA = 1.50

class Livro:
    def __init__(self, id_livro, titulo, autor, disponivel=True):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.disponivel = disponivel

class Usuario:
    def __init__(self, id_usuario, nome, livros_emprestados=None, multa_pendente=0.0):
        if livros_emprestados is None:
            livros_emprestados = []
        self.id_usuario = id_usuario
        self.nome = nome
        self.livros_emprestados = livros_emprestados
        self.multa_pendente = multa_pendente

class SistemaBiblioteca:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = {} 

    def cadastrar_usuario(self, id_usuario, nome):
        if id_usuario in self.usuarios:
            raise ValueError("Usuário já cadastrado.")
        else:
            self.usuarios[id_usuario] = Usuario(id_usuario, nome)
            print(f"Usuário {nome} cadastrado com sucesso.")

    def listar_usuarios(self):
        return [(u.id_usuario, u.nome) for u in self.usuarios.values()]
    
    def adicionar_livro(self, id_livro, titulo, autor):
        if id_livro in self.livros:
            raise ValueError("Livro já cadastrado.")
        else:
            self.livros[id_livro] = Livro(id_livro, titulo, autor)
            print(f"Livro '{titulo}' adicionado com sucesso.")

    def listar_livros(self):
        return [(l.id_livro, l.titulo, "Sim" if l.disponivel else "Não") for l in self.livros.values()]

    def emprestar_livro(self, id_usuario, id_livro, data_emprestimo_simulada=None):
        if id_usuario not in self.usuarios:
            raise ValueError("Usuário não cadastrado.")
        if id_livro not in self.livros:
            raise ValueError("Livro não cadastrado.")
        
        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]

        if not livro.disponivel:
            raise ValueError("Livro não está disponível para empréstimo.")
        if usuario.multa_pendente > 0:
            raise ValueError("Usuário possui multa pendente.")
        
        livro.disponivel = False
        usuario.livros_emprestados.append(id_livro)

        data_registro = data_emprestimo_simulada if data_emprestimo_simulada else datetime.now()
        self.emprestimos[(id_usuario, id_livro)] = data_registro
        
        print(f"Livro '{livro.titulo}' emprestado para o usuário {usuario.nome}. Prazo de {PRAZO_DEVOLUCAO} dias. (Data: {data_registro.strftime('%d/%m/%Y')})")

    def devolver_livro(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            raise ValueError("Usuário não cadastrado.")
        if id_livro not in self.livros:
            raise ValueError("Livro não cadastrado.")
        
        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]

        if id_livro not in usuario.livros_emprestados:
            raise ValueError("Este livro não foi emprestado por este usuário.")
            
        data_emprestimo = self.emprestimos.pop((id_usuario, id_livro))
        data_devolucao = datetime.now()
        
        atraso = data_devolucao - (data_emprestimo + timedelta(days=PRAZO_DEVOLUCAO))
        dias_atraso = atraso.days if atraso.days > 0 else 0
        
        if dias_atraso > 0:
            multa = dias_atraso * VALOR_MULTA_DIARIA
            usuario.multa_pendente += multa
            print(f"\n⚠️  ATENÇÃO: Devolução atrasada em {dias_atraso} dias. Multa aplicada de R${multa:.2f}.")
            
        livro.disponivel = True
        usuario.livros_emprestados.remove(id_livro)
        print(f"Livro '{livro.titulo}' devolvido pelo usuário {usuario.nome}.")

    def consultar_multa(self, id_usuario):
        if id_usuario not in self.usuarios:
            raise ValueError("Usuário não cadastrado.")
        
        usuario = self.usuarios[id_usuario]
        return usuario.multa_pendente
    
    def pagar_multa(self, id_usuario, valor_pago):
        if id_usuario not in self.usuarios:
            raise ValueError("Usuário não cadastrado.")
        
        usuario = self.usuarios[id_usuario]
        if valor_pago > usuario.multa_pendente:
            raise ValueError(f"Valor pago excede a multa pendente de R${usuario.multa_pendente:.2f}.")
        
        usuario.multa_pendente -= valor_pago
        print(f"Usuário {usuario.nome} pagou R${valor_pago:.2f} de multa. Saldo restante: R${usuario.multa_pendente:.2f}.")

    def analisar_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            raise ValueError("Usuário não cadastrado.")
        
        usuario = self.usuarios[id_usuario]
        
        multa_em_aberto = 0.0
        esta_atrasado = False
        
        print("=" * 40)
        print(f"ANÁLISE DO USUÁRIO: {usuario.nome} (ID: {usuario.id_usuario})")
        print("=" * 40)
        print(f"Multa Pendente (Dívida Anterior): R${usuario.multa_pendente:.2f}")
        print("-" * 40)

        if not usuario.livros_emprestados and usuario.multa_pendente == 0:
            print("Status Geral: OK (Sem Pendências)")
        elif not usuario.livros_emprestados:
            print("Nenhum livro emprestado atualmente.")
             
        if usuario.livros_emprestados:
            print("Livros Emprestados:")
            for id_livro in usuario.livros_emprestados:
                livro = self.livros[id_livro]
                data_emprestimo = self.emprestimos.get((id_usuario, id_livro))
                data_limite = data_emprestimo + timedelta(days=PRAZO_DEVOLUCAO)
                
                hoje = datetime.now()
                atraso = hoje - data_limite
                dias_atraso = atraso.days if atraso.days > 0 else 0
                
                status_livro = "Emprestado (Dentro do Prazo)"
                multa_livro = 0.0

                if dias_atraso > 0:
                    esta_atrasado = True
                    multa_livro = dias_atraso * VALOR_MULTA_DIARIA
                    multa_em_aberto += multa_livro
                    status_livro = f"Atrasado ({dias_atraso} dias)"

                print(f"  - Livro ID {id_livro}: '{livro.titulo}'")
                print(f"    Autor: {livro.autor}")
                print(f"    Empréstimo: {data_emprestimo.strftime('%d/%m/%Y %H:%M')}")
                print(f"    Devolução Limite: {data_limite.strftime('%d/%m/%Y')}")
                print(f"    Status: {status_livro}")
                if multa_livro > 0:
                    print(f"    Multa em Aberto: R${multa_livro:.2f}")
                print("-" * 40)
            
            if esta_atrasado:
                status_geral = "ATRASADO (Pendência de Devolução)"
            else:
                status_geral = "Emprestado (Dentro do Prazo)"
            
            print(f"STATUS GERAL: {status_geral}")
            print(f"Multa em Aberto (Atraso Atual): R${multa_em_aberto:.2f}")
            print(f"TOTAL GERAL DE DÉBITOS: R${usuario.multa_pendente + multa_em_aberto:.2f}")
        
        print("=" * 40)


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def input_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(',', '.'))
        except ValueError:
            print("Entrada inválida. Digite um número decimal (use ponto).")

def executar_cadastro_usuario(sistema: SistemaBiblioteca):
    print("--- Cadastro de Usuário ---")
    id_usuario = input_int("Digite o ID do novo usuário: ")
    nome = input("Digite o nome do usuário: ")
    try:
        sistema.cadastrar_usuario(id_usuario, nome)
    except ValueError as e:
        print(f"ERRO: {e}")

def executar_cadastro_livro(sistema: SistemaBiblioteca):
    print("--- Cadastro de Livro ---")
    id_livro = input_int("Digite o ID do novo livro: ")
    titulo = input("Digite o Título do livro: ")
    autor = input("Digite o Autor do livro: ")
    try:
        sistema.adicionar_livro(id_livro, titulo, autor)
    except ValueError as e:
        print(f"ERRO: {e}")

def listar_recursos(sistema: SistemaBiblioteca):
    print("--- Usuários Cadastrados ---")
    for id, nome in sistema.listar_usuarios():
        print(f"ID: {id} | Nome: {nome}")
        
    print("--- Livros no Acervo ---")
    for id, titulo, disponivel in sistema.listar_livros():
        print(f"ID: {id} | Título: {titulo} | Disponível: {disponivel}")
    print("-" * 30)

def executar_analise_usuario(sistema: SistemaBiblioteca):
    print("--- Análise de Usuário ---")
    id_usuario = input_int("Digite o ID do usuário para análise: ")
    try:
        sistema.analisar_usuario(id_usuario)
    except ValueError as e:
        print(f"ERRO: {e}")

def main():
    sistema = SistemaBiblioteca()

    dias_atraso = 15
    data_atrasada = datetime.now() - timedelta(days=dias_atraso)
    
    sistema.cadastrar_usuario(1, "Alice)")
    sistema.cadastrar_usuario(2, "Bob")
    sistema.cadastrar_usuario(3, "Charlie")
    sistema.cadastrar_usuario(4, "David")
    sistema.cadastrar_usuario(5, "Eve")
    print("-" * 50)

    sistema.adicionar_livro(101, "A Riqueza das Nações", "Adam Smith")
    sistema.adicionar_livro(102, "O Príncipe", "Nicolau Maquiavel")
    sistema.adicionar_livro(103, "Cem Anos de Solidão", "Gabriel García Márquez")
    sistema.adicionar_livro(104, "Orgulho e Preconceito", "Jane Austen")
    sistema.adicionar_livro(105, "1984", "George Orwell")
    print("-" * 50)


    sistema.emprestar_livro(1, 101) 
    sistema.emprestar_livro(2, 102) 
    sistema.emprestar_livro(3, 103, data_emprestimo_simulada=data_atrasada)
    sistema.emprestar_livro(4, 104, data_emprestimo_simulada=data_atrasada)
    print("-" * 50)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f" SISTEMA DE BIBLIOTECA ".center(50, "="))
        print(" Menu principal ".center(50))
        print("1. Emprestar Livro")
        print("2. Devolver Livro (Testa Multa na Devolução!)")
        print("3. Consultar Multa (Antigas)")
        print("4. Pagar Multa (Antigas)")
        print("5. Listar Usuários e Livros")
        print("6. Cadastrar Novo Usuário")
        print("7. Adicionar Novo Livro")
        print("8. Analisar Usuário (Novo Status e Multa em Aberto)")
        print("9. Sair")

        opcao = input("Escolha uma opção (1-9): ")
        
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            if opcao == '1':
                id_usuario = input_int("Digite o ID do usuário: ")
                id_livro = input_int("Digite o ID do livro: ")
                sistema.emprestar_livro(id_usuario, id_livro)
            elif opcao == '2':
                id_usuario = input_int("Digite o ID do usuário: ")
                id_livro = input_int("Digite o ID do livro: ")
                sistema.devolver_livro(id_usuario, id_livro)
            elif opcao == '3':
                id_usuario = input_int("Digite o ID do usuário: ")
                multa = sistema.consultar_multa(id_usuario)
                print(f"Multa pendente (antiga): R${multa:.2f}")
            elif opcao == '4':
                id_usuario = input_int("Digite o ID do usuário: ")
                valor_pago = input_float("Digite o valor a pagar: ")
                sistema.pagar_multa(id_usuario, valor_pago)
            elif opcao == '5':
                listar_recursos(sistema)
            elif opcao == '6':
                executar_cadastro_usuario(sistema)
            elif opcao == '7':
                executar_cadastro_livro(sistema)
            elif opcao == '8':
                executar_analise_usuario(sistema)
            elif opcao == '9':
                print("Saindo do sistema. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        
        except ValueError as e:
            print(f"ERRO DE OPERAÇÃO: {e}")

        if opcao != '9':
            os.system('pause' if os.name == 'nt' else 'read -n 1 -s -r -p "Pressione qualquer tecla para continuar..."')

if __name__ == "__main__":
    main()