import numpy as np
from copy import deepcopy

from .miml_to_mi_classifier import MIMLtoMIClassifier
from ...transformation import BinaryRelevanceTransformation
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMIBRClassifier(MIMLtoMIClassifier):
    """
    Class to represent a multi-instance classifier using a binary relevance transformation
    """

    def __init__(self, classifier) -> None:
        """
        Constructor of the class MIMLtoMIBRClassifier

        Parameters
        ----------
        classifier
            Specific classifier to be used
        """
        super().__init__(classifier)
        self.transformation = BinaryRelevanceTransformation()
        self.classifiers = []

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """

        # Create as many classifier as labels
        for x in range(dataset_train.get_number_labels()):
            classifier = deepcopy(self.classifier)
            self.classifiers.append(classifier)

        # Obtain converted datasets and train each classifier
        datasets = self.transformation.transform_dataset(dataset_train)
        for i, dataset in enumerate(datasets):
            self.classifiers[i].fit(dataset.get_features_by_bag(), dataset.get_labels_by_bag())

        self.trained = True

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n_instances, n_labels)
            Data to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        results = np.zeros((len(self.classifiers)))
        # Prediction of each label
        for i in range(len(self.classifiers)):
            results[i] = self.classifiers[i].predict(x)
        return results

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

        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))

        for i in range(len(self.classifiers)):
            results[0:, i] = self.classifiers[i].predict_proba(dataset_test.get_features_by_bag())
        return results
