import numpy as np
from scipy.spatial import distance

# TODO: DOC


class CitationKNNClassifier:

    def __init__(self, k, c) -> None:
        """
        Constructor of the class CitationKNNClassifier
        """
        self.k = k
        self.c = c
        self.x_train = None
        self.y_train = None

    def fit(self, x_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Fit the classifier to the training data.

        Parameters
        ----------
        x_train : ndarray of shape (n_bags, n_instances, n_features)
            Features values of bags in the training set.
        y_train : ndarray (n_bags, n_instances, n_labels)
            Labels of bags in the training set.
        """
        self.x_train = x_train
        self.y_train = y_train

    def predict(self, bag: np.array) -> int:
        """
        Predict the label of the bag

        Parameters
        ----------
        bag: np.ndarray of shape(n_instances, n_features)
            features values of bags

        Returns
        -------
        label: int
            Predicted label of the bag

        """
        citing_neighbors = self._get_nearest_neighbors(bag, self.k)
        cited_neighbors = self._get_cited_neighbors(bag, self.c)
        neighbors = np.concatenate((citing_neighbors, cited_neighbors))
        result = self._majority_vote(neighbors)
        return result

    def _get_nearest_neighbors(self, test_bag, num_neighbors):
        distances = np.array([self._compute_distance(test_bag, bag) for bag in self.x_train])
        nearest_indices = np.argsort(distances)[:num_neighbors]
        return nearest_indices

    def _get_cited_neighbors(self, test_bag, num_neighbors):
        distances = np.array([self._compute_distance(test_bag, bag) for bag in self.x_train])
        cited_neighbors = []
        for idx, bag in enumerate(self.x_train):
            nearest_indices = self._get_nearest_neighbors(bag, num_neighbors)
            if idx in nearest_indices:
                cited_neighbors.append(idx)
        return np.array(cited_neighbors)

    def _compute_distance(self, bag1, bag2):
        return distance.cdist(bag1, bag2, 'euclidean').mean()

    def _majority_vote(self, neighbor_indices):
        neighbor_labels = self.y_train[neighbor_indices]
        unique_labels, counts = np.unique(neighbor_labels, return_counts=True)
        print("unique label and counts: ", unique_labels, counts)
        majority_label = unique_labels[np.argmax(counts)]
        print("majority label: ",majority_label)
        return majority_label

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """
        Predict probabilities of given data of having a positive label

        Parameters
        ----------
        x : np.ndarray of shape (n_instances, n_features)
            Data to predict probabilities

        Returns
        -------
        results: np.ndarray of shape (n_instances, n_features)
            Predicted probabilities for given data
        """
        result = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            result[i] = self.predict(x[i])
        return result


