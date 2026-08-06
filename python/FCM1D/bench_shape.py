import time
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct

N = 200
t = time.perf_counter()
for _ in range(N):
    evalDerivOfShapeFunct(15, 0.3)
dt = time.perf_counter() - t
print(f"{N} calls: {dt:.4f} s  ->  {dt/N*1e6:.1f} us per call")