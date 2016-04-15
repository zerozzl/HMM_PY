# coding: UTF-8
import numpy as np

def calc_forward_prob(N, M, T, pi, A, B, O):
    alpha = np.zeros((N, T));
    for i in range(N):
        alpha[i, 0] = pi[i] * B[i, O[0]];
    
    for t in range(1, T, 1):
        for j in range(N):
            for i in range(N):
                alpha[j, t] += alpha[i, t - 1] * A[i, j];
            alpha[j, t] *= B[j, O[t]];
    
    prob = np.sum(alpha[:, T - 1]);
    return prob, alpha;


def calc_backward_prob(N, M, T, pi, A, B, O):
    beta = np.zeros((N, T));
    beta[:, T - 1] = 1;
    
    for t in range(T - 2, -1, -1):
        for i in range(N):
            for j in range(N):
                beta[i, t] += A[i, j] * beta[j, t + 1] * B[j, O[t + 1]];
    
    return beta;

def calc_gamma(N, T, alpha, beta):
    gamma = np.zeros((N, T));
    
    for t in range(T):
        sum = 0;
        for i in range(N):
            gamma[i, t] = alpha[i, t] * beta[i, t];
            sum += gamma[i, t];
        gamma[:, t] /= sum;
        
    return gamma;

def calc_zeta(N, T, A, B, O, alpha, beta):
    zeta = np.zeros((T - 1, N, N));
    
    for t in range(T - 1):
        sum = 0;
        for i in range(N):
            for j in range(N):
                zeta[t, i, j] = alpha[i, t] * A[i, j] * B[j, O[t + 1]] * beta[j, t + 1];
                sum += zeta[t, i, j];
        zeta[t, :, :] /= sum;
    
    return zeta;;

def compute(N, M, T, O, DELTA):
    A = np.random.random((N, N));
    B = np.random.random((N, M));
    pi = np.random.random(N);

    prob_pre, alpha = calc_forward_prob(N, M, T, pi, A, B, O);
    beta = calc_backward_prob(N, M, T, pi, A, B, O);
    gamma = calc_gamma(N, T, alpha, beta);
    zeta = calc_zeta(N, T, A, B, O, alpha, beta);
    
    delta = 1;
    while(delta > DELTA):
        print delta;
        # E-step
        pi = 0.001 + 0.999 * gamma[:, 0];
          
        for i in range(N):
            gamma_i_sum = np.sum(gamma[i, 0:T - 1]);
            for j in range(N):
                A [i, j] = np.sum(zeta[:, i, j]) / gamma_i_sum;
        A = 0.001 + 0.999 * A;
        
        for j in range(N):
            gamma_j_sum = np.sum(gamma[j, :]);
            for k in range(M):
                numerator = 0.0;
                for t in range(T):
                    if O[t] == k:
                        numerator += gamma[j, t];
                B[j, k] = numerator / gamma_j_sum;
        B = 0.001 + 0.999 * B;
        
        prob_cur, alpha = calc_forward_prob(N, M, T, pi, A, B, O);
        beta = calc_backward_prob(N, M, T, pi, A, B, O);
        gamma = calc_gamma(N, T, alpha, beta);
        zeta = calc_zeta(N, T, A, B, O, alpha, beta);
        
        delta = prob_cur - prob_pre;
    
def unit_testing():
    O = [0, 1, 0];
    T = len(O);
    M = len(set(O));
    N = 3;
    
    DELTA = 0.001
    
    compute(N, M, T, O, DELTA);

unit_testing();
