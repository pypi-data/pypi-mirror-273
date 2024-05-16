"""Enter text into an input field."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

if TYPE_CHECKING:
    from screenpy import Actor
    from typing_extensions import NotRequired, Self, Unpack

    from ..target import Target

    class EnterTypes(TypedDict):
        """Types that can be passed to Playwright's ElementHandle.fill method."""

        timeout: NotRequired[float | None]
        no_wait_after: NotRequired[bool | None]
        force: NotRequired[bool | None]


class Enter:
    """Enter text into an input field.

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(Enter("Hello!").into_the(GREETING_INPUT))

        the_actor.attempts_to(Enter("Hello!", force=True).into_the(GREETING_INPUT))

        the_actor.attempts_to(Enter.the_text("eggs").into_the(GROCERY_FIELD))

        the_actor.attempts_to(Enter.the_secret("12345").into_the(PASSWORD_FIELD))
    """

    target: Target | None

    @classmethod
    def the_text(cls, text: str, **kwargs: Unpack[EnterTypes]) -> Self:
        """Provide the text to enter into the field."""
        return cls(text, **kwargs)

    @classmethod
    def the_secret(cls, text: str, **kwargs: Unpack[EnterTypes]) -> Self:
        """Provide the **secret** text to enter into the field.

        The text will be masked, and appear as "[CENSORED]" in logs.

        Aliases:
            - ``the_password``
        """
        return cls(text, mask=True, **kwargs)

    the_password = the_secret

    def into_the(self, target: Target, **kwargs: Unpack[EnterTypes]) -> Enter:
        """Target the element to enter text into.

        Aliases:
            - ``into``
        """
        self.target = target
        self.kwargs.update(kwargs)
        return self

    into = into_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f'Enter "{self.text_to_log}" into the {self.target}.'

    @beat('{} enters "{text_to_log}" into the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter text into the Target."""
        if self.target is None:
            msg = (
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into(), .into_the(), or into_the_first_of_the() method."
            )
            raise UnableToAct(msg)

        self.target.found_by(the_actor).fill(self.text, **self.kwargs)

    def __init__(
        self, text: str, *, mask: bool = False, **kwargs: Unpack[EnterTypes]
    ) -> None:
        self.text = text
        self.target = None
        self.kwargs = kwargs

        if mask:
            self.text_to_log = "[CENSORED]"
        else:
            self.text_to_log = text
