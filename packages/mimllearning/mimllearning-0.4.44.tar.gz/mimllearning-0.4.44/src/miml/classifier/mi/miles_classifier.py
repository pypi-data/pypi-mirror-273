import mil.models
from mil.bag_representation import MILESMapping
from sklearn.tree import DecisionTreeClassifier
import numpy as np


class MILESClassifier:

    """
    Mapping bags to an instance based feature space, from paper

    Attributes
    ----------
    classifier
        Classifier used from mil library

    model
        Model to use

    mapping
        Mapping to be used

    sigma2 : float
        Parameter of the classifier

    References
    ----------
    MILES: Multiple-Instance Learning via Embedded Instance Selection (Chen et al.)
    http://infolab.stanford.edu/~wangz/project/imsearch/SVM/PAMI06/chen.pdf
    """

    def __init__(self, sigma2=4.5 ** 2) -> None:
        """
        Constructor of the class MILESClassifier
        """
        self.classifier = mil.models.MILES()
        self.model = None
        self.mapping = None
        self.sigma2 = sigma2

    def fit(self, x_train: np.array, y_train: np.array) -> None:
        """
        Fit the classifier to the training data.

        Parameters
        ----------
        x_train : ndarray of shape (n_bags, n_instances, n_features)
            Features values of bags in the training set.
        y_train : ndarray (n_bags, n_instances, n_labels)
            Labels of bags in the training set.
        """

        self.classifier.check_exceptions(x_train)
        self.mapping = MILESMapping(self.sigma2)
        mapped_bags = self.mapping.fit_transform(x_train)

        # train the SVM
        # self.model = LinearSVC(penalty="l1", C=self.c, dual=False, class_weight='balanced',max_iter=100000)

        self.model = DecisionTreeClassifier()
        self.model.fit(mapped_bags, y_train.flatten())

    def predict(self, bag: np.ndarray) -> int:
        """
        Predict the label of the bag

        Parameters
        ----------
        bag: np.ndarray of shape(n_instances, n_features)
            features values of a bag

        Returns
        -------
        label: int
            Predicted label of the bag

        """
        bag = bag.reshape(1, bag.shape[0], bag.shape[1])
        mapped_bag = self.mapping.transform(bag)
        return self.model.predict(mapped_bag)

    def predict_proba(self, x: np.ndarray):
        """
        Predict probabilities of given data

        Parameters
        ----------
        x : np.ndarray of shape (n_instances, n_features)
            Probabilities of data of being a positive label.

        Returns
        -------
        results: np.ndarray of shape (n_instances, n_features)
            Predicted probabilities for given data
        """
        # TODO: fix, this is a patch. Dont know how to implement it

        result = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            result[i] = self.predict(x[i])
        return result
