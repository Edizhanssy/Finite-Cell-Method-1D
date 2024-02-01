# Finite-Cell-Method-1D
A basic implementation of Finite Cell Method for 1-D problems

For the more proper and detailed implementation, especially for the application of 2-dimensional and 3-dimensional problems, 
please refer to the FCMLAB code which is implemented in TUM as cited in the references [2]. You can get access to FCMLab from [1]. Thank you for their wonderful work, as an curious person I try to get the concept of Finite Cell Method (FCM), and with this valuable implementation, I tried to implement my own version for the problem case of Uni-Axial Rod Example from [3]. The implemetation and detail of the structure of the FCMLab is described in [2]. In the following figures, the solution of axial strain values over the whole rod, and from the code that I implemented is illustrated to show the validation of my code. If you have additional questions, please feel free to contact with me.

Reference Figure from [3]:

![ReferenceSolution](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1e897611-8220-46e7-8e4a-d40dfeac499e)


FCM-1D's solution:

![pythonresult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/1fa1a931-2658-4900-a7a7-8fa2315fee34)


Matlab Model's solution:

![ModelResult](https://github.com/Edizhanssy/Finite-Cell-Method-1D/assets/128889535/187777a7-6998-4625-8de2-f89f9209c3c3)


References:

[1]- “FCMLAB: A Finite Cell Research Toolbox for MATLAB,” GitLab, https://gitlab.lrz.de/cie_sam_public/fcmlab. 

[2]- Zander, N.; Bog, T; Elhaddad, M.; Espinoza, R.; Hu, H.; Joly, A.F.; Wu, C.; Zerbe, P.; Düster, A.; Kollmannsberger, S.; Parvizian, J.; Ruess, M.; Schillinger, D.; Rank, E. 
FCMLab: A Finite Cell Research Toolbox for MATLAB 
Advances in Engineering Software 74, pp. 49-63, 2014 
DOI: 10.1016/j.advengsoft.2014.04.004 
https://www.sciencedirect.com/science/article/abs/pii/S0965997814000684

[3]- D. Schillinger, A. Düster, and E. Rank, "The hp-d-adaptive finite cell method for geometrically nonlinear problems of solid mechanics," International Journal for Numerical Methods in Engineering, vol. 89, no. 9, pp. 1171-1202, 2012, https://doi.org/10.1002/nme.3289
