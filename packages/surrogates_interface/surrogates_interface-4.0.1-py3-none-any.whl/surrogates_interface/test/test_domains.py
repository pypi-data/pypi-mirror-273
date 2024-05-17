# -*- coding: utf-8 -*-
import numpy as np
import numpy.testing as npt
import pytest

from surrogates_interface.domains import BoxDomain, GenericDomain


class TestBoxDomain:
    @staticmethod
    def test_in_domain():
        min = np.array([-1.0, +2.0, -15.0])
        max = np.array([+1.0, +7.0, +8.0])
        x = np.array(
            [[0.0, 0.0, 0.0], [0.0, 4.0, 9.0], [0.0, 4.0, 0.0], [3.0, 4.0, 6.0]]
        )
        box = BoxDomain(min, max)
        out = box.in_domain(x)
        npt.assert_array_equal(out, np.array([False, False, True, False]))

    @staticmethod
    def test_bad_box():
        min = np.array([-1.0, +7.0])
        max = np.array([+1.0, -15.0])
        with pytest.raises(AssertionError):
            BoxDomain(min, max)

    @staticmethod
    def test_eq():
        box1 = BoxDomain([-1.0, +2.0, -15.0], [+1.0, +7.0, +8.0])
        box2 = BoxDomain([-1.0, -5.0, -15.0], [+1.0, +7.0, +8.0])
        assert not box1 == box2

    @staticmethod
    def test_eq_different_type():
        class DummyDomain(GenericDomain):
            fields = []

            def in_domain():
                pass

        box1 = BoxDomain([-1.0, +2.0, -15.0], [+1.0, +7.0, +8.0])
        box2 = DummyDomain()
        assert not box1 == box2
