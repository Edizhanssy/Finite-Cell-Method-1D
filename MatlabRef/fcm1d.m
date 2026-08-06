clear all;

NumberOfXDivisions = 2;
PolynomialDegree = 11;
NumberGP = PolynomialDegree+1; % number of Gauss points
DofDimension = 1;

E = 1;      % Young's modulus
A = 1;      % cross-sectional area
L = 3;      % length
Density = 1;

Mat1D = Hooke1D(A,E,Density,1);
Mat2D = Hooke1D(A,E,Density,1e-8);
MatD = [Mat1D Mat2D]; % to make it work with FCM

MeshOrigin = [0];

domain = Rod(L);

vertex1 = Vertex([0.0 0.0 0.0]);
vertex2 = Vertex([3.0 0.0 0.0]);
overallDomain = Line(vertex1,vertex2);

SpaceTreeDepth = 20;

BoundaryFactory = BoundaryRecoveryFactory(domain,overallDomain,SpaceTreeDepth,0);

ElementFactory = ElementFactoryElasticBar(MatD, NumberGP, domain, SpaceTreeDepth);

MyMeshFactory = MeshFactory1DUniform(NumberOfXDivisions,...
        PolynomialDegree,PolynomialDegreeSorting(),1,...
        MeshOrigin,L,ElementFactory);

MyAnalysis = QuasiStaticAnalysis(MyMeshFactory);

BoundaryFactory.visualizeDomain();

% Adding line load

LoadCase = LoadCase();

MyAnalysis.addLoadCases(LoadCase);

FeMesh = MyAnalysis.getMesh();

% Adding Dirichlet boundary conditions
MyDirichletAlgorithm = StrongPenaltyAlgorithm(10E4);

PointSupport = StrongNodeDirichletBoundaryCondition([0 0 0],0,1,MyDirichletAlgorithm);
PointDisplacement = StrongNodeDirichletBoundaryCondition([3 0 0],-1,1,MyDirichletAlgorithm);

MyAnalysis.addDirichletBoundaryCondition(PointSupport);
MyAnalysis.addDirichletBoundaryCondition(PointDisplacement);

SolutionVector = MyAnalysis.solve();

K = full(MyAnalysis.getK);
kappa = cond(K);
TotalStrainEnergyPFEM = MyAnalysis.getStrainEnergy;

loadCaseToVisualize = 1;
indexOfPhysicalDomain = 2;

gridSize = 0.05;

postProcessingFactory = VisualPostProcessingFactory1D( gridSize );
postProcessor = postProcessingFactory.creatVisualPostProcessor( );

postProcessor.registerPointProcessor( @axialStrain, { loadCaseToVisualize, indexOfPhysicalDomain } );

postProcessor.visualizeResults( MyAnalysis.getMesh() );




