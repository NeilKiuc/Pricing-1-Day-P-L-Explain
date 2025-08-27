import math

def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_pdf(x: float) -> float:
    return (1.0 / math.sqrt(2.0*math.pi)) * math.exp(-0.5*x*x)

def price(S: float, r: float, K: float, T: float, sigma: float, opt: str = "call") -> float:
    d1 = (math.log(S / K) + (r + 0.5*sigma*sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    if opt == "call":
        return S * norm_cdf(d1) - K*math.exp(-r*T)*norm_cdf(d2)
    else:
        return K*math.exp(-r*T)*norm_cdf(-d2) - S*norm_cdf(-d1)

def greeks(S: float, r: float, K: float, T: float, sigma: float, opt: str = "call") -> dict:
    d1 = (math.log(S / K) + (r + 0.5*sigma*sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)


    gamma = norm_pdf(d1) / (S * sigma * math.sqrt(T))
    vega  = S * norm_pdf(d1) * math.sqrt(T)
    if opt=="call":
        delta = norm_cdf(d1)
        theta = -(S*norm_pdf(d1)*sigma)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm_cdf(d2)
        rho   = K*T*math.exp(-r*T)*norm_cdf(d2)
    else:
        delta = norm_cdf(d1) - 1
        theta = -(S*norm_pdf(d1)*sigma)/(2*math.sqrt(T)) + r*K*math.exp(-r*T)*norm_cdf(-d2)
        rho   = -K*T*math.exp(-r*T)*norm_cdf(-d2)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}


def pnl_explain(S, r, K, T, sigma, opt, dS_frac=0.01, dSigma_pts=1.0, dt_days=1):
    """
    Calcule le P&L exact et le P&L approx (par les greeks) pour un petit choc.
    dS_frac : variation relative du spot (ex 0.01 = +1%)
    dSigma_pts : variation de vol en points (ex 1.0 = +1% vol → +0.01 en sigma)
    dt_days : nb de jours écoulés (ex 1 = un jour de theta)
    """
    days_in_year = 252
    dt = dt_days / days_in_year

    # état initial
    V0 = price(S, r, K, T, sigma, opt)
    g = greeks(S, r, K, T, sigma, opt)

    # nouvel état (spot, vol, temps)
    S1 = S * (1 + dS_frac)
    sigma1 = sigma + dSigma_pts/100
    T1 = max(1e-8, T - dt)
    V1 = price(S1, r, K, T1, sigma1, opt)

    # P&L exact
    pnl_exact = V1 - V0

    # P&L approx via greeks
    dS = S * dS_frac
    approx = (g["delta"]*dS
              + 0.5*g["gamma"]*(dS**2)
              + g["vega"]*(dSigma_pts/100)
              + g["theta"]*dt)

    return {"pnl_exact": pnl_exact, "pnl_approx": approx, "start": V0, "end": V1, "S1": S1, "sigma1": sigma1, "T1": T1}
