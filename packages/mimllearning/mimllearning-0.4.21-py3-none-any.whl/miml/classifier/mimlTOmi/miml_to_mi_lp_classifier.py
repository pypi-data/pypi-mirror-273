import numpy as np
from copy import deepcopy

from .miml_to_mi_classifier import MIMLtoMIClassifier
from ...transformation import LabelPowersetTransformation
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMILPClassifier(MIMLtoMIClassifier):
    """
    Class to represent a multi-instance classifier using a label powerset transformation
    """

    def __init__(self, classifier) -> None:
        """
        Constructor of the class MIMLtoMILPClassifier

        Parameters
        ----------
        classifier
            Specific classifier to be used
        """
        super().__init__(classifier)
        self.transformation = LabelPowersetTransformation()

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        dataset = self.transformation.transform_dataset(dataset_train)
        # TODO: Temporal fix. Make sure it is okey
        self.classifier.fit(dataset.get_features(), dataset.get_labels())
        self.trained = True

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n_instances, n_features)
            Data to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        # Prediction of each label
        results = self.classifier.predict(x)
        binary_str = np.binary_repr(results, width=self.transformation.dataset.get_number_labels())
        return np.array([int(bit) for bit in binary_str])

    def predict_proba(self, dataset_test: MIMLDataset):
        """
        Predict probabilities of given dataset of having a positive label

        Parameters
        ----------
        dataset_test : MIMLDataset
            Dataset to predict probabilities

        Returns
        -------
        results: np.ndarray of shape (n_instances, n_features)
            Predicted probabilities for given dataset
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        return self.classifier.predict_proba(dataset_test.get_features_by_bag())

