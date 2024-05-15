import numpy as np
from tqdm import tqdm

import numqi

np_rng = np.random.default_rng()
hf_randc = lambda *size: np_rng.normal(size=size) + 1j*np_rng.normal(size=size)

def demo_matrix_subspace_real_complex_field_1qubit():
    matrix_subspace = np.stack([numqi.gate.PauliOperator.from_str(x).full_matrix for x in 'XZ'])

    # XZ_R
    basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(matrix_subspace, field='real')
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,1,0))
    theta_optim010 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,2,0))
    theta_optim020 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,1,1))
    theta_optim011 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    matH,coeff,residual = model.get_matrix(matrix_subspace)
    print(f'space={space_char} basis.shape={basis.shape} basis_orth.shape={basis_orth.shape}')
    print(f'loss(010): {theta_optim010.fun}') #1.0
    print(f'loss(020): {theta_optim020.fun}') #1.0
    print(f'loss(011): {theta_optim011.fun}, residual={residual}') #1e-9
    # space=R_T basis.shape=(2, 2, 2) basis_orth.shape=(1, 2, 2)
    # loss(010): 0.9999999999999971
    # loss(020): 1.0000000672122786
    # loss(011): 3.222853017830347e-26, residual=1.6095880932274593e-26

    # XZ_C
    basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(matrix_subspace, field='complex')
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=1)
    theta_optim1 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    matH,coeff,residual = model.get_matrix(matrix_subspace)
    print(f'space={space_char} basis.shape={basis.shape} basis_orth.shape={basis_orth.shape}')
    print(f'loss(1): {theta_optim1.fun}, residual={residual}') #1e-9
    # space=C_T basis.shape=(2, 2, 2) basis_orth.shape=(1, 2, 2)
    # loss(1): 8.314191254116187e-15, residual=4.1570956204761624e-15


def demo_matrix_space_real_complex_field_2qubit():
    pauli_str = 'XX XY'.split(' ')
    matrix_subspace = np.stack([numqi.gate.PauliOperator.from_str(x).full_matrix for x in pauli_str])

    # span_R(C_H)
    basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(matrix_subspace, field='real')

    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,3,1))
    theta_optim031 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,4,0))
    theta_optim040 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=(0,2,2))
    theta_optim022 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    matH,coeff,residual = model.get_matrix(matrix_subspace)
    print(f'space={space_char} basis.shape={basis.shape} basis_orth.shape={basis_orth.shape}')
    print(f'loss(031): {theta_optim031.fun}') #0.5
    print(f'loss(040): {theta_optim040.fun}') #1.0
    print(f'loss(022): {theta_optim022.fun}, residual={residual}') #1e-9

    # span_C(C_H)
    basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(matrix_subspace, field='complex')

    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=1)
    theta_optim1 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=2)
    theta_optim2 = numqi.optimize.minimize(model, 'normal', num_repeat=3, tol=1e-7)
    matH,coeff,residual = model.get_matrix(matrix_subspace)
    print(f'space={space_char} basis.shape={basis.shape} basis_orth.shape={basis_orth.shape}')
    print(f'loss(1): {theta_optim1.fun}') #0.5
    print(f'loss(2): {theta_optim2.fun}, residual={residual}') #0


def demo_hierarchical_method_random_matrix_subspace():
    dimA = 4
    dimB = 4
    rank = 2
    hierarchy_k = 2
    num_matrix = 9 #(da-rank+1)(db-rank+1)
    ret = []
    for _ in tqdm(range(int(100))):
        matrix_space = [hf_randc(dimA,dimB) for _ in range(num_matrix)]
        ret.append(numqi.matrix_space.has_rank_hierarchical_method(matrix_space, rank, hierarchy_k))
