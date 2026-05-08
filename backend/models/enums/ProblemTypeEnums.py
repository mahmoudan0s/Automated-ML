from enum import Enum


class ProblemType(str, Enum):
	classification = "classification"
	regression = "regression"
	clustering = "clustering"


SUPERVISED_PROBLEMS = {ProblemType.classification, ProblemType.regression}