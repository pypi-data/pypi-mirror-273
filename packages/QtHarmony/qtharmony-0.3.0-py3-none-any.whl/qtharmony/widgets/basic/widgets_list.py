from typing import Optional, TYPE_CHECKING

from PySide6.QtWidgets import (
    QListWidget, QListWidgetItem, QFrame,
    QHBoxLayout
)
from PySide6.QtCore import Qt

from qtharmony.core import StyleSheetLoader
from qtharmony.core.theme import ThemeManager
from .label import Label

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class WidgetsList(QListWidget):
    def __init__(
            self, 
            size: Optional[tuple[int, int]] = None,
            title: Optional[str] = None,
            *,
            object_name: str = "widgets-list",
            stylesheet: Optional[str] = None,
            parent: Optional["QWidget"] = None,
    ) -> None:
        super().__init__(parent)
        ThemeManager.add_widgets(self)
    
        if size is not None: self.setFixedSize(*size)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setObjectName(object_name)
        self.stylesheet = StyleSheetLoader.load_stylesheet(
            __file__, "styles/widgets_list.css",
            name=self.__class__.__name__, obj_name=f"QListWidget#{self.objectName()}",
            stylesheet=stylesheet
        )

    def add_widget(self, widget) -> None:
        item = QListWidgetItem()
        self.addItem(item)
        self.setItemWidget(item, widget)
