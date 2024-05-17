"""
Raw formalisms as written in paper
"""
import math

von_karman = 0.4  # [-] https://en.wikipedia.org/wiki/Von_K%C3%A1rm%C3%A1n_constant


def eq3(rho_a, cm, ts, ta, ra):
    return rho_a * cm * (ts - ta) / ra


def eq4(zm, d, zom, zoh, u):
    return math.log((zm - d) / zom) * math.log((zm - d) / zoh) / (von_karman ** 2 * u)


def eq5(hc):
    return 2 * hc / 3


def eq6(hc):
    return 0.123 * hc


def eq7(zom):
    return 0.1 * zom
