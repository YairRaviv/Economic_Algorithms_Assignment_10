from typing import List

import cvxpy
import functools

def Nash_budget(total: float, subjects: List[str],preferences:List[List[str]]):

    n = len(subjects)
    allocations = cvxpy.Variable(n)
    utilities = [0] * n
    for i in range(0,n):
        for subject in preferences[i]:
            for j in range(0,n):
                if subject == subjects[j]:
                    utilities[i] = utilities[i]+allocations[j]
    donations = [total/n] * n
    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == total]
    problem = cvxpy.Problem(cvxpy.Maximize(sum_of_logs), constraints = positivity_constraints+sum_constraint)
    problem.solve()
    for i in range(0,n):
        str = f'"Citizen {i} gives "'
        for j in range(0,n):
            if allocations[j] * donations[i]/utilities[i].value != 0:
                str = str+f'"{allocations[j] * donations[i]/utilities[i].value} to {subjects[j]} ,"'

