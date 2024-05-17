# -*- coding: utf-8 -*-
import re
import uuid

import h5py
import numpy as np
import numpy.testing as npt
import pytest
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, StandardScaler
from sklearn.preprocessing._data import QuantileTransformer

from surrogates_interface.transformers import PCA as PCASI
from surrogates_interface.transformers import MinMaxScaler as MinMaxScalerSI
from surrogates_interface.transformers import PowerTransformer as PowerTransformerSI
from surrogates_interface.transformers import PowerTransformerYeoJohnson
from surrogates_interface.transformers import StandardScaler as StandardScalerSI
from surrogates_interface.transformers import Transformer


class TestMinMaxScaler:
    @staticmethod
    @pytest.fixture(scope="class")
    def make_data():
        rng = np.random.default_rng(seed=1234)
        n_samples = 10
        x = np.column_stack(
            (
                rng.uniform(low=-5.0, high=20.0, size=(n_samples,)),
                rng.uniform(low=1.0, high=12.0, size=(n_samples,)),
                rng.uniform(low=-23.0, high=+101.0, size=(n_samples,)),
            )
        )
        # n_features = x.shape[1]

        sklearn_scaler = MinMaxScaler(feature_range=(-1.0, +1.0), copy=True, clip=False)
        x_transformed = sklearn_scaler.fit_transform(x)
        return sklearn_scaler, x, x_transformed

    @pytest.fixture(scope="class")
    def si_scaler(self, make_data):
        # test_from_sklearn
        sklearn_scaler, _, _ = make_data
        si_scaler = Transformer.from_sklearn(sklearn_scaler)
        npt.assert_array_equal(si_scaler.scale_, sklearn_scaler.scale_)
        npt.assert_array_equal(si_scaler.min_, sklearn_scaler.min_)
        return si_scaler

    @staticmethod
    def test_clip():
        scaler_with_clip = MinMaxScaler(clip=True)
        with pytest.raises(
            ValueError,
            match=re.escape(
                "clip is not supported, because it cannot be differentiated."
            ),
        ):
            MinMaxScalerSI.from_sklearn(scaler_with_clip)

    @staticmethod
    def test_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.transform(x, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed)

    @staticmethod
    def test_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x.copy()
        si_scaler.transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed)

    @staticmethod
    def test_inverse_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.inverse_transform(x_transformed, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=2)

    @staticmethod
    def test_inverse_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x_transformed.copy()
        si_scaler.inverse_transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=2)

    @staticmethod
    def test_transform_gradient(make_data, si_scaler):
        _, x, _ = make_data
        y_exact = si_scaler.transform_gradient(x)
        h = 1e-6
        y_fd = (
            si_scaler.transform(x + h, inplace=False)
            - si_scaler.transform(x, inplace=False)
        ) / h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_inverse_transform_gradient(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_exact = si_scaler.inverse_transform_gradient(x_transformed)
        h = 1e-6
        y_fd = (
            si_scaler.inverse_transform(x_transformed + h, inplace=False)
            - si_scaler.inverse_transform(x_transformed, inplace=False)
        ) / h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_eq():
        obj_1 = MinMaxScalerSI(
            np.array([1.1, 10.4, 3.7]), np.array([-3.0, -50.0, +21.0])
        )
        obj_2 = MinMaxScalerSI(
            np.array([1.1, 10.4, 3.7]), np.array([-3.0, -50.0, +21.0])
        )
        assert obj_1 == obj_2

    @staticmethod
    def test_eq_wrong_type():
        obj_1 = MinMaxScalerSI(
            np.array([1.1, 10.4, 3.7]), np.array([-3.0, -50.0, +21.0])
        )
        obj_2 = StandardScalerSI(np.array([1.1, 10.4]), np.array([-3.0, -50.0]))
        assert not (obj_1 == obj_2)


class TestStandardScaler:
    @staticmethod
    @pytest.fixture(scope="class")
    def make_data():
        rng = np.random.default_rng(seed=1234)
        n_samples = 10
        x = np.column_stack(
            (
                rng.uniform(low=-5.0, high=20.0, size=(n_samples,)),
                rng.uniform(low=1.0, high=12.0, size=(n_samples,)),
                rng.uniform(low=-23.0, high=+101.0, size=(n_samples,)),
            )
        )
        # n_features = x.shape[1]

        sklearn_scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
        x_transformed = sklearn_scaler.fit_transform(x)
        return sklearn_scaler, x, x_transformed

    @staticmethod
    @pytest.fixture(scope="class")
    def si_scaler(make_data):
        # test_from_sklearn
        sklearn_scaler, _, _ = make_data
        si_scaler = Transformer.from_sklearn(sklearn_scaler)
        npt.assert_array_almost_equal_nulp(si_scaler.scale_, sklearn_scaler.scale_)
        npt.assert_array_equal(si_scaler.mean_, sklearn_scaler.mean_)
        return si_scaler

    @staticmethod
    def test_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.transform(x, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed, nulp=180)

    @staticmethod
    def test_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x.copy()
        si_scaler.transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed, nulp=180)

    @staticmethod
    def test_inverse_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.inverse_transform(x_transformed, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=2)

    @staticmethod
    def test_inverse_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x_transformed.copy()
        si_scaler.inverse_transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=2)

    @staticmethod
    def test_transform_gradient(make_data, si_scaler):
        _, x, _ = make_data
        y_exact = si_scaler.transform_gradient(x)
        h = 1e-6
        y_fd = (
            si_scaler.transform(x + h, inplace=False)
            - si_scaler.transform(x, inplace=False)
        ) / h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_inverse_transform_gradient(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_exact = si_scaler.inverse_transform_gradient(x_transformed)
        h = 1e-6
        y_fd = (
            si_scaler.inverse_transform(x_transformed + h, inplace=False)
            - si_scaler.inverse_transform(x_transformed, inplace=False)
        ) / h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_eq():
        obj_1 = StandardScalerSI(np.array([1.1, 10.4]), np.array([-3.0, -50.0]))
        obj_2 = StandardScalerSI(np.array([1.1, 10.4]), np.array([-3.0, -50.0]))
        assert obj_1 == obj_2

    @staticmethod
    def test_eq_wrong_type():
        obj_1 = StandardScalerSI(np.array([1.1, 10.4]), np.array([-3.0, -50.0]))
        obj_2 = MinMaxScalerSI(
            np.array([1.1, 10.4, 3.7]), np.array([-3.0, -50.0, +21.0])
        )
        assert not (obj_1 == obj_2)


class TestPCA:
    @staticmethod
    @pytest.fixture(scope="class")
    def make_data_with_whitening():
        rng = np.random.default_rng(seed=1234)
        n_samples = 100
        n_features_original = 5
        x = rng.normal(
            loc=np.arange(n_features_original),
            scale=np.array([1.0, 5.0, 2.0, 20.0, 6.0]),
            size=(n_samples, n_features_original),
        )
        # Introduce linear correlation between some components.
        x[:, 1] = 2.0 * x[:, 0]
        x[:, 2] = 3.0 * x[:, 0] - 5.0
        sklearn_pca = PCA(n_components=3, whiten=True)
        x_transformed = sklearn_pca.fit_transform(x)
        # Test: with n_components=n_features_original,
        #       the last 2 elements of sklearn_pca.singular_values_ are small.
        return sklearn_pca, x, x_transformed

    @staticmethod
    @pytest.fixture(scope="class")
    def make_data_without_whitening():
        rng = np.random.default_rng(seed=1234)
        n_samples = 100
        n_features_original = 5
        x = rng.normal(
            loc=np.arange(n_features_original),
            scale=np.array([1.0, 5.0, 2.0, 20.0, 6.0]),
            size=(n_samples, n_features_original),
        )
        # Introduce linear correlation between some components.
        x[:, 1] = 2.0 * x[:, 0]
        x[:, 2] = 3.0 * x[:, 0] - 5.0
        sklearn_pca = PCA(n_components=3, whiten=False)
        x_transformed = sklearn_pca.fit_transform(x)
        # Test: with n_components=n_features_original,
        #       the last 2 elements of sklearn_pca.singular_values_ are small.
        return sklearn_pca, x, x_transformed

    @staticmethod
    @pytest.fixture(scope="class")
    def si_pca_with_whitening(make_data_with_whitening):
        # test_from_sklearn
        sklearn_pca, _, _ = make_data_with_whitening
        si_pca = Transformer.from_sklearn(sklearn_pca)
        npt.assert_array_almost_equal_nulp(
            np.sqrt(sklearn_pca.explained_variance_), si_pca.explained_std_
        )
        return si_pca

    @staticmethod
    @pytest.fixture(scope="class")
    def si_pca_without_whitening(make_data_without_whitening):
        # test_from_sklearn
        sklearn_pca, _, _ = make_data_without_whitening
        si_pca = Transformer.from_sklearn(sklearn_pca)
        npt.assert_array_almost_equal_nulp(
            np.sqrt(sklearn_pca.explained_variance_), si_pca.explained_std_
        )
        return si_pca

    @staticmethod
    def test_transform_outofplace_with_whitening(
        make_data_with_whitening, si_pca_with_whitening
    ):
        _, x, x_transformed = make_data_with_whitening
        y_si = si_pca_with_whitening.transform(x, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed, nulp=2500)

    @staticmethod
    def test_transform_inplace_with_whitening(
        make_data_with_whitening, si_pca_with_whitening
    ):
        _, x, _ = make_data_with_whitening
        with pytest.raises(
            ValueError,
            match=re.escape("The PCA transformation cannot be done inplace."),
        ):
            si_pca_with_whitening.transform(x, inplace=True)

    @staticmethod
    def test_inverse_transform_outofplace_with_whitening(
        make_data_with_whitening, si_pca_with_whitening
    ):
        _, x, x_transformed = make_data_with_whitening
        y_si = si_pca_with_whitening.inverse_transform(x_transformed, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=5900)

    @staticmethod
    def test_inverse_transform_inplace(make_data_with_whitening, si_pca_with_whitening):
        _, _, x_transformed = make_data_with_whitening
        with pytest.raises(
            ValueError,
            match=re.escape("The PCA inverse transformation cannot be done inplace."),
        ):
            si_pca_with_whitening.inverse_transform(x_transformed, inplace=True)

    @staticmethod
    def test_transform_outofplace_without_whitening(
        make_data_without_whitening, si_pca_without_whitening
    ):
        _, x, x_transformed = make_data_without_whitening
        y_si = si_pca_without_whitening.transform(x, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed, nulp=2500)

    @staticmethod
    def test_transform_inplace_without_whitening(
        make_data_without_whitening, si_pca_without_whitening
    ):
        _, x, _ = make_data_without_whitening
        with pytest.raises(
            ValueError,
            match=re.escape("The PCA transformation cannot be done inplace."),
        ):
            si_pca_without_whitening.transform(x, inplace=True)

    @staticmethod
    def test_inverse_transform_outofplace_without_whitening(
        make_data_without_whitening, si_pca_without_whitening
    ):
        _, x, x_transformed = make_data_without_whitening
        y_si = si_pca_without_whitening.inverse_transform(x_transformed, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=5900)

    @staticmethod
    def test_transform_gradient_with_whitening(
        make_data_with_whitening, si_pca_with_whitening
    ):
        _, x, _ = make_data_with_whitening
        # Compute exact gradient.
        y_exact = si_pca_with_whitening.transform_gradient(x)
        # Compute gradient with central finite differences.
        y_fd = np.zeros(
            (
                x.shape[0],
                si_pca_with_whitening.n_components,
                si_pca_with_whitening.n_features,
            )
        )
        h = 1e-5
        for i in range(x.shape[1]):
            xm = x.copy()
            xp = x.copy()
            xm[:, i] -= h
            xp[:, i] += h
            y_fd[:, :, i] = si_pca_with_whitening.transform(
                xp, inplace=False
            ) - si_pca_with_whitening.transform(xm, inplace=False)
        y_fd /= 2.0 * h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_transform_gradient_without_whitening(
        make_data_without_whitening, si_pca_without_whitening
    ):
        _, x, _ = make_data_without_whitening
        # Compute exact gradient.
        y_exact = si_pca_without_whitening.transform_gradient(x)
        # Compute gradient with central finite differences.
        y_fd = np.zeros(
            (
                x.shape[0],
                si_pca_without_whitening.n_components,
                si_pca_without_whitening.n_features,
            )
        )
        h = 1e-5
        for i in range(x.shape[1]):
            xm = x.copy()
            xp = x.copy()
            xm[:, i] -= h
            xp[:, i] += h
            y_fd[:, :, i] = si_pca_without_whitening.transform(
                xp, inplace=False
            ) - si_pca_without_whitening.transform(xm, inplace=False)
        y_fd /= 2.0 * h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_inverse_transform_gradient_with_whitening(
        make_data_with_whitening, si_pca_with_whitening
    ):
        _, _, x_transformed = make_data_with_whitening
        # Compute exact gradient.
        y_exact = si_pca_with_whitening.inverse_transform_gradient(x_transformed)
        # Compute gradient with central finite differences.
        y_fd = np.zeros(
            (
                x_transformed.shape[0],
                si_pca_with_whitening.n_features,
                si_pca_with_whitening.n_components,
            )
        )
        h = 1e-6
        for i in range(x_transformed.shape[1]):
            xm = x_transformed.copy()
            xp = x_transformed.copy()
            xm[:, i] -= h
            xp[:, i] += h
            y_fd[:, :, i] = si_pca_with_whitening.inverse_transform(
                xp, inplace=False
            ) - si_pca_with_whitening.inverse_transform(xm, inplace=False)
        y_fd /= 2.0 * h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_inverse_transform_gradient_without_whitening(
        make_data_without_whitening, si_pca_without_whitening
    ):
        _, _, x_transformed = make_data_without_whitening
        # Compute exact gradient.
        y_exact = si_pca_without_whitening.inverse_transform_gradient(x_transformed)
        # Compute gradient with central finite differences.
        y_fd = np.zeros(
            (
                x_transformed.shape[0],
                si_pca_without_whitening.n_features,
                si_pca_without_whitening.n_components,
            )
        )
        h = 1e-5
        for i in range(x_transformed.shape[1]):
            xm = x_transformed.copy()
            xp = x_transformed.copy()
            xm[:, i] -= h
            xp[:, i] += h
            y_fd[:, :, i] = si_pca_without_whitening.inverse_transform(
                xp, inplace=False
            ) - si_pca_without_whitening.inverse_transform(xm, inplace=False)
        y_fd /= 2.0 * h
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_eq_different_type(si_pca_with_whitening):
        obj_2 = StandardScalerSI(np.array([1.0]), np.array([0.5]))
        assert not si_pca_with_whitening == obj_2

    @staticmethod
    def test_save_load(si_pca_with_whitening):
        path = f"./{str(uuid.uuid4())}.h5"
        with h5py.File(path, "w") as fid:
            si_pca_with_whitening._save_h5(fid)
        with h5py.File(path, "r") as fid:
            si_pca_saved = PCASI._load_h5(fid)
        assert si_pca_with_whitening == si_pca_saved


class TestPowerTransformerYeoJohnson:
    @staticmethod
    @pytest.fixture(scope="class")
    def make_data():
        rng = np.random.default_rng(seed=1234)
        n_samples = 100
        # We need to cover 4 cases, 2 with positive values and 2 with negative ones.
        x = rng.uniform(low=-5.0, high=5.0, size=(n_samples, 4))
        sklearn_scaler = PowerTransformer(
            method="yeo-johnson", standardize=False, copy=True
        )
        sklearn_scaler.fit(x)
        # Overwrite lambdas_, so that we can test everything.
        sklearn_scaler.lambdas_ = np.array([0.5, 0.0, 3.5, 2.0])
        x_transformed = sklearn_scaler.transform(x)
        return sklearn_scaler, x, x_transformed

    @pytest.fixture(scope="class")
    def si_scaler(self, make_data):
        # test_from_sklearn
        sklearn_scaler, _, _ = make_data
        si_scaler = Transformer.from_sklearn(sklearn_scaler)
        npt.assert_array_almost_equal_nulp(si_scaler.lambdas_, sklearn_scaler.lambdas_)
        return si_scaler

    @staticmethod
    def test_standardize():
        with pytest.raises(
            NotImplementedError,
            match=re.escape(
                "The standardize option is not supported. Please add a StandardScaler."
            ),
        ):
            PowerTransformerSI(np.array([]), standardize=True)

    @staticmethod
    def test_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.transform(x, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed)

    @staticmethod
    def test_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x.copy()
        si_scaler.transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x_transformed)

    @staticmethod
    def test_inverse_transform_outofplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = si_scaler.inverse_transform(x_transformed, inplace=False)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=35)

    @staticmethod
    def test_inverse_transform_inplace(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_si = x_transformed.copy()
        si_scaler.inverse_transform(y_si, inplace=True)
        npt.assert_array_almost_equal_nulp(y_si, x, nulp=35)

    @staticmethod
    def test_transform_gradient(make_data, si_scaler):
        _, x, x_transformed = make_data
        # Compute exact gradient.
        y_exact = si_scaler.transform_gradient(x)
        # Compute gradient with central finite differences.
        h = 1e-6
        y_fd = (
            si_scaler.transform(x + h, inplace=False)
            - si_scaler.transform(x - h, inplace=False)
        ) / (2 * h)
        npt.assert_allclose(y_exact, y_fd)

    @staticmethod
    def test_inverse_transform_gradient(make_data, si_scaler):
        _, x, x_transformed = make_data
        y_exact = si_scaler.inverse_transform_gradient(x_transformed)
        h = 1e-6
        y_fd = (
            si_scaler.inverse_transform(x_transformed + h, inplace=False)
            - si_scaler.inverse_transform(x_transformed - h, inplace=False)
        ) / (2 * h)
        npt.assert_allclose(y_exact, y_fd, rtol=5e-5)

    @staticmethod
    def test_eq_same_type():
        obj_1 = PowerTransformerSI(np.array([0.0, 3.5]), method="yeo-johnson")
        obj_2 = PowerTransformerSI(np.array([0.0, 3.5]), method="yeo-johnson")
        assert obj_1 == obj_2

    @staticmethod
    def test_eq_different_type():
        obj_1 = PowerTransformerSI(np.array([0.0, 3.5]), method="yeo-johnson")
        # obj_2 = PowerTransformerSI(np.array([0.0, 3.5]), method="box-cox")
        obj_2 = StandardScalerSI(np.array([1.0]), np.array([0.5]))
        assert not obj_1 == obj_2

    @staticmethod
    def test_save_load(si_scaler):
        path = f"./{str(uuid.uuid4())}.h5"
        with h5py.File(path, "w") as fid:
            si_scaler._save_h5(fid)
        with h5py.File(path, "r") as fid:
            scaler_saved = PowerTransformerYeoJohnson._load_h5(fid)
        assert si_scaler == scaler_saved

    @staticmethod
    def test_box_cox():
        with pytest.raises(NotImplementedError):
            PowerTransformerSI(np.array([0.0, 3.5]), method="box-cox")


def test_not_implemented_transformer():
    scaler = QuantileTransformer()
    with pytest.raises(NotImplementedError, match="QuantileTransformer not supported"):
        Transformer.from_sklearn(scaler)


@pytest.mark.parametrize(
    "scaler_cls,data",
    [
        (MinMaxScaler, np.reshape([4, 5, 6], (-1, 1))),
        (MinMaxScaler, [[4, 5, 6], [6, 8, 10]]),
        (StandardScaler, np.reshape([4, 5, 6], (-1, 1))),
        (StandardScaler, [[4, 5, 6], [6, 8, 10]]),
    ],
)
def test_save_load(scaler_cls, data):
    # test save and load with 1 and more features
    scaler_sk = scaler_cls()
    scaler_sk.fit_transform(data)
    scaler_si = Transformer.from_sklearn(scaler_sk)

    with h5py.File("tmp.hdf5", "w") as f:
        scaler_si._save_h5(f)
        saved_scaler_cls = {
            MinMaxScaler: MinMaxScalerSI,
            StandardScaler: StandardScalerSI,
        }[scaler_cls]
        scaler_saved = saved_scaler_cls._load_h5(f)

    npt.assert_array_equal(
        scaler_si.transform(data, inplace=False),
        scaler_si.transform(data, inplace=False),
    )
    npt.assert_array_equal(
        scaler_si.transform(data, inplace=False),
        scaler_saved.transform(data, inplace=False),
    )
