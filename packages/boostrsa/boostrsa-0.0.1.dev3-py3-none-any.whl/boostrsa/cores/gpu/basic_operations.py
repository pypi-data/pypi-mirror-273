
from numba import cuda, jit

@cuda.jit
def outer_sum(matrices, out):
    i = cuda.grid(1)

    if i < len(matrices):
        matrix = matrices[i]

        for m_line in matrix:
            for j, e1 in enumerate(m_line):
                for k, e2 in enumerate(m_line):
                    out[i][j][k] += e1 * e2

@cuda.jit
def outer_sum_square(matrices, out):
    i = cuda.grid(1)

    if i < len(matrices):
        matrix = matrices[i]

        for m_line in matrix:
            for j, e1 in enumerate(m_line):
                for k, e2 in enumerate(m_line):
                    out[i][j][k] += (e1 * e2) ** 2

@cuda.jit
def scaling(out, lambs):
    i = cuda.grid(1)
    lamb = lambs[i]

    nd = out.shape[0]
    nr = out.shape[1]
    nc = out.shape[2]

    if i < len(out):
        for j in range(nr):
            for k in range(nc):
                if j != k:
                    out[i][j][k] = (1 - lamb)

@cuda.jit(device=True, inline=True)
def matmul(a,b, out):
    """
    Matrix multiplication a @ b
    
    :param a(np.array): 2d matrix
    :param b(np.array): 2d matrix
    :param out(device array): output
    """
    ar,ac = a.shape 
    br,bc = b.shape 
    
    for i in range(ar):
        for j in range(bc):
            for k in range(ac): # or br
                out[i,j] += a[i,k] * b[k,j]
    return out


