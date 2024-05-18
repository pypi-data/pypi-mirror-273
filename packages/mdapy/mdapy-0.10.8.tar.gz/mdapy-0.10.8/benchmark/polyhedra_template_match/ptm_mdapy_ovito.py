import mdapy as mp
import numpy as np
from time import time
import matplotlib.pyplot as plt

plt.switch_backend("tkagg")
from mdapy import pltset, cm2inch

from ovito.data import DataCollection, Particles, SimulationCell
from ovito.modifiers import PolyhedralTemplateMatchingModifier


def mdapy_ptm(pos, box):
    ptm = mp.PolyhedralTemplateMatching(pos, box)
    ptm.compute()


def ptm_average_time(ave_num=3):
    time_list = []
    print("*" * 30)

    for num in [5, 25, 45, 65, 85, 105, 125]:  # 5, 25, 45, 65, 85, 105
        FCC = mp.LatticeMaker(3.615, "FCC", num, 100, 100)
        FCC.compute()
        pos = FCC.pos
        box = FCC.box
        N = FCC.N
        print(f"Build {N} atoms...")
        mdapy_t_cpu, ovito_t = 0.0, 0.0

        for turn in range(ave_num):
            print(f"Running {turn} turn in mdapy cpu...")
            start = time()
            mdapy_ptm(pos, box)
            end = time()
            mdapy_t_cpu += end - start

        for turn in range(ave_num):
            print(f"Running {turn} turn in ovito...")

            particles = Particles()
            data = DataCollection()
            data.objects.append(particles)
            particles.create_property("Position", data=pos)
            cell = SimulationCell(pbc=(True, True, True))
            cell[...] = np.c_[box[:-1], box[-1]]
            data.objects.append(cell)
            start = time()
            data.apply(PolyhedralTemplateMatchingModifier(output_orientation=True))
            end = time()
            ovito_t += end - start

        time_list.append([N, mdapy_t_cpu / ave_num, ovito_t / ave_num])
        print("*" * 30)
    time_list = np.array(time_list)

    return time_list


def plot(time_list, title=None, savefig=True):
    pltset()
    colorlist = [i["color"] for i in list(plt.rcParams["axes.prop_cycle"])]
    fig = plt.figure(figsize=(cm2inch(10), cm2inch(8)), dpi=150)
    plt.subplots_adjust(left=0.16, bottom=0.165, top=0.92, right=0.95)
    N_max = time_list[-1, 0]
    exp_max = int(np.log10(N_max))
    x, y = time_list[:, 0] / 10**exp_max, time_list[:, 1]

    popt = np.polyfit(x, y, 1)
    plt.plot(x, np.poly1d(popt)(x), c=colorlist[0])
    plt.plot(x, y, "o", label=f"mdapy-cpu, k={popt[0]:.1f}")

    y = time_list[:, 2]
    popt = np.polyfit(x, y, 1)
    plt.plot(x, np.poly1d(popt)(x), c=colorlist[1])
    plt.plot(x, y, "o", label=f"ovito, k={popt[0]:.1f}")

    if title is not None:
        plt.title(title, fontsize=12)
    plt.legend()
    plt.xlabel("Number of atoms ($\mathregular{10^%d}$)" % exp_max)
    plt.ylabel("Time (s)")
    if savefig:
        plt.savefig("PTM.png", dpi=300, bbox_inches="tight", transparent=True)
    plt.show()


if __name__ == "__main__":
    mp.init()
    time_list = ptm_average_time(ave_num=3)
    np.savetxt("time_list.txt", time_list)
    time_list = np.loadtxt("time_list.txt")
    plot(time_list, "Calculate PTM")
