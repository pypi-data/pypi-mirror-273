import numpy as np
from . import autosklearn_modeling
from . import pymoo_optimization
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.termination import get_termination
from pymoo.optimize import minimize

class Solver():
    def __init__(self):
        self.solutions=None
        self.models_paths=None
        self.num_features=None
        self.num_objectives=None

    def train_models(self, X, y, max_train_secs_per_output=120, memory_limit=1024 * 100):
        self.num_features=np.array(X).shape[1]
        self.num_objectives=np.array(y).shape[1]
        self.models_paths = autosklearn_modeling.train_autosklearn_models(X, y, max_train_secs_per_output=max_train_secs_per_output, memory_limit=memory_limit)

    def find_optimal_solution(self, pop_size=500, n_offprings=500, n_gen=None, max_opt_secs=None, objectives_sense=None, inequality_constraints=None, equality_constraints=None, features_lower_bounds=None, features_upper_bounds=None):
        if self.models_paths == None:
            print(f'Sorry. You must create the models before')
        else:
            vectorized_problem = pymoo_optimization.OptimizationProblem(model_paths=self.models_paths, num_features=self.num_features, num_objectives=self.num_objectives, objectives_sense=objectives_sense, inequality_constraints=inequality_constraints, equality_constraints=equality_constraints, features_lower_bounds=features_lower_bounds, features_upper_bounds=features_upper_bounds)
            
            algorithm = NSGA2(
                pop_size=pop_size,
                n_offsprings=n_offprings,
                sampling=FloatRandomSampling(),
                crossover=SBX(prob=0.9, eta=15),
                mutation=PolynomialMutation(eta=20),
                eliminate_duplicates=True
            )

            if n_gen==None and max_opt_secs==None:
                termination = get_termination("n_gen", 100)
            elif n_gen!=None:
                termination = get_termination("n_gen", n_gen)
            else:
                opt_time = "{:02d}:{:02d}:{:02d}".format(max_opt_secs // 3600, (max_opt_secs % 3600) // 60, max_opt_secs % 60)
                termination = get_termination("time", opt_time)

            results = minimize(vectorized_problem, algorithm, termination=termination, seed=1, save_history=True, verbose=False)

            for i, goal in enumerate(vectorized_problem.objectives_sense):
                if goal == 'maximize':
                    results.F[:, i] = -1 * results.F[:, i]

            self.solutions = results

    def train_and_optimize(self, X, y, max_train_secs_per_output=120, memory_limit=1024 * 100, pop_size=500, n_offprings=500, n_gen=None, max_opt_secs=None, objectives_sense=None, inequality_constraints=None, equality_constraints=None, features_lower_bounds=None, features_upper_bounds=None):
        self.num_features=np.array(X).shape[1]
        self.num_objectives=np.array(y).shape[1]
        self.models_paths = autosklearn_modeling.train_autosklearn_models(X, y, max_train_secs_per_output=max_train_secs_per_output, memory_limit=memory_limit)
        vectorized_problem = pymoo_optimization.OptimizationProblem(model_paths=self.models_paths, num_features=self.num_features, num_objectives=self.num_objectives, objectives_sense=objectives_sense, inequality_constraints=inequality_constraints, equality_constraints=equality_constraints, features_lower_bounds=features_lower_bounds, features_upper_bounds=features_upper_bounds)
            
        algorithm = NSGA2(
            pop_size=pop_size,
            n_offsprings=n_offprings,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PolynomialMutation(eta=20),
            eliminate_duplicates=True
        )

        if n_gen==None and max_opt_secs==None:
            termination = get_termination("n_gen", 100)
        elif n_gen!=None:
            termination = get_termination("n_gen", n_gen)
        else:
            opt_time = "{:02d}:{:02d}:{:02d}".format(max_opt_secs // 3600, (max_opt_secs % 3600) // 60, max_opt_secs % 60)
            termination = get_termination("time", opt_time)

        results = minimize(vectorized_problem, algorithm, termination=termination, seed=1, save_history=True, verbose=False)

        for i, goal in enumerate(vectorized_problem.objectives_sense):
            if goal == 'maximize':
                results.F[:, i] = -1 * results.F[:, i]

        self.solutions = results