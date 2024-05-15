import networkx as nx
from _typeshed import Incomplete
from enot.graph.ir.ir import IR as IR
from enot.graph.ir.node import Node as Node
from enot.utils.python_container_parser import map_recursively as map_recursively
from torch import fx
from typing import Iterable, overload

class Snapshot:
    """Computational graph container for particular model state and input data."""
    meta: Incomplete
    def __init__(self, owner: IR, name: str, nodes: Iterable[Node] | None = None, *, fx_producer: type[fx.Tracer] | None = None) -> None:
        """
        Parameters
        ----------
        owner : IR
            Reference to the owner of the snapshot.
        name : str
            Name of the snapshot.
        nodes : Optional[Iterable[Node]]
            Iterable collection of computational graph nodes.
        fx_producer : Optional[Type[fx.Tracer]]
            Class of tracer that produced a graph (nodes). Only for the graphs produced by fx.
            Default value is None.

        """
    @classmethod
    def from_fx_graph(cls, owner: IR, name: str, graph: fx.Graph) -> tuple[Snapshot, dict[fx.Node, Node]]:
        """
        Creates ``Snapshot`` instance from ``fx.Graph``.

        Parameters
        ----------
        owner : IR
            Reference to the owner of the snapshot.
        name : str
            Name of the snapshot.
        graph : fx.Graph
            Source ``fx.Graph``.

        Returns
        -------
        Tuple[Snapshot, Dict[fx.Node, Node]]
            ``Snapshot`` instance and mapping the nodes of fx source graph to the nodes of snapshot graph.

        """
    @staticmethod
    @overload
    def deepcopy_metadata(mapping: dict[fx.Node, Node], keys: list | None = None) -> None: ...
    @staticmethod
    @overload
    def deepcopy_metadata(mapping: dict[Node, fx.Node], keys: list | None = None) -> None: ...
    @staticmethod
    @overload
    def copy_metadata(mapping: dict[fx.Node, Node], keys: list | None = None) -> None: ...
    @staticmethod
    @overload
    def copy_metadata(mapping: dict[Node, fx.Node], keys: list | None = None) -> None: ...
    @staticmethod
    def stable_topological_sort(graph: nx.DiGraph | Iterable[Node]) -> list[Node]:
        """
        Stable version of the NetworkX topological sorting. It sorts nodes in topological order and preserves order
        of nodes from input where possible.

        Parameters
        ----------
        graph : Union[nx.DiGraph, Iterable[Node]]
            Iterable collection of computational graph nodes or computational graph as ``fx.Graph``.

        Returns
        -------
        List[Node]
            List of sorted nodes.

        """
    @property
    def owner(self) -> IR:
        """Reference to the owner of the snapshot."""
    @property
    def name(self) -> str:
        """Name of the snapshot."""
    @property
    def graph(self) -> nx.DiGraph:
        """Snapshot computational graph in the form ``nx.DiGraph``."""
    @property
    def nodes(self) -> Iterable[Node]:
        """Alias for ``self.graph.nodes``."""
    @overload
    def update_graph(self, graph: Iterable[Node] | nx.DiGraph | None = None) -> None: ...
    @overload
    def update_graph(self, graph: fx.Graph) -> dict[fx.Node, Node]: ...
    def fx_graph(self) -> tuple[fx.Graph, dict[Node, fx.Node]]:
        """
        Return a computational graph in the form ``fx.Graph``.

        Returns
        -------
        Tuple[fx.Graph, Dict[Node, fx.Node]]
            Snapshot computational graph in the form ``fx.Graph`` and mapping the nodes of source graph to the
            nodes of fx graph.

        """
