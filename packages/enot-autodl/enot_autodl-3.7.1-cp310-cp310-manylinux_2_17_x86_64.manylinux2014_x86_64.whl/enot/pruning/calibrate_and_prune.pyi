import torch
from enot.pruning.calibrate import calibrate_model_for_pruning as calibrate_model_for_pruning
from enot.pruning.label_selector import ChannelsSelectorConstraint as ChannelsSelectorConstraint, GlobalPruningLabelSelectorByChannels as GlobalPruningLabelSelectorByChannels, OptimalPruningLabelSelector as OptimalPruningLabelSelector, PruningLabelSelector as PruningLabelSelector, UniformPruningLabelSelector as UniformPruningLabelSelector
from enot.pruning.prune import prune_model as prune_model
from enot.utils.batch_norm import tune_bn_stats as tune_bn_stats
from enot.utils.common import Number as Number
from enot.utils.dataloader2model import DataLoaderSampleToModelInputs as DataLoaderSampleToModelInputs, DataLoaderSampleToNSamples as DataLoaderSampleToNSamples, default_sample_to_model_inputs as default_sample_to_model_inputs, default_sample_to_n_samples as default_sample_to_n_samples
from torch.utils.data import DataLoader as DataLoader
from typing import Any, Callable

def calibrate_and_prune_model(label_selector: PruningLabelSelector, model: torch.nn.Module, dataloader: DataLoader, loss_function: Callable[[Any, Any], torch.Tensor], finetune_bn: bool = False, calibration_steps: int | None = None, calibration_epochs: int = 1, sample_to_n_samples: DataLoaderSampleToNSamples = ..., sample_to_model_inputs: DataLoaderSampleToModelInputs = ..., show_tqdm: bool = False, entry_point: str = 'forward') -> torch.nn.Module:
    '''
    Estimates channel importance values and prunes model with user defined strategy.

    This function searches for prunable channels in user-defined ``model``. After extracting channel information from
    model graph, estimates channel importance values for later pruning. After that prunes model by removing channels
    provided by user-defined channel selection strategy ``label_selector``.

    Parameters
    ----------
    label_selector : PruningLabelSelector
        Channel selector object. This object should implement :meth:`.PruningLabelSelector.select` method which returns
        list with channel indices to prune.
    model : torch.nn.Module
        Model to prune.
    dataloader : torch.utils.data.DataLoader
        Dataloader for estimation of model channel importance values.
    loss_function : Callable[[Any, Any], torch.Tensor]
        Function which takes model output and dataloader sample and computes loss tensor. This function should take two
        inputs and return scalar PyTorch tensor.
    finetune_bn : bool, optional
        Finetune batch norm layers (specifically, their running mean and running variance values) for better model
        quality. Default value is False.
    calibration_steps : int or None, optional
        Number of total calibration steps. Default value is None, which runs calibration on all dataloader images for
        the number of epochs specified in ``calibration_epochs`` argument.
    calibration_epochs : int, optional
        Number of total calibration epochs. Not used when ``calibration_steps`` argument is not None. Default value is
        1.
    sample_to_n_samples : Callable, optional
        Function which computes the number of instances (objects to process) in single dataloader batch (dataloader
        sample). This function should take single input (dataloader sample) and return single integer - the number of
        instances. Default value is :func:`.default_sample_to_n_samples`. See more :ref:`here <s2ns ref>`.
    sample_to_model_inputs : Callable, optional
        Function to map dataloader samples to model input format. Default value is
        :func:`.default_sample_to_model_inputs`. See more :ref:`here <s2mi ref>`.
    show_tqdm : bool, optional
        Whether to log calibration procedure with `tqdm <https://github.com/tqdm/tqdm>`_ progress bar. Default value is
        False.
    entry_point : str, optional
        Model function for execution. See ``Notes`` section for the detailed argument description. Default value is
        "forward".

    Returns
    -------
    torch.nn.Module
        Pruned model.

    '''
def calibrate_and_prune_model_equal(model: torch.nn.Module, dataloader: DataLoader, loss_function: Callable[[Any, Any], torch.Tensor], pruning_ratio: Number = 0.5, finetune_bn: bool = False, calibration_steps: int | None = None, calibration_epochs: int = 1, sample_to_n_samples: DataLoaderSampleToNSamples = ..., sample_to_model_inputs: DataLoaderSampleToModelInputs = ..., show_tqdm: bool = False, entry_point: str = 'forward') -> torch.nn.Module:
    '''
    Estimates channel importance values and prunes model with equal pruning strategy (same percentage of channels are
    pruned in each prunable layer).

    Parameters
    ----------
    model : torch.nn.Module
        Model to prune.
    dataloader : torch.utils.data.DataLoader
        Dataloader for estimation of model channel importance values.
    loss_function : Callable[[Any, Any], torch.Tensor]
        Function which takes model output and dataloader sample and computes loss tensor. This function should take two
        inputs and return scalar PyTorch tensor.
    pruning_ratio : float, optional
        Relative amount of channels to prune at each prunable layers. Default value is 0.5 (prunes 50% of channels,
        which typically reduces the number of FLOPs and parameters by a factor of 4).
    finetune_bn : bool, optional
        Finetune batch norm layers (specifically, their running mean and running variance values) for better model
        quality. Default value is False.
    calibration_steps : int or None, optional
        Number of total calibration steps. Default value is None, which runs calibration on all dataloader samples for
        the number of epochs specified in ``calibration_epochs`` argument.
    calibration_epochs : int, optional
        Number of total calibration epochs. Not used when ``calibration_steps`` argument is not None. Default value is
        1.
    sample_to_n_samples : Callable, optional
        Function which computes the number of instances (objects to process) in single dataloader batch (dataloader
        sample). This function should take single input (dataloader sample) and return single integer - the number of
        instances. Default value is :func:`.default_sample_to_n_samples`. See more :ref:`here <s2ns ref>`.
    sample_to_model_inputs : Callable, optional
        Function to map dataloader samples to model input format. Default value is
        :func:`.default_sample_to_model_inputs`. See more :ref:`here <s2mi ref>`.
    show_tqdm : bool, optional
        Whether to log calibration procedure with `tqdm <https://github.com/tqdm/tqdm>`_ progress bar. Default value is
        False.
    entry_point : str, optional
        Model function for execution. See notes below for the detailed argument description.
        Default value is "forward".

    Returns
    -------
    torch.nn.Module
        Pruned model.

    '''
def calibrate_and_prune_model_optimal(model: torch.nn.Module, dataloader: DataLoader, loss_function: Callable[[Any, Any], torch.Tensor], latency_calculation_function: Callable[[torch.nn.Module], float], target_latency: Number, finetune_bn: bool = False, calibration_steps: int | None = None, calibration_epochs: int = 1, sample_to_n_samples: DataLoaderSampleToNSamples = ..., sample_to_model_inputs: DataLoaderSampleToModelInputs = ..., show_tqdm: bool = False, channels_selection_constraint: ChannelsSelectorConstraint | None = None, n_search_steps: int = 200, entry_point: str = 'forward', **kwargs) -> torch.nn.Module:
    '''
    Estimates channel importance values, searches for the optimal pruning configuration (percentage of channels to prune
    in each prunable layer) and prunes model.

    Parameters
    ----------
    model : torch.nn.Module
        Model to prune.
    dataloader : torch.utils.data.DataLoader
        Dataloader for estimation of model channel importance values.
    loss_function : Callable[[Any, Any], torch.Tensor]
        Function which takes model output and dataloader sample and computes loss tensor. This function should take two
        inputs and return scalar PyTorch tensor.
    latency_calculation_function : Callable[[torch.nn.Module], float]
        Function that calculates model latency.
        It should take model (torch.nn.Module) and measure the "speed" (float) of its execution.
        It could be a number of FLOPs, MACs, inference time on CPU/GPU or other "speed" criteria.
    target_latency : float
        Target model latency. This argument should have the same units as ``latency_calculation_function``\'s output.
    finetune_bn : bool, optional
        Finetune batch norm layers (specifically, their running mean and running variance values) for better model
        quality. Default value is False.
    calibration_steps : int or None, optional
        Number of total calibration steps. Default value is None, which runs calibration on all dataloader samples for
        the number of epochs specified in ``calibration_epochs`` argument.
    calibration_epochs : int, optional
        Number of total calibration epochs. Not used when ``calibration_steps`` argument is not None. Default value is
        1.
    sample_to_n_samples : Callable, optional
        Function which computes the number of instances (objects to process) in single dataloader batch (dataloader
        sample). This function should take single input (dataloader sample) and return single integer - the number of
        instances. Default value is :func:`.default_sample_to_n_samples`. See more :ref:`here <s2ns ref>`.
    sample_to_model_inputs : Callable, optional
        Function to map dataloader samples to model input format. Default value is
        :func:`.default_sample_to_model_inputs`. See more :ref:`here <s2mi ref>`.
    show_tqdm : bool, optional
        Whether to log calibration procedure with `tqdm <https://github.com/tqdm/tqdm>`_ progress bar. Default value is
        False.
    channels_selection_constraint : Optional[ChannelsSelectorConstraint]
        Optional :class:`~enot.pruning.ChannelsSelectorConstraint` instance,
        that calculates low, high and step for the channels constraint for total number of channels in gate.
        If None, then :class:`~enot.pruning.DefaultChannelsSelectorConstraint` will be used.
        None by default.
    n_search_steps : int, optional
        Number of sampled configurations for pruning to select optimal architecture. Default value is 200.
    entry_point : str, optional
        Model function for execution. See notes in :func:`~calibrate_and_prune_model_equal`
        for the detailed argument description.
        Default value is "forward".
    **kwargs
        Additional keyword arguments for label selector.

    Returns
    -------
    torch.nn.Module
        Pruned model.

    '''
def calibrate_and_prune_model_global_wrt_metric_drop(model: torch.nn.Module, dataloader: DataLoader, loss_function: Callable[[Any, Any], torch.Tensor], validation_function: Callable[[torch.nn.Module], float], maximal_acceptable_metric_drop: Number, minimal_channels_to_prune: int = 100, maximal_channels_to_prune: int = 300, channel_step_to_search: int = 10, finetune_bn: bool = False, calibration_steps: int | None = None, calibration_epochs: int = 1, sample_to_n_samples: DataLoaderSampleToNSamples = ..., sample_to_model_inputs: DataLoaderSampleToModelInputs = ..., show_tqdm: bool = False, entry_point: str = 'forward') -> torch.nn.Module:
    '''
    Estimates channel importance values and prunes model with global pruning strategy (same percentage of channels are
    pruned in each prunable layer).

    Parameters
    ----------
    model : torch.nn.Module
        Model to prune.
    dataloader : torch.utils.data.DataLoader
        Dataloader for estimation of model channel importance values.
    loss_function : Callable[[Any, Any], torch.Tensor]
        Function which takes model output and dataloader sample and computes loss tensor. This function should take two
        inputs and return scalar PyTorch tensor.
    validation_function : Callable[[torch.nn.Module], float]
        Function which evaluates pruned model to measure desired metric.
    maximal_acceptable_metric_drop : float
       Maximal value of the metric decrease.
    minimal_channels_to_prune : int
        Minimal channels amount to prune within all network.
    maximal_channels_to_prune: int
        Maximal channels amount to prune within all network.
    channel_step_to_search : int
        Channel configuration search step size. The greater value gives faster but less accurate results.
    finetune_bn : bool, optional
        Finetune batch norm layers (specifically, their running mean and running variance values) for better model
        quality. Default value is False.
    calibration_steps : int or None, optional
        Number of total calibration steps. Default value is None, which runs calibration on all dataloader images for
        the number of epochs specified in ``calibration_epochs`` argument.
    calibration_epochs : int, optional
        Number of total calibration epochs. Not used when ``calibration_steps`` argument is not None. Default value is
        1.
    sample_to_n_samples : Callable, optional
        Function which computes the number of instances (objects to process) in single dataloader batch (dataloader
        sample). This function should take single input (dataloader sample) and return single integer - the number of
        instances. Default value is :func:`.default_sample_to_n_samples`. See more :ref:`here <s2ns ref>`.
    sample_to_model_inputs : Callable, optional
        Function to map dataloader samples to model input format. Default value is
        :func:`.default_sample_to_model_inputs`. See more :ref:`here <s2mi ref>`.
    show_tqdm : bool, optional
        Whether to log calibration procedure with `tqdm <https://github.com/tqdm/tqdm>`_ progress bar. Default value is
        False.
    entry_point : str, optional
        Model function for execution. See ``Notes`` section for the detailed argument description. Default value is
        "forward".

    Returns
    -------
    torch.nn.Module
        Pruned model.

    Notes
    -----
    Before calling this function, your model should be prepared to be as close to practical inference usage as possible.
    For example, it is your responsibility to call ``eval`` method of your model if your inference requires calling this
    method (e.g. when the model contains dropout layers).

    Typically, it is better to calibrate model for pruning on validation-like data without augmentations (but with
    inference input preprocessing).

    If you encounter errors during backward call, you can wrap this function call with the following statement::

        with torch.autograd.set_detect_anomaly(True):
            calibrate_and_prune_model_equal(...)

    ``entry_point`` is a string that specifies which function of the user\'s model will be traced. Simple examples:
    "forward", "execute_model", "forward_train". If such a function is located in the model\'s submodule - then you
    should first write the submodule\'s name followed by the function name, all separated by dots:
    "submodule.forward", "head.predict_features", "submodule1.submodule2.forward".

    '''
