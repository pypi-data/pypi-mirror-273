"""
Side panel widgets
"""

import random
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QLabel,
)
import pkg_resources

from PySide6.QtCore import Qt


class SidePanelWidget(QWidget):
    """
    Side pannel widget
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_ = parent
        self.sidebar_layout = QVBoxLayout()

        self.main_title = Title("Terrain generation")
        self.options_subtitle = Subtitle("Options")
        self.seed_input_label = SeedInputLabel()
        self.seed_input = SeedInput(self)
        self.size_label = SizeLabel()
        self.size_input_n = SizeField(self)
        self.by = QLabel("x")
        self.size_input_m = SizeField(self)

        self.size_box = QWidget()
        self.size_box_layout = QHBoxLayout()
        self.size_box_layout.addWidget(self.size_input_m)
        self.size_box_layout.addWidget(self.by)
        self.size_box_layout.addWidget(self.size_input_n)
        self.size_box_layout.setContentsMargins(0, 0, 0, 0)
        self.size_box.setLayout(self.size_box_layout)

        self.delay_label = DelayLabel()
        self.delay_slider = DelaySlider(self)

        self.info_title = Subtitle("Info")
        self.info = Info(self)
        self.regenerate_button = RegenerateButton(self)
        self.start_button = ToggleButton(self)
        self.textures_button = ApplyTexturesButton(self)
        self.export_button = ExportButton(self)

        self.top_section = QWidget()
        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.main_title, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.info_title, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(
            self.options_subtitle, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(
            self.seed_input_label, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(self.seed_input, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.size_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.size_box, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.delay_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(
            self.delay_slider, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(self.regenerate_button)
        self.top_section.setLayout(self.top_layout)

        self.bottom_section = QWidget()
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setSpacing(30)
        self.bottom_layout.addWidget(
            self.start_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        self.bottom_layout.addWidget(
            self.textures_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        self.bottom_layout.addWidget(
            self.regenerate_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        self.bottom_layout.addWidget(
            self.export_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        self.bottom_section.setLayout(self.bottom_layout)

        self.sidebar_layout.addWidget(self.top_section)
        self.sidebar_layout.addWidget(self.bottom_section)
        self.setLayout(self.sidebar_layout)
        self.setMaximumWidth(400)
        self.setMaximumHeight(1080)

    def validate_all_inputs(self):
        """
        Validate all inputs
        """
        return self.size_input_n.validate_input() and self.size_input_m.validate_input()


class Subtitle(QLabel):
    """
    Subtitle class
    """

    def _init__(self, title):
        super().__init__()
        self.setText(title)


class Title(QLabel):
    """
    Title class
    """

    def __init__(self, title):
        super().__init__()
        self.setText(title)


class ToggleButton(QPushButton):
    """
    Start/stop toggle button
    """

    def __init__(self, parent=None):
        super().__init__("Start")
        self.parent_ = parent


class SeedInputLabel(QLabel):
    """
    Label of the seed input window
    """

    def __init__(self):
        super().__init__("Seed")
        self.setContentsMargins(0, 0, 0, 0)


class SeedInput(QLineEdit):
    """
    Seed input text field
    """

    def __init__(self, parent=None):
        super().__init__()
        self.parent_ = parent
        self.setMaxLength(20)
        self.textChanged.connect(self.reset_color)

    def reset_color(self):
        """
        Reset the background color back from red
        """
        self.setStyleSheet("SeedInput {}")


class DelayLabel(QLabel):
    """
    Delay adjustment label
    """

    def __init__(self):
        super().__init__("Generation delay")
        self.setContentsMargins(0, 0, 0, 0)


class DelaySlider(QSlider):
    """
    Delay adjustment slider
    """

    MIN_DELAY = 10
    MAX_DELAY = 1000

    def __init__(self, parent=None):
        super().__init__()
        self.parent_ = parent
        self.setOrientation(Qt.Horizontal)
        self.setRange(self.MIN_DELAY, self.MAX_DELAY)
        self.setValue(50)
        self.valueChanged.connect(self.update_info)

    def update_info(self):
        """
        Update info's delay val
        """
        info = self.parent_.info
        info.delay = self.value()
        info.update_text()


class RegenerateButton(QPushButton):
    """
    Regenerate seed button
    """

    def __init__(self, parent=None):
        super().__init__("Regenerate")
        self.parent_ = parent
        self.clicked.connect(self.on_click)

    def on_click(self) -> None:
        """
        Regenerate button, on click event
        """
        if self.parent_.validate_all_inputs():
            grid = self.parent_.parent_.grid
            try:
                size = (
                    int(self.parent_.size_input_n.text()),
                    int(self.parent_.size_input_m.text()),
                )
            except ValueError:
                size = grid.n_rows, grid.n_cols
            self.parent_.parent_.grid.n_rows, self.parent_.parent_.grid.n_cols = size
            seed = (
                self.parent_.seed_input.text()
                if self.parent_.seed_input.text()
                else grid.grid.generate_seed()
            )
            info = self.parent_.info
            info.seed = seed
            info.size = size
            info.update_text()

            grid.setParent(None)
            self.parent_.textures_button.setEnabled(False)
            self.parent_.parent_.init_grid(size, seed)


class ExportButton(QPushButton):
    """
    Export button
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_ = parent
        self.setText("Export")


class SizeLabel(QLabel):
    """
    Label for the size input field
    """

    def __init__(self):
        super().__init__("Size")
        self.setContentsMargins(0, 0, 0, 0)


class SizeField(QLineEdit):
    """
    Size input field
    """

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.parent_ = parent
        self.textChanged.connect(self.reset_color)

    def reset_color(self):
        """
        Reset the background color back from red
        """
        self.setStyleSheet("SizeInput {}")

    def validate_input(self):
        """
        Validate input
        """
        data = self.text().strip()
        if data:
            try:
                num = int(data)
            except Exception:
                self.setStyleSheet("SizeField { background-color: red; }")
                return False
            if num not in range(10, 101):
                self.setStyleSheet("SizeField { background-color: red; }")
                return False
        return True


class Info(QLabel):
    """
    Info class
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_ = parent
        self.seed = None
        self.size = None
        self.delay = None

    def update_text(self):
        """
        Update info text
        """
        self.setText(
            f"""Seed: {self.seed}
Map's size: {self.size[1]}x{self.size[0]}
Delay: {self.delay}"""
        )


class ApplyTexturesButton(QPushButton):
    """
    Tuxtures application button
    """

    def __init__(self, parent):
        super().__init__("Apply textures")
        self.parent_ = parent
        self.setEnabled(False)
        self.clicked.connect(self.on_click)

    def on_click(self):
        """
        Apply textures, on click event
        """
        # print('click')
        grid = self.parent_.parent_.grid
        for i, cell_ in enumerate(grid.cells):
            cell_.setPixmap(QPixmap())
            cell = grid.grid[i // grid.n_cols][i % grid.n_cols]
            cell.texture = False
        for i, cell_ in enumerate(grid.cells):
            cell = grid.grid[i // grid.n_cols][i % grid.n_cols]
            if cell.texture or random.random() > cell.probability:
                continue
            large_subtypes = ["pyramid", "wavy", "house", "ship"]
            texture_neighbours = [
                n
                for n in grid.grid.get_adjacent(cell)
                if n.type == cell.type and n.texture
            ]
            if len(texture_neighbours) == 0:
                subtype = cell.get_subtype()
                if subtype in large_subtypes and grid.grid.large_texture(cell):
                    cells_directions = [0, 1, grid.n_cols, grid.n_cols + 1]
                    for n, c in enumerate(cells_directions):
                        curr_cell = grid.cells[i + c]
                        texture_path = f"assets/{cell.type}/{subtype}{n + 1}.png"
                        curr_cell.set_texture(pkg_resources.resource_filename(
                            __name__,
                            texture_path,
                        ))
                    cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
                    for n, m in cells:
                        grid.grid[cell.x + n][cell.y + m].texture = True
                else:
                    texture_path = f"assets/{cell.type}/{subtype}.png"
                    cell_.set_texture(pkg_resources.resource_filename(__name__, texture_path))
                    cell.texture = True
