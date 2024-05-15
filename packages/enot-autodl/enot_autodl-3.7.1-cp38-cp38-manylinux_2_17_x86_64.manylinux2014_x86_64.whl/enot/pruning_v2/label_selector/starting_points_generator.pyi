import abc
from abc import ABC, abstractmethod
from enot.graph.ir.snapshot import Snapshot as Snapshot
from enot.pruning_v2.criteria.label_groups import label_groups as label_groups
from enot.pruning_v2.label import Label as Label
from enot.pruning_v2.label_selector.base import LabelSelector as LabelSelector

class StartingPointsGenerator(ABC, metaclass=abc.ABCMeta):
    """An abstract class which defines a method for generating a list of starting points for a label selector algorithm,
    where every starting point is a list of labels for pruning."""
    @abstractmethod
    def generate(self, snapshot: Snapshot) -> list[list[Label]]:
        """
        Generate a list of starting points for a label selector algorithm, where every starting point is a list of
        labels for pruning.

        Parameters
        ----------
        snapshot : Snapshot
            Target snapshot.

        Returns
        -------
        List[List[Label]]
            List of starting point, where every starting point is a list of labels for pruning.

        """
    def generate_as_coordinates_list(self, snapshot: Snapshot, *, normalized: bool = False) -> list[list[int] | list[float]]:
        """
        Generate a list of starting points for a label selector algorithm and convert result to coordinate format.

        Parameters
        ----------
        snapshot : Snapshot
            Target snapshot.
        normalized : bool
            If True, the coordinates will be represented as the ratio of the number of selected labels to the total
            number of labels in the group.

        Returns
        -------
        List[Union[List[int], List[float]]]
            Starting point in coordinate format.

        """
    @staticmethod
    def starting_points_as_coordinates_list(starting_points: list[list[Label]], sorted_group_labels: list[list[Label]], normalized: bool = False) -> list[list[int] | list[float]]:
        """
        Convert the list of starting points to coordinate format. The coordinate format is a list of integers, where
        each integer corresponds to group and means number of labels that selected for pruning. Labels must always be
        selected in ascending order of score, otherwise ValueError will be generated.

        Parameters
        ----------
        starting_points : List[List[Label]]
            The list of starting points for conversion.
        sorted_group_labels : List[List[Label]]
            Labels are divided into groups and sorted within each group.
        normalized : bool
            If True, the coordinates will be represented as the ratio of the number of selected labels to the total
            number of labels in the group.

        Returns
        -------
        List[Union[List[int], List[float]]]
            Starting point in coordinate format.

        """

class LabelSelectorsStartingPointsGenerator(StartingPointsGenerator):
    """Generator of starting points that is based on list of instances of ``PruningLabelSelector``."""
    def __init__(self, *args: LabelSelector) -> None:
        """
        Parameters
        ----------
        *args : PruningLabelSelector
            Label selectors to be used to generate the starting points.

        """
    def generate(self, snapshot: Snapshot) -> list[list[Label]]: ...
