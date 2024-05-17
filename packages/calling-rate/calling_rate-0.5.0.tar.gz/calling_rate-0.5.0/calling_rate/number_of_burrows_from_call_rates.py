from matplotlib import path
from scipy.spatial import ConvexHull
import numpy as np
import pandas as pd


def _get_burrow_coordinates(burrow_geci_data, burrow_jm_data):
    merged_data = pd.concat([burrow_geci_data[["X", "Y"]], burrow_jm_data[["X", "Y"]]])
    return merged_data


def _get_number_of_burrows_in_burrow_area(burrow_geci_data, burrow_jm_data):
    return _get_burrow_coordinates(burrow_geci_data, burrow_jm_data).shape[0]


def _get_burrow_area(burrow_geci_data, burrow_jm_data):
    burrow_points = _get_burrow_coordinates(burrow_geci_data, burrow_jm_data)
    return ConvexHull(burrow_points).volume


def get_density_in_burrow_area(burrow_geci_data, burrow_jm_data):
    return _get_number_of_burrows_in_burrow_area(
        burrow_geci_data, burrow_jm_data
    ) / _get_burrow_area(burrow_geci_data, burrow_jm_data)


def _get_burrow_polygon(burrow_geci_data, burrow_jm_data):
    burrow_points = _get_burrow_coordinates(burrow_geci_data, burrow_jm_data)
    hull = ConvexHull(burrow_points)
    return burrow_points.iloc[hull.vertices, :]


def is_inside_burrow_area(recorder_data, burrow_geci_data, burrow_jm_data):
    recorder_coordinates = get_recorder_coordinates(recorder_data)
    burrow_polygon = _get_burrow_polygon(burrow_geci_data, burrow_jm_data)
    return path.Path(burrow_polygon).contains_points(recorder_coordinates)


def get_call_rate_in_burrow_area(recorder_data, burrow_geci_data, burrow_jm_data):
    is_recorder_inside = is_inside_burrow_area(recorder_data, burrow_geci_data, burrow_jm_data)
    return recorder_data.loc[is_recorder_inside, "Tasa_Voc"].mean()


def get_call_rate_in_recorder_area(recorder_data):
    return recorder_data["Tasa_Voc"].mean()


def get_density_in_recorder_area(paths):
    data = RateCalling_Burrow_Data(paths)
    return (
        get_density_in_burrow_area(data.burrow_geci_data, data.burrow_jm_data)
        * get_call_rate_in_recorder_area(data.recorded_data)
        / get_call_rate_in_burrow_area(
            data.recorded_data, data.burrow_geci_data, data.burrow_jm_data
        )
    )


class RateCalling_Burrow_Data:
    def __init__(self, paths, B=2000):
        self.recorded_data = pd.read_csv(paths["recorders_data"])
        self.burrow_geci_data = pd.read_csv(paths["geci_data"])
        self.burrow_jm_data = pd.read_csv(paths["jm_data"])
        self.random_state = np.random.default_rng(seed=42)
        self.B = B
        self.paths = paths

    def get_bootstrapped_number_of_burrows_in_recorder_area(self):
        return self.get_density_in_recorder_area() * get_recorder_area(self.paths["recorders_data"])

    def bootstrapping(self):
        number_samples = len(self.recorded_data)
        return self.recorded_data.sample(
            n=number_samples, replace=True, random_state=self.random_state
        )

    def get_density_in_recorder_area(self):
        interval = np.nanquantile(
            self.get_distribution_density_in_recorder_area(), [0.05, 0.5, 0.95]
        )
        return interval

    def get_distribution_density_in_recorder_area(self):
        return [self._density_for_each_sample() for _ in range(self.B)]

    def _density_for_each_sample(self):
        resample = self.bootstrapping()
        return (
            get_density_in_burrow_area(self.burrow_geci_data, self.burrow_jm_data)
            * get_call_rate_in_recorder_area(resample)
            / get_call_rate_in_burrow_area(resample, self.burrow_geci_data, self.burrow_jm_data)
        )


def get_recorder_coordinates(recorder_data):
    return recorder_data.loc[:, ["Coordenada_X", "Coordenada_Y"]]


def get_area_for_each_recorder(recorder_data_path):
    recorder_data = pd.read_csv(recorder_data_path)
    dx = np.median(np.diff(recorder_data["Coordenada_X"].sort_values().unique()))
    dy = np.median(np.diff(recorder_data["Coordenada_Y"].sort_values().unique()))
    dA = dx * dy
    return dA


def get_number_of_recorders(recorder_data_path):
    number_of_recorders = pd.read_csv(recorder_data_path).shape[0]
    return number_of_recorders


def get_recorder_area(recorder_data_path):
    return get_number_of_recorders(recorder_data_path) * get_area_for_each_recorder(
        recorder_data_path
    )


def get_number_of_burrows_in_recorder_area(paths):
    return get_density_in_recorder_area(paths) * get_recorder_area(paths["recorders_data"])
