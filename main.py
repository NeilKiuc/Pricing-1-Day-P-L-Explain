import bs

S, K, T = 100, 100, 1
r, sigma = 0.05, 0.20

print("Call price:", bs.price(S,r,K,T,sigma,"call"))

# Exemple de P&L : +1% spot, +1pt vol, 1 jour
res = bs.pnl_explain(S,r,K,T,sigma,"call",dS_frac=0.01,dSigma_pts=1.0,dt_days=1)

print("\nP&L exact :", res["pnl_exact"])
print("P&L approx:", res["pnl_approx"])
print("Start:", res["start"], "End:", res["end"])