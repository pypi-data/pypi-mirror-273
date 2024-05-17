"""Hoppr exceptions and warnings."""

from __future__ import annotations


class HopprError(RuntimeError):
    """Base exception raised within the hoppr app."""


class HopprPluginError(HopprError):
    """Exception raised for errors working with plug-ins."""


class HopprLoadDataError(HopprError):
    """Exception raised for errors loading json/yml data."""


class HopprCredentialsError(HopprError):
    """Exception raised for errors loading credential data."""


class HopprValidationError(ValueError):  # pragma: no cover
    """Exception raised for failures during SBOM validation."""

    def __init__(self, *args: object, check_name: str) -> None:
        super().__init__(*args)
        self.check_name = check_name

    def __str__(self) -> str:
        return "".join(str(arg) for arg in self.args)


class HopprExperimentalWarning(UserWarning):
    """Warning raised when experimental features are accessed."""
