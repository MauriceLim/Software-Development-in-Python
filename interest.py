import numpy as np
from scipy.linalg import solve_triangular

def continuous_to_annual(r: float) -> float:
    annual = np.exp(r) - 1
    return annual
    
def annual_to_continuous(i: float) -> float:
    cont = np.log(1+i)
    return cont
    
def annual_to_mthly(i: float, m: int) -> float:
    mthly = m*((1+i)**(1/m)-1)
    return mthly
    
def mthly_to_annual(i: float, m: int) -> float:
    annual = (1+i/m)**m - 1
    return annual
    
def zcb_to_continuous(z: float, t: float) -> float:
    annual = (1/z)**(1/t) - 1
    cont =  annual_to_continuous(annual)
    return cont
    
def continuous_to_zcb(r: float, t: float) -> float:
    annual = continuous_to_annual(r)
    zcb = 1/(1+annual)**t 
    return zcb

def bootstrap(par_yields: 'np.ndarray', tenors: 'np.ndarray') -> 'tuple[np.ndarray, np.ndarray]':
    
    if len(par_yields) != len(tenors):
        raise ValueError("Mismatch between the number of par yields and lengths of tenors")

    # Check if tenors are strictly monotonic increasing
    if not np.all(np.diff(tenors) > 0):
        raise ValueError("Tenors are not strictly monotonic increasing")
    
    one = []
    for i in range(len(par_yields)):
        one.append(1)

    e = []
    for i in range(len(par_yields)):
        e.append([])
        for j in range(len(par_yields)):
            if j <= i:
                e[i].append(par_yields[i]/2)
            else:
                e[i].append(0)

    original = np.array(e)
    matrix_size = original.shape[0]
    diagonal_matrix = np.eye(matrix_size)
    result_matrix = original + diagonal_matrix

    x = solve_triangular(result_matrix, one, lower=True)
    return (x,np.array(tenors))

def zcb(t: float, curve: 'tuple[np.ndarray, np.ndarray]') -> float:
    
    #binary search to find the index of the number (not in the array) between 2 numbers 
    def binary_search(arr, target):
        
        if target < arr[0]:
            raise ValueError("Target is below the minimum value in the array")
        elif target > arr[-1]:
            raise ValueError("Target is above the maximum value in the array")

        low, high = 0, len(arr) -1     
        
        while low < high: 
            mid = (low+high)//2
            if arr[mid] < target:
                low = mid + 1
            else:
                high = mid

        return low-1, low
    
    for i in range(len(curve[1])):
        if t == curve[1][i]:
            return curve[0][i]
    
    #if not t not in the curve, linear interpolation
    low, up = binary_search(curve[1],t)  
    linear_interpolate = (curve[0][low]*(curve[1][up]-t)+curve[0][up]*(t-curve[1][low]))/(curve[1][up]-curve[1][low])
    return linear_interpolate

def annuity(n: int, i: float) -> float:
    p = (1 - (1+i)**(-n))/i
    return p