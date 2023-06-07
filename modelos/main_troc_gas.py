from tqdm import tqdm
import pandas as pd
import numpy as np
import math as m
import time as t
import os

from parametros import cts_mp, cts_tg
from funcoes.entrada_troc_gas import entrada_tg
from funcoes.derivada_troc_gas import derivada_tg
from funcoes.saida_troc_gas import saida_tg
from funcoes.plot_troc_gas import plot_tg
from decorators.timefunc import timefunc

RR = cts_tg["RR"]
dt = cts_tg["dt"]
Pfis = cts_tg["Pfis"]
f = RR/60


class TrocaGases:
    def __init__(self):
        tempo_simulacao = os.getenv("tempo_simulacao", default=None)
        if tempo_simulacao:
            cts_tg["N"] = int(int(tempo_simulacao)/cts_tg["dt"])
        
        n_A_O2 = np.zeros(cts_tg["N"], dtype=int)
        n_A_CO2 = np.zeros(cts_tg["N"], dtype=int)
        n_A_N2 = np.zeros(cts_tg["N"], dtype=int)
        n_cap_O2 = np.zeros(cts_tg["N"], dtype=int)
        n_cap_CO2 = np.zeros(cts_tg["N"], dtype=int)
        n_cap_N2 = np.zeros(cts_tg["N"], dtype=int)
        n_t_O2 = np.zeros(cts_tg["N"], dtype=int)
        n_t_CO2 = np.zeros(cts_tg["N"], dtype=int)
        n_t_N2 = np.zeros(cts_tg["N"], dtype=int)
        P_A_O2 = np.zeros(cts_tg["N"], dtype=int)
        P_A_CO2 = np.zeros(cts_tg["N"], dtype=int)
        P_A_N2 = np.zeros(cts_tg["N"], dtype=int)
        P_cap_O2 = np.zeros(cts_tg["N"], dtype=int)
        P_cap_CO2 = np.zeros(cts_tg["N"], dtype=int)
        P_cap_N2 = np.zeros(cts_tg["N"], dtype=int)
        VA_dot = np.zeros(cts_tg["N"], dtype=int)
        
        self.t = np.arange(0, cts_tg["N"] * cts_tg["dt"], cts_tg["dt"])
        self.entrada_tg_from_mp = None
        self.x_tg = pd.DataFrame(
            {
                'n_A_O2': n_A_O2, 'n_A_CO2': n_A_CO2, 'n_A_N2': n_A_N2,
                'n_cap_O2': n_cap_O2, 'n_cap_CO2': n_cap_CO2,
                'n_t_O2': n_t_O2, 'n_t_CO2': n_t_CO2
            }
        )
        self.y_tg = pd.DataFrame(
            {
                'P_A_O2': P_A_O2,
                'P_A_CO2': P_A_CO2,
                'P_A_N2': P_A_N2,
                'P_cap_O2': P_cap_O2,
                'P_cap_CO2': P_cap_CO2,
            }
        )
        self.u_tg = pd.DataFrame(
            {
                'VA_dot': VA_dot,
            }
        )

    @timefunc
    def run_troca_gases(self):
        self.inicializa_var_estado()
        self.rungekutta2()
        if os.getenv("save_data", default="") == 'TRUE':
            timestamp = str(int(round(t.time() * 1000)))
            self.x_tg.to_csv(
                f"results/tg/data/troca_gases_variaveis_estado_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )
            self.y_tg.to_csv(
                f"results/tg/data/troca_gases_saidas_dt_{dt}_{cts_tg['modo_ventilacao']}_{timestamp}.csv",
                sep=";",
                index=False
            )

    def inicializa_var_estado(self):
        nt_inicial = ((cts_tg["Patm"]*cts_tg["VA_t"])/(cts_tg["R"]*cts_tg["Temp"]))*1000
        self.x_tg.iloc[0, 0] = nt_inicial*cts_tg["f_O2"]  # 6.7145
        self.x_tg.iloc[0, 1] = nt_inicial*cts_tg["f_CO2"]  # 2.5817
        self.x_tg.iloc[0, 2] = nt_inicial*cts_tg["f_N2_H2O"]

        self.x_tg.iloc[0, 3] = 0.5388
        self.x_tg.iloc[0, 4] = 0.2072

        self.x_tg.iloc[0, 5] = 181.56
        self.x_tg.iloc[0, 6] = 85.23
        
        if os.getenv("tipo_entrada_sistema", default="2") == '2':
            print("Utilizando entrada do modelo da mecânica pulmonar")
            self.entrada_tg_from_mp = pd.read_csv(f"results/mp/data/saidas_dt_0.0004_{500000}.csv", sep=";")['VA_dot']
        else:
            print("Utilizando entrada senoidal")

    def plot_troca_gases(self):
        plot_tg(self.t, self.x_tg, self.y_tg, self.u_tg)

    def rungekutta2(self):
        for i in tqdm(range(cts_tg["N"]-1)):
            t = self.t[i]

            if self.entrada_tg_from_mp is not None:
                u_tg_t_array = self.entrada_tg_from_mp.iloc[i]
                u_tg = u_tg_t_array
                self.u_tg.iloc[i + 1, :] = u_tg_t_array
            else:
                phi = 2 * m.pi * f * t
                u_tg_t_array = entrada_tg(phi=phi, Pfis=Pfis)
                u_tg = u_tg_t_array
                self.u_tg.iloc[i+1, :] = u_tg_t_array

            x_tg_array = self.x_tg.iloc[i, 0:].to_numpy()
            x_tg = x_tg_array

            # constantes para RK2
            k1_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)
            k2_tg_rk2 = derivada_tg(x_tg, u_tg, cts_tg)

            # atribuindo os valores em x
            x_tg_rk2 = x_tg + dt*(k1_tg_rk2 + k2_tg_rk2)/2
            self.x_tg.iloc[i+1, :] = pd.DataFrame(np.matrix(x_tg_rk2))

            # atribuindo os valores em y
            self.y_tg.iloc[i + 1, :] = saida_tg(x_tg_rk2, cts_tg)
