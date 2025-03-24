from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QVBoxLayout,
    QWidget, QToolBar, QAction, QGraphicsPixmapItem
)
from PyQt5.QtGui import QPen, QColor, QPainter, QIcon, QPixmap
from PyQt5.QtCore import Qt


class diagramWorkspace(QGraphicsScene):
    def __init__(self, grid_size=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size

    def drawBackground(self, painter, rect):
        
        painter.fillRect(rect, QColor(240, 240, 240))  

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)


        pen = QPen(QColor(200, 200, 200))
        painter.setPen(pen)

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
        toolbar = QToolBar("Componetn Library")
        self.addToolBar(toolbar)
        resistor_action = QAction(QIcon("resistor.svg"), "Add Resistor", self)
        resistor_action.triggered.connect(lambda: self.add_component("Resistor"))
        toolbar.addAction(resistor_action)

        
        led_action = QAction(QIcon("led.svg"), "Add LED", self)
        led_action.triggered.connect(lambda: self.add_component("LED"))
        toolbar.addAction(led_action)

        
        microcontroller_action = QAction(QIcon("C:\\Users\\hp\\Desktop\\WireWorks\\microcontroller.svg"), "Add Microcontroller", self)
        microcontroller_action.triggered.connect(lambda: self.add_component("Microcontroller"))
        toolbar.addAction(microcontroller_action)

        
        arduino_action = QAction(QIcon("C:\\Users\\hp\\Desktop\\WireWorks\\arduino_uno.svg"), "Add Arduino Uno", self)
        arduino_action.triggered.connect(lambda: self.add_component("Arduino Uno"))
        toolbar.addAction(arduino_action)


    def add_component(self, component_type):
        
        if component_type == "Resistor":
            component = DraggableComponent(self.create_pixmap(60, 20, QColor(200, 50, 50)))  
        elif component_type == "LED":
            component = DraggableComponent(self.create_pixmap(20, 20, QColor(50, 200, 50)))  
        elif component_type == "Microcontroller":
            component = DraggableComponent(self.create_pixmap(80, 40, QColor(50, 50, 200)))  
        elif component_type == "Arduino Uno":
            pixmap = QPixmap("C:\\Users\\hp\\Desktop\\WireWorks\\arduino_uno.svg")
            component = DraggableComponent(pixmap)
        else:
            return
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
