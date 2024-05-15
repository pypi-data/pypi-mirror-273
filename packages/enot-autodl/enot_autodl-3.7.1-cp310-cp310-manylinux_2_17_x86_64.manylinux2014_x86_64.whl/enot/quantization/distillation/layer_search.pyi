from enot.quantization.qnn.quantized_layer import QuantizedLayer as QuantizedLayer
from enot.quantization.quant_distillation_layer import QuantDistillationModule as QuantDistillationModule
from enot.utils.common import get_submodule as get_submodule
from torch.fx.graph_module import GraphModule as GraphModule
from torch.fx.node import Node as Node

def is_quant_node(traced_model: GraphModule, node: Node) -> bool:
    '''
    Checks whether a node is associated with a quantized layer or not.

    Node is associated with a regular pytorch layer (or module) if node execution is this layer call.
    Therefore, it\'s op should be "call_module", and node target should refer to a quantized module.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        Traced model instance, which is the root for the considered node.
    node : torch.fx.Node
        Node to test.

    Returns
    -------
    bool
        Whether the node is associated with a quantized layer or not.

    '''
def find_all_quant_nodes(traced_model: GraphModule) -> list[Node]:
    """
    Finds all nodes associated with quantized layers.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        Traced model instance (root module for all nodes).

    Returns
    -------
    list with torch.fx.Node
        List with all nodes associated with quantized layers.

    Notes
    -----
    This function uses :func:`.is_quant_node` function to determine quant nodes.

    """
def find_last_quant_nodes(traced_model: GraphModule, output_node: Node) -> list[Node]:
    """
    Finds last quant nodes, whose outputs are connected to model outputs through regular (non-quantized) nodes.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        Traced model instance (root module for all nodes).
    output_node : torch.fx.Node
        Traced model output node.

    Returns
    -------
    list with torch.fx.Node
        List with last quantized nodes.

    Notes
    -----
    To find last quant nodes, we launch breadth-first search from all output nodes. We enqueue input nodes only for non-
    quantized nodes, and add all encountered quantized nodes to the result list.

    This function uses :func:`.is_quant_node` function to determine quant nodes.

    """
def is_distillation_node(traced_model: GraphModule, node: Node) -> bool:
    '''
    Checks whether a node is associated with a user-inserted distillation layer or not.

    To satisfy all requirements, node op should be "call_module", and node target should refer to a user-inserted
    distillation layer.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        Traced model instance, which is the root for the considered node.
    node : torch.fx.Node
        Node to test.

    Returns
    -------
    bool
        Whether the node is associated with a user-inserted distillation layer or not.

    '''
def find_distillation_nodes(traced_model: GraphModule) -> list[Node]:
    """
    Finds all nodes associated with user-inserted distillation layers.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        Traced model instance (root module for all nodes).

    Returns
    -------
    list with torch.fx.Node
        List with all nodes associated with user-inserted distillation layers.

    """
def find_user_defined_nodes(traced_model: GraphModule, onnx_tensors_to_match: list[str], raise_on_number_mismatch: bool = True) -> list[Node]:
    """
    Finds specific nodes in a PyTorch model converted from onnx.

    Each node output tensors should match a specific subset of onnx model tensor names defined by user.

    Parameters
    ----------
    traced_model : torch.fx.GraphModule
        PyTorch model converted from onnx file.
    onnx_tensors_to_match : list with str
        Tensor names in the original onnx file.
    raise_on_number_mismatch : bool, optional
        Whether to raise RuntimeError when the number of found nodes is not equal to the number of requested tensors to
        match. Default value is True.

    Returns
    -------
    list with torch.fx.Node
        List with nodes which outputs match at least one output tensor name from the provided list.

    Raises
    ------
    RuntimeError
        When the number of found nodes is not equal to the number of requested tensors to match.

    """
def find_node_references_in_output_node(output_node: Node) -> list[Node]: ...
