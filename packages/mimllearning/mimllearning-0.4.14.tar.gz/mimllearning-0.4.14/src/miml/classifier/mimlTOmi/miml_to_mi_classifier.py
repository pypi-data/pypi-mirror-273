import numpy as np
from abc import abstractmethod
from ..miml_classifier import MIMLClassifier
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMIClassifier(MIMLClassifier):
    """
    Class to represent a multi-instance classifier
    """

    def __init__(self, mi_classifier) -> None:
        """
        Constructor of the class MIMLtoMIClassifier

        Parameters
        ----------
        mi_classifier
            Specific classifier to be used
        """
        super().__init__()
        self.classifier = mi_classifier

    @abstractmethod
    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        pass

    @abstractmethod
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
        pass

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels of the bag
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        return self.predict(bag.get_features())

    @abstractmethod
    def predict_proba(self, dataset_test: MIMLDataset) -> np.ndarray:
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

        pass

    def evaluate(self, dataset_test: MIMLDataset) -> np.ndarray:
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of dataset_test
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        # Features are the same in all datasets
        for i, bag in enumerate(dataset_test.get_features_by_bag()):
            results[i] = self.predict(bag)

        return results
