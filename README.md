 SISTEMA DE GESTÃO DE PRODUTOS EM PYTHON E PyQt5
 
Esse é um projeto que desenvolvi recentemente para colocar em prática a criação de interfaces gráficas com **PyQt5** integradas a um banco de dados relacional (**MySQL**). 

A ideia do sistema é ser uma aplicação desktop simples, direta e funcional para cadastro e controle de estoque de produtos, incluindo a emissão de relatórios em PDF.

## O que o sistema faz?

- **Cadastro de produtos:** Registro rápido com código, descrição, preço e categoria (selecionada via botões de rádio).
- **Listagem e consulta:** Visualização de todos os itens cadastrados em uma tabela estilizada.
- **Edição em tempo real:** Alteração de informações de qualquer produto selecionado na tabela.
- **Exclusão de registros:** Remoção direta com atualização automática da interface.
- **Geração de relatórios:** Exportação da lista completa de produtos para um arquivo PDF com layout customizado.

## Tecnologias que utilizei

- **Python 3** (Linguagem principal)
- **PyQt5 & Qt Designer** (Para construção das telas `.ui`)
- **MySQL / mysql-connector-python** (Para persistência dos dados)
- **ReportLab** (Para desenhar e exportar a lista em PDF)
