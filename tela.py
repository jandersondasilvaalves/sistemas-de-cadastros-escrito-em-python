#from cgitb import text
from tkinter import *
import awesometkinter as atk
from tkinter import ttk
#from tkinter import tix
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import  SimpleDocTemplate, Image
import webbrowser
from PIL import ImageTk, Image
import base64
from tkinter import messagebox



import select

janela = Tk()

class validadores():
    def validate_entry2(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100
    def validanome(self, number):
        if number == '': return True
        try:
            value1 = int(number)
        except ValueError:
            return False
        return 0 <= value1 <= 5000000000000000


class funcs():
    def limpa_tela(self):
        self.e_codigo.delete(0, END)
        self.e_telefone.delete(0, END)
        self.e_nome.delete(0, END)
        self.e_cidade.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("Clientes.bd")
        self.cursor= self.conn.cursor(); print("Conectando ao banco de dados")
    def desconect(self):
        self.conn.close()
    def montaTabelas(self):
        self.conecta_bd()
        #Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
            
        """)
        self.conn.commit(); print('Banco de dad os criado')
        self.desconect()
    def add_cliente(self):
        self.variaveis()
        if self.e_nome.get() == '':
            masg = 'Para cadastrar um novo cliiente, é necessario inserir o nome'
            messagebox.showinfo('Cadastro de clientes - Aviso!!!', masg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
            self.conn.commit()
            self.desconect()
            self.select_lista()
            self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone, cidade FROM clientes
        ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconect()
    def Ondobleclick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.e_codigo.insert(END, col1)
            self.e_nome.insert(END, col2)
            self.e_telefone.insert(END, col3)
            self.e_cidade.insert(END, col4)
    def variaveis(self):
        self.codigo = self.e_codigo.get()
        self.nome = self.e_nome.get()
        self.fone = self.e_telefone.get()
        self.cidade = self.e_cidade.get()
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.codigo))
        self.conn.commit()
        self.desconect()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ?""",(self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconect()
        self.select_lista()
        self.limpa_tela()
    #-----------------------------Funções de pdf-----------------------------
    def printCliente(self):
        webbrowser.open('Cliente.pdf')
    def geraRelaCliente(self): #fazer um pdf
        self.c = canvas.Canvas('Cliente.pdf')

        self.codigoRel = self.e_codigo.get()
        self.nomeRel = self.e_nome.get()
        self.foneRel = self.e_telefone.get()
        self.cidadeRel = self.e_cidade.get()

        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont('Helvetica-Bold', 12)
        self.c.drawString(50,700, 'Codigo:' )
        self.c.drawString(50, 670, 'Codigo:' )
        self.c.drawString(50, 630, 'Codigo:')
        self.c.drawString(50, 600, 'Codigo:')

        self.c.setFont('Helvetica', 12)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670,  self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20, 520, 550, 300, fill = False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente() #Pdf
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.e_nome.insert(END, '%')
        nome = self.e_nome.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
    #def imagens_base64(self):
        #self.btnovo_base=''

class aplication(funcs, validadores):

    def __init__(self):
        self.janela = janela
        self.validaentrada()
        self.tela()
        self.frames_da_tela()
        self.funçoes_do_frame1()
        self.frame2_widgets()
        self.montaTabelas()
        self.Menus()
        self.select_lista()



        janela.mainloop()

    def tela(self):
        self.janela.geometry("700x500")
        self.janela.title('Cadastro de Clientes')
        #self.janela.resizable('False','False')
        self.janela.resizable('True', 'True')#permitir ou não o aumento do tamanho da tela
        self.janela.configure(background= '#2e2d2b')
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=480, height=220)
    def frames_da_tela(self):
        self.frame1 = Frame(self.janela, bd=4, bg= '#dfe3ee',
                            highlightbackground= '#759fe6',highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame02 = Frame(self.janela, bd=4, bg= '#dfe3ee',
                            highlightbackground= '#759fe6',highlightthickness=3)
        self.frame02.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def funçoes_do_frame1(self):
        #------------------Criando Abas--------------------------------------------------
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background= '#dfe3ee')
        self.aba2.configure(background= '#dfe3ee')

        self.abas.add(self.aba1, text= 'Aba 1')
        self.abas.add(self.aba2, text= 'Aba 2')

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)


        #------------------Colocando barra de progresso-----------------------------------
        bar = atk.RadialProgressbar3d(self.aba1, fg='cyan', bg=atk.DEFAULT_COLOR, size=50)
        bar.place(relx =0.7, rely=0.35)
        bar.start()

        #------------------Usando comando canvas para edição de butão---------------------
        self.canvas_bt1 = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground='gray',
            highlightthickness=3)
        self.canvas_bt1.place(relx=0.19, rely=0.08, relwidth = 0.22, relheight=0.19)

        self.canvas_bt2 = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground='gray',
                                highlightthickness=3)
        self.canvas_bt2.place(relx=0.59, rely=0.08, relwidth=0.32, relheight=0.19)

        #------------------criando butões----------------------------------------------------------
        self.bt_limpar = Button( self.aba1,width=95,text='Limpar',compound=LEFT, overrelief=RIDGE,
                                 activebackground='#108ecb', activeforeground="white",
                                 bg='#107db2', fg='#feffff', bd=4, command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2,rely=0.1, relwidth=0.1,relheight=0.15)
        atk.tooltip(self.bt_limpar, 'Limpar os campos preenchidos')

        self.bt_apagar = Button(self.aba1, width=95, text='Apagar', compound=LEFT, overrelief=RIDGE,
                                bg='#107db2', fg='#feffff', bd=4, command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_apagar, 'Apagar item da lista')

        self.bt_buscar = Button(self.aba1, width=95, text='Buscar', compound=LEFT, overrelief=RIDGE,
                                bg='#107db2', fg='#feffff', bd=4, command= self.busca_cliente )
        self.bt_buscar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_buscar,'Buscar item da lista')

        #criando variavel para botão 'novo' para colocar imagem
        '''self.imgnovo = PhotoImage(file = "botaonovo.png")
        self.imgnovo = self.imgnovo.subsample(3, 5)
        self.style = ttk.Style()
        self.style.configure("BW.TButton", relwidth=1, relheight=1, foreground= "gray",
                             borderwidth=0, bordercolor= "grey", background= '#dfe3ee',
                             image = self.imgnovo)'''

        self.bt_novo = Button(self.aba1,width=95, text='Novo', compound=LEFT, overrelief=RIDGE,
                                bg='#107db2', fg='#feffff', bd=4, command=self.add_cliente)
        self.bt_novo.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_novo, 'Adicionar item a lista')

        #self.bt_novo.configure(image=self.imgnovo)
        self.bt_alterar = Button(self.aba1, width=95, text='Alterar', compound=LEFT, overrelief=RIDGE,
                                bg='#107db2', fg='#feffff', bd=4, command=self.altera_cliente)
        self.bt_alterar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_alterar, 'Alterar/Atualizar item da lista')

        #self.balao_buscar = tix.Balloon(self.frame1)
        # pyinstaller --onefile --noconsole --windowed  tela.pyself.balao_buscar.bind_widget(self.balao_buscar)


        #------------------------------Fim da criação de botões-------------------------------

        #------------------------------Criando labels e Entrys do codigo-----------------------------------------
        self.label1 = Label(self.aba1, text='Código',height=1, anchor=NW, font=('Ivy 10 bold'), bg= '#dfe3ee',
                            fg = 'blue')
        self.label1.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.15)

        self.e_codigo = Entry(self.aba1,validate = 'key', validatecommand = self.vcmd2, width=30, justify='left', relief=SOLID)
        self.e_codigo.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.1)

        # ------------------------------Criando labels e Entrys do nome-----------------------------------------
        self.l_nome = Label(self.aba1, text='Nome', height=1, anchor=NW, font=('Ivy 10 bold'), bg='#dfe3ee',
                            fg = 'blue')
        self.l_nome.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.15)

        self.e_nome = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_nome.place(relx=0.05, rely=0.45, relwidth=0.4, relheight=0.1)
        #-------------------------------Label e Entry do numero de telefone--------------------------------
        self.l_telefone = Label(self.aba1, text='Telefone', height=1, anchor=NW, font=('Ivy 10 bold'), bg='#dfe3ee',
                                fg = 'blue')
        self.l_telefone.place(relx=0.05, rely=0.6, relwidth=0.1, relheight=0.15)

        self.e_telefone = Entry(self.aba1, validate= 'key', validatecommand=self.vcmd3,width=30, justify='left', relief=SOLID)
        self.e_telefone.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.1)
        #-------------------------------Label e Entry da Cidade-------------------------------------------
        self.l_cidade = Label(self.aba1, text='Cidade', height=1, anchor=NW, font=('Ivy 10 bold'), bg='#dfe3ee',
                              fg = 'blue')
        self.l_cidade.place(relx=0.5, rely=0.6, relwidth=0.1, relheight=0.15)

        self.e_cidade = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_cidade.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.1)

        #-------------------------------------Drop down button--------------------------------------
        self.tipvar = StringVar()
        self.tipv = ("Solteiro(a)", 'Casado(a)', 'Divorciado(a)', 'Viuvo(a)')
        self.tipvar.set('Solteiro(a)')
        self.popupMenu = OptionMenu(self.aba2, self.tipvar, *self.tipv)
        self.popupMenu.place(relx = 0.1, rely = 0.1, relwidth = 0.2, relheight = 0.2)
        self.estado_civil = self.tipvar.get()

    def frame2_widgets(self):
        #-----------------------------Criação da lista a amostra no sistema-------------------------
        self.listaCli = ttk.Treeview(self.frame02, height=3, columns=('col1', 'col2', 'col3','col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Codigo')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)

        self.listaCli.place(relx=0.01, rely=0.01,  relwidth= 0.95,relheight=0.85)
        #------------------------------Criação do scroll--------------------------------------
        self.scroollista = Scrollbar(self.frame02, orient='vertical')
        self.listaCli.configure(yscroll=self.scroollista.set)
        self.scroollista.place(relx=0.96, rely=0.015, relwidth=0.04, relheight=0.85)
        self.scroollista2 = Scrollbar(self.frame02, orient='horizontal')
        self.scroollista2.place(relx=0.01, rely=0.88, relwidth=0.95, relheight=0.1)
        self.listaCli.configure(xscroll=self.scroollista2.set)
        self.listaCli.bind("<Double-1>", self.Ondobleclick)
    def Menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label = "Abrir nova janela", menu = filemenu)
        menubar.add_cascade(label= "Opções" , menu = filemenu2)

        filemenu.add_command(label= "Abrir", command= self.janela_2)
        #filemenu2.add_command(label = "Limpa Cliente", command= self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelaCliente)
    def janela_2(self):
        self.janela2 = Toplevel()
        self.janela2.title('Janela 2 de teste')
        self.janela2.configure(background= 'lightblue')
        self.janela2.geometry('400x200')
        self.janela2.resizable(False, False)
        self.janela2.transient(self.janela)
        self.janela2.focus_force()
        self.janela2.grab_set()
    def validaentrada(self):
        self.vcmd2 = (self.janela.register(self.validate_entry2), "%P")
        self.vcmd3 = (self.janela.register(self.validanome), "%P")





aplication()