"""Represent an element on the page using its locator and a description."""

from __future__ import annotations

from collections import UserString
from dataclasses import dataclass
from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from .abilities import BrowseTheWebSynchronously
from .exceptions import TargetingError

if TYPE_CHECKING:
    from screenpy import Actor
    from typing_extensions import Self


@dataclass
class _Manipulation(UserString):
    """Represent one of the Playwright options for creating a locator.

    Could be a function or an attribute.

    This class allows the ScreenPy Playwright Target to behave just like a
    Playwright Locator, which has a robust, chainable API for describing
    elements.
    """

    target: Target
    name: str
    args: tuple | None = None
    kwargs: dict | None = None

    def __hash__(self) -> int:
        """Appear as the name, in case this is an attribute and not a method."""
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        """Appear as the name, in case this is an attribute and not a method."""
        return self.name == other

    def __getattr__(self, name: str) -> Target | _Manipulation:
        """Defer back to the Target for unknown attributes."""
        return getattr(self.target, name)

    def __call__(self, *args: str, **kwargs: str) -> Target:
        """Add args and kwargs to the manipulation."""
        self.args = args
        self.kwargs = kwargs
        return self.target

    def __repr__(self) -> str:
        """Reconstruct the locator function/attribute string."""
        args = kwargs = left_paren = right_paren = comma = ""
        if self.args is not None or self.kwargs is not None:
            left_paren = "("
            right_paren = ")"
        if self.args:
            args = ", ".join(repr(a) for a in self.args)
        if self.kwargs:
            kwargs = ", ".join(f"{k}={v!r}" for k, v in self.kwargs.items())
        if args and kwargs:
            comma = ", "
        return f"{self.name}{left_paren}{args}{comma}{kwargs}{right_paren}"

    # make sure we handle str here as well
    __str__ = __repr__


class Target:
    """A described element on a webpage.

    Uses Playwright's Locator API to describe an element on a webpage, with a
    few natural-language helpers. See the
    `Playwright documentation <https://playwright.dev/python/docs/locators>`_
    for more information.

    Examples::

        # Using CSS
        Target.the('"Log In" button').located_by("button:has-text('Log In')")

        # Using xpath
        Target.the("toast message").located_by("//toast")

        # Using Target methods with Playwright strategies
        Target.the('"Pick up Milk" todo item').in_frame("#todoframe").get_by_text(
            "Pick up Milk"
        )

        # Using Playwright strategies directly
        Target().frame_locator("#todoframe").get_by_label("todo")
    """

    manipulations: list[_Manipulation]
    _description: str | None

    @classmethod
    def the(cls: type[Self], name: str) -> Self:
        """Provide a human-readable description of the target."""
        return cls(name)

    def located_by(self, locator: str) -> Target:
        """Provide the CSS locator which describes the element."""
        self.manipulations.append(
            _Manipulation(self, "locator", args=(locator,), kwargs={})
        )
        return self

    def in_frame(self, frame_locator: str) -> Target:
        """Provide the CSS locator which describes the frame."""
        self.manipulations.append(
            _Manipulation(self, "frame_locator", args=(frame_locator,), kwargs={})
        )
        return self

    def __getattr__(self, name: str) -> _Manipulation:
        """Convert a Playwright Locator strategy into a Manipulation."""
        if not hasattr(Locator, name):
            msg = f"'{name}' is not a valid Playwright Locator strategy."
            raise AttributeError(msg)

        manipulation = _Manipulation(self, name)
        self.manipulations.append(manipulation)
        return manipulation

    @property
    def target_name(self) -> str:
        """Get the name of the Target.

        If a description was not provided, an identifier will be created using
        the manipulation chain.

        Returns:
            The text representation of this Target.
        """
        if self._description:
            target_name = self._description
        elif self.manipulations:
            target_name = ".".join(map(repr, self.manipulations))
        else:
            target_name = "None"
        return target_name

    @target_name.setter
    def target_name(self, value: str) -> None:
        """Set the target_name.

        Args:
            value: the new description to use.
        """
        self._description = value

    def found_by(self, the_actor: Actor) -> Locator:
        """Get the Playwright Locator described by this Target.

        Args:
            the_actor: the Actor who should find this Locator.

        Returns:
            The Locator which describes the element.
        """
        page = the_actor.ability_to(BrowseTheWebSynchronously).current_page

        if not self.manipulations:
            msg = f"{self} does not have any locator strategy set."
            raise TargetingError(msg)

        # Start with a base locator to ease typing. :face_rolling_eyes:
        locator = page.locator("html")
        for manipulation in self.manipulations:
            if manipulation.args is None and manipulation.kwargs is None:
                locator = getattr(locator, manipulation.name)
            else:
                locator = getattr(locator, manipulation.name)(
                    *manipulation.args, **manipulation.kwargs
                )

        return locator

    def __repr__(self) -> str:
        """Get a human-readable representation of this Target.

        Returns:
            A string representing this Target.
        """
        return self.target_name

    __str__ = __repr__

    def __init__(self, name: str | None = None) -> None:
        self._description = name
        self.manipulations = []
