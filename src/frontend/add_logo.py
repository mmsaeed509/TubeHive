#####################################
#                                   #
#  @author      : 00xWolf           #
#    GitHub    : @mmsaeed509       #
#    Developer : Mahmoud Mohamed   #
#  﫥  Copyright : Exodia OS         #
#                                   #
#####################################

import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QRegion, QPixmap, QPainterPath
from PyQt5.QtWidgets import QWidget


class AddLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the geometry (position and size) of the internal window
        self.setGeometry(20, 20, 200, 200)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        # self.radius = min(self.width(), self.height()) // 2

        # Resolve the image path relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        icons_dir = os.path.join(script_dir, "../icons")  # Navigate to the icons directory
        self.image_path = os.path.join(icons_dir, "TubeHive.png")
        print(f"Resolved image path: {self.image_path}")  # Debugging: Print the resolved path

        # Load the image
        self.pixmap = QPixmap(self.image_path)

        # Check if the pixmap is loaded correctly
        if self.pixmap.isNull():
            print(f"Failed to load image from: {self.image_path}")
        else:
            print("Image loaded successfully!")

    def createCustomMask(self):
        # Define a circular mask
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)  # Apply the mask to make the window circular
        return path  # Return the path for use in the paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the custom shape with the image fill if the pixmap is valid
        if not self.pixmap.isNull():
            # Get the bounding rectangle of the circular path
            bounding_rect = self.rect()

            # Scale the pixmap to fit the bounding rectangle of the circle
            scaled_pixmap = self.pixmap.scaled(
                bounding_rect.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )

            # Clip the painter to the circular region
            painter.setClipRegion(QRegion(self.createCustomMask().toFillPolygon().toPolygon()))

            # Calculate offsets to center the pixmap within the bounding rectangle
            offset_x = (bounding_rect.width() - scaled_pixmap.width()) // 2
            offset_y = (bounding_rect.height() - scaled_pixmap.height()) // 2

            # Draw the scaled pixmap centered within the circle
            painter.drawPixmap(offset_x, offset_y, scaled_pixmap)