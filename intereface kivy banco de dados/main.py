from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

class MyWidget(BoxLayout):
    def changelb(self):
        """
        Método simples para incremento do valor mostrado no label
        """
        self.ids.lb.text = str(int(self.ids.lb.text) + 1)

    def pesquisar(self):
        inicial = str(self.ids.datai.text) + ' ' + str(self.ids.horai.text)
        final = str(self.ids.dataf.text) + ' ' + str(self.ids.horaf.text)
        #Teste do textinput 
        print(f'Entrada inicial: {inicial}\n')
        print(f'Entrada final: {final}\n')

        #Adicionar lógica do Banco de dados
    


class InterfaceApp(App):
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        return MyWidget()
 
if __name__ == '__main__':
    Config.set('graphics','resizable',True)
    InterfaceApp().run()