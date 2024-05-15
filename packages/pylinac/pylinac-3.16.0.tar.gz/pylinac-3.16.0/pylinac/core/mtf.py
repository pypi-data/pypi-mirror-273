from __future__ import annotations

import warnings
from typing import Sequence

import argue
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

from .contrast import michelson
from .roi import HighContrastDiskROI


class MTF:
    """This class will calculate relative MTF"""

    def __init__(
        self,
        lp_spacings: Sequence[float],
        lp_maximums: Sequence[float],
        lp_minimums: Sequence[float],
    ):
        """
        Parameters
        ----------
        lp_spacings : sequence of floats
            These are the physical spacings per unit distance. E.g. 0.1 line pairs/mm.
        lp_maximums : sequence of floats
            These are the maximum values of the sample ROIs.
        lp_minimums : sequence of floats
            These are the minimum values of the sample ROIs.
        """
        self.spacings = lp_spacings
        self.maximums = lp_maximums
        self.minimums = lp_minimums
        self.mtfs = {}
        self.norm_mtfs = {}
        for spacing, max, min in zip(lp_spacings, lp_maximums, lp_minimums):
            arr = np.array((max, min))
            self.mtfs[spacing] = michelson(arr)
        # sort according to spacings
        self.mtfs = {k: v for k, v in sorted(self.mtfs.items(), key=lambda x: x[0])}
        for key, value in self.mtfs.items():
            self.norm_mtfs[key] = (
                value / self.mtfs[lp_spacings[0]]
            )  # normalize to first region

        # check that the MTF drops monotonically by measuring the deltas between MTFs
        # if the delta is increasing it means the MTF rose on a subsequent value
        max_delta = np.max(np.diff(list(self.norm_mtfs.values())))
        if max_delta > 0:
            warnings.warn(
                "The MTF does not drop monotonically; be sure the ROIs are correctly aligned."
            )

    @argue.bounds(x=(0, 100))
    def relative_resolution(self, x: float = 50) -> float:
        """Return the line pair value at the given rMTF resolution value.

        Parameters
        ----------
        x : float
            The percentage of the rMTF to determine the line pair value. Must be between 0 and 100.
        """
        f = interp1d(
            list(self.norm_mtfs.values()),
            list(self.norm_mtfs.keys()),
            fill_value="extrapolate",
        )
        mtf = f(x / 100)
        if mtf > max(self.spacings):
            warnings.warn(
                f"MTF resolution wasn't calculated for {x}% that was asked for. The value returned is an extrapolation. Use a higher % MTF to get a non-interpolated value."
            )
        return float(mtf)

    @classmethod
    def from_high_contrast_diskset(
        cls, spacings: Sequence[float], diskset: Sequence[HighContrastDiskROI]
    ) -> MTF:
        """Construct the MTF using high contrast disks from the ROI module."""
        maximums = [roi.max for roi in diskset]
        minimums = [roi.min for roi in diskset]
        return cls(spacings, maximums, minimums)

    def plot(
        self,
        axis: plt.Axes | None = None,
        grid: bool = True,
        x_label: str = "Line pairs / mm",
        y_label: str = "Relative MTF",
        title: str = "RMTF",
        margins: float = 0.05,
        marker: str = "o",
        label: str = "rMTF",
    ) -> tuple:
        """Plot the Relative MTF.

        Parameters
        ----------
        axis : None, matplotlib.Axes
            The axis to plot the MTF on. If None, will create a new figure.
        """
        if axis is None:
            fig, axis = plt.subplots()
        points = axis.plot(
            list(self.norm_mtfs.keys()),
            list(self.norm_mtfs.values()),
            marker=marker,
            label=label,
        )
        axis.margins(margins)
        axis.grid(grid)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.set_title(title)
        return points
