# -*- coding: utf-8 -*-
import pytest

from surrogates_interface.surrogates import SurrogateModel


def test__save_model():
    obj = SurrogateModel(lambda x: x + 2.0)
    with pytest.raises(NotImplementedError):
        obj._save_model("file")


def test__load_model():
    obj = SurrogateModel(lambda x: x + 2.0)
    with pytest.raises(NotImplementedError):
        obj._load_model("file")


def test__predict_model_jacobian():
    obj = SurrogateModel(lambda x: x + 2.0)
    with pytest.raises(NotImplementedError):
        obj._predict_model_jacobian(1.0)
