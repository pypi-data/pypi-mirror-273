from functools import partial
from typing import TYPE_CHECKING

from compas_viewer.actions import Action
from compas_viewer.configurations import ActionConfig

if TYPE_CHECKING:
    from .layout import Layout


class MenubarLayout:
    """
    The MenubarLayout class manages all
    the layout and other UI-related information of the menu.

    Parameters
    ----------
    layout : :class:`compas_viewer.layout.Layout`
        The parent layout.
    viewer : :class:`compas_viewer.viewer.Viewer`
        The parent viewer.
    config : :class:`compas_viewer.configurations.MenubarConfig`
        The menu configuration.

    See Also
    --------
    :class:`compas_viewer.configurations.layout_config.MenubarConfig`

    References
    ----------
    :PySide6:`PySide6/QtWidgets/QLayout`
    """

    def __init__(self, layout: "Layout"):
        self.layout = layout
        self.viewer = self.layout.viewer
        self.config = layout.config.menubar
        self._menubar = self.viewer.window.menuBar()

    def init(self):
        for k, i in self.config.config.items():
            parent = self._menubar.addMenu(k)
            assert isinstance(i, dict)
            for _k, _i in i.items():
                action_config = ActionConfig("no")
                parent.addAction(
                    _k,
                    partial(
                        Action(_i["action"], self.viewer, action_config).pressed_action,
                        **_i.get("kwargs", {}),  # type: ignore
                    ),
                )
