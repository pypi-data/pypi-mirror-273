from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QSize

from qtharmony.src.core import StyleSheetLoader
from qtharmony.src.core.theme import ThemeManager

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class CheckBox(QCheckBox):
    """
    Custom QCheckBox widget for checkbox functionality.

    Methods:
    - __init__(text: Optional[str] = None, size: tuple[int, int] = (150, 30),
              is_checkable: bool = True, is_checked: bool = False, is_disabled: bool = False,
              *, stylesheet: Optional[str] = None, parent: Optional["QWidget"] = None): None
              - Initializes the CheckBox widget with optional text, size, checkability, checked state, disabled state, and stylesheet.
    """

    def __init__(
            self,
            text: Optional[str] = None,
            size: tuple[int, int] = (150, 30),
            is_checkable: bool = True,
            is_checked: bool = False,
            is_disabled: bool = False,
            *,
            stylesheet: Optional[str] = None,
            parent: Optional["QWidget"] = None
    ) -> None:
        """
        Initializes the CheckBox widget with optional text, size, checkability, checked state, disabled state, and stylesheet.

        Args:
            text (Optional[str], optional): The text displayed next to the checkbox. Defaults to None.
            size (tuple[int, int], optional): The size of the checkbox widget (width, height). Defaults to (150, 30).
            is_checkable (bool, optional): Flag to enable/disable checkbox functionality. Defaults to True.
            is_checked (bool, optional): Flag to set the initial checked state of the checkbox. Defaults to False.
            is_disabled (bool, optional): Flag to set the initial disabled state of the checkbox. Defaults to False.
            stylesheet (Optional[str], optional): Custom stylesheet for the checkbox widget. Defaults to None.
            parent (Optional["QWidget"], optional): Parent widget of the checkbox. Defaults to None.
        """

        super().__init__(parent)
        ThemeManager.add_widgets(self)

        self.setFixedSize(QSize(*size))
        self.setChecked(is_checked)
        self.setCheckable(is_checkable)
        self.setDisabled(is_disabled)

        self.setObjectName("check-box")
        if text is not None:
            self.setText(text)
        
        self.stylesheet = StyleSheetLoader.load_stylesheet(
            __file__, "styles/check_box.css", 
            name="CheckBox", obj_name="CheckBox#check-box",
            stylesheet=stylesheet
        )
