from sklearn.base import BaseEstimator, ClassifierMixin
from autogluon.tabular import TabularDataset


class AutogluonToScikitWrapperMethod(BaseEstimator, ClassifierMixin):

    def __init__(self, **kwargs):
        self.init = None
        self.classes_ = []
        self._estimator_type = "classifier"
        if len(kwargs) != 0:
            self.mdl = TabularPredictor(**kwargs)

    def fit(self, X, y=None, **kwargs):
        self.mdl.fit(X, **kwargs)
        self.is_fitted_ = True
        if self.problem_type != "regression":
            self.classes_ = self.mdl.class_labels_internal
            self._estimator_type = "classifier"
        else:
            self._estimator_type = "regressor"
        return self

    def load(self, path):
        self.mdl = TabularPredictor.load(path=path, require_version_match=False)
        self.is_fitted_ = True
        if self.problem_type != "regression":
            self.classes_ = self.mdl.class_labels_internal
            self._estimator_type = "classifier"
        else:
            self._estimator_type = "regressor"
        return self

    def predict(self, X):
        if not (isinstance(X, pd.DataFrame) or isinstance(X, TabularDataset)):
            try:
                X = pd.DataFrame(data=X, columns=self.mdl.features())
            except Exception:
                raise TypeError(f"Cannot convert data of type {str(type(X))} to tabular form.")
        return self.mdl.predict(X)

    def predict_proba(self, X):
        return self.mdl.predict_proba(X)

    def feature_importance(self, X, **kwargs):
        return self.mdl.feature_importance(X, kwargs)

    def info(self):
        return self.mdl.info()

    def evaluate(self, X):
        return self.mdl.evaluate(X)

    def features(self):
        return self.mdl.features()

    def transform_features(self, X, **kwargs):
        return self.mdl.transform_features(X, kwargs)

    def transform_labels(self, y, **kwargs):
        return self.mdl.transform_labels(y, kwargs)

    @property
    def problem_type(self):
        return self.mdl.problem_type

    @property
    def eval_metric(self):
        return self.mdl.eval_metric

    @property
    def label(self):
        return self.mdl.label

    @property
    def class_labels(self):
        return self.mdl.class_labels
