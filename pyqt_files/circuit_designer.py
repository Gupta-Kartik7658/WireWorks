
# import os
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QGraphicsView, QGraphicsScene, 
#     QGraphicsPixmapItem, QVBoxLayout, QWidget, QToolBar, QAction
# )
# from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter
# from PyQt5.QtCore import Qt
# from PyQt5.QtSvg import QSvgRenderer


# class DiagramWorkspace(QGraphicsScene):
#     def __init__(self, grid_size=20, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.grid_size = grid_size

#     def drawBackground(self, painter, rect):
#         painter.fillRect(rect, QColor(240, 240, 240))  
#         painter.setPen(QColor(200, 200, 200))  

#         left = int(rect.left()) - (int(rect.left()) % self.grid_size)
#         top = int(rect.top()) - (int(rect.top()) % self.grid_size)

#         for x in range(left, int(rect.right()), self.grid_size):
#             painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
#         for y in range(top, int(rect.bottom()), self.grid_size):
#             painter.drawLine(int(rect.left()), y, int(rect.right()), y)


# class DraggableComponent(QGraphicsPixmapItem):
#     def __init__(self, pixmap):
#         super().__init__(pixmap)
#         self.setFlags(QGraphicsPixmapItem.ItemIsMovable | QGraphicsPixmapItem.ItemIsSelectable)


# class ScalableGraphicsView(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.setRenderHint(QPainter.Antialiasing)
#         self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

#     def wheelEvent(self, event):
#         zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
#         self.scale(zoom_factor, zoom_factor)


# class CircuitDesigner(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("WireWorks - Grid Workspace")
#         self.setGeometry(100, 100, 1000, 700)
#         self.scene = DiagramWorkspace(20)
#         self.view = ScalableGraphicsView(self.scene)

#         central_widget = QWidget()
#         layout = QVBoxLayout()
#         layout.addWidget(self.view)
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         self.create_toolbar()

#     def create_toolbar(self):
#         toolbar = QToolBar("Component Library")
#         self.addToolBar(toolbar)

#         components = {
#             "Resistor": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\resistor.svg",
#             "LED": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\led.svg",
#             "RGB LED": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\rgb_led.svg",
#             "Transistor": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\transistor.svg",
#             "Potentiometer": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\Potentiometer.svg",
#             "DHT11": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\dht11.svg",
#             "ESP32": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\esp32.svg",
#             "Microcontroller": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\microcontroller.svg",
#             "Arduino Uno": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\arduino_uno.svg"
#               #             "Arduino Mega": "arduino_mega.svg",
# #             "Arduino Nano": "arduino_nano.svg"
#         }

#         for name, icon_path in components.items():
#             if not os.path.exists(icon_path):
#                 print(f"Warning: {icon_path} not found!")  

#             action = QAction(QIcon(icon_path), f"Add {name}", self)
#             action.triggered.connect(lambda checked, t=name: self.add_component(t, components[t]))
#             toolbar.addAction(action)

#     def add_component(self, component_type, image_path):
#         if os.path.exists(image_path) and image_path.endswith(".svg"):
#             pixmap = self.svg_to_pixmap(image_path, 80, 80)  
#             component = DraggableComponent(pixmap)
#         else:
#             print(f"Error: {image_path} not found or not an SVG!")
#             return

#         center = self.view.mapToScene(self.view.viewport().rect().center())
#         component.setPos(center.x() - component.pixmap().width() / 2, center.y() - component.pixmap().height() / 2)
#         self.scene.addItem(component)

#     def svg_to_pixmap(self, svg_path, width=80, height=80):
#         """Convert an SVG file to QPixmap."""
#         renderer = QSvgRenderer(svg_path)
#         pixmap = QPixmap(width, height)
#         pixmap.fill(Qt.transparent)  
#         painter = QPainter(pixmap)
#         renderer.render(painter)
#         painter.end()
#         return pixmap


# if __name__ == "__main__":
#     app = QApplication([])
#     window = CircuitDesigner()
#     window.show()
#     app.exec_()
#there are some errors in below code
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QVBoxLayout, QWidget, QToolBar, QAction,
    QGraphicsItem, QGraphicsRectItem
)
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtSvg import QSvgRenderer


class DiagramWorkspace(QGraphicsScene):
    """ Workspace with grid background """
    def __init__(self, grid_size=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size

    def drawBackground(self, painter, rect):
        """ Draw grid background """
        painter.fillRect(rect, QColor(240, 240, 240))
        painter.setPen(QColor(200, 200, 200))

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        for x in range(left, int(rect.right()), self.grid_size):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
        for y in range(top, int(rect.bottom()), self.grid_size):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)


class DraggableComponent(QGraphicsPixmapItem):
    """ Draggable and resizable component """
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(QGraphicsPixmapItem.ItemIsMovable | QGraphicsPixmapItem.ItemIsSelectable)
        self.resize_handle = ResizeHandle(self)
        self.update_handle_position()

    def resize(self, width, height):
        """ Resize component while maintaining aspect ratio """
        width, height = int(width), int(height)  # Ensure integer values
        new_pixmap = self.pixmap().scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(new_pixmap)
        self.update_handle_position()

    def update_handle_position(self):
        """ Update resize handle position """
        self.resize_handle.setPos(self.pixmap().width(), self.pixmap().height())


class ResizeHandle(QGraphicsRectItem):
    """ Corner resize handle for resizing components """
    def __init__(self, parent_item):
        super().__init__(0, 0, 10, 10, parent_item)
        self.setBrush(QColor(100, 100, 100))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsScenePositionChanges)
        self.parent_item = parent_item
        self.last_position = self.pos()

    def itemChange(self, change, value):
        """ Resize parent component when handle is moved """
        if change == QGraphicsItem.ItemPositionChange:
            delta = value - self.last_position
            new_width = self.parent_item.pixmap().width() + delta.x()
            new_height = self.parent_item.pixmap().height() + delta.y()

            if new_width < 20 or new_height < 20:  # Prevent shrinking too much
                return self.last_position

            self.parent_item.resize(new_width, new_height)
            self.last_position = value

        return super().itemChange(change, value)


class ScalableGraphicsView(QGraphicsView):
    """ Zoomable view for the workspace """
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom_factor, zoom_factor)


class CircuitDesigner(QMainWindow):
    """ Main Circuit Designer Application """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WireWorks - Grid Workspace")
        self.setGeometry(100, 100, 1000, 700)
        self.scene = DiagramWorkspace(20)
        self.view = ScalableGraphicsView(self.scene)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_toolbar()

    def create_toolbar(self):
        """ Create toolbar with electronic components """
        toolbar = QToolBar("Component Library")
        self.addToolBar(toolbar)

        components = {
            "Resistor": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\resistor.svg",
            "LED": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\led.svg",
            "RGB LED": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\rgb_led.svg",
            "Transistor": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\transistor.svg",
            "Potentiometer": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\Potentiometer.svg",
            "DHT11": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\dht11.svg",
            "ESP32": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\esp32.svg",
            "Microcontroller": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\microcontroller.svg",
            "Arduino Uno": r"C:\Users\kavit\Pictures\WireWorks\WireWorks\diagrams_and_documents\arduino_uno.svg"
        }

        for name, icon_path in components.items():
            if not os.path.exists(icon_path):
                print(f"Warning: {icon_path} not found!")

            action = QAction(QIcon(icon_path), f"Add {name}", self)
            action.triggered.connect(lambda checked, t=name, p=icon_path: self.add_component(t, p))
            toolbar.addAction(action)

    def add_component(self, component_type, image_path):
        """ Add electronic component to the scene """
        if os.path.exists(image_path) and image_path.endswith(".svg"):
            pixmap = self.svg_to_pixmap(image_path, 80, 80)
            component = DraggableComponent(pixmap)
        else:
            print(f"Error: {image_path} not found or not an SVG!")
            return

        center = self.view.mapToScene(self.view.viewport().rect().center())
        component.setPos(center.x() - component.pixmap().width() / 2, center.y() - component.pixmap().height() / 2)
        self.scene.addItem(component)

    def svg_to_pixmap(self, svg_path, width=80, height=80):
        """ Convert an SVG file to QPixmap """
        renderer = QSvgRenderer(svg_path)
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap


if __name__ == "__main__":
    app = QApplication([])
    window = CircuitDesigner()
    window.show()
    app.exec_()



