from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from pyModbusTCP.client import ModbusClient
from datetime import datetime
from dbhandler import DBHandler
from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg

tags_addrs = {
    'temperatura': 1000,
    'pressao': 1001,
    'umidade': 1002,
    'consumo': 1003,
}

class MyWidget(BoxLayout):

    def pesquisar(self):
        inicial = str(self.ids.datai.text) + ' ' + str(self.ids.horai.text)
        final = str(self.ids.dataf.text) + ' ' + str(self.ids.horaf.text)

        #Teste do textinput 
        print(f'\nEntrada inicial: {inicial}\n')
        print(f'Entrada final: {final}\n')
        self.conectar()

        #Adicionar lógica do Banco de dados

        try:
            #print("Bem vindo ao sistema de busca de dados históricos")
            while True:
                # init = input("Digite o horário inicial para a busca (DD/MM/AAAA HH:MM:SS):")
                # final = input("Digite o horário final para a busca (DD/MM/AAAA HH:MM:SS):")
                inicial = datetime.strptime(inicial, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                final = datetime.strptime(final, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                #result = self._dbclient.select_data(self._tags_addrs.keys(), inicial, final)
                #Teste do textinput 
                print(f'\nEntrada inicial: {inicial}\n')
                print(f'Entrada final: {final}\n')
                #print(tabulate(result['data'], headers=result['cols']))

                signal = [7, 89.6, 45.-56.34]
  
                signal = np.array(signal)
                
                # this will plot the signal on graph
                plt.plot(signal)
                
                # setting x label
                plt.xlabel('Time(s)')
                
                # setting y label
                plt.ylabel('signal (norm)')
                plt.grid(True, color='lightgray')
                
                # adding plot to kivy boxlayout
                self.str.grafico.add_widget(FigureCanvasKivyAgg(plt.gcf()))
                return self.str


        except Exception as e:
            print("Erro: ", e.args)
    
    def conectar(self):
        try:
            self._cliente = ModbusClient(host='localhost', port = 502)
            self._scan_time = 1

            self._tags_addrs = tags_addrs
            self._dbclient = DBHandler('data\data.db',self._tags_addrs.keys(),'modbusData') #   ERRO! 'DBHandler' object has no attribute '_con'
            #self._threads = []

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
    Config.set('graphics','resizable',True)
    InterfaceApp().run()