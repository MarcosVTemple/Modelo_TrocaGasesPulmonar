import os

from modelos.main_mec_pulm import MecanicaPulmonar
from modelos.main_troc_gas import TrocaGases

if __name__ == "__main__":
    os.environ["modo_ventilacao"] = "normal"
    os.environ["modo_atividade"] = "repouso"
    os.environ["tipo_entrada_sistema"] = input("Tipo de entrada do sistema:\n   1. Senoide\n   2. Resultado do modelo da mecânica pulmonar\n->")
    
    os.environ["save_figures"] = "FALSE"
    os.environ["save_data"] = "FALSE"
    
    os.environ["tempo_simulacao"] = input("Tempo de simulação do sistema? Ex.: 24 [segundos]\n->")

    print("Iniciando Troca de Gases")
    troc_gas_obj = TrocaGases()
    troc_gas_obj.run_troca_gases()
    troc_gas_obj.plot_troca_gases()
