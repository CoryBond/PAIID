import logging
from typing import Callable
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QImage
from repoManager.Models import NextToken

from ui.dialogs.ErrorMessage import ErrorMessage
from ui.widgets.home.ImageMeta import ImageMetaInfo

from repoManager.RepoManager import DIRECTION, RepoManager
from ui.widgets.gallery.GalleryDisplay import GalleryDisplay


def generateWiderButton(text: str, callback: Callable = None) -> QPushButton:
    button = QPushButton(text)
    button.setFixedWidth(40)
    if callback is not None: 
        button.clicked.connect(callback)
    return button


class PageLink(QLabel):

    clicked = pyqtSignal([str])  # Signal emited when label is clicked

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.setStyleSheet("color: blue;") # set text color to blue to emulate a link
        self.setCursor(Qt.PointingHandCursor)  # set the cursor to link pointer
        # self.setFont(QFont())

    def mousePressEvent(self, event):
        self.clicked.emit(self.text())   # emit the clicked signal when pressed
        return super().mousePressEvent(event)


PAGE_SIZE = 10


class GalleryPage(QWidget):
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
    imageClickedSignal = pyqtSignal(ImageMetaInfo, QImage)
    galleryRefreshedSignal = pyqtSignal()

    def __init__(self, repoManager: RepoManager):
        super().__init__()


        self.repoManager = repoManager

        self.init_ui()

        # Set bookmarks
        self.set_left_bookmark(None)
        self.set_right_bookmark(None)


        # pass through emit from child to this parent
        self.gallery.imageClickedSignal.connect(self.imageClickedSignal.emit)
        self.galleryRefreshedSignal.connect(self.refresh_page)


    def set_left_bookmark(self, bookmark: NextToken):
        self.backward_page_button.setDisabled(bookmark is None)
        self.leftBookmarkPageToken = bookmark
        

    def set_right_bookmark(self, bookmark: NextToken):
        self.forward_page_button.setDisabled(bookmark is None)
        self.rightBookmarkPageToken = bookmark
        

    def init_ui(self):

        layout = QVBoxLayout()
        self.setLayout(layout)

        # create the stacked widget that will contain each page...       
        self.gallery = GalleryDisplay()
        layout.addWidget(self.gallery)

        # setup the layout for the page numbers below the stacked widget
        self.pagination_layout = QHBoxLayout()
        self.pagination_layout.addStretch(0)
        self.pagination_layout.addWidget(generateWiderButton("<<", lambda _ : self.init_page()))
        self.backward_page_button = generateWiderButton("<", lambda _ : self.change_page(self.leftBookmarkPageToken, DIRECTION.BACKWARD))
        self.pagination_layout.addWidget(self.backward_page_button)

        for i in range(1, 3):
            page_link = PageLink(str(i), parent=self)
            self.pagination_layout.addWidget(page_link)
            # page_link.clicked.connect(self.switch_page)
        page_link = PageLink("...", parent=self)
        self.pagination_layout.addWidget(page_link)
        self.forward_page_button = generateWiderButton(">", lambda _ : self.change_page(self.rightBookmarkPageToken, DIRECTION.FORWARD))
        self.pagination_layout.addWidget(self.forward_page_button)
        layout.addLayout(self.pagination_layout)


        self.init_page()


    def init_page(self,):
  
        getImagesResult = self.repoManager.get_images(PAGE_SIZE)

        if(getImagesResult is not None):
            if(getImagesResult.errorMessage is not None):
                ErrorMessage(getImagesResult.errorMessage).exec()
        
            self.set_right_bookmark(getImagesResult.nextToken)
            self.gallery.replace_display(getImagesResult.results)


    def change_page(self, currentNextToken = None, direction: DIRECTION = DIRECTION.FORWARD):
        getImagesResult = self.repoManager.get_images(PAGE_SIZE, token=currentNextToken, direction=direction)

        if(getImagesResult is not None):
            if(getImagesResult.errorMessage is not None):
                ErrorMessage(getImagesResult.errorMessage).exec()

            self.gallery.replace_display(getImagesResult.results)
            # Set the new "edge" token based on the direciton we are going
            if(direction is DIRECTION.FORWARD):
                self.set_left_bookmark(self.rightBookmarkPageToken)
                self.set_right_bookmark(getImagesResult.nextToken)
            else:
                self.set_right_bookmark(self.leftBookmarkPageToken)
                self.set_left_bookmark(getImagesResult.nextToken)


    def refresh_page(self):
        logging.info("refresh_page")
        self.change_page(currentNextToken = self.leftBookmarkPageToken)