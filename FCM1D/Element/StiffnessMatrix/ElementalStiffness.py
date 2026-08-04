import numpy as np
from Element.StrainDisplacement import StrainDisplacement


def calculate_element_stiffness(element, cfg, quad):
    EA = cfg.E * cfg.A
    Ke = None
    for xi, w, m in zip(quad.xi, quad.w, quad.mat):
        B = StrainDisplacement(xi, element, cfg)
        Mat = EA * m
        contribution = np.dot(np.dot(B.T, Mat), B) * w
        Ke = contribution if Ke is None else Ke + contribution
    return Ke


