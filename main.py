import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from reportlab.pdfgen import canvas

numero_id = 0
banco = None

# --- CONEXÃO COM O BANCO DE DADOS ---
try:
    banco = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cadastro_produtos",
    )
    print("Conexão com o banco realizada com sucesso!")
except mysql.connector.Error as err:
    print(f"\n[ERRO CRÍTICO] Falha ao conectar ao MySQL: {err}")
    print("-> Ligue o MySQL no XAMPP/WAMP e certifique-se de que a base 'cadastro_produtos' existe.\n")
    sys.exit(1)  # Encerra o programa com segurança antes de carregar as telas


# --- FUNÇÕES DO SISTEMA ---
def funcao_principal():
    linha1 = form.lineEdit.text()
    linha2 = form.lineEdit_2.text()
    linha3 = form.lineEdit_3.text()

    categoria = ""
    if form.radioButton.isChecked():
        categoria = "Informática"
    elif form.radioButton_2.isChecked():
        categoria = "Alimentos"
    else:
        categoria = "Eletrônicos"

    try:
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s, %s, %s, %s)"
        dados = (str(linha1), str(linha2), str(linha3), categoria)
        cursor.execute(comando_SQL, dados)
        banco.commit()
        
        # Limpa os campos após salvar
        form.lineEdit.setText("")
        form.lineEdit_2.setText("")
        form.lineEdit_3.setText("")
        print("Produto cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")


def chama_segunda_tela():
    segunda_tela.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(len(dados_lidos)):
        for j in range(5):
            segunda_tela.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))
            )


def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    if linha < 0:
        print("Selecione uma linha para editar!")
        return

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]

    cursor.execute(f"SELECT * FROM produtos WHERE id = {valor_id}")
    produto = cursor.fetchall()

    if produto:
        numero_id = valor_id
        tela_editar.show()

        # Preenche os campos do form de edição
        tela_editar.lineEdit.setText(str(produto[0][0]))
        tela_editar.lineEdit_2.setText(str(produto[0][1]))
        tela_editar.lineEdit_3.setText(str(produto[0][2]))
        tela_editar.lineEdit_4.setText(str(produto[0][3]))
        tela_editar.lineEdit_5.setText(str(produto[0][4]))


def salvar_dados_editados():
    global numero_id

    # Garantir nomes correspondentes aos campos da interface
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()

    cursor = banco.cursor()
    comando_SQL = "UPDATE produtos SET codigo = %s, descricao = %s, preco = %s, categoria = %s WHERE id = %s"
    dados = (codigo, descricao, preco, categoria, numero_id)
    
    cursor.execute(comando_SQL, dados)
    banco.commit()  # Confirma a alteração no banco

    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    if linha < 0:
        print("Selecione uma linha para excluir!")
        return

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]

    cursor.execute(f"DELETE FROM produtos WHERE id = {valor_id}")
    banco.commit()

    segunda_tela.tableWidget.removeRow(linha)
    print(f"Linha {linha} excluída com sucesso.")


def gerar_pdf():
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados_lidos = cursor.fetchall()

    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados")

    pdf.setFont("Times-Bold", 12)
    pdf.drawString(30, 750, "ID")
    pdf.drawString(80, 750, "CÓDIGO")
    pdf.drawString(170, 750, "PRODUTO")
    pdf.drawString(350, 750, "PREÇO")
    pdf.drawString(450, 750, "CATEGORIA")

    pdf.setFont("Times-Roman", 10)
    y = 0
    for row in dados_lidos:
        y += 30
        pdf.drawString(30, 750 - y, str(row[0]))
        pdf.drawString(80, 750 - y, str(row[1]))
        pdf.drawString(170, 750 - y, str(row[2]))
        pdf.drawString(350, 750 - y, str(row[3]))
        pdf.drawString(450, 750 - y, str(row[4]))

    pdf.save()
    print("PDF GERADO COM SUCESSO!")


# --- EXECUÇÃO DA APLICAÇÃO ---
app = QtWidgets.QApplication(sys.argv)

try:
    form = uic.loadUi("form.ui")
    segunda_tela = uic.loadUi("listar_dados.ui")
    tela_editar = uic.loadUi("menu_editar.ui")

    # Conexão dos botões
    form.pushButton.clicked.connect(funcao_principal)
    form.pushButton_2.clicked.connect(chama_segunda_tela)
    segunda_tela.pushButton.clicked.connect(gerar_pdf)
    segunda_tela.pushButton_2.clicked.connect(excluir_dados)
    segunda_tela.pushButton_3.clicked.connect(editar_dados)
    tela_editar.pushButton.clicked.connect(salvar_dados_editados)

    form.show()
    sys.exit(app.exec_())
except FileNotFoundError as e:
    print(f"Erro ao carregar arquivos .ui: {e}")