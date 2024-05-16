"""Resolutions provide answers to the Actor's Questions."""

from .is_visible import IsVisible

# Natural-language-enabling aliases
Visible = IsVisible

__all__ = [
    "IsVisible",
    "Visible",
]
