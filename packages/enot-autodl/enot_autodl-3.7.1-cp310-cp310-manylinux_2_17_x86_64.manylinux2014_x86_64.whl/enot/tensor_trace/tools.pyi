from enot.tensor_trace.tracing import Node as Node, OpNode as OpNode, ParameterNode as ParameterNode

def get_tracing_node_by_module_name(name: str, graph: list[Node]) -> OpNode:
    '''
    Return the tracing node corresponding to the module with the given name.

    Note: current implementation works ONLY for modules with "weight" parameter.

    Parameters
    ----------
    name : str
        Name of module in torch model, for example: "features.5.conv.1.0".
    graph : List[Node]
        Tracing graph.

    Returns
    -------
    OpNode
        Node (OpNode) corresponding to the module with the given name.

    Raises
    ------
    ValueError
        If node corresponding to the module name is not found.

    '''
def get_module_name_by_tracing_node(node: OpNode) -> str:
    '''
    Return the module name corresponding to the node.

    Note: current implementation works ONLY for modules with "weight" parameter.
    Also, you can easy get a module by its name with the help of ``getattr_complex``.

    Parameters
    ----------
    node : OpNode
        The node for which the module name should be found.

    Returns
    -------
    str
        Module name corresponding to the node.

    Raises
    ------
    ValueError
        If module name corresponding to the node is not found.

    '''
