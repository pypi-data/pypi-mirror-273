from _typeshed import Incomplete
from enot.distillation.mapping._adder.factory import create_adder as create_adder
from enot.distillation.mapping._output_replacer.factory import create_output_replacer as create_output_replacer
from enot.distillation.mapping._output_replacer.output_replacer import OutputReplacer as OutputReplacer
from typing import Any, NamedTuple

Module: Incomplete
Mappable: Incomplete

class Mapping:
    """Mapping between modules of student and teacher models."""

    class _Mapping(NamedTuple):
        student_module: Mappable
        teacher_module: Mappable
        payload: Any
    def __init__(self, student: Module, teacher: Module) -> None:
        """
        Parameters
        ----------
        student : Module
            Student module.
        teacher : Module
            Teacher module.

        """
    def add(self, student_module: Mappable, teacher_module: Mappable, *, payload: Any = None) -> None:
        """
        Add pair to mapping.

        Parameters
        ----------
        student_module : Mappable
            Student module which will be associated with teacher module.
        teacher_module : Mappable
            Teacher module which will be associated with student module.
        payload : Any
            Payload, default value is None.

        """
    def apply(self) -> tuple[Module, Module]:
        """Apply mapping."""
    def revert(self) -> tuple[Module, Module]:
        """Revert all changes."""
    @property
    def student(self) -> Module: ...
    @property
    def teacher(self) -> Module: ...
    def payload(self) -> list[Any]:
        """Payload, order is preserved."""
