# Trabalho Avaliativo – POO - Desenvolvimento de API em Python (Flask)


Desenvolva uma API REST em Python, utilizando o framework Flask, aplicando os princípios da Programação Orientada a Objetos, com implementação de cadastro e autenticação de usuários, pelo menos um CRUD completo de registros, e o uso de um banco de dados SQLite.

O aluno deverá desenvolver uma aplicação backend (API) em Python, utilizando o Flask, que atenda aos seguintes requisitos mínimos:

## 1. Módulo de Usuários
- Cadastro de novos usuários (registro).
- Autenticação com **login e geração de token JWT**.
- Validação de acesso a rotas protegidas por meio do token.


## 2. CRUD de Registros (entidade principal)
- O sistema deve conter ao menos uma entidade principal com as operações:
    - C: Create (criação de registro)
    - R: Read (listagem e consulta individual)
    - U: Update (atualização)
    - D: Delete (remoção)
- As operações de CRUD devem estar associadas ao usuário autenticado.


## 3. Banco de Dados
- Utilizar SQLite como banco de dados local.
- Implementar os modelos de dados com SQLAlchemy (ORM).
- Criar classes representando as tabelas e seus relacionamentos.

## 4. Estrutura do Projeto
- O projeto deve seguir uma estrutura modular, com boa organização de código.  
  Sugestão de estrutura:  
        app.py  
        database.py  
        models/  
        ├── user.py  
        └── registro.py  
        routes/  
        ├── users.py  
        └── registros.py  

## Tema Sugerido: *API de Gerenciamento Financeiro Pessoal*
Como sugestão, pode-se desenvolver uma API para controle financeiro, contendo:
- Usuários: autenticação e gerenciamento de perfis.
- Receitas: cadastro, listagem, atualização e exclusão de entradas financeiras.
- Despesas: cadastro, listagem, atualização e exclusão de gastos.
- Campos mínimos sugeridos:
    - valor, categoria, descrição, data, tipo (receita/ despesa)
- Regras sugeridas:
    - Apenas o usuário autenticado pode acessar e gerenciar suas próprias transações.


O tema é flexível: o aluno pode propor outro sistema (ex: API de tarefas, biblioteca, controle de estoque etc.), desde que atenda aos requisitos mínimos de autenticação, CRUD e uso de banco de dados.

## Critérios de Avaliação
- **Organização e Estrutura do Projeto**
    Pastas, modularização, legibilidade e boas práticas de POO
- **Implementação de Autenticação**
    Cadastro, login e validação com JWT ou similar
- **CRUD Funcional e Completo**
    Operações Create, Read, Update e Delete corretamente implementadas
- **Integração com o Banco de Dados**
    Persistência e relacionamentos entre tabelas via SQLAlchemy
- **Documentação**
    README, exemplos de uso e clareza nas instruções da API



## Entrega
- Forma: Commit no repositório GitHub.
- Link para o clone do Projeto: https://classroom.github.com/a/zi5zy4rq
    - Ou, faça o Fork: https://github.com/guilherme-augusto-ferraz/av2-api-flask
- Conteúdo obrigatório no pacote:
    - Código-fonte completo.
    - Arquivo requirements.txt com dependências.
    - Arquivo README.md com:
        - Descrição do sistema;
        - Instruções de instalação e execução;
        - Exemplos de requisições (endpoints e JSONs).
- Prazo: 28/11/2025

## Desafio Extra (opcional)
Para alunos que desejarem ir além dos requisitos mínimos:
- Implementar filtros e busca (ex: despesas por mês ou categoria).
- Adicionar relatórios de saldo (total de receitas – total de despesas).
- Implementar refresh token e expiração do JWT.
- Adicionar testes automatizados (pytest).

## Resultado Esperado
Ao final da atividade, o aluno deverá demonstrar:
- Domínio dos conceitos de POO aplicada ao desenvolvimento web;
- Capacidade de modelar e implementar uma API RESTful;
- Conhecimento prático do framework Flask e do banco SQLite;
- Habilidade para organizar e documentar projetos de software.