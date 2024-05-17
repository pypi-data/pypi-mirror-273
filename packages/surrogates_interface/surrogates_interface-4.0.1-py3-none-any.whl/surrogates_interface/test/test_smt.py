# -*- coding: utf-8 -*-

import uuid

import numpy as np
import numpy.testing as npt
import pytest
from smt.surrogate_models import KRG, RBF

from surrogates_interface.domains import BoxDomain
from surrogates_interface.surrogates import SMTModel

# %% Test SMTModel.


@pytest.fixture
def make_data_siso_rbf():
    # Example from https://smt.readthedocs.io/en/stable/_src_docs/surrogate_models/rbf.html
    xt = np.array([0.0, 1.0, 2.0, 3.0, 4.0]).reshape(-1, 1)
    yt = np.array([0.0, 1.0, 1.5, 0.9, 1.0]).reshape(-1, 1)

    sm = RBF(d0=5, print_global=False)

    sm.set_training_values(xt, yt)
    sm.train()

    x = np.linspace(0.0, 4.0, 100).reshape(-1, 1)
    y = sm.predict_values(x)

    model = SMTModel(
        sm,
        n_inputs=1,
        n_outputs=1,
    )
    return model, x, y


@pytest.fixture
def make_data_siso_krg():
    # Example from https://smt.readthedocs.io/en/stable/_src_docs/surrogate_models/rbf.html
    xt = np.array([0.0, 1.0, 2.0, 3.0, 4.0]).reshape(-1, 1)
    yt = np.array([0.0, 1.0, 1.5, 0.9, 1.0]).reshape(-1, 1)

    sm = KRG(print_global=False)

    sm.set_training_values(xt, yt)
    sm.train()

    x = np.linspace(0.0, 4.0, 100).reshape(-1, 1)
    y = sm.predict_values(x)

    model = SMTModel(
        sm,
        n_inputs=1,
        n_outputs=1,
    )
    return model, x, y


def test_predict_output_siso_rbf(make_data_siso_rbf):
    si_model, input, output = make_data_siso_rbf
    output_si = si_model.predict_output(input)
    npt.assert_array_equal(output_si, output)


def test_predict_jacobian_siso_rbf(make_data_siso_rbf):
    si_model, input, _ = make_data_siso_rbf
    # Compute jacobian using the chain rule and SMT.
    jacobian_si = si_model.predict_jacobian(input)
    # Compute jacobian using central finite differences.
    h = 1e-5
    jacobian_fd = np.zeros(jacobian_si.shape)
    jacobian_fd[:, 0, 0] = (
        si_model.predict_output(input + h).ravel()
        - si_model.predict_output(input - h).ravel()
    ) / (2.0 * h)
    npt.assert_allclose(jacobian_si, jacobian_fd, rtol=2e-5, atol=5e-7)


@pytest.fixture
def make_data_miso_rbf():
    # Build input and output.
    domain = BoxDomain([-5.0, -10.0], [10.0, 2.0])
    xt = np.column_stack(
        (
            np.linspace(domain.min[0], domain.max[0], 11),
            np.linspace(domain.min[1], domain.max[1], 11),
        )
    )
    yt = np.sum(xt**2, axis=1, keepdims=True)

    # Train.
    sm = RBF(d0=5, print_global=False)

    sm.set_training_values(xt, yt)
    sm.train()

    x = np.column_stack(
        (
            np.linspace(domain.min[0], domain.max[0], 21),
            np.linspace(domain.min[1], domain.max[1], 21),
        )
    )
    y = sm.predict_values(x)

    model = SMTModel(
        sm,
        n_inputs=2,
        n_outputs=1,
        domain=domain,
    )
    return model, x, y


def test_predict_output_miso_rbf(make_data_miso_rbf):
    si_model, input, output = make_data_miso_rbf
    output_si = si_model.predict_output(input)
    npt.assert_array_equal(output_si, output)


def test_predict_jacobian_miso_rbf(make_data_miso_rbf):
    si_model, input, _ = make_data_miso_rbf
    # Compute jacobian using the chain rule and SMT.
    jacobian_si = si_model.predict_jacobian(input)
    # Compute jacobian using central finite differences.
    jacobian_fd = np.zeros(jacobian_si.shape)
    h = 1e-5
    for i in range(input.shape[1]):
        xm = input.copy()
        xp = input.copy()
        xm[:, i] -= h
        xp[:, i] += h
        jacobian_fd[:, 0, i] = (
            si_model.predict_output(xp).ravel() - si_model.predict_output(xm).ravel()
        )
    jacobian_fd /= 2.0 * h
    npt.assert_allclose(jacobian_si, jacobian_fd, rtol=5e-7)


@pytest.fixture
def make_data_simo_rbf():
    # Build input and output.
    domain = BoxDomain([-5.0], [10.0])
    xt = np.linspace(domain.min[0], domain.max[0], 11).reshape(-1, 1)
    yt = np.column_stack((xt**2, 0.5 * xt**2))

    # Train.
    sm = RBF(d0=5, print_global=False)

    sm.set_training_values(xt, yt)
    sm.train()

    x = np.linspace(domain.min[0], domain.max[0], 21).reshape(-1, 1)
    y = sm.predict_values(x)

    model = SMTModel(
        sm,
        n_inputs=1,
        n_outputs=2,
        domain=domain,
    )
    return model, x, y


def test_predict_output_simo_rbf(make_data_simo_rbf):
    si_model, input, output = make_data_simo_rbf
    output_si = si_model.predict_output(input)
    npt.assert_array_equal(output_si, output)


def test_predict_jacobian_simo_rbf(make_data_simo_rbf):
    si_model, input, _ = make_data_simo_rbf
    # Compute jacobian using the chain rule and SMT.
    jacobian_si = si_model.predict_jacobian(input)
    # Compute jacobian using central finite differences.
    h = 1e-5
    jacobian_fd = np.zeros(jacobian_si.shape)
    jacobian_fd[:, :, 0] = (
        si_model.predict_output(input + h) - si_model.predict_output(input - h)
    ) / (2.0 * h)
    npt.assert_allclose(jacobian_si, jacobian_fd, rtol=5e-7)


@pytest.fixture
def make_data_mimo_rbf():
    # Build input and output.
    domain = BoxDomain([-5.0, -10.0], [10.0, 2.0])
    xt = np.column_stack(
        (
            np.linspace(domain.min[0], domain.max[0], 11),
            np.linspace(domain.min[1], domain.max[1], 11),
        )
    )
    yt = np.column_stack(
        (0.8 * xt[:, 0] ** 2, 0.5 * xt[:, 1] ** 2, np.sum(xt**2, axis=1))
    )

    # Train.
    sm = RBF(d0=5, print_global=False)

    sm.set_training_values(xt, yt)
    sm.train()

    x = np.column_stack(
        (
            np.linspace(domain.min[0], domain.max[0], 21),
            np.linspace(domain.min[1], domain.max[1], 21),
        )
    )
    y = sm.predict_values(x)

    model = SMTModel(
        sm,
        n_inputs=2,
        n_outputs=3,
        domain=domain,
    )
    return model, x, y


def test_predict_output_mimo_rbf(make_data_mimo_rbf):
    si_model, input, output = make_data_mimo_rbf
    output_si = si_model.predict_output(input)
    npt.assert_array_equal(output_si, output)


def test_predict_jacobian_mimo_rbf(make_data_mimo_rbf):
    si_model, input, _ = make_data_mimo_rbf
    # Compute jacobian using the chain rule and SMT.
    jacobian_si = si_model.predict_jacobian(input)
    # Compute jacobian using central finite differences.
    jacobian_fd = np.zeros(jacobian_si.shape)
    h = 1e-5
    for i in range(input.shape[1]):
        xm = input.copy()
        xp = input.copy()
        xm[:, i] -= h
        xp[:, i] += h
        jacobian_fd[:, :, i] = si_model.predict_output(xp) - si_model.predict_output(xm)
    jacobian_fd /= 2.0 * h
    npt.assert_allclose(jacobian_si, jacobian_fd, rtol=5e-7)


def test_save_load_python(make_data_siso_krg):
    si_model, _, _ = make_data_siso_krg
    model_path = f"./{str(uuid.uuid4())}-model.h5"
    extra_data_path = f"./{str(uuid.uuid4())}-extra-data.h5"
    si_model.save_h5(model_path, extra_data_path)
    si_model_loaded = SMTModel.load_h5(model_path, extra_data_path)
    assert si_model == si_model_loaded


def test_save_load_cpp(make_data_siso_rbf):
    si_model, _, _ = make_data_siso_rbf
    model_path = f"./{str(uuid.uuid4())}-model.h5"
    extra_data_path = f"./{str(uuid.uuid4())}-extra-data.h5"
    with pytest.raises(NotImplementedError):
        si_model.save_h5(model_path, extra_data_path)
