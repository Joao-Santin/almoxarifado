from kivy.uix.screenmanager import ScreenManager, Screen  # , SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem, TwoLineListItem, OneLineListItem, MDList  # , ThreeLineListItem
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from back.mongodb import Usuarios, Itens, Historico
from back.email_automatico import envio_email
from objetos.funcionario import Funcionario
from objetos.item import Item
# esse aqui será usado no futuro
# import asyncio

global funcionario_selecionado
funcionario_selecionado = ""

def pegar_telas():
    todas_telas = ScreenManager().screens
    return todas_telas

def apagar_text_inputs(screen):
    print(screen)
    pass
    

class SelecaoFuncionarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def selecionado(self, botao):
        global funcionario_selecionado
        funcionario_selecionado = botao.text
        self.manager.current = "main_screen"

    def on_pre_enter(self, *args):
        self.ids.container_selecao.clear_widgets()
        global funcionario_selecionado
        funcionario_selecionado = ""
        for funcionario in Usuarios.read():
            self.ids.container_selecao.add_widget\
                (OneLineListItem(text=funcionario['nome'],
                                on_release=lambda x=self: self.selecionado(x)))

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipos = ["retirar/adicionar", "modificar", "criar"]
        self.categorias = ['geral', 'epi', 'limpeza', 'manutenção', 'papelaria', 'produção', 'montagem', 'cozinha']
        self.dicionario_selecionado = {
      "nome": "",
      "quantidade": "",
      "limite": "",
      "localizacao": "",
      "funcionario_criou": "",
      "categoria": ""
    }
        self.tipo_selecionadoo = self.tipos[0]
        self.item_selecionado = ""
        self.quantidade_selecionada = ""
        self.localizacao = ""
        self.limite = ""
        self.categoria = ""
        self.categoria_lista = self.categorias[0]
        self.item_criando = {
            "nome": "",
            "quantidade": "",
            "limite": "",
            "localizacao": "",
            "funcionario_criou": "",
            "categoria": ""
      }
        
    def on_pre_enter(self, *args):
        self.refresh()

    def switch_to_historico_screen(self):
        self.manager.current = "historico_screen"

    def switch_to_compras_screen(self):
        self.manager.current = "compras_screen"

    def retirada_de_item(self):
        for widget in self.ids.retirada.children[:]:
            if isinstance(widget, TextInput):
                self.quantidade_retirada = widget.text
        if self.quantidade_retirada != "":
            self.dicionario_selecionado['quantidade'] =str(int(self.dicionario_selecionado['quantidade']) - int(self.quantidade_retirada))
            Itens.update(self.dicionario_selecionado)
            self.refresh()
        else:
            print("insira um numeor para tirar ai")

    def modificar_item(self):
        dicionario = self.selecionar_item_novo()
        dicionario['_id'] = self.dicionario_selecionado['_id']
        if dicionario['nome'] != "":
            Itens.update(dicionario)
            self.dicionario_selecionado = dicionario
        else:
            print("selecione um item")
        
        self.refresh()

    def deletar_item(self):
        print(self.dicionario_selecionado)
        Itens.delete(self.dicionario_selecionado)
        self.refresh()

    def selecionar_item_novo(self):
        informacoes = []
        informacoes.clear()
        layouts = [self.ids.box_layout_nome, 
                   self.ids.box_layout_quantidade, 
                   self.ids.box_layout_limite, 
                   self.ids.box_layout_localizacao]
        
        for layout in layouts:    
            for widget in layout.children[:]:  
                if isinstance(widget, TextInput):
                    informacoes.append(widget.text)
        layout = self.ids.box_layout_funcionario
        for widget in layout.children[:]:
            if isinstance(widget, Button):
                informacoes.append(widget.text)
        layout = self.ids.retirada
        for widget in layout.children[:]:
            if isinstance(widget, TextInput):
                informacoes.append(widget.text)
        layout = self.ids.retirada      
        for widget in layout.children[:]:
            if isinstance(widget, Button):
                informacoes.append(widget.text)        
        item = Item(informacoes[0], 
                    informacoes[1], 
                    informacoes[2], 
                    informacoes[3], 
                    informacoes[4],
                    informacoes[5],
                    )
        self.quantidade_retirada = informacoes[5]
        item_json = item.json()
        return item_json
    
    def adicionar_item(self):
        self.item_criando = {
            "nome": "",
            "quantidade": "",
            "limite": "",
            "localizacao": "",
            "funcionario_criou": "",
            "categoria": ""
      }
        item = self.selecionar_item_novo()
        if item['nome'] != '':
            Itens.create(item)
            Historico.create(item)
        self.refresh()

    def troca_tipo(self):
        try:
            self.tipo_selecionadoo = self.tipos[self.tipos.index(self.tipo_selecionadoo)+1]
        except IndexError:
            self.tipo_selecionadoo = self.tipos[0]
        self.categoria = ""
        self.ids.botao_troca.text = self.tipo_selecionadoo
        self.refresh()

    def switch_to_selecionar_funcionario(self):
        if self.tipo_selecionadoo == "criar":
            self.item_criando = self.selecionar_item_novo()
        self.manager.current = "selecionar_funcionario_screen"

    def funcao_botao(self):
        self.categoria = ""
        self.refresh()

    def funcao_botoes(self, botao):
        self.categoria = botao.text
        self.ids.retirada.clear_widgets()
        self.ids.retirada.add_widget(Label(text="Categoria:"))
        self.ids.retirada.add_widget\
            (Button(text=self.categoria, on_release=lambda x=self: self.funcao_botao()))
        pass

    def selecionar_item(self, item):
        self.item_selecionado = item.text
        for itemm in Itens.read():
            if self.item_selecionado == itemm['nome']:
                self.dicionario_selecionado = itemm
        self.refresh()

    def refresh(self):
        self.ids.container_itens.clear_widgets()
        self.ids.botao_categorias.text = self.categoria_lista
        lista_objetos = Itens.read()
        filtro = self.ids.text_input_search.text.lower()
        # aqui vou ter que colocar um for para criar todos os itens da db
        for item in lista_objetos:
            if item['nome'].find(filtro) >= 0 or filtro == "":
                if self.categoria_lista != 'geral':
                    if item['categoria'] == self.categoria_lista:
                        self.ids.container_itens.add_widget\
                            (ThreeLineListItem(text=item['nome'],\
                                            on_release=lambda x=self: self.selecionar_item(x),
                                            secondary_text='quantidade: '+item['quantidade'],
                                            tertiary_text='localização: '+item['localizacao']))
                else:
                    self.ids.container_itens.add_widget\
                            (ThreeLineListItem(text=item['nome'],\
                                            on_release=lambda x=self: self.selecionar_item(x),
                                            secondary_text='quantidade: '+item['quantidade'],
                                            tertiary_text='localização: '+item['localizacao']))
            
        global funcionario_selecionado
        if funcionario_selecionado != "":
                self.ids.botao_selecionar_funcionario.text = funcionario_selecionado
        else:
            self.ids.botao_selecionar_funcionario.text = "Selecionar funcionário!"

        
        self.ids.retirada.clear_widgets()
        self.ids.botoes.clear_widgets()
        self.ids.box_layout_nome.clear_widgets()
        self.ids.box_layout_nome.add_widget(Label(text="Nome item:"))
        self.ids.box_layout_quantidade.clear_widgets()
        self.ids.box_layout_quantidade.add_widget(Label(text="Quantidade:"))
        self.ids.box_layout_limite.clear_widgets()
        self.ids.box_layout_limite.add_widget(Label(text="Limite:"))
        self.ids.box_layout_localizacao.clear_widgets()
        self.ids.box_layout_localizacao.add_widget(Label(text="Localização:"))
        self.ids.retirada.clear_widgets()
        
        if self.tipo_selecionadoo == "retirar/adicionar":
            self.ids.box_layout_nome.add_widget(Label(text=self.dicionario_selecionado['nome']))
            self.ids.box_layout_quantidade.add_widget(Label(text=self.dicionario_selecionado['quantidade']))
            self.ids.box_layout_limite.add_widget(Label(text=self.dicionario_selecionado['limite']))
            self.ids.box_layout_localizacao.add_widget(Label(text=self.dicionario_selecionado['localizacao']))
            self.ids.retirada.add_widget(Label(text="Retirar:"))
            self.ids.retirada.add_widget(TextInput())
            self.ids.botoes.add_widget(Button(text="Retirar/adicionar",
                                            background_color="green",
                                            on_release=lambda x=None: self.retirada_de_item()))
            

        elif self.tipo_selecionadoo == "modificar":
            self.ids.box_layout_nome.add_widget(TextInput(text=self.dicionario_selecionado['nome']))
            self.ids.box_layout_quantidade.add_widget(TextInput(text=self.dicionario_selecionado['quantidade']))
            self.ids.box_layout_limite.add_widget(TextInput(text=self.dicionario_selecionado['limite']))
            self.ids.box_layout_localizacao.add_widget(TextInput(text=self.dicionario_selecionado['localizacao']))
            self.ids.botoes.add_widget(Button(text="Deletar",
                                            background_color="red",
                                            on_release=lambda x=self: self.deletar_item()))
            self.ids.botoes.add_widget(Button(text="Modificar",
                                            background_color="green",
                                            on_release=lambda x=self: self.modificar_item()))
            self.ids.retirada.add_widget(Label(text="Categoria:"))
            if self.categoria == "":
                for item in self.categorias:
                    if item != 'geral':
                        self.ids.retirada.add_widget(Button(text=item, on_release=lambda x=self: self.funcao_botoes(x)))
            else:
                self.ids.retirada.add_widget(Button(text=self.categoria, on_release=lambda x=self: self.funcao_botao()))
            
        elif self.tipo_selecionadoo == "criar":
            if self.item_criando:
                self.ids.box_layout_nome.add_widget(TextInput(text=self.item_criando['nome']))
                self.ids.box_layout_quantidade.add_widget(TextInput(text=self.item_criando['quantidade']))
                self.ids.box_layout_limite.add_widget(TextInput(text=self.item_criando['limite']))
                self.ids.box_layout_localizacao.add_widget(TextInput(text=self.item_criando['localizacao']))
            self.ids.botoes.add_widget(Button(text="Criar",
                                                background_color="green",
                                                on_release=lambda x=self: self.adicionar_item()
                                                ))
            self.ids.retirada.add_widget(Label(text="Categoria:"))
            if self.categoria == "":
                for item in self.categorias:
                    if item != 'geral':
                        self.ids.retirada.add_widget(Button(text=item, on_release=lambda x=self: self.funcao_botoes(x)))
            else:
                self.ids.retirada.add_widget(Button(text=self.categoria, on_release=lambda x=self: self.funcao_botao()))
            

    def switch_to_adicionar_funcionario(self):
        self.manager.current = "adicionar_funcionario_screen"
        pass

    def switch_to_adicionar_categoria(self):
        self.manager.current = "adicionar_categoria_screen"
        pass

    def switch_to_adicionar_item(self):
        self.manager.current = "adicionar_item_screen"
        pass

    def troca_categoria_item(self):
        try:
            self.categoria_lista = self.categorias[self.categorias.index(self.categoria_lista)+1]
        except IndexError:
            self.categoria_lista = self.categorias[0]
        self.refresh()


class AdicionarFuncionario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def criar(self):
        self.criar_perfil = True
        self.refresh()

    def add_perfil(self):
        novo_usuario = Funcionario(self.ids.text_input_nome.text, self.ids.text_input_telefone.text)
        Usuarios.create(novo_usuario)
        Historico.create(novo_usuario)
        self.refresh()

    def remover_perfil(self):
        Usuarios.delete(self.id_selecionado)
        self.nome_selecionado = ""
        self.telefone_selecionado = ""
        self.id_selecionado = ""
        self.refresh()

    def atualizar_perfil(self):
        update_usuario = Funcionario(self.ids.text_input_nome.text, self.ids.text_input_telefone.text)
        Usuarios.update(self.id_selecionado, update_usuario)
        self.refresh()

    def selecionar(self, nome, telefone, id_selecionado):
        print(nome, telefone)
        self.nome_selecionado = nome
        self.telefone_selecionado = telefone
        self.id_selecionado = id_selecionado
        self.criar_perfil = False
        self.refresh()

    def on_pre_enter(self, *args):
        self.criar_perfil = True
        self.nome_selecionado = ""
        self.refresh()

    def refresh(self):
        from bson.objectid import ObjectId
        def remover_botoes():
            layout = self.ids.box_layout
            for widget in layout.children[:]:  
                if isinstance(widget, Button):
                    layout.remove_widget(widget)
            layout = self.ids.box_layout_direita
            for box in layout.children[:]:
                for widget in box.children[:]:
                    if isinstance(widget, TextInput):
                        widget.text = ''
        self.ids.container_funcionarios.clear_widgets()
        self.ids.ultimo_box_layout.clear_widgets()
        apagar_text_inputs(self)
        for usuario in Usuarios.read():
            botao_criando = ThreeLineListItem(text=usuario['nome'],
                                              secondary_text= usuario['telefone'],
                                              tertiary_text= str(usuario['_id']),
                                              on_release=lambda x=self: self.selecionar\
                (x.text, x.secondary_text, x.tertiary_text))
            self.ids.container_funcionarios.add_widget(botao_criando)
        if self.criar_perfil:
            self.ids.criar_editar.text = "Criando perfil!"
            remover_botoes()
            self.ids.ultimo_box_layout.add_widget\
                (Button(text="Criar!",
                        background_color="green",
                        on_release=lambda x=None: self.add_perfil()))

        else:
            self.ids.criar_editar.text = f"Perfil selecionado: {self.nome_selecionado}"
            remover_botoes()
            self.ids.box_layout.add_widget\
                (Button(text="add perfil",
                        background_color="red",
                        on_release=lambda x=0: self.criar(),
                        size_hint=(0.25, 1)))
            self.ids.text_input_nome.text = self.nome_selecionado
            self.ids.text_input_telefone.text = self.telefone_selecionado
            self.ids.ultimo_box_layout.add_widget\
                (Button(text="Remover!",
                        background_color="red",
                        on_release=lambda x=None: self.remover_perfil()))
            self.ids.ultimo_box_layout.add_widget\
                (Button(text="Atualizar!",
                        background_color="green",
                        on_release=lambda x=None: self.atualizar_perfil()))

    def switch_to_main_screen(self):
        self.manager.current = "main_screen"


class AdicionarCategoriaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        print("entrando adicionar_categoria")

    def refresh(self):
        pass

    def switch_to_main_screen(self):
        self.manager.current = "main_screen"


class ComprasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.container_emergencias.clear_widgets()
        lista_comprar = []
        lista_comprar.clear()
        print("entrando compras screen")
        lista = Itens.read()
        for item in lista:
            if int(item['quantidade']) < int(item['limite']):
                quantidade_comprar = int(item['limite']) - int(item['quantidade'])
                self.ids.container_emergencias.add_widget\
                    (ThreeLineListItem(text=item['nome'],
                                    secondary_text="quantidade atual: "\
                                        +item['quantidade']+" || limite: "+item['limite'],
                                        tertiary_text="comprar: "+str(quantidade_comprar)))
                lista_comprar.append(item)
        self.envio_email(lista_comprar)

    def envio_email(self, lista_comprar):
        if len(lista_comprar) >= 1:
            envio_email()
    def switch_to_main_screen(self):
        self.manager.current = "main_screen"

class HistoricoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.refresh()
        print("Entrando historico screen")

    def switch_to_main_screen(self):
        self.manager.current = "main_screen"
    
    def refresh(self):
        Historico.read()


class AlmoxarifadoApp(MDApp):
    def build(self):
        # Create a ScreenManager to manage multiple screens
        sm = ScreenManager()
        # Add your screens to the ScreenManager
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(HistoricoScreen(name="historico_screen"))
        sm.add_widget(SelecaoFuncionarioScreen(name="selecionar_funcionario_screen"))
        sm.add_widget(AdicionarFuncionario(name="adicionar_funcionario_screen"))
        sm.add_widget(AdicionarCategoriaScreen(name="adicionar_categoria_screen"))
        sm.add_widget(ComprasScreen(name="compras_screen"))
        return sm

if __name__ == '__main__':  # run
    AlmoxarifadoApp().run()
