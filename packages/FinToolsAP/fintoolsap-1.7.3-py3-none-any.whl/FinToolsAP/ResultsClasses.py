import numpy

class PCAResults:

    def __init__(self, L, Q, PC, var_expl) -> None:
    
        self.eigenvalues =          L
        self.eigenvectors =         Q
        self.variance_explained =   var_expl
        self.principal_components = PC

    def __str__(self) -> str:
        print('Todo')