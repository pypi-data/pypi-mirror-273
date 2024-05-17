# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as npt
import openmdao.api as om
import pytest
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, PowerTransformer

from surrogates_interface.openmdao import InputOutputType, SurrogateModelComp
from surrogates_interface.surrogates import SurrogateModel
from surrogates_interface.transformers import Transformer


class Paraboloid(SurrogateModel):
    """Define a paraboloid."""

    coef_1 = np.array([0.2, 0.5, 0.3])
    coef_2 = np.array([1.2, 1.5, 1.3])

    def _predict_model_output(self, x):
        y = np.column_stack(
            (np.sum(self.coef_1 * x**2, axis=1), np.sum(self.coef_2 * x**2, axis=1))
        )
        return y

    def _predict_model_jacobian(self, x):
        y = self._predict_model_output(x)
        jac = np.stack((2.0 * self.coef_1 * x, 2.0 * self.coef_2 * x), axis=1)
        return y, jac


@pytest.fixture
def make_data():
    rng = np.random.default_rng(seed=123)
    n_points = 100
    n_inputs_original = 5
    n_outputs_original = 4
    input = rng.uniform(-1.0, +1.0, size=(n_points, n_inputs_original))
    # Introduce linear correlation between some input features.
    input[:, 1] = 2.0 * input[:, 0]
    input[:, 2] = 3.0 * input[:, 0] - 5.0
    # Build input transformers.
    sklearn_input_transformers = [
        PowerTransformer(standardize=False),
        PCA(n_components=3, whiten=False),
    ]
    input_transformed = input.copy()
    for transformer in sklearn_input_transformers:
        input_transformed = transformer.fit_transform(input_transformed)
    si_input_transformers = [
        Transformer.from_sklearn(t) for t in sklearn_input_transformers
    ]
    # Make a dummy output. We only need it to create the transformers.
    output = np.zeros((n_points, n_outputs_original))
    output[:, 0] = np.sin(input[:, 0]) * np.cos(input[:, 4])
    output[:, 1] = np.sum(input**2, axis=1)
    # Introduce linear correlation between some output features.
    output[:, 2] = 1.1 * output[:, 0]
    output[:, 3] = 0.5 * output[:, 1]
    # Build output transformers.
    sklearn_output_transformers = [
        MinMaxScaler(feature_range=(-1.0, +1.0), clip=False),
        PCA(n_components=2, whiten=False),
    ]
    output_transformed = output.copy()
    for transformer in sklearn_output_transformers:
        output_transformed = transformer.fit_transform(output_transformed)
    si_output_transformers = [
        Transformer.from_sklearn(t) for t in sklearn_output_transformers
    ]
    # Build the surrogate model.
    si_model = Paraboloid(
        [],  # model is dummy.
        input_transformers=si_input_transformers,
        output_transformers=si_output_transformers,
        n_inputs=n_inputs_original,
        n_outputs=n_outputs_original,
    )
    # Evaluate it on the input, and overwrite the transformed output.
    output_transformed = si_model._predict_model_output(input_transformed)
    # Apply inverse output transformations and overwrite the original output.
    output = output_transformed.copy()
    for transformer in reversed(si_output_transformers):
        output = transformer.inverse_transform(output, inplace=False)
    return (
        si_model,
        input,
        output,
    )


def test_jacobian(make_data):
    si_model, input, _ = make_data
    # Compute exact Jacobian.
    jacobian_si = si_model.predict_jacobian(input)
    # Compute Jacobian using central finite differences.
    jacobian_fd = np.zeros_like(jacobian_si)
    h = 1e-6
    for i in range(input.shape[1]):
        xm = input.copy()
        xp = input.copy()
        xm[:, i] -= h
        xp[:, i] += h
        jacobian_fd[:, :, i] = si_model.predict_output(xp) - si_model.predict_output(xm)
    jacobian_fd /= 2.0 * h
    # Test.
    npt.assert_allclose(jacobian_si, jacobian_fd, rtol=2e-7)


def test_om_compute_partials_joined_joined(make_data):
    # Get the data.
    si_model, input, _ = make_data
    # Make the OpenMDAO problem.
    problem = om.Problem()
    component = SurrogateModelComp(
        model=si_model,
        input_type=InputOutputType.JOINED,
        output_type=InputOutputType.JOINED,
        n_points=input.shape[0],
    )
    problem.model.add_subsystem(
        "surrogate", component, promotes_inputs=["x"], promotes_outputs=["y"]
    )
    problem.setup()
    # Set the input.
    problem.set_val("x", input)
    # Check partial derivatives.
    om_partials = problem.check_partials(
        out_stream=None, step=1e-6, step_calc="abs", form="central"
    )
    # Jacobian computed by finite differences.
    jacobian_fd = om_partials["surrogate"][("y", "x")]["J_fd"]
    # Exact Jacobian.
    jacobian_exact = om_partials["surrogate"][("y", "x")]["J_fwd"]
    # Test.
    npt.assert_allclose(jacobian_fd, jacobian_exact, rtol=2e-7)
