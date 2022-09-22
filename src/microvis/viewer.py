from __future__ import annotations

from typing import TYPE_CHECKING, Any

from . import _validators as valid
from . import backend as _backend
from .util import in_notebook

if TYPE_CHECKING:
    from ._types import ValidClim, ValidCmap
    from .backend._base import CanvasBase, Image, ViewBase


class Viewer:
    def __init__(
        self,
        background_color: str | None = None,
        size: tuple[int, int] = (600, 600),
        show: bool = False,
        backend: str | None = None,
    ) -> None:
        backend = backend or "vispy"
        backend_module = getattr(_backend, backend)
        Canvas: type[CanvasBase] = backend_module.Canvas
        if background_color is None:
            background_color = "white" if in_notebook() else "black"
        self.canvas = Canvas(background_color=background_color, size=size)
        self._current_view = (0, 0)
        if show:
            self.show()

    def add_image(
        self,
        data: Any,
        *,
        cmap: ValidCmap | None = None,
        clim: ValidClim = "auto",
        idx: tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> Image:
        idx = idx or self._current_view
        clim = valid.clim(clim)
        cmap = valid.cmap(cmap)
        return self[idx].add_image(data, cmap=cmap, clim=clim, **kwargs)

    def show(self) -> None:
        self.canvas.show()

    def _repr_mimebundle_(self, *_: Any, **__: Any) -> Any:
        if method := getattr(self.canvas.native, "_repr_mimebundle_", None):
            return method()
        raise NotImplementedError()

    def __getitem__(self, idx: tuple[int, int]) -> ViewBase:
        return self.canvas[idx]

    def __delitem__(self, idxs: tuple[int, int]) -> None:
        del self.canvas[idxs]

    def __enter__(self) -> Viewer:
        self.canvas.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self.canvas.__exit__(*args)


# Viewer
#   - Canvas
#     - 1 or more View ([m, n] with [0, 0] as default)
#   .default_view
#   .add_image
#   .add_points
#   ...


# View
#   - scene
#   - camera
#   - add_<layer>()
#   - remove_<layer>()
