# API RESTful de Gerenciamento de Biblioteca (AV2 - Poo)
Esta API foi desenvolvida utilizando Python, o framework Flask e o ORM SQLAlchemy, aplicando os princípios da Programação Orientada a Objetos para gerenciar o acervo de livros, empréstimos e multas de usuários.

## Requisitos Mínimos Atendidos
* A aplicação atende aos seguintes requisitos:
* **Módulo de Usuários**: Cadastro, Login e Autenticação via JWT.
* **CRUD de Registros**: Implementação completa de Livros (C, R, U, D).
* **Regras de Negócio**: Lógica de Empréstimo, Devolução e Cálculo de Multas.
* **Banco de Dados**: Utilização de SQLite e Modelos SQLAlchemy.

## Instalação e Execução
### 1. Clonar o Repositório e Navegar para a Pasta
```
# Navegue até o diretório onde deseja instalar o projeto
git clone https://github.com/ferreiraLucasnsc/av2-api-flask
cd api-biblioteca
```

### 2. Configurar o Ambiente Virtual (venv)
```
# Cria o ambiente virtual
python -m venv venv
# Ativa o ambiente (Windows)
# .\venv\Scripts\activate
# Ativa o ambiente (Linux/macOS)
source venv/bin/activate
```

### 3. Instalar Dependências
Com o ambiente ativo, instale as bibliotecas necessárias:
```
pip install -r requirements.txt
```

### 4. Executar a API
O comando abaixo inicia o servidor de desenvolvimento do Flask. Ele também criará o arquivo biblioteca.db (banco de dados SQLite) e as tabelas na primeira execução (através do init_db(app) no app.py).
```
python app.py
```
A API estará acessível em ```http://127.0.0.1:5000```.

## Exemplos de Requisições (Endpoints)
Use ferramentas como Postman, Insomnia ou Thunder Client para testar a API.

### 1. Módulo de Usuários (Autenticação)
#### A. Cadastro (Registro)
* **POST** ```/users/register```
```
{
    "nome": "João Silva",
    "email": "joao@email.com",
    "password": "senhaforte123"
}
```
#### B. Login (Geração de Token)
* **POST** ```/users/login```
```
{
    "email": "joao@email.com",
    "password": "senhaforte123"
}
```
    **Resultado**: Retorna o ```access_token``` JWT. Este token é obrigatório para todas as rotas de gerenciamento (```/registros```).

### 2. Gerenciamento da Biblioteca (Rotas Protegidas)
Todas as rotas abaixo exigem o Header ```Authorization: Bearer <TOKEN>```.

#### A. Adicionar Novo Livro (Create)
* **POST** ```/registros/livros```
```
{
    "titulo": "A Arte da Guerra",
    "autor": "Sun Tzu"
}
```

#### B. Emprestar Livro (Lógica de Negócio)
* **POST** ```/registros/emprestar```
```
{
    "livro_id": 1 
}
```

#### C. Devolver Livro (Calculcar Multa)
* **POST** ```/registros/devolver```
```
{
    "livro_id": 1 
}
```

#### D. Consultar Multa Pendente
* **GET** ```/registros/multa/consultar```
* **BODY**: (Vazio)

#### E. Pagar Multa Pendente
* **POST** ```/registros/multa/pagar```