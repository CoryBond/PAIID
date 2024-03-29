import logging
from PyQt5.QtWidgets import QSplashScreen, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem, QGestureEvent
from PyQt5.QtCore import QRectF, QEvent, Qt
from PyQt5.QtGui import QPixmap, QTransform


class ImageViewer(QGraphicsView):
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

    def __init__(self, startingImageBytes: bytes = None):
        super().__init__()
        self.init_ui(startingImageBytes)


    def init_ui(self, startingImageBytes: bytes):

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.grabGesture(Qt.PinchGesture)

        # Create a graphics view and scene
        if startingImageBytes is not None:
            self.replace_image(startingImageBytes)
        
    
    def replace_image(self, image: bytes):
        scene = QGraphicsScene(parent=self)

        # Add an image to the scene
        pixmap = QPixmap()
        pixmap.loadFromData(image)

        splash = QSplashScreen(pixmap) 
        splash.show()
        self.pixmapItem = QGraphicsPixmapItem(pixmap)
        self.pixmapItem.setFlag(QGraphicsItem.ItemIsMovable)

        scene.addItem(self.pixmapItem)
        self.setScene(scene)

        self.fit_in_view_event()

    
    def has_photo(self):
        return hasattr(self, "pixmapItem")


    def get_scale_factor(self):
        # Get the current transformation matrix of the view
        matrix = self.transform()

        # Extract the horizontal and vertical scale factors
        scale_x = matrix.m11()
        scale_y = matrix.m22()

        return scale_x, scale_y


    def event(self, event: QEvent):
        if event.type() == QEvent.Gesture:
            # Only pinch events are supported so we don't have to discriminate what event handler to delegate to
            return self.pinch_zoom_event(event)
        return super().event(event)
    

    def pinch_zoom_event(self, event: QGestureEvent):
        pinch = event.gesture(Qt.PinchGesture)
        if pinch:
            # Calculate the scale factor from the pinch gsture and the current graphical matrix scale
            pinch_scale_factor = pinch.scaleFactor()

            scale_x, scale_y = self.get_scale_factor()
            # Adjust the scale factor and update the transformation
            self.setTransform(QTransform().scale(scale_x * pinch_scale_factor, scale_y * pinch_scale_factor))
        return True


    # From https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
    def fit_in_view_event(self, scale=True):
        rect = QRectF(self.pixmapItem.pixmap().rect())
        logging.info("rect " + str(rect.height))
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)