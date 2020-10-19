# Contexto:
Precisamos obter a evolução percentual diária da colheita de soja por “Regiões do IMEA”
para criarmos alguns gráficos no Tableau. No entanto, os dados estão em uma tabela dentro de
um PDF e são separados em relatórios semanais.

Seu desafio consiste em obter os dados das últimas duas safras e garantir que os dados
da nova safra sejam obtidos automaticamente após as novas publicações.

Link do site: http://www.imea.com.br/imea-site/relatorios-mercado-detalhe?c=4&s=8

# Resultado esperado:
- Criação do pipeline de dados com recorrência semanal;
- Uma tabela no banco de dados para armazenar os registros (respeitando as boas
práticas);
- Disponibilizar acesso ao banco de dados (público) ou “dump” para possível teste no
Tableau;
- Criação de repositório no GitHub com todo o código.


# Tecnologias obrigatórias:
- Linguagem Python;
- Banco de dados PostgreSQL ou similar;
- Versionamento de código no GitHub.

# Opcionais (não obrigatório):
- Utilização de serviços na AWS (EC2, ECR, RDS e EKS);
- Docker;
- SQLAlchemy (Python);
- GitHub Actions para CI/CD.

# Guia de Instalação
- Clonar o Repositorio
- Criar uma instancia de postgre e rodar o script script/bancoDados.sql
- iniciar o shell e entrar na pasta colonada e instalar as bibliotecas necessárioas:
    - pip install -r requirements.txt

- criar as variaveis de ambiente:
    - pgServerJB -> recebe o endereo do servidor do Postgre 
    - pgBaseJB -> recebe o nome da base de dados 
    - pgUserJB -> recebe o nome do usuario pra conexão com o banco de dados
    - pgPassJB -> recebe a senha do usuario para conexão com o banco de dados

- agendar para rodar o arquivo main.py 1 vez por semana
