# -*- coding: utf-8 -*-
from scipy import *
from scipy.integrate import quad
import math
import cmath


# public
def c_p(kappa, theta, sigma, rho, v0, r, T, s0, K):
    p1 = __p1(kappa, theta, sigma, rho, v0, r, T, s0, K)
    p2 = __p2(kappa, theta, sigma, rho, v0, r, T, s0, K)
    return (s0 * p1 - K * math.exp(-r * T) * p2)


# private
def __p(kappa, theta, sigma, rho, v0, r, T, s0, K, status):
    integrand = lambda phi: (cmath.exp(-1j * phi * math.log(K)) *
                             __f(phi, kappa, theta, sigma, rho, v0, r, T, s0, status) / (1j * phi)).real
    return (0.5 + (1 / math.pi) * quad(integrand, 0, 100)[0])


def __p1(kappa, theta, sigma, rho, v0, r, T, s0, K):
    return __p(kappa, theta, sigma, rho, v0, r, T, s0, K, 1)


def __p2(kappa, theta, sigma, rho, v0, r, T, s0, K):
    return __p(kappa, theta, sigma, rho, v0, r, T, s0, K, 2)


def __f(phi, kappa, theta, sigma, rho, v0, r, T, s0, status):
    if status == 1:
        u = 0.5
        b = kappa - rho * sigma
    else:
        u = -0.5
        b = kappa

    a = kappa * theta
    x = math.log(s0)
    d = cmath.sqrt((rho * sigma * phi * 1j - b) ** 2 - sigma ** 2 * (2 * u * phi * 1j - phi ** 2))
    g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)
    C = r * phi * 1j * T + (a / sigma ** 2) * (
    (b - rho * sigma * phi * 1j + d) * T - 2 * cmath.log((1 - g * cmath.exp(d * T)) / (1 - g)))
    D = (b - rho * sigma * phi * 1j + d) / sigma ** 2 * ((1 - cmath.exp(d * T)) / (1 - g * cmath.exp(d * T)))
    return cmath.exp(C + D * v0 + 1j * phi * x)

def c_p1(kappa, theta, sigma, rho, v0, r, T, s0, K):
    p1 = __p1(kappa, theta, sigma, rho, v0, r, T, s0+0.00001, K)
    p2 = __p2(kappa, theta, sigma, rho, v0, r, T, s0+0.00001, K)
    print ((s0+0.00001) * p1 - K * math.exp(-r * T) * p2)
    return ((s0+0.00001) * p1 - K * math.exp(-r * T) * p2)

def delta(kappa, theta, sigma, rho, v0, r, T, s0, K):
    d_c_heston=(c_p1(kappa, theta, sigma, rho, v0, r, T, s0, K)-c_p(kappa, theta, sigma, rho, v0, r, T, s0, K))/0.00001
    return d_c_heston



