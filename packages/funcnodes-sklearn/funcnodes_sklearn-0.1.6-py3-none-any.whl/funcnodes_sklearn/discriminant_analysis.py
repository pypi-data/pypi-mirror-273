from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from typing import Literal, Optional, Union, Callable
import numpy as np
from sklearn.base import BaseEstimator
from enum import Enum
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis,
)


class Solver(Enum):
    svd = "svd"
    lsqr = "lsqr"
    eigen = "eigen"

    @classmethod
    def default(cls):
        return cls.svd.value


# class TransformAlgorithm(Enum):
#     lasso_lars = "lasso_lars"
#     lasso_cd = "lasso_cd"
#     lars = "lars"
#     omp = "omp"
#     threshold = "threshold"

#     @classmethod
#     def default(cls):
#         return cls.omp.value


@NodeDecorator(
    node_id="sklearn.discriminant_analysis.LinearDiscriminantAnalysis",
    name="LinearDiscriminantAnalysis",
)
@controlled_wrapper(LinearDiscriminantAnalysis, wrapper_attribute="__fnwrapped__")
def _dictionary_learning(
    solver: Solver = Solver.default(),
    shrinkage: Optional[Union[float, Literal['auto']]] = None,
    priors
    
) -> Callable[[], BaseEstimator]:
    def create_dictionary_learning():
        return LinearDiscriminantAnalysis(
            n_components=n_components,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            fit_algorithm=fit_algorithm,
            transform_algorithm=transform_algorithm,
            transform_n_nonzero_coefs=transform_n_nonzero_coefs,
            transform_alpha=transform_alpha,
            n_jobs=n_jobs,
            code_init=code_init,
            dict_init=dict_init,
            callback=callback,
            verbose=verbose,
            split_sign=split_sign,
            random_state=random_state,
            positive_code=positive_code,
            positive_dict=positive_dict,
            transform_max_iter=transform_max_iter,
        )

    return create_dictionary_learning
