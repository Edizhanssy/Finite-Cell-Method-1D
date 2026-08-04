from Element.Element import Element
from Integration.DOFPartitioning import DOFPartitioning
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Element.LocationMatrix import setupPerElement
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct
from Element.StiffnessMatrix.AssembleStiffnessMatrix import assemble_global_stiffness_matrix
from Element.createEdgesandNodes import create_nodes_and_edges
from Element.ForceVector.assembleGlobalForceVector import assemble_Force_Vector
from BoundaryCondition.NodeStrongBoundaryCondition.ApplyBoundaryConditions import ApplyBoundaryConditions
from BoundaryCondition.PenaltyValueAlgorithm.StrongPenaltyAlgorithm import StrongPenaltyAlgorithm
from BoundaryCondition.NodeStrongBoundaryCondition.StrongNodeDirichlet import StrongNodeDirichletBoundaryCondition
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalShapeFunct
import matplotlib.pyplot as plt
import numpy as np

# Properties!
L = 3 # length
E = 1 # elastic modulus
density = 1
A = 1 # Area
ScalingFactor = 1e-8
startnode = 0 # location of the first node of fictitious domain
endnode = 7/3 # location of the end node of fictitious domain
number_of_x_divisions = 2 # the initial division of the overall rod

# Define the domain boundaries in global coordinates
global_domain_boundaries = [(0, 1), (1, 7/3), (7/3, 3)]

# Convert global coordinates to local coordinates
global_to_local = lambda x: (2 * x - L) / L

# Convert domain boundaries to local coordinates
local_domain_boundaries = [(global_to_local(start), global_to_local(end)) for start, end in global_domain_boundaries]

print('the boundaries in local coordinates [-1, 1]: ', local_domain_boundaries)

# Initial line segment in local coordinates
initial_line_segment = (global_to_local(startnode), global_to_local(endnode))

# The initial elements have been constructed !!
elements = [Element(0, (global_to_local(0), global_to_local(L)), (0, L))]

nodes, edges, elements = create_nodes_and_edges(elements, number_of_x_divisions)

Nodes = []
Edges = []

# For this problem, we are considering higher-order shape functions
PolynomialDegree = 15
NumberOfGaussPoints = PolynomialDegree + 1

DOF = []

# Partition each element
for element in elements:
    flattened_nodes = [node for element_nodes in nodes for node in element_nodes]
    flattened_edges = [edge for element_edges in edges for edge in element_edges]

    # Assigning DOFs
    sorting_scheme = DOFPartitioning(flattened_nodes, flattened_edges, PolynomialDegree, 1)
    DOF = sorting_scheme.assign_all_dofs()

print('the total Degree of Freedom of the whole domain: ', DOF)

print('the Gauss Points and Weights will be constructed based upon the desired polynomial degree')
for element in elements:
    element.gaussPoints = GaussQuadratureCoordinates(NumberOfGaussPoints)
    element.gaussWeights = GaussQuadratureWeights(NumberOfGaussPoints)

LtoG = setupPerElement(nodes[0], edges[0],  NumberOfGaussPoints, 1, number_of_x_divisions)
print('the location mapping matrix: ', LtoG)

print('the shape functions and their derivatives for each integration point will be calculated !!')
print('the integration points for each sub-domain will be also obtained from gauss points and local coordinates')

print('the Global Stiffness Matrix will be calculated !!')
StiffnessMatrix = assemble_global_stiffness_matrix(elements, NumberOfGaussPoints, DOF, LtoG)

#kappa = np.linalg.cond(StiffnessMatrix)
#print('the ill-conditioning of the original stiffness matrix: ', kappa)

print('the Global Force Vector will be calculated !!')
ForceVector = assemble_Force_Vector(elements, NumberOfGaussPoints, DOF, LtoG)

print(f'nodal DOF force sum = {ForceVector[[0,1,2],0].sum():.3e}   expected ~0')

print('the boundary conditions are obtained')
print('the strong penalty algorithm and strong dirichlet boundary conditions will be used')
print('the weak composition of the boundary conditions can also be in consideration; however, strong from is in considertation for this code !')

PenaltyAlgorithm = StrongPenaltyAlgorithm(10e4)
InitialFix = StrongNodeDirichletBoundaryCondition([0, 0 ,0], 0, 1, PenaltyAlgorithm)
DisplacementEnd = StrongNodeDirichletBoundaryCondition([3, 0, 0], -1, 1, PenaltyAlgorithm)

print('appending boundary conditions to the Force vector')
StiffnessMatrix, ForceVector = ApplyBoundaryConditions([nodes[0][0], nodes[0][2]], StiffnessMatrix, ForceVector, [InitialFix, DisplacementEnd])

kappa = np.linalg.cond(StiffnessMatrix)
print('the ill-conditioning of the original stiffness matrix: ', kappa)

print('SOLUTION !!')
solution = np.linalg.solve(StiffnessMatrix, ForceVector)
solution = np.array(solution).flatten()


print('POST-PROCESS')
print('Calculating Axial Strains')

samples = 400
strains = []
positions = []

for e, element in enumerate(elements):
    x1, x2 = element.global_coordinates
    J = 0.5 * (x2 - x1)
    ue = solution[np.array(LtoG[e]).flatten()]
    xi = np.linspace(-1.0, 1.0, samples)
    pos_e = x1 + (xi + 1.0) * J
    eps_e = np.array([float(np.dot(evalDerivOfShapeFunct(PolynomialDegree, x), ue)) / J
                      for x in xi])
    plt.plot(pos_e, eps_e, lw=1.2, color='tab:blue')
    positions.append(pos_e)
    strains.append(eps_e)

positions = np.concatenate(positions)
strains = np.concatenate(strains)

m = (positions >= 1.0) & (positions <= 7/3)
mean_eps = np.trapezoid(strains[m], positions[m]) / (7/3 - 1.0)
print(f'mean strain (from strain field) = {mean_eps:8.5f}   expected -0.75')

plt.axhline(-0.75, ls='--', lw=0.8, color='gray')
plt.axvspan(1.0, 7/3, alpha=0.12, color='gray')
plt.xlabel('Global Position')
plt.ylabel('Axial strain')
plt.title('Axial Strain Distribution along the uni-axial rod')
plt.grid(True)
plt.show()

print('element 1 right end:', strains[samples-1], '| element 2 left end:', strains[samples])

def u_at(x_global):
    for e, element in enumerate(elements):
        x1, x2 = element.global_coordinates
        if x1 - 1e-12 <= x_global <= x2 + 1e-12:
            xi = 2 * (x_global - x1) / (x2 - x1) - 1
            N = evalShapeFunct(PolynomialDegree, xi)
            return float(np.dot(N, solution[np.array(LtoG[e]).flatten()]))
    raise ValueError(f'{x_global} is not in the domain')

u0, u1, u2, u3 = u_at(0.0), u_at(1.0), u_at(7/3), u_at(3.0)
print(f'u(0)   = {u0:12.6e}   expected  0')
print(f'u(1)   = {u1:12.6e}   expected  0')
print(f'u(7/3) = {u2:12.6e}   expected -1')
print(f'u(3)   = {u3:12.6e}   expected -1')
print(f'mean strain in fictitious = {(u2 - u1) / (7/3 - 1):8.5f}   expected -0.75')





