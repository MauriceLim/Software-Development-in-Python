import numpy as np 
from scipy import linalg

def payoff_call(S,K):
    return np.maximum(S - K, 0)

def payoff_put(S, K):
    return np.maximum(K - S, 0)

class BlackScholesPDESolver(object):
    def __init__(self, S0, Smax, K, T, r, q, sigma, M, N):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.q = q
        self.sigma = sigma
        self.M = M # height 
        self.N = N # lenght

        self.Smax = Smax
        self.grid_S = np.linspace(0, self.Smax, M + 1)  # Spatial grid
        self.F = np.zeros((self.M+1, self.N+1)) # base grid
        self.i = np.arange(N) # horizontal
        self.j = np.arange(M) # vertical
        self.dt = T / N
        self.dS = Smax / M
        
    def _initialize_boundary_conditions(self, payoff_function):
    
        # terminal values (at the end of the griud) | "time" = terminal
        self.time_bound = payoff_function(self.grid_S, self.K)
        
        # bottom/top values (depending if they are call/puts) 
        self.upper_or_lower_bound = payoff_function(self.Smax, self.K) * \
        np.exp(-(self.r - self.q) * self.dt * (self.N - self.i))  
        
    def _GridBoundaryStructure_(self, option_type, payoff_function):
        
        self._initialize_boundary_conditions(payoff_function)

        # if the option type is call, place boundary in the bottom
        if option_type == "call":
            self.F[-1, :-1] = self.upper_or_lower_bound
        elif option_type == "put":
            self.F[0, :-1] = self.upper_or_lower_bound
        else: 
            raise ValueError("Invalid option type. Use 'call' or 'put'.")
            
        # filling grid with terminal value (@ expiration)
        self.F[:, -1] = self.time_bound            
    
    def _ComputeCoeff_(self):
        
        # coefficient a
        self.a = (1/2) * (self.dt) * (
            ((self.r - self.q)*self.j) - ((self.sigma*self.j)**2) 
        ) 
        # coefficient b
        self.b = 1 + self.dt*(
            ((self.sigma*self.j)**2) + self.r
        )
        # coefficient c
        self.c = -(1/2) * (self.dt) * (
            ((self.r - self.q)*self.j) + ((self.sigma*self.j)**2)
        )
        
    def _computeCoeffMatrix_(self):
        
        # get the coeff values
        self._ComputeCoeff_()
        
        # create matrix of coefficients
        self.matrix_coeff = np.zeros((3, self.M-1))
        # fill coefficient matrix (3x(M-1) matrix)
        self.matrix_coeff[2, :-1] = self.a[2:self.M]
        self.matrix_coeff[1, :] = self.b[1:self.M]     
        self.matrix_coeff[0, 1:] = self.c[1:self.M-1]
    
    def _getSystemSolved_(self, payoff_function, option_nature = "european"):
        
        self._computeCoeffMatrix_()
        
        # iteration over each N value
        for i in reversed(range(self.N)):
            
            # right hand side grid matrix
            F_rhs = self.F[1:self.M, i+1]
            
            # updating first rhs value
            F_rhs[0] -= self.a[1] * self.F[0, i]
            
            # solve the linear system with the banded matrix
            self.F[1:self.M, i] = linalg.solve_banded((1, 1), self.matrix_coeff, F_rhs)
            
            # check for early exercise 
            if option_nature == "american":
                for j in range(1, self.M):
                    # early exe
                    early_exercise = payoff_function(
                        self.grid_S[j], self.K
                    )
                    # update grid value
                    self.F[j, i] = max(self.F[j, i], early_exercise)      
                    
        return self.F
    
    def get_val(self, payoff_function, option_type, option_nature):
        
        self._GridBoundaryStructure_(option_type, payoff_function)

        final_grid = self._getSystemSolved_(payoff_function, option_nature)
        
        final_price = np.interp(self.S0, self.grid_S, final_grid[:,0])
        
        return final_price