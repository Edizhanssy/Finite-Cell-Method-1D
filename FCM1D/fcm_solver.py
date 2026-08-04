import numpy as np

from Element.Element import Element
from Element.createEdgesandNodes import create_nodes_and_edges
from Element.LocationMatrix import setupPerElement
from Element.ShapeFunctions.calcDerivativeofShapeFunction import (
    evalDerivOfShapeFunct, evalShapeFunct)
from Element.StiffnessMatrix.AssembleStiffnessMatrix import assemble_global_stiffness_matrix
from Element.ForceVector.assembleGlobalForceVector import assemble_Force_Vector
from Integration.DOFPartitioning import DOFPartitioning
from BoundaryCondition.NodeStrongBoundaryCondition.ApplyBoundaryConditions import ApplyBoundaryConditions
from BoundaryCondition.PenaltyValueAlgorithm.StrongPenaltyAlgorithm import StrongPenaltyAlgorithm
from BoundaryCondition.NodeStrongBoundaryCondition.StrongNodeDirichlet import StrongNodeDirichletBoundaryCondition


def solve(cfg):
    elements = [Element(0, (cfg.to_local(0.0), cfg.to_local(cfg.L)), (0.0, cfg.L))]
    nodes, edges, elements = create_nodes_and_edges(elements, cfg.n_elements)

    flat_nodes = [n for en in nodes for n in en]
    flat_edges = [e for ee in edges for e in ee]
    DOF = DOFPartitioning(flat_nodes, flat_edges, cfg.p, 1).assign_all_dofs()

    LtoG = setupPerElement(nodes[0], edges[0], cfg.n_modes, 1, cfg.n_elements)

    K = assemble_global_stiffness_matrix(elements, DOF, LtoG, cfg)
    F = assemble_Force_Vector(elements, DOF, LtoG, cfg)
    nodal_force_sum = float(F[[0, 1, 2], 0].sum())

    penalty = StrongPenaltyAlgorithm(cfg.penalty)
    bc_fix = StrongNodeDirichletBoundaryCondition([0, 0, 0], 0, 1, penalty)
    bc_end = StrongNodeDirichletBoundaryCondition([cfg.L, 0, 0], cfg.disp_load, 1, penalty)
    K, F = ApplyBoundaryConditions([nodes[0][0], nodes[0][2]], K, F, [bc_fix, bc_end])

    kappa = float(np.linalg.cond(K))
    u = np.array(np.linalg.solve(K, F)).flatten()

    return dict(elements=elements, DOF=DOF, LtoG=LtoG, solution=u,
                kappa=kappa, nodal_force_sum=nodal_force_sum)


def strain_field(cfg, elements, LtoG, solution, samples=400):
    out = []
    for e, element in enumerate(elements):
        x1, x2 = element.global_coordinates
        J = 0.5 * (x2 - x1)
        ue = solution[np.array(LtoG[e]).flatten()]
        xi = np.linspace(-1.0, 1.0, samples)
        pos = x1 + (xi + 1.0) * J
        eps = np.array([float(np.dot(evalDerivOfShapeFunct(cfg.p, t), ue)) / J for t in xi])
        out.append((pos, eps))
    return out


def displacement_at(cfg, elements, LtoG, solution, x_global):
    for e, element in enumerate(elements):
        x1, x2 = element.global_coordinates
        if x1 - 1e-12 <= x_global <= x2 + 1e-12:
            xi = 2 * (x_global - x1) / (x2 - x1) - 1
            N = evalShapeFunct(cfg.p, xi)
            return float(np.dot(N, solution[np.array(LtoG[e]).flatten()]))
    raise ValueError(f'{x_global} is not in the domain')


def run(cfg, samples=400):
    res = solve(cfg)
    elements, LtoG, u = res['elements'], res['LtoG'], res['solution']

    per_element = strain_field(cfg, elements, LtoG, u, samples)
    positions = np.concatenate([p for p, _ in per_element])
    strains = np.concatenate([s for _, s in per_element])

    xf0, xf1 = cfg.fictitious_span
    mask = (positions >= xf0) & (positions <= xf1)
    mean_field = float(np.trapezoid(strains[mask], positions[mask]) / (xf1 - xf0))

    ux = {x: displacement_at(cfg, elements, LtoG, u, x)
          for x in (0.0, xf0, xf1, cfg.L)}
    mean_disp = (ux[xf1] - ux[xf0]) / (xf1 - xf0)

    res.update(per_element=per_element, positions=positions, strains=strains,
               u=ux, mean_strain_field=mean_field, mean_strain_disp=mean_disp,
               samples=samples)
    return res