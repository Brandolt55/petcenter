#------------IMPORATANDO AS BIBLIOTECAS QUE VÃO SER UTILIZADAS------------
from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox

#=============================================================================
#------------------------FAZENDO CONEXÃO COM O SQL---------------------
conn = sqlite3.connect('produtos.db')
#===========================================================================================
#--------------------------CRINADO FUNCTION PARA DELETAR INSUMO------------------------------
    
def deletar_insumo():
    if len(nome_insumo.get()) < 2:
        caixa_texto.delete("1.0", END)
        # escrever na caixa de texto
        caixa_texto.insert("1.0", f"Nome do Insumo inválido!")
        # finalizar a função
        return
    
    # deletar o insumo
    conn.execute(f'''
    DELETE FROM produtos 
    WHERE produto="{nome_insumo.get()}"
    ''')
    conn.commit()
    
    # deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)
    
    # escrever na caixa de texto
    caixa_texto.insert("1.0", f'''
    =====DELETADO DO ESTOQUE======
           COM SUCESSO!
    ==============================
    O produto: {nome_insumo.get()}
    foi deletado do estoque.
    -----------------------------
            PET CENTER
    ''')    
#====================================================================================
#-------------------------CRINADO FUNCTION DE VENDER PRODUTO------------------------
# define a função vender_produto
cursor = conn.cursor()

def registrar_venda():
    # Execute a SELECT query to check if the product is in stock
    cursor.execute("SELECT * FROM produtos WHERE produto = ?", (nome_insumo.get(),))
    resultado = cursor.fetchone()
    
    # If the product is not found in stock, display an error message
    if not resultado:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", f'''
        ===============================
        O produto: {nome_insumo.get()} 
        Não foi encontrado no estoque!!
        Tente verificar a quantidade
        e o nome do produto no botão
        "VISUALIZAR PLANILHA DO ESTOQUE"
        ================================
        ''')
        return
    
    # Retrieve the available quantity of the requested product
    produto_quantidade = resultado[2]
    
    # If the requested quantity is greater than the available quantity, display an error message
    if int(qtde_insumo.get()) > produto_quantidade:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", f'''
        ----ATENÇÃO QUANTIDADE!----
                INSUFICIENTE
        ===============================
        Produto: {nome_insumo.get()} 
        Não há quantidade suficiente em estoque!!
        Quantidade disponível: {produto_quantidade}
        ================================
        ''')
        return

    # Update the stock quantity
    conn.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE produto = ?", (qtde_insumo.get(), nome_insumo.get()))

    # Update the sales column
    valor_venda = int(qtde_insumo.get()) * float(preco_produto.get())
    conn.execute("UPDATE produtos SET vendas = vendas + ? WHERE produto = ?", (valor_venda, nome_insumo.get()))
    
    # Commit the changes to the database
    conn.commit()

    # Display the sale details
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f'''
=================================
       NOTA DA VENDA DO PRODUTO
------------------------------------
  PRODUTO:  {nome_insumo.get()}
  VALOR:   {preco_produto.get()}R$
  QUANTIDADE:  {qtde_insumo.get()} und
  PESO Kg:  {kg_insumo.get()}kg
------------------------------------
       TOTAL:{valor_venda}R$  
-----------------------------------
            PET CENTER
''')

 
#========================================================================================
#----------------------CRIANDO A FUNCTION DE ADICIONAR INSUMO---------------------------
def adicionar_insumo():
    # Check if the product already exists in the database
    result = conn.execute(f'SELECT * FROM produtos WHERE produto="{nome_insumo.get()}"').fetchone()

    if result:
        # If the product already exists, add the input quantity to the existing quantity
        nova_quantidade = result[2] + int(qtde_insumo.get())
        conn.execute(f'UPDATE produtos SET quantidade={nova_quantidade} WHERE produto="{nome_insumo.get()}"')
        conn.commit()
        mensagem = f'''
        ====================================
        QUANTIDADE DO PRODUTO ATUALIZADA!
        -------------------------------------
        PRODUTO: {nome_insumo.get()}
        NOVA QUANTIDADE: {nova_quantidade}und
        -------------------------------------
                    PET CENTER
        '''
    else:
        # If the product doesn't exist, insert a new record with the input values
        conn.execute(f'''
        INSERT INTO produtos(produto, preco, quantidade, peso, vendas)
        VALUES
        ("{nome_insumo.get()}", {preco_produto.get()}, {qtde_insumo.get()}, {kg_insumo.get()}, 0)
        ''')
        conn.commit()
        mensagem = f'''
        ====================================
        ADICIONADO AO ESTOQUE COM SUCESSO!
        -------------------------------------
        PRODUTO: {nome_insumo.get()}
        VALOR: {preco_produto.get()}R$
        QUANTIDADE: {qtde_insumo.get()}und
        PESO Kg: {kg_insumo.get()}kg
        -------------------------------------
                    PET CENTER
        '''

    # Delete the contents of the tkinter Entry widgets
    nome_insumo.delete(0, END)
    preco_produto.delete(0, END)
    qtde_insumo.delete(0, END)
    kg_insumo.delete(0, END)

    # Write the message to the tkinter Text widget
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", mensagem)


# ==========================================================================
# ------------- FUNCTION DE VISUALIZAR PLANILHA---------------------------
def visualizar_estoque():
    # Criar nova janela para exibir os dados
    janela = Toplevel()
    janela.title("PLANILHA DO ESTOQUE")
    janela.geometry("600x400")
    janela.iconbitmap("icone.ico")
    janela.configure(bg = "#0CC0D0")
    # Criar uma árvore para exibir os dados
    tree = ttk.Treeview(janela)
    
    # Configurar as colunas da árvore
    tree["columns"] = ("preco", "quantidade", "peso", "vendas")
    tree.column("#0", width=200, minwidth=200)
    tree.column("preco", width=100, minwidth=100)
    tree.column("quantidade", width=100, minwidth=100)
    tree.column("peso", width=100, minwidth=100)
    tree.column("vendas", width=100, minwidth=100)
    tree.heading("#0", text="Produto", anchor=W)
    tree.heading("preco", text="Preço", anchor=W)
    tree.heading("quantidade", text="Quantidade", anchor=W)
    tree.heading("peso", text="Peso", anchor=W)
    tree.heading("vendas", text="Vendas", anchor=W)
    
    # Recuperar os dados do banco de dados
    cursor = conn.execute("SELECT * FROM produtos")
    for row in cursor:
        tree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))
        
    # Adicionar a árvore à janela
    tree.pack()

# ===============================================================================
# ----------------------FUNCTION DE SOMAR VENDAS-----------------------------
def somar_vendas():
    # Execute a SELECT query to sum the sales column
    cursor.execute("SELECT SUM(vendas) FROM produtos")
    resultado = cursor.fetchone()
    
    # Retrieve the total sales amount
    total_vendas = resultado[0]
    
    # Display the total sales amount in the text box
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f'''
    ====================================
    TOTAL DE VENDAS
    -------------------------------------
    R$: {total_vendas:.2f}
    -------------------------------------
                PET CENTER
    ''')
# =========================================================================
# --------------------FUNCTION DE VERIFICAR QUANTIDADE MINIMA------------------
def produtos_abaixo_quantidade_minima():
    cursor = conn.cursor()
    cursor.execute("SELECT produto, quantidade FROM produtos WHERE quantidade < 3")
    resultado = cursor.fetchall()
    if resultado:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", '''
    -----------------ATENÇÃO!!-----------------------
        PRODUTOS QUE ESTÃO ABAIXO
        DO ESTOQUE MINIMO
    ======================================
        ABAIXO DA QUANTIDADE MINIMA:\n
        ''')
        for produto in resultado:
            caixa_texto.insert(END, f'''{produto[0]}: {produto[1]} unidades\n        ''')
    else:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", '''
        Todos os produtos estão acima
        da quantidade mínima.           
        ''')
# ==============================================================================
# --------------------FUNCTION DE REDEFINIR TABELA DE VENDAS-------------------
def resetar_vendas():
    # Confirmação do usuário
    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja resetar as vendas?")

    # Se o usuário confirmar, redefine as vendas
    if confirmacao:
        conn.execute("UPDATE produtos SET vendas = 0")
        conn.commit()

        # Atualiza a caixa de texto com a mensagem de sucesso
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", f'''
        =====================================
        VENDAS REDEFINIDAS COM SUCESSO!
        -------------------------------------
                    PET CENTER
        ''')


#===============================================================================
#------------------------CRIANDO JANELA DE EXIBIÇÃO-----------------------------
#----------------ciração da janela----------------------
#configurando a janela
window = Tk()
window.title('CONTROLE DE ESTOQUE')
window.iconbitmap("icone.ico")
window.geometry("1050x550")
window.configure(bg = "#0CC0D0")
# window.attributes("-alpha",0.9)
#-------------------------------------------------------

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 550,
    width = 1050,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    524.5, 275.1,
    image=background_img)

#----------botão de deletar produto-----------
botão_deletar = Button(text="DELETAR PRODUTO", width=20, height=2, bg="#ed0505", fg="white",command=deletar_insumo)
botão_deletar.place(x=475, y=125)

#----------botão de consumir produto----------
botão_consumir = Button(text="VENDER PRODUTO", width=20, height=2, bg="#075bb0", fg="white",command=registrar_venda)
botão_consumir.place(x=475, y=175)

#-----------botão de adicinar produto----------
botão_adicionar = Button(text="ADICIONAR PRODUTO", width=20, height=2, bg="#149406", fg="white",command=adicionar_insumo)
botão_adicionar.place(x=475, y=225)
#===================INPUTS==========================

caixa_texto = Text(window, font=('Arial',12,'italic'))
caixa_texto.place(x = 650, y = 62,width = 380,height = 380)


#------input do nome do insumo------
nome_insumo = ttk.Entry(window)
nome_insumo.place(x = 170, y = 130,width = 280,height = 31)

#------input do peso do produto-----
kg_insumo = ttk.Entry(window)
kg_insumo.place(x = 170, y = 180, width = 280,height = 31)

#-------input da quantidade do produto------
qtde_insumo = ttk.Entry(window)
qtde_insumo.place(x = 170, y = 230, width = 280,height = 31)

#-------input de preço---------

preco_produto = ttk.Entry(window)
preco_produto.place(x = 170, y = 280, width = 280,height = 31)

#botão de verificar estoque
verificar_produtos = Button(text = "VERFICAR RAÇÕES DO ESTOQUE", width=30, bg="#1d474a", fg="white",command=produtos_abaixo_quantidade_minima)
verificar_produtos.place(x=735, y=447)

#botão de bisualizar planilha
visualizar_planilha = Button(text = "VISUALIZAR PLANILHA DO ESTOQUE", width=30, bg='#1d474a',fg="white", command=visualizar_estoque)
visualizar_planilha.place(x=735, y=478)

#botão de somar as vendas
somar_vendas_do_estoque = Button(text = "SOMAR VENDAS", width=30, bg='#1d474a',fg="white", command=somar_vendas)
somar_vendas_do_estoque .place(x=735, y=509)

#botão de redefinir coluna de vendas
#botão de somar as vendas
redefinir_vendas = Button(text = "REDEFINIR COLUNA VENDAS", width=30, bg='#1d474a',fg="white", command=resetar_vendas)
redefinir_vendas .place(x=735, y=25)

#--------adicionando insumos-------
#insumo de adicionar produto
produtolabel = Label(text="Produto:",font=("century gothic",19),bg='#0CC0D0',fg="white")
produtolabel.place(x=30,y=130)
#insumo de kilos
kilolabel = Label(text="Peso Kg:",font=("century gothic",19),bg='#0CC0D0',fg="white")
kilolabel.place(x=30,y=180)
#insumo da quantidade
quatidadelabel = Label(text="Quantidade:",font=("century gothic",19),bg='#0CC0D0',fg="white")
quatidadelabel.place(x=30,y=230)
#insumo preco
preco_label = Label(text="Preço:",font=("century gothic",19),bg='#0CC0D0',fg="white")
preco_label.place(x=30,y=280)

#==============FECHANDO A JANELA E FECHANDO A CONEXÃO COM O BANCO DE DADOS==============
window.resizable(False, False)
window.mainloop()

conn.close()