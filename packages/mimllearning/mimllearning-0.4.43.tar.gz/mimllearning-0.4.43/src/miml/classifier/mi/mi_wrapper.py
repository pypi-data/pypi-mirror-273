import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class MIWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, base_classifier=DecisionTreeClassifier()):
        self.base_classifier = base_classifier

    def fit(self, x_train, y_train):
        # Flatten the bags into instances
        x_instances = np.vstack(x_train)
        y_instances = np.zeros((x_instances.shape[0], 1))
        count = 0
        for bag, label in zip(x_train, y_train):
            for instance in bag:
                y_instances[count] = label
                count += 1
        instance_weights = np.hstack([np.ones(len(bag)) / len(bag) for bag in x_train])

        # Check that X and y have correct shape
        x_instances, y_instances = check_X_y(x_instances, y_instances)

        # Fit the base classifier with instance weights
        self.base_classifier.fit(x_instances, y_instances, sample_weight=instance_weights)
        self.classes_ = self.base_classifier.classes_

    def predict_proba(self, x_test):

        check_is_fitted(self)

        instance_probs = self.base_classifier.predict_proba(x_test)
        # Average the probabilities for the bag
        avg_probs = np.mean(instance_probs, axis=0)

        return avg_probs

    def predict(self, x_test):
        #x_test = x_test.reshape(1, -1)
        print(x_test.shape, x_test)
        # Predict class labels for bags
        bag_probs = self.predict_proba(x_test)
        return self.classes_[np.argmax(bag_probs, axis=1)]