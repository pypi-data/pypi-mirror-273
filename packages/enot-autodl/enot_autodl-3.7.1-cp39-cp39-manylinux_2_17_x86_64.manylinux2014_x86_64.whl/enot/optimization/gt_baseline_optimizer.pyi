import torch
from torch import nn
from torch.optim.optimizer import Optimizer
from typing import Any, Callable

class GTBaselineOptimizer:
    """
    Recommended optimizer for baseline training and tuning after pruning.
    GTBaselineOptimizer allows to achieve better metrics in most cases.

    Notes
    -----
    Use this optimizer simultaneously in train and tune procedure or do not use at all.
    The performance of this optimizer is two times lower than performance of base optimizer,
    and memory consumption is 1.5 times higher than memory consumption of base optimizer.

    """
    def __init__(self, model: nn.Module, optimizer: Optimizer | Any, *, allow_non_optimizer: bool = False, **kwargs) -> None:
        """
        Parameters
        ----------
        model : torch.nn.Module
            PyTorch model to optimize.
        optimizer : torch.optim.Optimizer
            PyTorch optimizer which will be wrapped by our optimizer.

        """
    @property
    def model(self) -> nn.Module:
        """
        Model passed to the constructor.

        Returns
        -------
        torch.nn.Module
            PyTorch model passed to the optimizer constructor.

        """
    @property
    def param_groups(self) -> list[dict[str, Any]]:
        """
        Returns ``param_groups`` variable of the wrapped optimizer.

        Returns
        -------
        list with dict with str keys
            User optimizer parameter groups.

        """
    def state_dict(self) -> dict[str, Any]:
        """
        Call ``state_dict`` of the wrapped optimizer and return the result.

        Returns
        -------
        dict with str keys
            User optimizer state dict.

        """
    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        """
        Call ``load_state_dict`` of the wrapped optimizer.

        Parameters
        ----------
        state_dict : dict with str keys
            State dict to be loaded to user optimizer instance.

        """
    def zero_grad(self, set_to_none: bool = True) -> None:
        """Call ``zero_grad`` of the wrapped optimizer."""
    def add_param_group(self, param_group: dict[str, Any]) -> None:
        """
        Call ``add_param_group`` of the wrapped optimizer.

        Parameters
        ----------
        param_group : dict with str keys
            Parameter group description to add to user optimizer.

        """
    def model_step(self, closure: Callable) -> float | torch.Tensor | None:
        '''
        Perform gradient accumulation step.

        Besides gradient computation, this method performs ENOT internal
        ENOT algorithms and utility configurations.

        To accumulate gradients, this method must perform complete
        gradient computation cycle, which consists of forward step
        following by backward step. To achieve this, it requires
        user-defined closure, which encapsulates both of these steps.

        It is usually enough to calculate model predictions, compute loss
        function by using model predictions, and then apply backprop
        algorithm to compute model parameter\'s gradients by calling
        `loss.backward()`.

        In more sophisticated situations, you should contact ENOT team to
        make sure that in your situation it is possible to use our current
        API and that nothing would go wrong.

        This function must be used in conjunction with the `step`
        function.

        Usually, you only need to call this function when you need
        gradient accumulation for multiple data batches. In this case, you
        should call `model_step` for each data batch within your larger
        "ghost batch". After accumulating gradients, you should call
        `step` function without arguments.

        Parameters
        ----------
        closure : Callable
            A closure (nested function which has access to a free variable
            from an enclosing function) that performs complete gradient
            accumulation procedure.

        Returns
        -------
        float or torch.Tensor or None
            The result of closure execution, which should be either a loss
            value stored in torch.Tensor or in float, or None.

        '''
    def step(self, closure: Callable | None = None) -> float | torch.Tensor | None:
        """
        Performs a single optimization step (parameter update).

        Optimization step includes gradient computation (forward+backward
        passes, only when closure is not None) and parameter update.
        Parameter update is performed by base optimizer provided by user.

        Besides gradient computation, this method performs ENOT internal
        ENOT algorithms and utility configurations.

        Calling this function with a non-None closure argument is
        equivalent to calling `model_step` with this closure followed by
        `step` call without any argument.

        More detailed description of gradient computation and closure
        structure can be found in `model_step` function documentation.

        Parameters
        ----------
        closure : Callable or None, optional
            A closure (nested function which has access to a free variable
            from an enclosing function) that performs complete gradient
            accumulation procedure. Must be None if you accumulated
            gradients using `model_step`. Default value is None.

        Returns
        -------
        float or torch.Tensor or None
            The result of closure execution, which should be either a loss
            value stored in torch.Tensor or in float, or None.

        """
