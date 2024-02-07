# Finite-Cell-Method-1D
A basic implementation of Finite Cell Method for 1-D problems

Python IDE: PyCharm

In the following figure, the problem model is illusrated as state in [3], the geometric and material properties are also illustrated in the figure, as you can see it consists of two rod which are having
fictitious domain between them so the problem is actually for analyzing the behaviour between these two separate integrated rods with fictitious domain. The first discretization, as stated in the figure, is made with
two elements and after that the spatial-parititoning and adaptive quadrature is made accordingly. The details can be found in the code as comments.

![model](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/cdcf2746-4f4c-4b28-8512-8302a813a203)

                      Figure 1: the problem model of uni-axial rod [3]


For the more proper and detailed implementation, especially for the application of 2-dimensional and 3-dimensional problems, 
please refer to the FCMLAB code which is implemented in TUM as cited in the references [2]. You can get access to FCMLab from [1]. Thank you for their wonderful work, as an curious person I try to get the concept of Finite Cell Method (FCM), and with this valuable implementation, I tried to implement my own version for the problem case of Uni-Axial Rod Example from [3]. The implemetation and detail of the structure of the FCMLab is described in [2]. In the following figures, the solution of axial strain values over the whole rod, and from the code that I implemented is illustrated to show the validation of my code. If you have additional questions, please feel free to contact with me.




Reference Figure from [3]:

![ReferenceSolution](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1e897611-8220-46e7-8e4a-d40dfeac499e)

                      Figure 2: the reference solution of uni-axial rod model [3]

FCM-1D's solution:

![pythonresult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1fa1a931-2658-4900-a7a7-8fa2315fee34)

                      Figure 2: the solution from my python code

MATLAB Model's solution:

![ModelResult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/187777a7-6998-4625-8de2-f89f9209c3c3)

                      Figure 3: the solution from my the MATLAB model that I created
                      
Note: As you can see the even though the behaviour of the solutions are very close to each other the values are higher then the reference solution. I am still working on this issue to solve the problem. However, since it is an linear-static analysis, the behaviour that we get from both MATLAB and Python codes validates my approach compared to reference solution. Possible issue can be the fact that the model has some differences between them in terms of boundary conditions or properties even though the model in the both MATLAB and python codes are constructed very carefully.


# References:

[1]- “FCMLAB: A Finite Cell Research Toolbox for MATLAB,” GitLab, https://gitlab.lrz.de/cie_sam_public/fcmlab. 

[2]- Zander, N.; Bog, T; Elhaddad, M.; Espinoza, R.; Hu, H.; Joly, A.F.; Wu, C.; Zerbe, P.; Düster, A.; Kollmannsberger, S.; Parvizian, J.; Ruess, M.; Schillinger, D.; Rank, E. 
FCMLab: A Finite Cell Research Toolbox for MATLAB 
Advances in Engineering Software 74, pp. 49-63, 2014 
DOI: 10.1016/j.advengsoft.2014.04.004 
https://www.sciencedirect.com/science/article/abs/pii/S0965997814000684

[3]- D. Schillinger, A. Düster, and E. Rank, "The hp-d-adaptive finite cell method for geometrically nonlinear problems of solid mechanics," International Journal for Numerical Methods in Engineering, vol. 89, no. 9, pp. 1171-1202, 2012, https://doi.org/10.1002/nme.3289
