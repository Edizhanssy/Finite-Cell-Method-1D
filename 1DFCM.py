from Element.Element import Element
from Integration.polynomialDegreeSorting import PolynomialDegreeSorting
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Element.getLocationMatrix import setupPerElement
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct
from Element.StiffnessMatrix.AssembleStiffnessMatrix import assemble_global_stiffness_matrix
from Element.createEdgesandNodes import create_nodes_and_edges
from Element.ForceVector.assembleGlobalForceVector import assemble_Force_Vector
from BoundaryCondition.NodeStrongBoundaryCondition.ApplyBoundaryConditions import ApplyBoundaryConditions
from BoundaryCondition.PenaltyValueAlgorithm.StrongPenaltyAlgorithm import StrongPenaltyAlgorithm
from BoundaryCondition.NodeStrongBoundaryCondition.StrongNodeDirichlet import StrongNodeDirichletBoundaryCondition
import matplotlib.pyplot as plt
import numpy as np

# Properties !
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

# the initial elements has been constructed !!
elements = [Element(0, (global_to_local(0), global_to_local(L)), (0, L))]

nodes, edges, elements = create_nodes_and_edges(elements, number_of_x_divisions)

Nodes = []
Edges = []

# For this problem, we are considering higher order shape functions
PolynomialDegree = 11
NumberOfGaussPoints = PolynomialDegree + 1

DOF = []

# Partition each element
for element in elements:
    flattened_nodes = [node for element_nodes in nodes for node in element_nodes]
    flattened_edges = [edge for element_edges in edges for edge in element_edges]

    # Assigning DOFs
    sorting_scheme = PolynomialDegreeSorting(flattened_nodes, flattened_edges, PolynomialDegree, 1)
    DOF = sorting_scheme.assign_dofs()

print('the total Degree of Freedom of the whole domain: ', DOF)

print('the Gauss Points and Weights will be constructed based upon the desired polynomial degree')
for element in elements:
    element.gaussPoints = GaussQuadratureCoordinates(NumberOfGaussPoints)
    element.gaussWeights = GaussQuadratureWeights(NumberOfGaussPoints)

LtoG = setupPerElement(nodes[0], edges[0],  NumberOfGaussPoints, 1, number_of_x_divisions)
print('the location mapping matrix: ', LtoG)

print('the shape functions and their derivatives for each integration point will be calculated !!')
print('the integration points for each sub-domain will be also obtained from gauss points and local coordinates')

localtoglobal = lambda local_x, L: 0.5 * L * (local_x + 1)

print('the Global Stiffness Matrix will be calculated !!')
StiffnessMatrix = assemble_global_stiffness_matrix(elements, NumberOfGaussPoints, DOF, LtoG)

kappa = np.linalg.cond(StiffnessMatrix)
print('the ill-conditioning of the original stiffness matrix: ', kappa)

print('the Global Force Vector will be calculated !!')
ForceVector = assemble_Force_Vector(elements, NumberOfGaussPoints, DOF, LtoG)

print('the boundary conditions are obtained')
print('the strong penalty algorithm and strong dirichlet boundary conditions will be used')
print('the weak composition of the boundary conditions can also be in consideration; however, strong from is in considertation for this code !')

PenaltyAlgorithm = StrongPenaltyAlgorithm(10e4)
InitialFix = StrongNodeDirichletBoundaryCondition([0, 0 ,0], 0, 1, PenaltyAlgorithm)
DisplacementEnd = StrongNodeDirichletBoundaryCondition([3, 0, 0], -1, 1, PenaltyAlgorithm)

print('appending boundary conditions to the Force vector')
StiffnessMatrix, ForceVector = ApplyBoundaryConditions([nodes[0][0], nodes[0][2]], StiffnessMatrix, ForceVector, [InitialFix, DisplacementEnd])

print('SOLUTION !!')
solution = np.linalg.solve(StiffnessMatrix, ForceVector)
solution = np.array(solution).flatten()

print('POST-PROCESS')
print('Calculating Axial Strains')

Strains = []
position = []

for i, element in enumerate(elements):
    # Get local displacements for the current element
    local_indices = LtoG[i]
    local_displacements = solution[local_indices]
    # Initialize array to hold strains at each Gauss point for this element
    strains_at_gauss_points = []
    GP = GaussQuadratureCoordinates(NumberOfGaussPoints)
    # Calculate strain at each Gauss point
    for j, gp in enumerate(GP):
        # Derivative of shape functions at this Gauss point
        dN = evalDerivOfShapeFunct(PolynomialDegree, gp)
        strain_at_gauss_point = np.dot(dN, np.array(local_displacements).reshape(-1, 1))
        strains_at_gauss_points.append(strain_at_gauss_point)
    Strains.append(strains_at_gauss_points)

global_positions = np.linspace(0, 3, 24)
strains = np.squeeze([strain for strain in Strains]).flatten()

plt.plot(global_positions, strains, marker='o', label='Axial Strain Distribution')
plt.xlabel('Global Position')
plt.ylabel('Axial strain ε')
plt.title('Axial Strain Distribution along the Structure')
plt.grid(True)
plt.show()

















