/* RPD simulation*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double Uniform( void ){
    return ((double)rand()+1.0) / ((double)RAND_MAX + 2.0);
}

int main(int argc, char *argv[]){
    srand(time(NULL));
    
    // momory-one strategy
    // p_0: p_0, p1: p_CC, p2: p_CD, p3: p_DC, p4: p_DD
    // q_0: q_0, q1: q_CC, q2: q_CD, q3: q_DC, q4: q_DD
    
    double p[5] = {atof(argv[1]),
                   atof(argv[2]),
                   atof(argv[3]),
                   atof(argv[4]),
                   atof(argv[5])};// x's strategy
    double q[5];                  // y's strategy
    
    double payoff_x, payoff_y;// expected payoff
    double stage_payoff_x, stage_payoff_y;// paypff per stage game
    double T = 1.5, R = 1.0, P = 0.0, S = -0.5;// stage geme payoff
    int t_max = 100000;
    int state;
    int i_max = 20;
    
    
    int action_x, action_y;//C:0, D:1
    
    for (int i=0; i < i_max; i++){
        for (int j=0; j<5; j++) q[j] = Uniform();// Change Y's strategy
        state = 0;
        // Repeated Game t = {0, 1, 2,...}
        for (int t = 0; t < t_max; t++){
            if (Uniform() < p[state]) action_x = 0;// Cooperate
            else action_x = 1;                 // Defect
            
            if (Uniform() < q[state]) action_y = 0;// Cooperate
            else action_y = 1;                 // Defect
            
            
            
            if (action_x == 0 && action_y == 0) {// CC
                payoff_x += R;
                payoff_y += R;
                state = 1;
            }
            if (action_x == 0 && action_y == 1) {// CD
                payoff_x += S;
                payoff_y += T;
                state = 2;
            }
            if (action_x == 1 && action_y == 0) {// DC
                payoff_x += T;
                payoff_y += S;
                state = 3;
            }
            if (action_x == 1 && action_y == 1) {// DD
                payoff_x += P;
                payoff_y += P;
                state = 4;
            }
            
        }
        payoff_x = (double) payoff_x / t_max;
        payoff_y = (double) payoff_y / t_max;
        printf("%f,%f\n", payoff_x, payoff_y);
    }
    return 0;
}
