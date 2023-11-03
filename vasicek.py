import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class VasicekModel(object):
    def __init__(self, a: float, b: float, r0: float, sigma: float) -> float:
        self.a = a
        self.b = b
        self.r0 = r0
        self.sigma = sigma
    
    def __iter__(self):
        return iter([self.a, self.b, self.r0, self.sigma])

    def mean(self, t: float) -> float:
        return self.r0 * np.exp(-self.a * t) + self.b * (1 - np.exp(-self.a * t))

    def var(self, t: float) -> float:
        return (self.sigma ** 2) / (2 * self.a) * (1 - np.exp(-2 * self.a * t))

    def btt(self, t: float, T: float) -> float:
        return 1 / self.a * (1 - np.exp(-self.a * (T - t)))

    def att(self, t: float, T: float) -> float:
        btt = self.btt(t, T)
        return np.exp((btt - T + t) * (self.a ** 2 * self.b - self.sigma ** 2 / 2) / self.a ** 2 - self.sigma ** 2 * btt ** 2 / (4 * self.a))

    def zcb(self, t: float, T: float, rt: float):
        att = self.att(t, T)
        btt = self.btt(t, T)
        return att * np.exp(-btt * rt)


class Bondoptions(object):
    def __init__(self, VasicekModel, TO: float, TB: float, K: float) -> float:
        self.vasicek = VasicekModel
        self.TO = TO
        self.TB = TB
        self.K = K
    def sz(self) -> float:
        return self.vasicek.btt(self.TO,self.TB) * np.sqrt(self.vasicek.var(self.TO))
    def d1(self) -> float:
        return (1 / (self.sz()) * np.log(self.vasicek.zcb(0,self.TB,self.vasicek.r0)/(self.K*self.vasicek.zcb(0,self.TO,self.vasicek.r0)))+ self.sz()/2)
    def d2(self) -> float:
        return self.d1() - self.sz()
    def V_call(self):
        return self.vasicek.zcb(0,self.TB,self.vasicek.r0) * norm.cdf(self.d1()) - self.K * self.vasicek.zcb(0,self.TO,self.vasicek.r0) * norm.cdf(self.d2())
    def V_put(self):
        return self.K * self.vasicek.zcb(0,self.TO,self.vasicek.r0) * norm.cdf(-self.d2()) - self.vasicek.zcb(0,self.TB,self.vasicek.r0) * norm.cdf(-self.d1())
