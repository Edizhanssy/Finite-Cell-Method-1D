# Finite-Cell-Method-1D
This repository presents a basic implementation of the Finite Cell Method (FCM) for 1-D problems.

Development Environment: Python IDE (PyCharm)

The figure below illustrates the problem model as stated in [3], including geometric and material properties. It features two rods separated by a fictitious domain, thereby analyzing the behavior across these two integrated rods with a fictitious domain in between. Initial discretization is performed using two elements, followed by spatial partitioning and adaptive quadrature as detailed in the figure. For further insights, refer to the code comments.

![model](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/cdcf2746-4f4c-4b28-8512-8302a813a203)

                      Figure 1: the problem model of uni-axial rod [3]

The penalization factor is set to 10^-8, chosen by assigning the q-value as -8. To simplify, the sine load was not applied to the first physical domain.

For a more comprehensive and detailed implementation, particularly for 2D and 3D problems, refer to the FCMLAB code developed at TUM, as cited in the references [1]. As an enthusiastic engineer exploring the Finite Cell Method (FCM), I leveraged the FCMLAB's implementation to conceptualize and develop my version for the Uni-Axial Rod Example from [3]. If you want to look for the structure, the structure of the implementation fo FCMLAB described in [2]. My approach began with understanding the fictitious domain method and advancing to implement my p-version based FEM. Despite encountering instabilities and unvalidated solutions with similar characteristics, thorough analysis of FCMLAB's approach to Degree of Freedom (DOF) partitioning, node and edge initialization, and integration parts (adaptive quadrature) has been insightful. I am committed to refining my solutions and distinguishing my code from FCMLAB.

The figures below depict axial strain values across the entire rod, demonstrating my code's validation. For additional inquiries, please feel free to contact me.

Reference Figure from [3]

![ReferenceSolution](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1e897611-8220-46e7-8e4a-d40dfeac499e)

                      Figure 2: the reference solution of uni-axial rod model [3]

FCM-1D's solution

![pythonresult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1fa1a931-2658-4900-a7a7-8fa2315fee34)

                      Figure 2: the solution from my python code

MATLAB Model's solution

![ModelResult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/187777a7-6998-4625-8de2-f89f9209c3c3)

                      Figure 3: the solution from my the MATLAB model that I created
                      
Note: As observed, although the behaviors of the solutions are very closely aligned, the values are higher than those in the reference solution. I am diligently working to address this discrepancy. It's important to note that, as this is a linear-static analysis, the congruence in behavior between the MATLAB and Python implementations and the reference solution validates my approach. The discrepancy in values may be attributed to subtle differences in boundary conditions or material properties between the models, despite meticulous construction in both the MATLAB and Python codes.

# References

[1]- “FCMLAB: A Finite Cell Research Toolbox for MATLAB,” GitLab, https://gitlab.lrz.de/cie_sam_public/fcmlab. 

[2]- Zander, N.; Bog, T; Elhaddad, M.; Espinoza, R.; Hu, H.; Joly, A.F.; Wu, C.; Zerbe, P.; Düster, A.; Kollmannsberger, S.; Parvizian, J.; Ruess, M.; Schillinger, D.; Rank, E. 
FCMLab: A Finite Cell Research Toolbox for MATLAB 
Advances in Engineering Software 74, pp. 49-63, 2014 
DOI: 10.1016/j.advengsoft.2014.04.004 
https://www.sciencedirect.com/science/article/abs/pii/S0965997814000684

[3]- D. Schillinger, A. Düster, and E. Rank, "The hp-d-adaptive finite cell method for geometrically nonlinear problems of solid mechanics," International Journal for Numerical Methods in Engineering, vol. 89, no. 9, pp. 1171-1202, 2012, https://doi.org/10.1002/nme.3289
