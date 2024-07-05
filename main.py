import os

from modelos.main_mec_pulm import MecanicaPulmonar
from modelos.main_troc_gas import TrocaGases
from plot import plot


if __name__ == "__main__":
    os.environ["modo_ventilacao"] = "normal"
    os.environ["modo_atividade"] = "repouso"
    os.environ["save_figures"] = "FALSE"
    os.environ["save_data"] = "FALSE"
    os.environ["tempo_simulacao"] = input("Tempo de simulação do sistema? Ex.: 24 [segundos]\n->")
        
    print("Iniciando Troca de Gases Senoide")
    os.environ["tipo_entrada_sistema"] = "1"
    # input("Tipo de entrada do sistema:\n   1. Senoide\n   2. Resultado do modelo da mecânica pulmonar\n->")  
    troc_gas_obj_sen = TrocaGases()
    troc_gas_obj_sen.run_troca_gases()
    # troc_gas_obj_sen.plot_troca_gases()
    
    print("Iniciando Troca de Gases Mecanica Pulmonar")
    os.environ["tipo_entrada_sistema"] = "2"
    # input("Tipo de entrada do sistema:\n   1. Senoide\n   2. Resultado do modelo da mecânica pulmonar\n->")  
    troc_gas_obj_mp = TrocaGases()
    troc_gas_obj_mp.run_troca_gases()
    # troc_gas_obj_mp.plot_troca_gases()

    plot(
        x=troc_gas_obj_sen.t, 
        y1=troc_gas_obj_sen.y_tg,
        y2=troc_gas_obj_mp.y_tg,
    )