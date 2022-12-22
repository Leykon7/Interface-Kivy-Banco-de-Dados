from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from pyModbusTCP.client import ModbusClient
from datetime import datetime
from dbhandler import DBHandler
from matplotlib import pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.core.window import Window

tags_addrs = {
    'temperatura': 1000,
    'pressao': 1001,
    'umidade': 1002,
    'consumo': 1003,
}

class MyWidget(BoxLayout):

    graf = False
    def pesquisar(self):
        """
        Método que acessa o histórico de dados
        """
        if self.graf == True:
            self.ids.grafico.clear_widgets()
            plt.cla()
        self.conectar()
        try:            
            #Acessando histórico
            inicial = str(self.ids.datai.text) + ' ' + str(self.ids.horai.text)
            final = str(self.ids.dataf.text) + ' ' + str(self.ids.horaf.text)
            inicial = datetime.strptime(inicial, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            final = datetime.strptime(final, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
            result = self._dbclient.select_data(self._tags_addrs.keys(), inicial, final)

            #Selecionando apenas os dados escolhidos e pondo na lista signal
            signal = []
            if self.ids.seletor.text == 'Temperatura':
                for i in range(len(result['data'])):
                    signal.append(result['data'][i][1])
            elif self.ids.seletor.text == 'Pressão':
                for i in range(len(result['data'])):
                    signal.append(result['data'][i][2])
            elif self.ids.seletor.text == 'Umidade':
                for i in range(len(result['data'])):
                    signal.append(result['data'][i][3])
            elif self.ids.seletor.text == 'Consumo':
                for i in range(len(result['data'])):
                    signal.append(result['data'][i][4])
            
            #Plotando gráfico
            plt.plot(signal)
            plt.xlabel('Número de dados')      
            plt.ylabel(self.ids.seletor.text)
            plt.grid(True, color='lightgray')
            self.ids.grafico.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.graf = True

        except Exception as e:
            print("Erro: ", e.args)
    
    def conectar(self):
        """
        Método que conecta com o servidor
        """
        try:
            self._cliente = ModbusClient(host='localhost', port = 502)
            self._scan_time = 1
            self._tags_addrs = tags_addrs
            self._dbclient = DBHandler('data\data.db',self._tags_addrs.keys(),'modbusData') 
            self._cliente.open()
        except Exception as e:
            print('Erro no atendimento: ',e.args)

class InterfaceApp(App):
    def build(self):
        """
        Método para construção do aplicativo com base no widget criado
        """
        return MyWidget()
 
if __name__ == '__main__':
    Window.size = (1200,600)
    Window.fullscreen = False
    InterfaceApp().run()