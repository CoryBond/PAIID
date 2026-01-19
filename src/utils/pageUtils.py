from PyQt5.QtWidgets import QWidget

from typing import TypedDict
from enum import Enum


class PageName(str, Enum):
    HOME = "home"
    GALLERY = "gallery"
    SETTINGS = "settings"


class PageCaption(str, Enum):
    HOME = "Home"
    GALLERY = "Gallery"
    SETTINGS = "Settings"


class PageHint(str, Enum):
    HOME = "This Will Take You To The Home Page"
    GALLERY = "This Will Let You Load Previous Images"
    SETTINGS = "This will change PAIID settings"


PageDictType = TypedDict("PageDictType", {
    'home': QWidget,
    'gallery': QWidget,
    'settings': QWidget,
})


class PageMetaDecorator():
    """
    QT Widget to display a singular and move a singular image.
    
    Images can be moved via:
    1. Panning the image when click/touch drag movements
    2. Zomming in/out of the image with a pinch (touch) gesture anywhere in the viewer

    Attributes
    ----------

    Methods
    ----------
    replace_image(imagePath)
        Replaces the current image with a new one from the given path. The new image will "fit" into the views current frame when fully loaded.

    has_photo()
        Returns if the current view has any image loaded to it currently
    """

    def __init__(self, widget: QWidget, pageName: PageName, pageCaption: PageCaption, hint: PageHint):
        super().__init__()

        self.widget = widget
        self.pageName = pageName
        self.pageCaption = pageCaption
        self.hint = hint
