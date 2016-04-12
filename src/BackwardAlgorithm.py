# coding: UTF-8
import numpy as np

def calc_prob(N, M, pi, A, B, O):
    T = len(O);
    beta = np.zeros((N, T));
    beta[:, T - 1] = 1;
    
    for t in range(T - 2, -1, -1):
        for i in range(N):
            for j in range(N):
                beta[i, t] += A[i, j] * beta[j, t + 1] * B[j, O[t + 1]];
    
    prob = 0;
    for i in range(N):
        prob += pi[i] * beta[i, 0] * B[i, O[0]];
    
    return prob, beta;

def unit_testing():
#     '''
#     0:Sunny, 1:Cloudy, 2:Rainy
#     '''
#     N = 3;
#     
#     '''
#     0:Dry, 1:Dryish, 2:Damp, 3:Soggy
#     '''
#     M = 4;
#         
#     '''
#     initial state: P(Sunny)=0.63, P(Cloudy)=0.17, P(Rainy)=0.20
#     '''
#     pi = [0.63, 0.17, 0.2];
#     
#     '''
#                         weather today
#                      Sunny  Cloudy  Rainy
#     weather   Sunny  0.500  0.375   0.125
#     yesterday Cloudy 0.250  0.125   0.625
#               Rainy  0.250  0.375   0.375
#     '''
#     A = np.mat([[0.5, 0.375, 0.125],
#                 [0.25, 0.125, 0.625],
#                 [0.25, 0.375, 0.375]]);
#     
#     '''
#                        observed states
#                    Dry   Dryish  Damp  Soggy
#     hidden  Sunny  0.60  0.20    0.15  0.05
#     states  Cloudy 0.25  0.25    0.25  0.25
#             Rainy  0.05  0.10    0.35  0.50 
#     '''
#     B = np.mat([[0.6, 0.2, 0.15, 0.05],
#                 [0.25, 0.25, 0.25, 0.25],
#                 [0.05, 0.1, 0.35, 0.5]]);
#     
#     '''
#     observation: Dry, Damp, Soggy
#     '''
#     O = [0, 2, 3];

    N = 3;
    M = 2;
    A = np.mat([[0.5, 0.2, 0.3],
                [0.3, 0.5, 0.2],
                [0.2, 0.3, 0.5]]);
    B = np.mat([[0.5, 0.5],
                [0.4, 0.6],
                [0.7, 0.3]]);
    pi = [0.2, 0.4, 0.4];
    O = [0, 1, 0];
    
    prob, beta = calc_prob(N, M, pi, A, B, O);
    
    print beta;
    print prob;

unit_testing();
