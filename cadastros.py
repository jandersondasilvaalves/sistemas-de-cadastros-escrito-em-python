from tkinter import *
from tkinter import ttk
from datetime import date
import sqlite3
from PIL import Image, ImageTk
import select
from tkcalendar import DateEntry

root = Tk()

class backend_funcoes():
    def conecta_bd(self):
        self.conn = sqlite3.connect('Cadastros.bd')
        self.cursor = self.conn.cursor(); print("Conectado com banco de dados")
    def tabela_do_banco_de_dados(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cadastros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cadastro TEXT NOT NULL,
            telefone INTEGER(20),
            endereco CHAR(40),
            data_de_nascimento DATE,
            rg INTEGER(20),
            cpf INTEGER(20)
            );
 
        """)
        self.conn.commit(); print('criado banco de dados')
        self.conn.close()
    def limpa_tela(self):
        self.e_id.delete(0, END)
        self.e_nome.delete(0, END)
        self.e_telefone.delete(0, END)
        self.e_endereco.delete(0, END)
        self.e_data.delete(0, END)
        self.e_rg.delete(0, END)
        self.e_cpf.delete(0, END)

    def variaveis(self):
        self.id = self.e_id.get()
        self.nome = self.e_nome.get()
        self.cell = self.e_telefone.get()
        self.endereco = self.e_endereco.get()
        self.data = self.e_data.get()
        self.rg = self.e_rg.get()
        self.cpf = self.e_cpf.get()
    def inserir(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO cadastros(nome_cadastro, telefone, endereco, data_de_nascimento, rg, cpf) VALUES(?,?,?,?,?,?)""",
                            ( self.nome, self.cell, self.endereco, self.data, self.rg ,self.cpf))
        self.conn.commit()
        self.conn.close()
        self.select_menu()
        self.limpa_tela()
    def select_menu(self):
        self.lista.delete(*self.lista.get_children())
        self.conecta_bd()
        lis = self.cursor.execute("""SELECT  id, nome_cadastro, telefone, endereco, data_de_nascimento, rg, cpf
        FROM cadastros ORDER BY nome_cadastro ASC;""")
        for i in lis:
            self.lista.insert("", END, values=i)
        self.conn.close()
    def Onecliclk(self, event):#essa função ira trazer as variaveis para a label
        self.limpa_tela()
        self.lista.selection()#lista que fiz la embaixo

        for n in self.lista.selection():#função que intentifica as colunas
            col1, col2, col3, col4, col5, col6, col7 = self.lista.item(n,'values')
            self.e_id.insert(END, col1)
            self.e_nome.insert(END, col2)
            self.e_telefone.insert(END, col3)
            self.e_endereco.insert(END, col4)
            self.e_data.insert(END, col5)
            self.e_rg.insert(END, col6)
            self.e_cpf.insert(END, col7)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM cadastros WHERE id = ?""", (self.id,))
        self.conn.commit()
        self.conn.close()
        self.limpa_tela()
        self.select_menu()
    def autaliza_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE cadastros SET nome_cadastro = ?, telefone = ?, endereco = ?, data_de_nascimento = ?, rg = ?, cpf = ?
        WHERE id = ?""", (self.nome, self.cell,self.endereco, self.data, self.rg, self.cpf, self.id))
        self.conn.commit()
        self.conn.close()
        self.select_menu()
        self.limpa_tela()

class Aplicar(backend_funcoes):
    def __init__(self):
        self.janela = root
        self.tela_root()
        self.abas_do_frame()
        self.labels_entrys()
        self.tabela_do_banco_de_dados()
        self.botoes_widgets()
        self.treeviwer()
        self.select_menu()


        root.mainloop()


    def tela_root(self):
        #---------------------Renderização da tela-----------------------------
        self.janela.geometry('900x620')
        self.janela.title('Cadastro de Funcionarios')
        self.janela.resizable(True, True)
        self.janela.configure(background = '#e9edf5')
        self.janela.minsize(width=512, height=256)

        #---------------------Criação dos frames-------------------------------
        self.frame1 = Frame(self.janela, bd= 4, bg= '#feffff',
                             relief=FLAT)
        self.frame1.place(relx = 0.01, rely = 0.01,relwidth=0.98, relheight=0.5)

        self.frame2 = Frame(self.janela, bd = 4, bg = '#feffff', relief = FLAT)
        self.frame2.place(relx = 0.01, rely = 0.52, relwidth = 0.98, relheight = 0.47)
    def abas_do_frame(self):
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background='#feffff')
        self.aba2.configure(background='#feffff')

        self.abas.add(self.aba1, text='Registrar funcionarios')
        self.abas.add(self.aba2, text='Em teste...')

        self.abas.place(relx = 0, rely= 0, relwidth =1, relheight=1)
    def labels_entrys(self):
        self.e_id = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_id.place(relx=0.35, rely=0.45, relwidth=0.08, relheight=0.08)


        self.l_nome = Label(self.aba1, text ='Nome:',height=1,anchor=NW, font=('Ivy 10 bold'),
                            bg='#feffff', fg='#263238')
        self.l_nome.place(relx = 0.02, rely =0.05, relwidth=0.1, relheight=0.15)

        self.e_nome = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_nome.place(relx = 0.025, rely =0.15, relwidth = 0.3, relheight=0.08)

        self.l_telefone = Label(self.aba1, text = 'Telefone/Celular:',height=1,anchor=NW, font=('Ivy 10 bold'),
                                bg='#feffff', fg= '#263238')
        self.l_telefone.place(relx=0.02, rely=0.25, relwidth=0.3, relheight=0.15)

        self.e_telefone = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_telefone.place(relx=0.025, rely=0.35, relwidth=0.3, relheight=0.08)

        self.l_data = Label(self.aba1, text = 'Data de nascimeto:',height=1,anchor=NW, font=('Ivy 10 bold'),
                                bg='#feffff', fg= '#263238')
        self.l_data.place(relx=0.02, rely=0.45, relwidth=0.3, relheight=0.15)

        self.e_data = DateEntry(self.aba1, width=12,background='darkblue', boardwidth=2,year=2024)
        self.e_data.place(relx=0.025, rely=0.55, relwidth=0.1, relheight=0.08)

        self.l_endereco = Label(self.aba1, text = 'Endereço', height=1, anchor=NW, font=('Ivy 10 bold'),
                                bg = '#feffff', fg='#263238')
        self.l_endereco.place(relx=0.02, rely=0.65, relwidth=0.1, relheight=0.15)

        self.e_endereco = Entry(self.aba1, width=30,justify='left',relief=SOLID)
        self.e_endereco.place(relx=0.025, rely=0.75, relwidth=0.3, relheight=0.08)

        self.l_rg = Label(self.aba1, text= 'RG', height=1, anchor=NW, font=('Ivy 10 bold'),
                          bg = '#feffff', fg='#263238')
        self.l_rg.place(relx = 0.35, rely =0.05, relwidth=0.1, relheight=0.15)

        self.e_rg = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_rg.place(relx= 0.35, rely=0.15, relwidth=0.3, relheight=0.08)

        self.l_cpf = Label(self.aba1, text='CPF', height=1, anchor=NW, font=('Ivy 10 bold'),
                          bg='#feffff', fg='#263238')
        self.l_cpf.place(relx=0.35, rely=0.25, relwidth=0.1, relheight=0.15)

        self.e_cpf = Entry(self.aba1, width=30, justify='left', relief=SOLID)
        self.e_cpf.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.08)
    def botoes_widgets(self):
        self.ima_add = Image.open('add.png')
        self.ima_add = self.ima_add.resize((20, 20))
        self.ima_add = ImageTk.PhotoImage(self.ima_add)

        self.bt_Inserir = Button(self.aba1, image= self.ima_add, width=95, text=' Adicionar  ', compound=LEFT, overrelief=RIDGE,
                                 bg='#feffff', fg='#2e2d2b',  font=('Iv 8'), command=self.inserir)
        self.bt_Inserir.place(relx=0.45, rely=0.55, relwidth=0.1, relheight=0.1)

        self.ima_atu = Image.open('atu.png')
        self.ima_atu = self.ima_atu.resize((20, 20))
        self.ima_atu = ImageTk.PhotoImage(self.ima_atu)

        self.bt_atualizar = Button(self.aba1, image=self.ima_atu,width=95, text=' Atualizar    ', compound=LEFT, overrelief=RIDGE,
                                   bg='#feffff', fg='#2e2d2b',  font=('Iv 8'), command=self.autaliza_cliente)
        self.bt_atualizar.place(relx=0.55, rely=0.55, relwidth=0.1, relheight=0.1)

        self.ima_lim = Image.open('limpar.png')
        self.ima_lim  = self.ima_lim .resize((20, 20))
        self.ima_lim  = ImageTk.PhotoImage(self.ima_lim )


        self.bt_limpar = Button(self.aba1,  image= self.ima_lim ,width=95, text=' Limpar       ', compound=LEFT, overrelief=RIDGE,
                                bg='#feffff', fg='#2e2d2b',  font=('Iv 8'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.45, rely=0.65, relwidth=0.1, relheight=0.1)

        self.ima_del = Image.open('del.png')
        self.ima_del = self.ima_del.resize((20, 20))
        self.ima_del = ImageTk.PhotoImage(self.ima_del)

        self.bt_apagar = Button(self.aba1, image=self.ima_del ,width=95, text=' Apagar      ', compound=LEFT, overrelief=RIDGE,
                                bg='#feffff', fg='#2e2d2b',  font=('Iv 8'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.55, rely=0.65, relwidth=0.1, relheight=0.1)
    def treeviwer(self):
        self.lista= ttk.Treeview(self.frame2,height=3, columns=('col1', 'col2', 'col3','col4','col5','col6','col7'))
        self.lista.heading('#0', text='')
        self.lista.heading('#1', text='Codigo')
        self.lista.heading('#2', text='Nome')
        self.lista.heading('#3', text='Telefone/Celular')
        self.lista.heading('#4', text='Endereço')
        self.lista.heading('#5', text='Data de Nascimento')
        self.lista.heading('#6', text='RG')
        self.lista.heading('#7', text='CPF')

        self.lista.column('#0', width=1)
        self.lista.column('#1', width=1)
        self.lista.column('#2', width=50)
        self.lista.column('#3', width=50)
        self.lista.column('#4', width=150)
        self.lista.column('#5', width=50)
        self.lista.column('#6', width=50)
        self.lista.column('#7', width=50)

        self.lista.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.95)

        self.scroolbar = Scrollbar(self.frame2, orient='vertical')
        self.lista.configure(yscroll=self.scroolbar.set)
        self.scroolbar.place(relx=0.97, rely=0.015, relwidth=0.03, relheight=0.95)

        self.lista.bind("<Double-1>",self.Onecliclk)#função que fiz sendo mencionada aqui e 
        #o comando <Double-1> unsando bind




Aplicar()

