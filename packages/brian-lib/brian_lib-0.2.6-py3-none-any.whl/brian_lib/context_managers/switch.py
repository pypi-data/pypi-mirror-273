"""
Module providing a context manager for switch-like behavior in Python.

This module defines the `Switch` class, which acts as a context manager
and facilitates implementing switch statements using type annotations and a
structured approach. 

The `Switch` class allows you to compare a variable against different
expressions within cases and execute code blocks accordingly. It supports
both strict and non-strict behavior to control if only the first matching
case is executed.
"""

from typing import Any
from beartype import beartype

@beartype
class Switch:
    """
    Context manager for implementing switch-like behavior in Python.

    This class provides a more structured and type-annotated way to implement
    switch statements in Python using a context manager approach."""

    def __init__(self, variable: Any, comparator: Any = lambda x, y: x == y, strict: bool = True):
        """
        Parameters:
        ----------
        variable (any): The variable to be compared against in each case.
        comparator (callable, optional): A function used to compare the variable
            with the expressions in each case. Defaults to lambda x, y: x == y.
        strict (bool, optional): A flag indicating strict behavior. When set to True,
            only the first matching case will be executed. Defaults to True.

        Returns:
        -------
        Switch: An instance of the Switch class.

        Yields:
        -------
        bool: True if a matching case is found, False otherwise.

        """

        self.variable = variable
        self.matched = False
        self.matching = False
        if comparator:
            self.comparator = comparator
        else:
            self.comparator = lambda x, y: x == y
        self.strict = strict

    def __enter__(self):
        """
        Enters the context manager.

        This method is called when entering the context manager block using the
        `with` statement. It returns the current Switch instance to allow for
        chaining methods within the context.

        Returns:
        -------
        Switch: The current Switch instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def case(self, expr: Any, break_: bool=False):
        """
        Checks if a case matches the variable and executes the corresponding code.

        This method compares the `expr` with the `variable` using the defined
        `comparator` function. If a match is found, it executes the code block
        within the `if` statement or subsequent `elif` statements (based on
        `break_` flag).

        Parameters:
        ----------
        expr (any): The expression to compare with the variable.
        break_ (bool, optional): A flag indicating whether to stop evaluating 
            further cases after a match is found. Defaults to False.

        Returns:
        -------
        bool: True if a match is found and the code is executed (or `break_` 
            is False), False 
        """
        if self.strict:
            if self.matched:
                return False
        if self.matching or self.comparator(self.variable, expr):
            if not break_:
                self.matching = True
            else:
                self.matched = True
                self.matching = False
            return True
        return False


    def default(self):
        """
        Checks if no case matched and executes the default code block.

        This method is called after all `case` methods have been evaluated. 
        It returns True if no matching case was found and the `variable` did not
        satisfy any comparison within the `case` methods.

        Returns:
        -------
        bool: True if no case matched, False otherwise.
        """
        return not self.matched and not self.matching
