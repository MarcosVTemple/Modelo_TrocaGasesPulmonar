import os
import numpy as np
import matplotlib.pyplot as plt


def plot(x, y1, y2):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle('')
    ax1.plot(x[1:], np.array(y1["P_cap_O2"])[1:], color="r", label="sen")
    ax1.plot(x[1:], np.array(y2["P_cap_O2"])[1:], color="b", label="mp")
    ax1.set_title('Oxigênio')
    ax1.set(ylabel="Pressão Parcial [mmHg]")
    ax2.plot(x[1:], np.array(y1["P_cap_CO2"])[1:], color="r", label="sen")
    ax2.plot(x[1:], np.array(y2["P_cap_CO2"])[1:], color="b", label="mp")
    ax2.set_title('Dióxido de Carbono')
    ax2.set(ylabel="Pressão Parcial [mmHg]", xlabel="Tempo [s]")
    fig.savefig(
        f"results/tg/figures/6_pparcial_capilar_"
            f"teste_10"
    )