from __future__ import annotations

import dataclasses

import numpy as np
from numpy.typing import NDArray


@dataclasses.dataclass(frozen=True)
class BoundingBox2d:
    min_: NDArray[np.float_]
    max_: NDArray[np.float_]

    def __post_init__(self) -> None:
        """

        Args:
            min_:
                A 2D point in the Cartesian coordinate system represented by an
                array of shape (2,).
            max_:
                See `min_`.
        """
        assert self.min_.shape == (2,), self.min_.shape
        assert self.max_.shape == (2,), self.max_.shape
        assert np.all(self.min_ <= self.max_)

    @property
    def min_x(self) -> float:
        return self.min_[0]

    @property
    def min_y(self) -> float:
        return self.min_[1]

    @property
    def max_x(self) -> float:
        return self.max_[0]

    @property
    def max_y(self) -> float:
        return self.max_[1]

    @property
    def dimensions(self) -> NDArray[np.float_]:
        return self.max_ - self.min_

    @property
    def area(self) -> float:
        return np.prod(self.dimensions)

    @property
    def midpoint(self) -> NDArray[np.float_]:
        return (self.min_ + self.max_) / 2

    def get_vertices(self) -> NDArray[np.float_]:
        return np.array(
            [
                [self.min_x, self.min_y],
                [self.min_x, self.max_y],
                [self.max_x, self.max_y],
                [self.max_x, self.min_y],
            ]
        )

    def get_dilated_bounding_box(
        self, dilation: NDArray[np.float_] | float
    ) -> BoundingBox2d:
        return BoundingBox2d(
            min_=self.min_ - dilation, max_=self.max_ + dilation
        )

    def liang_barsky_line_clipping(
        self, line_segments: NDArray[np.float_]
    ) -> NDArray[np.float_]:
        x1, y1 = line_segments[:, 0].T
        x2, y2 = line_segments[:, 1].T
        dx = x2 - x1
        dy = y2 - y1
        p = np.stack([-dx, dx, -dy, dy], dtype=np.float_)
        q = np.stack(
            [
                x1 - self.min_x,
                self.max_x - x1,
                y1 - self.min_y,
                self.max_y - y1,
            ],
            dtype=np.float_,
        )
        t_enter = np.zeros_like(x1)
        t_exit = np.ones_like(x1)

        for i in range(4):
            is_parallel = np.isclose(p[i], 0)
            outside_parallel = np.logical_and(is_parallel, q[i] < 0)
            t_enter[outside_parallel] = np.nan
            t_exit[outside_parallel] = np.nan
            # To avoid RuntimeWarning: divide by zero encountered in divide
            t = np.divide(
                q[i], p[i], out=np.full_like(q[i], np.inf), where=~is_parallel
            )
            t_enter = np.where(p[i] < 0, np.maximum(t_enter, t), t_enter)
            t_exit = np.where(p[i] > 0, np.minimum(t_exit, t), t_exit)

        outside = np.logical_or(np.isnan(t_enter), t_enter > t_exit)
        x1_clip = np.where(~outside, x1 + t_enter * dx, np.nan)
        y1_clip = np.where(~outside, y1 + t_enter * dy, np.nan)
        x2_clip = np.where(~outside, x1 + t_exit * dx, np.nan)
        y2_clip = np.where(~outside, y1 + t_exit * dy, np.nan)

        result = np.stack(
            [
                np.column_stack((x1_clip, y1_clip)),
                np.column_stack((x2_clip, y2_clip)),
            ],
            axis=1,
        )
        result = np.where(
            np.all(np.isclose(result[:, 0], result[:, 1]), axis=1),
            np.full_like(result, fill_value=np.nan).T,
            result.T,
        ).T
        return result

    def clip_line_segments(
        self, line_segments: NDArray[np.float_]
    ) -> NDArray[np.float_]:
        return self.liang_barsky_line_clipping(line_segments=line_segments)
