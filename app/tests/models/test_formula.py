import pytest

from app.models.formula import ContinuousRange


def test_continuous_range_without_min_max():
    with pytest.raises(ValueError):
        ContinuousRange()
