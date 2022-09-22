from __future__ import annotations

from typing import Any

import numpy as np

from .viewer import Viewer


def imshow(
    data: Any, background_color=None, size=(600, 600), clim="auto", *, backend=None
) -> tuple[Viewer, Any]:
    viewer = Viewer(background_color=background_color, size=size, backend=backend)
    img = viewer.add_image(data, clim=clim)
    viewer.show()
    return viewer, img


def ortho(data: np.ndarray) -> Viewer:
    from itertools import product

    from vispy import scene

    viewer = Viewer()

    shape = data.shape
    cmap = "gray"

    scene.visuals.Volume(np.transpose(data, (-1, 0, 1)), parent=viewer[0, 0].scene)
    scene.visuals.Image(data[:, :, shape[2] // 2], parent=viewer[1, 0].scene, cmap=cmap)
    scene.visuals.Image(data[:, shape[1] // 2, :], parent=viewer[0, 1].scene, cmap=cmap)
    scene.visuals.Image(
        data[shape[0] // 2, :, :].T, parent=viewer[1, 1].scene, cmap=cmap
    )

    for coord in product((0, 1), (0, 1)):
        viewer[coord].camera.set_range()

    return viewer
