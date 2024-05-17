"""Subclasses of AssembleQualityData that cause the correct polcal metrics to build."""
from dkist_processing_common.tasks import AssembleQualityData

__all__ = ["CIAssembleQualityData", "SPAssembleQualityData"]


class CIAssembleQualityData(AssembleQualityData):
    """Subclass just so that the polcal_label_list can be populated."""

    @property
    def polcal_label_list(self) -> list[str]:
        """Return label(s) for Cryo CI."""
        return ["CI Beam 1"]


class SPAssembleQualityData(AssembleQualityData):
    """Subclass just so that the polcal_label_list can be populated."""

    @property
    def polcal_label_list(self) -> list[str]:
        """Return labels for beams 1 and 2."""
        return ["SP Beam 1", "SP Beam 2"]
