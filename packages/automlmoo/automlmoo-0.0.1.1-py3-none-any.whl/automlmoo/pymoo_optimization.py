import six.moves.cPickle as pickle
import gc
import numpy as np
from pymoo.core.problem import Problem

class OptimizationProblem(Problem):
    def __init__(self, model_paths=None, num_features=-1, num_objectives=1, objectives_sense=None, inequality_constraints=None, equality_constraints=None, features_lower_bounds=None, features_upper_bounds=None):
        self.model_paths = model_paths
        self.num_features = num_features
        self.num_objectives = num_objectives
        self.objectives_sense = ['minimize'] * self.num_objectives if objectives_sense is None else objectives_sense
        self.inequality_constraints = inequality_constraints
        self.equality_constraints = equality_constraints
        self.features_lower_bounds = features_lower_bounds
        self.features_upper_bounds = features_upper_bounds
        super().__init__(n_var=self.num_features,
                         n_obj=self.num_objectives,
                         n_ieq_constr=0 if self.inequality_constraints is None else len(self.inequality_constraints),
                         n_eq_constr=0 if self.equality_constraints is None else len(self.equality_constraints),
                         xl=features_lower_bounds,
                         xu=features_upper_bounds)
    
    def _evaluate(self, x, out, *args, **kwargs):
        # Evaluate each objective function
        for i, model_path in enumerate(self.model_paths):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
                
                if i == 0:
                    out["F"] = model.predict(x)
                else:
                    out["F"] = np.column_stack([out["F"], model.predict(x)])
                
                # Modify the objective sense if the goal is maximize
                if self.objectives_sense[i] == 'maximize':
                    out["F"][:, i] = -1 * out["F"][:, i]

                # Evaluate constraints if present
                if self.inequality_constraints is not None:
                    for i, constraint in enumerate(self.inequality_constraints):
                        if i == 0:
                            out["G"] = constraint
                        else:
                            out["G"] = np.column_stack([out["G"], constraint])
                if self.equality_constraints is not None:
                    for i, constraint in enumerate(self.equality_constraints):
                        if i == 0:
                            out["H"] = constraint
                        else:
                            out["H"] = np.column_stack([out["H"], constraint])

                del model
                gc.collect()