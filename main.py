import numpy as np
import matplotlib.pyplot as plt
import bs

# Params
S, K, T = 100, 100, 1
r, sigma = 0.05, 0.20
opt = "call"

# Case grid
dS_list = np.array([-0.03,-0.02,-0.01,0.0,0.01,0.02,0.03])
dVol_list = np.array([-2.0,-1.0,0.0,1.0,2.0])

pnl = np.zeros((len(dVol_list), len(dS_list)))

for i, dv in enumerate(dVol_list):
    for j, ds in enumerate(dS_list):
        res = bs.pnl_explain(S,r,K,T,sigma,opt,dS_frac=ds,dSigma_pts=dv,dt_days=1)
        pnl[i,j] = res["pnl_exact"]

# Heatmap
fig, ax = plt.subplots()
im = ax.imshow(pnl,
               aspect="auto",
               origin="lower",
               cmap="RdYlGn",
               extent=[dS_list[0]*100, dS_list[-1]*100, dVol_list[0], dVol_list[-1]])

plt.colorbar(im, ax=ax, label="Exact 1-day P&L")
ax.set_xlabel("Spot move (%)")
ax.set_ylabel("Vol change (points)")
ax.set_title("1-day P&L heatmap (exact repricing)")
plt.show()

