import numpy as np

def calculate_parameters(e, k_1, k_2, a):
    c_1 = k_1 / (1 + e + k_1)
    v_1 = (1 - c_1) / (1 + e)
    s_1 = e * v_1
    c_2 = k_2 / (1 + e + k_2)
    v_2 = (1 - c_2) / (1 + e)
    s_2 = e * v_2
    b = 1 - a
    M_11 = c_1
    M_12 = c_2
    M_21 = (b * s_1 * c_1 + v_1) / (1 - b * s_2)
    M_22 = (b * s_1 * c_2 + v_2) / (1 - b * s_2)
    return M_11, M_12, M_21, M_22, c_1, v_1, s_1, c_2, v_2, s_2

def calculate_eigenvalues(M_11, M_12, M_21, M_22):
    mu_1 = 0.5 * (M_11 + M_22 + np.sqrt((M_11 - M_22) ** 2 + 4 * M_12 * M_21))
    mu_2 = 0.5 * (M_11 + M_22 - np.sqrt((M_11 - M_22) ** 2 + 4 * M_12 * M_21))
    return mu_1, mu_2

def calculate_growth_rates(mu_1, mu_2, M_11, M_12):
    m_11 = 1
    m_12 = (mu_1 - M_11) / M_12 * m_11
    m_21 = 1
    m_22 = -(M_11 - mu_2) / M_12 * m_21
    return m_11, m_12, m_21, m_22

def calculate_r1(m_11, m_12, m_21, m_22, y_1i, y_2i):
    return (m_22 * y_1i - m_21 * y_2i) / (m_11 * m_22 - m_12 * m_21)

def calculate_transformation_vectors(m_11, m_12, m_21, m_22, y_1i, y_2i):
    P = np.array([[m_11, m_21], [m_12, m_22]])
    P_inverse = np.linalg.inv(P)
    y_vec = np.array([[y_1i], [y_2i]])
    eta_vec = np.matmul(P_inverse, y_vec)
    t_range = np.linspace(-3, 14, 1000)
    return eta_vec, t_range

def calculate_transformation_vectors(m_11, m_12, m_21, m_22, y_1i, y_2i):
    P = np.array([[m_11, m_21], [m_12, m_22]])
    P_inverse = np.linalg.inv(P)
    y_vec = np.array([[y_1i], [y_2i]])
    eta_vec = np.matmul(P_inverse, y_vec)
    return eta_vec

def calculate_exponentials(mu_1, mu_2, t_range, k_1, k_2, r_l, m_11, m_12):
    exp_1 = (1 / mu_1) ** t_range
    if k_2 > k_1:
        exp_2 = (-1 / mu_2) ** t_range
        exp_2 = exp_2 * np.cos(np.pi * t_range)
    else:
        exp_2 = 1 / mu_2 ** t_range
    z_l1 = r_l * m_11 * exp_1
    z_l2 = r_l * m_12 * exp_1
    return exp_1, exp_2, z_l1, z_l2