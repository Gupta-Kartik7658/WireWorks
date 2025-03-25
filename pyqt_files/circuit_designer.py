import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, 
    QVBoxLayout, QWidget, QToolBar, QAction
)
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter
from PyQt5.QtCore import Qt


class diagramWorkspace(QGraphicsScene):
    def __init__(self, grid_size=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QColor(240, 240, 240))  
        pen = QPainter()
        pen.setPen(QColor(200, 200, 200))
        painter.setPen(pen)

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        for x in range(left, int(rect.right()), self.grid_size):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
        for y in range(top, int(rect.bottom()), self.grid_size):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)


class DraggableComponent(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(QGraphicsPixmapItem.ItemIsMovable | QGraphicsPixmapItem.ItemIsSelectable)


class CircuitDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WireWorks - Grid Workspace")
        self.setGeometry(100, 100, 1000, 700)
        self.scene = diagramWorkspace(20)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Component Library")
        self.addToolBar(toolbar)

        components = {
            "Resistor": "resistor.svg",
            "LED": "led.svg",
            "RGB LED": "rgb_led.svg",
            "Transistor": "transistor.svg",
            "Potentiometer": "potentiometer.svg",
            "DHT11": "dht11.svg",
            "ESP32": "esp32.svg",
            "Microcontroller": "microcontroller.svg",
            "Arduino Uno": "arduino_uno.svg",
            "Arduino Mega": "arduino_mega.svg",
            "Arduino Nano": "arduino_nano.svg"
        }

        for name, icon_path in components.items():
            if not os.path.exists(icon_path):
                print(f"Warning: {icon_path} not found!")  

            action = QAction(QIcon(icon_path), f"Add {name}", self)
            action.triggered.connect(lambda checked, t=name: self.add_component(t))
            toolbar.addAction(action)

    def add_component(self, component_type):
        component = None

        if component_type == "Resistor":
            component = DraggableComponent(self.create_pixmap(60, 20, QColor(200, 50, 50)))
        elif component_type == "LED":
            component = DraggableComponent(self.create_pixmap(20, 20, QColor(50, 200, 50)))
        elif component_type == "RGB LED":
            component = DraggableComponent(self.create_pixmap(25, 25, QColor(50, 50, 200)))  
        elif component_type == "Transistor":
            component = DraggableComponent(self.create_pixmap(30, 40, QColor(100, 100, 100)))  
        elif component_type == "Potentiometer":
            component = DraggableComponent(self.create_pixmap(40, 40, QColor(150, 100, 50)))  
        elif component_type == "DHT11":
            component = DraggableComponent(self.create_pixmap(40, 50, QColor(0, 100, 255)))  
        elif component_type == "ESP32":
            component = DraggableComponent(self.create_pixmap(60, 40, QColor(255, 50, 0)))  
        elif component_type == "Microcontroller":
            component = DraggableComponent(self.create_pixmap(80, 40, QColor(50, 50, 200)))
        elif component_type in ["Arduino Uno", "Arduino Mega", "Arduino Nano"]:
            image_path = f"{component_type.lower().replace(' ', '_')}.svg"
            if os.path.exists(image_path):
                component = DraggableComponent(QPixmap(image_path))
            else:
                print(f"Error: {image_path} not found!")  
                return

        if component:
            center_x = self.view.mapToScene(self.view.viewport().rect().center()).x()
            center_y = self.view.mapToScene(self.view.viewport().rect().center()).y()
            component.setPos(center_x - component.pixmap().width() / 2, center_y - component.pixmap().height() / 2)
            self.scene.addItem(component)

    def create_pixmap(self, width, height, color):
        pixmap = QPixmap(width, height)
        pixmap.fill(color)
        return pixmap


if __name__ == "__main__":
    app = QApplication([])
    window = CircuitDesigner()
    window.show()
    app.exec_()



