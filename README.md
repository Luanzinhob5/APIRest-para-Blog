# API RESTful de Blog - Projeto de Portfólio

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-black?style=for-the-badge&logo=flask&logoColor=white)
![Flask-RESTx](https://img.shields.io/badge/Flask--RESTx-gray?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-blueviolet?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-blue?style=for-the-badge&logo=sqlite&logoColor=white)

## 1. Visão Geral

Esta é uma API RESTful robusta e escalável para gerenciar os posts de um blog. O projeto foi feito para estudos proprios em desenvolvimento backend com Python, aplicando arquitetura de software, segurança e testes.

A API permite a criação, leitura, atualização e exclusão de posts, com endpoints de autenticação e autorização para proteger operações sensíveis.

## 2. Funcionalidades Principais

* **Gerenciamento Completo de Posts:** Endpoints para todas as operações CRUD (`GET`, `POST`, `PUT`, `DELETE`).
* **Autenticação e Autorização com JWT:** Sistema de registro e login que gera tokens de acesso (JWT). Rotas de modificação de dados são protegidas, exigindo um token válido.
* **Paginação:** A rota de listagem de posts (`GET /api/posts/`) é paginada para lidar com grandes volumes de dados de forma eficiente.
* **Documentação Automática Interativa (Swagger UI):** A API é autodocumentada pelo Flask-RESTx. Que faz com que todas as rotas sejam entregues ao usuario.

## 3. Showcase Tecnológico e Boas Práticas

As seguintes tecnologias e padrões foram empregados:

* **Framework Backend:** **Flask** e **Flask-RESTx** para uma estrutura de API organizada e baseada em Recursos.
* **Banco de Dados e ORM:** **SQLAlchemy 2.0** para mapeamento objeto-relacional. O banco de dados utilizado é o **SQLite**.
* **Validação e Serialização de Dados:** **Pydantic V2** para definir esquemas de dados robustos, garantindo que os dados que entram e saem da API sejam sempre válidos e bem estruturados.
* **Segurança:** Autenticação baseada em **JSON Web Tokens (JWT)** gerenciada pela biblioteca `Flask-JWT-Extended`. Senhas de usuário são seguramente armazenadas usando hashes `Bcrypt`.
* **Testes:** Suíte de testes de integração com **Pytest**, garantindo a confiabilidade dos endpoints e a lógica de negócio. A configuração de testes utiliza um banco de dados em secundario dedicado para testes, sendo ideal para o isolamento total dos testes.
* **Arquitetura de Software:**
    * **Padrão App Factory (`criar_app`)**: Para permitir a criação de múltiplas instâncias da aplicação com diferentes configurações (ex: desenvolvimento, teste).
    * **Blueprints**: Para organizar o código de forma modular e escalável.
    * **Configuração baseada em Ambiente**: Uso de arquivos `.env` para gerenciar segredos e configurações, separando o código da configuração.