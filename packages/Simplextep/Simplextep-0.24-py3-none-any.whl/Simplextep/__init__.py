import Simplextep
from Simplextep import Simplextep
from Simplextep.Simplextep import Simplex, Problem_Prepration, Dual, Me_Plot, Sensitivity_Analysis

"""Examples:
    1) Solve Simplex.
    objective_function = [0, 6, 5, 4]
    constraints = [[240, 2, 1, 1], [360, 1, 3, 2], [300, 2, 1, 2]]
    equality = ["ineq", "ineq", "ineq"]
    parameters = [("x1", "+"), ("x2", "+"), ("x3", "+")]

    problem = Problem_Prepration(objective_function=objective_function,
                                constraints=constraints,
                                equality=equality,
                                parameters=parameters,
                                mode="max")

    simplex = Simplex(problem=problem)
    simplex.fit()
    print()
    simplex.make_table(format_="github") # This line will show all the steps.

    2) Solve Dual Simplex:
    dual_problem = Dual(objective_function=objective_function, constraints=constraints, equality=equality, parameters=parameters, mode=mode)
    dual_problem.fit()
    simplex = Simplex(problem=dual_problem.problem)
    simplex.fit(max_iterations=10)
    simplex.make_table() # This line will show all the steps.

    3) Simplex Analyse:
    objective_function = [0, 5, 4.5, 6]
    constraints = [[60, 6, 5, 8], [150, 10, 20, 10], [8, 1, 0, 0]]
    equality = ["ineq", "ineq", "ineq"]
    parameters = [("x1", "+"), ("x2", "+"), ("x3", "+")]

    problem = Problem_Prepration(objective_function=objective_function,
                             constraints=constraints,
                             equality=equality,
                             parameters=parameters,
                             mode="max")

    simplex = Simplex(problem=problem)
    simplex.fit()
    # simplex.make_table(format_="github")

    analysis = Sensitivity_Analysis(simplex)
    analysis.change_righthand(righthands_at_first=[0, 1, 0, 0])
"""



