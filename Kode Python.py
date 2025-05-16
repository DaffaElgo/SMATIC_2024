
"""
Author:            Daffa Elgo Santosa and Collaborators
Project:           Smart Statistics Competition 2024 (Statistics Olympiad)
Award:             First Place
Repository:        https://github.com/DaffaElgo/SMATIC_2024
Description:       Implementasi simulasi penyeberangan kendaraan berdasarkan data selang waktu.
"""

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import time

# Load data
# 1. URL harus dalam tanda kutip, 2. pakai raw.githubusercontent.com
raw_path = "https://raw.githubusercontent.com/DaffaElgo/SMATIC_2024/main/Data%20selang%20waktu%20kendaraan%20_clean.xlsx"

try:
    data = pd.read_excel(raw_path, engine="openpyxl")
    time_intervals = data["X"].values
except Exception as e:
    messagebox.showerror("Data Error", f"Failed to load Excel:\n{e}")
    time_intervals = np.array([])

# === Simulation core ===
def simulate_crossing(N, L, k, intervals, iterations=1):
    crossed_list, queued_list = [], []
    for _ in range(iterations):
        total_crossed = total_queued = queue = 0
        for interval in intervals:
            new = np.random.poisson(N * interval)
            queue += new
            total_queued += new
            if interval < L:
                serve = 0
            elif interval < 2 * L:
                serve = min(queue, k)
            elif interval < 3 * L:
                serve = min(queue, 2 * k)
            else:
                serve = min(queue, int(interval // L) * k)
            total_crossed += serve
            queue -= serve
        crossed_list.append(total_crossed)
        queued_list.append(total_queued)
    return np.mean(crossed_list), np.mean(queued_list)

# === 2D (Max L) functions ===
def evaluate_2d(params):
    N, intervals, L, k, threshold, iters = params
    crossed, queued = simulate_crossing(N, L, k, intervals, iters)
    eff = crossed / queued if queued else 0
    optimal = abs(eff - 1) <= threshold
    return (L, eff, optimal)

def find_2d(N, intervals, Ls, k, threshold, iters):
    return [evaluate_2d((N, intervals, L, k, threshold, iters)) for L in tqdm(Ls)]

def plot_2d(results, threshold, N, k):
    Ls = [r[0] for r in results]
    effs = [r[1] for r in results]
    fig, ax = plt.subplots()
    ax.plot(Ls, effs, '-o')
    ax.axhline(1, linestyle='--', color='red')
    ax.fill_between(Ls, 1 - threshold, 1 + threshold, alpha=0.2)
    ax.set(xlabel='L', ylabel='Efficiency', title=f'Efficiency vs L (N={N}, k={k})')
    return fig

# === 3D (Surface) functions ===
def evaluate_3d(params):
    N, intervals, L, k, iters = params
    crossed, queued = simulate_crossing(N, L, k, intervals, iters)
    eff = crossed / queued if queued else 0
    return (L, N, eff)

def find_3d(Ns, intervals, Ls, k, iters):
    return [evaluate_3d((N, intervals, L, k, iters)) for N in Ns for L in Ls]

def plot_3d(results, k):
    Ls = np.array([r[0] for r in results])
    Ns = np.array([r[1] for r in results])
    effs = np.array([r[2] for r in results])
    Lu, Nu = np.unique(Ls), np.unique(Ns)
    Lg, Ng = np.meshgrid(Lu, Nu)
    Eff = np.zeros_like(Lg, dtype=float)
    for i, L in enumerate(Lu):
        for j, N in enumerate(Nu):
            mask = (Ls == L) & (Ns == N)
            if mask.any():
                Eff[j, i] = effs[mask][0]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(Lg, Ng, Eff, cmap='viridis')
    ax.set(xlabel='L', ylabel='N', zlabel='Efficiency', title=f'3D Efficiency (k={k})')
    fig.colorbar(surf, ax=ax, label='Efficiency')
    return fig

# === GUI setup ===
root = tk.Tk()
root.title("Monte Carlo Simulation GUI")
root.geometry("480x720")
# Scrollable area
canvas = tk.Canvas(root)
scroll = tk.Scrollbar(root, command=canvas.yview, orient='vertical')
frame = tk.Frame(canvas)
frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0,0), window=frame, anchor='nw')
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side='left', fill='both', expand=True)
scroll.pack(side='right', fill='y')

# Mode selection
tk.Label(frame, text="Mode:").grid(row=0, column=0, sticky='w')
mode_var = tk.StringVar(value='Max L')
tk.Radiobutton(frame, text='Max L', variable=mode_var, value='Max L').grid(row=0, column=1)
tk.Radiobutton(frame, text='3D Plot', variable=mode_var, value='3D Plot').grid(row=0, column=2)

# 2D Settings frame
frame_2d = ttk.LabelFrame(frame, text='Max L Settings')
labels2 = ['N', 'k', 'L start', 'L end', 'L step', 'Threshold', 'Iterations']
def2 = ['5', '5', '0.01', '1', '0.01', '0.05', '20']
vars2 = {}
for i, (lbl, dv) in enumerate(zip(labels2, def2), start=1):
    ttk.Label(frame_2d, text=lbl+':').grid(row=i, column=0, sticky='e')
    ent = ttk.Entry(frame_2d); ent.insert(0, dv); ent.grid(row=i, column=1, sticky='we', padx=5, pady=2)
    vars2[lbl] = ent

# 3D Settings frame
frame_3d = ttk.LabelFrame(frame, text='3D Settings')
labels3 = ['k', 'L start', 'L end', 'L step', 'N start', 'N end', 'N step', 'Iterations']
def3 = ['5', '0.01', '1', '0.01', '1', '10', '1', '20']
vars3 = {}
for i, (lbl, dv) in enumerate(zip(labels3, def3), start=1):
    ttk.Label(frame_3d, text=lbl+':').grid(row=i, column=0, sticky='e')
    ent = ttk.Entry(frame_3d); ent.insert(0, dv); ent.grid(row=i, column=1, sticky='we', padx=5, pady=2)
    vars3[lbl] = ent

# Place and toggle frames
frame_2d.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='we')
frame_3d.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='we')
frame_3d.grid_remove()
def toggle():
    if mode_var.get()=='Max L': frame_3d.grid_remove(); frame_2d.grid()
    else: frame_2d.grid_remove(); frame_3d.grid()
mode_var.trace_add('write', lambda *args: toggle()); toggle()

# Buttons and execution time
tk.Button(frame, text='Run', command=lambda: run_simulation()).grid(row=2, column=0, pady=10)
tk.Button(frame, text='Reset', command=lambda: reset_output()).grid(row=2, column=1)
time_var = tk.StringVar(); ttk.Label(frame, textvariable=time_var).grid(row=2, column=2)

# Tables for Max L results
maxL_tbl = ttk.Treeview(frame, columns=('L','Efficiency'), show='headings', height=2)
for c in ('L','Efficiency'): maxL_tbl.heading(c, text=c)
opt_tbl = ttk.Treeview(frame, columns=('L','Efficiency'), show='headings', height=5)
for c in ('L','Efficiency'): opt_tbl.heading(c, text=c)
alt_tbl = ttk.Treeview(frame, columns=('L','Efficiency'), show='headings', height=5)
for c in ('L','Efficiency'): alt_tbl.heading(c, text=c)
maxL_tbl.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='we')
opt_tbl.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky='we')
alt_tbl.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky='we')
maxL_tbl.grid_remove(); opt_tbl.grid_remove(); alt_tbl.grid_remove()

# Simulation runner
def run_simulation():
    if mode_var.get()=='Max L':
        try:
            N=float(vars2['N'].get()); k=float(vars2['k'].get())
            Ls=np.arange(float(vars2['L start'].get()), float(vars2['L end'].get())+float(vars2['L step'].get()), float(vars2['L step'].get()))
            thr=float(vars2['Threshold'].get()); it=int(vars2['Iterations'].get())
        except:
            return messagebox.showerror('Error','Invalid Max L inputs')
        def task2d():
            start=time.time(); res=find_2d(N,time_intervals,Ls,k,thr,it); dur=time.time()-start; time_var.set(f'2D Time: {dur:.2f}s')
            opt=[r for r in res if r[2]]; alt=[r for r in res if not r[2]]
            maxL_tbl.delete(*maxL_tbl.get_children()); opt_tbl.delete(*opt_tbl.get_children()); alt_tbl.delete(*alt_tbl.get_children())
            if opt: maxL_tbl.insert('', 'end', values=opt[-1][:2])
            for r in opt: opt_tbl.insert('', 'end', values=r[:2])
            for r in alt: alt_tbl.insert('', 'end', values=r[:2])
            maxL_tbl.grid(); opt_tbl.grid(); alt_tbl.grid()
            fig=plot_2d(res,thr,N,k); win=tk.Toplevel(root); win.title('2D Plot'); c=FigureCanvasTkAgg(fig,win); c.draw(); c.get_tk_widget().pack(fill='both',expand=True)
        Thread(target=task2d).start()
    else:
        try:
            k=float(vars3['k'].get());
            Ls=np.arange(float(vars3['L start'].get()), float(vars3['L end'].get())+float(vars3['L step'].get()), float(vars3['L step'].get()));
            Ns=np.arange(float(vars3['N start'].get()), float(vars3['N end'].get())+float(vars3['N step'].get()), float(vars3['N step'].get()));
            it=int(vars3['Iterations'].get())
        except:
            return messagebox.showerror('Error','Invalid 3D inputs')
        def task3d():
            start=time.time(); res=find_3d(Ns,time_intervals,Ls,k,it); dur=time.time()-start; time_var.set(f'3D Time: {dur:.2f}s')
            fig=plot_3d(res,k); win=tk.Toplevel(root); win.title('3D Plot'); c=FigureCanvasTkAgg(fig,win); c.draw(); c.get_tk_widget().pack(fill='both',expand=True)
        Thread(target=task3d).start()

# Reset function
def reset_output():
    time_var.set(''); maxL_tbl.delete(*maxL_tbl.get_children()); opt_tbl.delete(*opt_tbl.get_children()); alt_tbl.delete(*alt_tbl.get_children());
    maxL_tbl.grid_remove(); opt_tbl.grid_remove(); alt_tbl.grid_remove()

if __name__=='__main__':
    root.mainloop()
