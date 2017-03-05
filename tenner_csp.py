#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
#IMPLEMENT
    cons_list = []
    row_num = len(initial_tenner_board[0]);
    col_num = len(initial_tenner_board[0][0]);
    for i in range(row_num):
        for j in range(col_num):
            if initial_tenner_board[0][i][j] == -1:
                x = Variable(str(i) + str(j), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
            else:
                x = Variable(str(i) + str(j), [initial_tenner_board[0][i][j]]);
            cons_list.append(x);
    csp = CSP("model1", cons_list);
    create_cons(cons_list, csp);
    create_sum(cons_list, initial_tenner_board[1], csp);
    return csp, cons_list;





##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''

    cons_list = []
    row_num = len(initial_tenner_board[0]);
    col_num = len(initial_tenner_board[0][0]);
    for i in range(row_num):
        for j in range(col_num):
            if initial_tenner_board[0][i][j] == -1:
                x = Variable(str(i) + str(j), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
            else:
                x = Variable(str(i) + str(j), [initial_tenner_board[0][i][j]]);
            cons_list.append(x);
    csp = CSP("model2", cons_list);
    create_cons2(cons_list, csp);
    create_sum(cons_list, initial_tenner_board[1], csp);
    return csp, cons_list;




def create_cons(bi_cons_list, csp):
    for i in range(int(len(bi_cons_list)/10)):
        for j in range(10):
            ind = 10*i + j
            nearby = [ind-1, ind+1, ind+1-10, ind-1-10, ind-10, ind+10, ind-1+10, ind+1+10];
            for m in range(10):
                if m > j:
                    cur_list = [bi_cons_list[ind], bi_cons_list[10*i + m]];
                    c = Constraint("c" + str(i) + str(j) + str(m), cur_list);
                    sat_tuples = add_tup(cur_list);
                    c.add_satisfying_tuples(sat_tuples);
                    csp.add_constraint(c);
            add_nearby(bi_cons_list, nearby, csp, i, j);

                

def create_cons2(bi_cons_list, csp):
    for i in range(int(len(bi_cons_list)/10)):
        cur_list = [];
        for j in range(10):
            cur_list.append(bi_cons_list[10*i + j]);
            add_nearby(bi_cons_list, nearby, csp, i, j);

        c = Constraint("c" + i, cur_list);
        sat_tuples = add_row(cur_list);
        c.add_satisfying_tuples(sat_tuples);
        csp.add_constraint(c);




def create_sum(bi_cons_list, sum_list, csp):
    for i in range(len(sum_list)):
        cur_list = [];
        for j in range(int(len(bi_cons_list)/10)):
            cur_list.append(bi_cons_list[i + 10*j]);
        c = Constraint("sum" + str(i), cur_list);
        sal_tuples = add_sum(cur_list, sum_list[i]);
        c.add_satisfying_tuples(sal_tuples);
        csp.add_constraint(c);


def add_nearby(bi_cons_list, nearby, csp, i, j):
    for m in nearby:
        try:
            cur_list = [bi_cons_list[10*i + j], bi_cons_list[m]];
            c = Constraint("c" + str(i) + str(j) + str(m), cur_list);
            sat_tuples = add_tup(cur_list);
            c.add_satisfying_tuples(sat_tuples);
            csp.add_constraint(c);
        except:
            continue;

def add_row(cur_list):
    varDoms = []
    for v in cur_list:
        varDoms.append(v.domain())    
    sat_tuples = []
    for t in itertools.product(*varDoms):
    #NOTICE use of * to convert the list v to a sequence of arguments to product
        if check_row(t):
            sat_tuples.append(t)
    return sat_tuples;


def add_tup(cur_list):
    varDoms = []
    for v in cur_list:
        varDoms.append(v.domain())    
    sat_tuples = []
    for t in itertools.product(*varDoms):
    #NOTICE use of * to convert the list v to a sequence of arguments to product
        if check_bi(t):
            sat_tuples.append(t)
    return sat_tuples;

def add_sum(cur_list, total):
    varDoms = []
    for v in cur_list:
        varDoms.append(v.domain())    
    sat_tuples = []
    for t in itertools.product(*varDoms):
    #NOTICE use of * to convert the list v to a sequence of arguments to product
        if check_sum(t, total):
            sat_tuples.append(t)
    return sat_tuples;

def check_sum(cur_list, total):
    value = 0;
    for item in cur_list:
        value += item;
    return value == total;

def check_bi(tup):
    x, y = tup;
    return x != y;

def check_row(cur_list):
    flags = [-1 for m in range(10)];
    for i in range(len(cur_list)):
        if flags[i] == -1:
            flags[i] = 1;
        else:
            return False;
    return True