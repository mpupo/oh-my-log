# Central de Erros - Oh My Log

Projeto final realizado para a plataforma da Codenation no **Acelera Dev - Python**, apoiado pela Stone.

## 1. Sobre o projeto

---

### 1.1 Informações cedidas pela Codenation para realização do projeto

#### 1.1.1 Contexto

Em projetos modernos é cada vez mais comum o uso de arquiteturas baseadas em serviços ou microsserviços. Nestes ambientes complexos, erros podem surgir em diferentes camadas da aplicação (backend, frontend, mobile, desktop) e mesmo em serviços distintos. Desta forma, é muito importante que os desenvolvedores possam centralizar todos os registros de erros em um local, de onde podem monitorar e tomar decisões mais acertadas. Neste projeto vamos implementar um sistema para centralizar registros de erros de aplicações.

#### 1.1.2 Objetivo

Como o programa (ou aceleração) possui ênfase no backend, o objetivo principal é:

- Criar endpoints para serem usados pelo frontend da aplicação;
- Criar um endpoint que será usado para gravar os logs de erro em um banco de dados relacional;
- A API deve ser segura, permitindo acesso apenas com um token de autenticação válido;

Porém, a implementação do frontend (não obrigatória) também pode ocorrer nos seguintes moldes:

- Deve implementar as funcionalidades apresentadas nos wireframes;
- Deve ser acessada adequadamente tanto por navegadores desktop quanto mobile;
- Deve consumir a API do produto;
- Desenvolvida na forma de uma Single Page Application;

### 1.2. Wireframes

#### 1.2.1 Cadastro

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/1-cadastro.png"
     alt="Tela de cadastro"
     style="float: left; margin-right: 10px;" />

#### 1.2.2 Login

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/2-login.png"
     alt="Tela de login"
     style="float: left; margin-right: 10px;" />

#### 1.2.3 Dashboard

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/3-dashboard.png"
     alt="Dashboard"
     style="float: left; margin-right: 10px;" />

#### 1.2.4 Ambientes

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/4-ambientes.png"
     alt="Ambientes"
     style="float: left; margin-right: 10px;" />

#### 1.2.5 Ordenação

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/5-order.png"
     alt="Ordenação"
     style="float: left; margin-right: 10px;" />

#### 1.2.6 Filtro

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/6-filtro.png"
     alt="Filtro"
     style="float: left; margin-right: 10px;" />

#### 1.2.7 Detalhes do erro

<img src="https://codenation-challenges.s3-us-west-1.amazonaws.com/central-erros/7-detalhes.png"
     alt="Detalhes do erro"
     style="float: left; margin-right: 10px;" />

## 2. Mão na massa

---

### 2.3 Ferramentas utilizadas

- [Visual Studio Code](https://code.visualstudio.com/)

### 2.2 Dependências

Para testar o projeto em sua máquina, é necessário seguir os seguintes passos:

- Instalar a biblioteca **virtualenv** globalmente para criar um virtual environment:

```bash
pip3 install virtualenv
```

- Criar um novo virtual environment:

```bash
cd venv
python -m venv .
```

- Ativar o virtual environment para execução:

```bash
cd ..
source venv/bin/activate
```

- Instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```
