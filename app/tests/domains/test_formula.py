import pytest

from app.domains.formula import ContinuousRange


def test_continuous_range_without_min_max():
    with pytest.raises(ValueError):
        ContinuousRange()
