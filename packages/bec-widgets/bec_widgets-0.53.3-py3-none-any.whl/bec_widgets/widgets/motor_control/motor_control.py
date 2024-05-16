# pylint: disable = no-name-in-module,missing-module-docstring
import os
from enum import Enum

from bec_lib.alarm_handler import AlarmBase
from bec_lib.device import Positioner
from qtpy import uic
from qtpy.QtCore import Qt, QThread
from qtpy.QtCore import Signal as pyqtSignal
from qtpy.QtCore import Slot as pyqtSlot
from qtpy.QtGui import QDoubleValidator, QKeySequence
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QShortcut,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from bec_widgets.utils.bec_dispatcher import BECDispatcher

CONFIG_DEFAULT = {
    "motor_control": {
        "motor_x": "samx",
        "motor_y": "samy",
        "step_size_x": 3,
        "step_size_y": 50,
        "precision": 4,
        "step_x_y_same": False,
        "move_with_arrows": False,
    }
}


class MotorControlWidget(QWidget):
    """Base class for motor control widgets."""

    def __init__(self, parent=None, client=None, motor_thread=None, config=None):
        super().__init__(parent)
        self.client = client
        self.motor_thread = motor_thread
        self.config = config

        self.motor_x = None
        self.motor_y = None

        if not self.client:
            bec_dispatcher = BECDispatcher()
            self.client = bec_dispatcher.client

        if not self.motor_thread:
            self.motor_thread = MotorThread(client=self.client)

        self._load_ui()

        if self.config is None:
            print(f"No initial config found for {self.__class__.__name__}")
            self._init_ui()
        else:
            self.on_config_update(self.config)

    def _load_ui(self):
        """Load the UI from the .ui file."""

    def _init_ui(self):
        """Initialize the UI components specific to the widget."""

    @pyqtSlot(dict)
    def on_config_update(self, config):
        """Handle configuration updates."""
        self.config = config
        self._init_ui()


class MotorControlSelection(MotorControlWidget):
    """
    Widget for selecting the motors to control.

    Signals:
        selected_motors_signal (pyqtSignal(str,str)): Signal to emit the selected motors.
    Slots:
        get_available_motors (pyqtSlot): Slot to populate the available motors in the combo boxes and set the index based on the configuration.
        enable_motor_controls (pyqtSlot(bool)): Slot to enable/disable the motor controls GUI.
        on_config_update (pyqtSlot(dict)): Slot to update the config dict.
    """

    selected_motors_signal = pyqtSignal(str, str)

    def _load_ui(self):
        """Load the UI from the .ui file."""
        current_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(current_path, "motor_control_selection.ui"), self)

    def _init_ui(self):
        """Initialize the UI."""
        # Lock GUI while motors are moving
        self.motor_thread.lock_gui.connect(self.enable_motor_controls)

        self.pushButton_connecMotors.clicked.connect(self.select_motor)
        self.get_available_motors()

        # Connect change signals to change color
        self.comboBox_motor_x.currentIndexChanged.connect(
            lambda: self.set_combobox_style(self.comboBox_motor_x, "#ffa700")
        )
        self.comboBox_motor_y.currentIndexChanged.connect(
            lambda: self.set_combobox_style(self.comboBox_motor_y, "#ffa700")
        )

    @pyqtSlot(dict)
    def on_config_update(self, config: dict) -> None:
        """
        Update config dict
        Args:
            config(dict): New config dict
        """
        self.config = config

        # Get motor names
        self.motor_x, self.motor_y = (
            self.config["motor_control"]["motor_x"],
            self.config["motor_control"]["motor_y"],
        )

        self._init_ui()

    @pyqtSlot(bool)
    def enable_motor_controls(self, enable: bool) -> None:
        """
        Enable or disable the motor controls.
        Args:
            enable(bool): True to enable, False to disable.
        """
        self.motorSelection.setEnabled(enable)

    @pyqtSlot()
    def get_available_motors(self) -> None:
        """
        Slot to populate the available motors in the combo boxes and set the index based on the configuration.
        """
        # Get all available motors
        self.motor_list = self.motor_thread.get_all_motors_names()

        # Populate the combo boxes
        self.comboBox_motor_x.addItems(self.motor_list)
        self.comboBox_motor_y.addItems(self.motor_list)

        # Set the index based on the config if provided
        if self.config:
            index_x = self.comboBox_motor_x.findText(self.motor_x)
            index_y = self.comboBox_motor_y.findText(self.motor_y)
            self.comboBox_motor_x.setCurrentIndex(index_x if index_x != -1 else 0)
            self.comboBox_motor_y.setCurrentIndex(index_y if index_y != -1 else 0)

    def set_combobox_style(self, combobox: QComboBox, color: str) -> None:
        """
        Set the combobox style to a specific color.
        Args:
            combobox(QComboBox): Combobox to change the color.
            color(str): Color to set the combobox to.
        """
        combobox.setStyleSheet(f"QComboBox {{ background-color: {color}; }}")

    def select_motor(self):
        """Emit the selected motors"""
        motor_x = self.comboBox_motor_x.currentText()
        motor_y = self.comboBox_motor_y.currentText()

        # Reset the combobox color to normal after selection
        self.set_combobox_style(self.comboBox_motor_x, "")
        self.set_combobox_style(self.comboBox_motor_y, "")

        self.selected_motors_signal.emit(motor_x, motor_y)


class MotorControlAbsolute(MotorControlWidget):
    """
    Widget for controlling the motors to absolute coordinates.

    Signals:
        coordinates_signal (pyqtSignal(tuple)): Signal to emit the coordinates.
    Slots:
        change_motors (pyqtSlot): Slot to change the active motors.
        enable_motor_controls (pyqtSlot(bool)): Slot to enable/disable the motor controls.
    """

    coordinates_signal = pyqtSignal(tuple)

    def _load_ui(self):
        """Load the UI from the .ui file."""
        current_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(current_path, "motor_control_absolute.ui"), self)

    def _init_ui(self):
        """Initialize the UI."""

        # Check if there are any motors connected
        if self.motor_x is None or self.motor_y is None:
            self.motorControl_absolute.setEnabled(False)
            return

        # Move to absolute coordinates
        self.pushButton_go_absolute.clicked.connect(
            lambda: self.move_motor_absolute(
                self.spinBox_absolute_x.value(), self.spinBox_absolute_y.value()
            )
        )

        self.pushButton_set.clicked.connect(self.save_absolute_coordinates)
        self.pushButton_save.clicked.connect(self.save_current_coordinates)
        self.pushButton_stop.clicked.connect(self.motor_thread.stop_movement)

        # Enable/Disable GUI
        self.motor_thread.lock_gui.connect(self.enable_motor_controls)

        # Error messages
        self.motor_thread.motor_error.connect(
            lambda error: MotorControlErrors.display_error_message(error)
        )

        # Keyboard shortcuts
        self._init_keyboard_shortcuts()

    @pyqtSlot(dict)
    def on_config_update(self, config: dict) -> None:
        """Update config dict"""
        self.config = config

        # Get motor names
        self.motor_x, self.motor_y = (
            self.config["motor_control"]["motor_x"],
            self.config["motor_control"]["motor_y"],
        )

        # Update step precision
        self.precision = self.config["motor_control"]["precision"]

        self._init_ui()

    @pyqtSlot(bool)
    def enable_motor_controls(self, enable: bool) -> None:
        """
        Enable or disable the motor controls.
        Args:
            enable(bool): True to enable, False to disable.
        """

        # Disable or enable all controls within the motorControl_absolute group box
        for widget in self.motorControl_absolute.findChildren(QWidget):
            widget.setEnabled(enable)

        # Enable the pushButton_stop if the motor is moving
        self.pushButton_stop.setEnabled(True)

    @pyqtSlot(str, str)
    def change_motors(self, motor_x: str, motor_y: str):
        """
        Change the active motors and update config.
        Can be connected to the selected_motors_signal from MotorControlSelection.
        Args:
            motor_x(str): New motor X to be controlled.
            motor_y(str): New motor Y to be controlled.
        """
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.config["motor_control"]["motor_x"] = motor_x
        self.config["motor_control"]["motor_y"] = motor_y

    @pyqtSlot(int)
    def set_precision(self, precision: int) -> None:
        """
        Set the precision of the coordinates.
        Args:
            precision(int): Precision of the coordinates.
        """
        self.precision = precision
        self.config["motor_control"]["precision"] = precision
        self.spinBox_absolute_x.setDecimals(precision)
        self.spinBox_absolute_y.setDecimals(precision)

    def move_motor_absolute(self, x: float, y: float) -> None:
        """
        Move the motor to the target coordinates.
        Args:
            x(float): Target x coordinate.
            y(float): Target y coordinate.
        """
        # self._enable_motor_controls(False)
        target_coordinates = (x, y)
        self.motor_thread.move_absolute(self.motor_x, self.motor_y, target_coordinates)
        if self.checkBox_save_with_go.isChecked():
            self.save_absolute_coordinates()

    def _init_keyboard_shortcuts(self):
        """Initialize the keyboard shortcuts."""
        # Go absolute button
        self.pushButton_go_absolute.setShortcut("Ctrl+G")
        self.pushButton_go_absolute.setToolTip("Ctrl+G")

        # Set absolute coordinates
        self.pushButton_set.setShortcut("Ctrl+D")
        self.pushButton_set.setToolTip("Ctrl+D")

        # Save Current coordinates
        self.pushButton_save.setShortcut("Ctrl+S")
        self.pushButton_save.setToolTip("Ctrl+S")

        # Stop Button
        self.pushButton_stop.setShortcut("Ctrl+X")
        self.pushButton_stop.setToolTip("Ctrl+X")

    def save_absolute_coordinates(self):
        """Emit the setup coordinates from the spinboxes"""

        x, y = round(self.spinBox_absolute_x.value(), self.precision), round(
            self.spinBox_absolute_y.value(), self.precision
        )
        self.coordinates_signal.emit((x, y))

    def save_current_coordinates(self):
        """Emit the current coordinates from the motor thread"""
        x, y = self.motor_thread.get_coordinates(self.motor_x, self.motor_y)
        self.coordinates_signal.emit((round(x, self.precision), round(y, self.precision)))


class MotorControlRelative(MotorControlWidget):
    """
    Widget for controlling the motors to relative coordinates.

    Signals:
        precision_signal (pyqtSignal): Signal to emit the precision of the coordinates.
    Slots:
        change_motors (pyqtSlot(str,str)): Slot to change the active motors.
        enable_motor_controls (pyqtSlot): Slot to enable/disable the motor controls.
    """

    precision_signal = pyqtSignal(int)

    def _load_ui(self):
        """Load the UI from the .ui file."""
        # Loading UI
        current_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(current_path, "motor_control_relative.ui"), self)

    def _init_ui(self):
        """Initialize the UI."""
        self._init_ui_motor_control()
        self._init_keyboard_shortcuts()

    @pyqtSlot(dict)
    def on_config_update(self, config: dict) -> None:
        """
        Update config dict
        Args:
            config(dict): New config dict
        """
        self.config = config

        # Get motor names
        self.motor_x, self.motor_y = (
            self.config["motor_control"]["motor_x"],
            self.config["motor_control"]["motor_y"],
        )

        # Update step precision
        self.precision = self.config["motor_control"]["precision"]
        self.spinBox_precision.setValue(self.precision)

        # Update step sizes
        self.spinBox_step_x.setValue(self.config["motor_control"]["step_size_x"])
        self.spinBox_step_y.setValue(self.config["motor_control"]["step_size_y"])

        # Checkboxes for keyboard shortcuts and x/y step size link
        self.checkBox_same_xy.setChecked(self.config["motor_control"]["step_x_y_same"])
        self.checkBox_enableArrows.setChecked(self.config["motor_control"]["move_with_arrows"])

        self._init_ui()

    def _init_ui_motor_control(self) -> None:
        """Initialize the motor control elements"""

        # Connect checkbox and spinBoxes
        self.checkBox_same_xy.stateChanged.connect(self._sync_step_sizes)
        self.spinBox_step_x.valueChanged.connect(self._update_step_size_x)
        self.spinBox_step_y.valueChanged.connect(self._update_step_size_y)

        self.toolButton_right.clicked.connect(
            lambda: self.move_motor_relative(self.motor_x, "x", 1)
        )
        self.toolButton_left.clicked.connect(
            lambda: self.move_motor_relative(self.motor_x, "x", -1)
        )
        self.toolButton_up.clicked.connect(lambda: self.move_motor_relative(self.motor_y, "y", 1))
        self.toolButton_down.clicked.connect(
            lambda: self.move_motor_relative(self.motor_y, "y", -1)
        )

        # Switch between key shortcuts active
        self.checkBox_enableArrows.stateChanged.connect(self._update_arrow_key_shortcuts)
        self._update_arrow_key_shortcuts()

        # Enable/Disable GUI
        self.motor_thread.lock_gui.connect(self.enable_motor_controls)

        # Precision update
        self.spinBox_precision.valueChanged.connect(lambda x: self._update_precision(x))

        # Error messages
        self.motor_thread.motor_error.connect(
            lambda error: MotorControlErrors.display_error_message(error)
        )

        # Stop Button
        self.pushButton_stop.clicked.connect(self.motor_thread.stop_movement)

    def _init_keyboard_shortcuts(self) -> None:
        """Initialize the keyboard shortcuts"""

        # Increase/decrease step size for X motor
        increase_x_shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        decrease_x_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        increase_x_shortcut.activated.connect(
            lambda: self._change_step_size(self.spinBox_step_x, 2)
        )
        decrease_x_shortcut.activated.connect(
            lambda: self._change_step_size(self.spinBox_step_x, 0.5)
        )
        self.spinBox_step_x.setToolTip("Increase step size: Ctrl+A\nDecrease step size: Ctrl+Z")

        # Increase/decrease step size for Y motor
        increase_y_shortcut = QShortcut(QKeySequence("Alt+A"), self)
        decrease_y_shortcut = QShortcut(QKeySequence("Alt+Z"), self)
        increase_y_shortcut.activated.connect(
            lambda: self._change_step_size(self.spinBox_step_y, 2)
        )
        decrease_y_shortcut.activated.connect(
            lambda: self._change_step_size(self.spinBox_step_y, 0.5)
        )
        self.spinBox_step_y.setToolTip("Increase step size: Alt+A\nDecrease step size: Alt+Z")

        # Stop Button
        self.pushButton_stop.setShortcut("Ctrl+X")
        self.pushButton_stop.setToolTip("Ctrl+X")

    def _update_arrow_key_shortcuts(self) -> None:
        """Update the arrow key shortcuts based on the checkbox state."""
        if self.checkBox_enableArrows.isChecked():
            # Set the arrow key shortcuts for motor movement
            self.toolButton_right.setShortcut(Qt.Key_Right)
            self.toolButton_left.setShortcut(Qt.Key_Left)
            self.toolButton_up.setShortcut(Qt.Key_Up)
            self.toolButton_down.setShortcut(Qt.Key_Down)
        else:
            # Clear the shortcuts
            self.toolButton_right.setShortcut("")
            self.toolButton_left.setShortcut("")
            self.toolButton_up.setShortcut("")
            self.toolButton_down.setShortcut("")

    def _update_precision(self, precision: int) -> None:
        """
        Update the precision of the coordinates.
        Args:
            precision(int): Precision of the coordinates.
        """
        self.spinBox_step_x.setDecimals(precision)
        self.spinBox_step_y.setDecimals(precision)
        self.precision_signal.emit(precision)

    def _change_step_size(self, spinBox: QDoubleSpinBox, factor: float) -> None:
        """
        Change the step size of the spinbox.
        Args:
            spinBox(QDoubleSpinBox): Spinbox to change the step size.
            factor(float): Factor to change the step size.
        """
        old_step = spinBox.value()
        new_step = old_step * factor
        spinBox.setValue(new_step)

    def _sync_step_sizes(self):
        """Sync step sizes based on checkbox state."""
        if self.checkBox_same_xy.isChecked():
            value = self.spinBox_step_x.value()
            self.spinBox_step_y.setValue(value)

    def _update_step_size_x(self):
        """Update step size for x if checkbox is checked."""
        if self.checkBox_same_xy.isChecked():
            value = self.spinBox_step_x.value()
            self.spinBox_step_y.setValue(value)

    def _update_step_size_y(self):
        """Update step size for y if checkbox is checked."""
        if self.checkBox_same_xy.isChecked():
            value = self.spinBox_step_y.value()
            self.spinBox_step_x.setValue(value)

    @pyqtSlot(str, str)
    def change_motors(self, motor_x: str, motor_y: str):
        """
        Change the active motors and update config.
        Can be connected to the selected_motors_signal from MotorControlSelection.
        Args:
            motor_x(str): New motor X to be controlled.
            motor_y(str): New motor Y to be controlled.
        """
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.config["motor_control"]["motor_x"] = motor_x
        self.config["motor_control"]["motor_y"] = motor_y

    @pyqtSlot(bool)
    def enable_motor_controls(self, disable: bool) -> None:
        """
        Enable or disable the motor controls.
        Args:
            disable(bool): True to disable, False to enable.
        """

        # Disable or enable all controls within the motorControl_absolute group box
        for widget in self.motorControl.findChildren(QWidget):
            widget.setEnabled(disable)

        # Enable the pushButton_stop if the motor is moving
        self.pushButton_stop.setEnabled(True)

    def move_motor_relative(self, motor, axis: str, direction: int) -> None:
        """
        Move the motor relative to the current position.
        Args:
            motor: Motor to move.
            axis(str): Axis to move.
            direction(int): Direction to move. 1 for positive, -1 for negative.
        """
        if axis == "x":
            step = direction * self.spinBox_step_x.value()
        elif axis == "y":
            step = direction * self.spinBox_step_y.value()
        self.motor_thread.move_relative(motor, step)


class MotorCoordinateTable(MotorControlWidget):
    """
    Widget to save coordinates from motor, display them in the table and move back to them.
    There are two modes of operation:
        - Individual: Each row is a single coordinate.
        - Start/Stop: Each pair of rows is a start and end coordinate.
    Signals:
        plot_coordinates_signal (pyqtSignal(list, str, str)): Signal to plot the coordinates in the MotorMap.
    Slots:
        add_coordinate (pyqtSlot(tuple)): Slot to add a coordinate to the table.
        mode_switch (pyqtSlot): Slot to switch between individual and start/stop mode.
    """

    plot_coordinates_signal = pyqtSignal(list, str, str)

    def _load_ui(self):
        """Load the UI for the coordinate table."""
        current_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(current_path, "motor_control_table.ui"), self)

    def _init_ui(self):
        """Initialize the UI"""
        # Setup table behaviour
        self._setup_table()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # for tag columns default tag
        self.tag_counter = 1

        # Connect signals and slots
        self.checkBox_resize_auto.stateChanged.connect(self.resize_table_auto)
        self.comboBox_mode.currentIndexChanged.connect(self.mode_switch)

        # Keyboard shortcuts for deleting a row
        self.delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self.table)
        self.delete_shortcut.activated.connect(self.delete_selected_row)
        self.backspace_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self.table)
        self.backspace_shortcut.activated.connect(self.delete_selected_row)

        # Warning message for mode switch enable/disable
        self.warning_message = True

    @pyqtSlot(dict)
    def on_config_update(self, config: dict) -> None:
        """
        Update config dict
        Args:
            config(dict): New config dict
        """
        self.config = config

        # Get motor names
        self.motor_x, self.motor_y = (
            self.config["motor_control"]["motor_x"],
            self.config["motor_control"]["motor_y"],
        )

        # Decimal precision of the table coordinates
        self.precision = self.config["motor_control"].get("precision", 3)

        # Mode switch default option
        self.mode = self.config["motor_control"].get("mode", "Individual")

        # Set combobox to default mode
        self.comboBox_mode.setCurrentText(self.mode)

        self._init_ui()

    def _setup_table(self):
        """Setup the table with appropriate headers and configurations."""
        mode = self.comboBox_mode.currentText()

        if mode == "Individual":
            self._setup_individual_mode()
        elif mode == "Start/Stop":
            self._setup_start_stop_mode()
            self.start_stop_counter = 0  # TODO: remove this??

        self.wipe_motor_map_coordinates()

    def _setup_individual_mode(self):
        """Setup the table for individual mode."""
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Show", "Move", "Tag", "X", "Y"])
        self.table.verticalHeader().setVisible(False)

    def _setup_start_stop_mode(self):
        """Setup the table for start/stop mode."""
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "Show",
                "Move [start]",
                "Move [end]",
                "Tag",
                "X [start]",
                "Y [start]",
                "X [end]",
                "Y [end]",
            ]
        )
        self.table.verticalHeader().setVisible(False)
        # Set flag to track if the coordinate is stat or the end of the entry
        self.is_next_entry_end = False

    def mode_switch(self):
        """Switch between individual and start/stop mode."""
        last_selected_index = self.comboBox_mode.currentIndex()

        if self.table.rowCount() > 0 and self.warning_message is True:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(
                "Switching modes will delete all table entries. Do you want to continue?"
            )
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = msgBox.exec()

            if returnValue is QMessageBox.Cancel:
                self.comboBox_mode.blockSignals(True)  # Block signals
                self.comboBox_mode.setCurrentIndex(last_selected_index)
                self.comboBox_mode.blockSignals(False)  # Unblock signals
                return

        # Wipe table
        self.wipe_motor_map_coordinates()

        # Initiate new table with new mode
        self._setup_table()

    @pyqtSlot(tuple)
    def add_coordinate(self, coordinates: tuple):
        """
        Add a coordinate to the table.
        Args:
            coordinates(tuple): Coordinates (x,y) to add to the table.
        """
        tag = f"Pos {self.tag_counter}"
        self.tag_counter += 1
        x, y = coordinates
        self._add_row(tag, x, y)

    def _add_row(self, tag: str, x: float, y: float) -> None:
        """
        Add a row to the table.
        Args:
            tag(str): Tag of the coordinate.
            x(float): X coordinate.
            y(float): Y coordinate.
        """

        mode = self.comboBox_mode.currentText()
        if mode == "Individual":
            checkbox_pos = 0
            button_pos = 1
            tag_pos = 2
            x_pos = 3
            y_pos = 4
            coordinate_reference = "Individual"
            color = "green"

            # Add new row -> new entry
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            # Add Widgets
            self._add_widgets(
                tag,
                x,
                y,
                row_count,
                checkbox_pos,
                tag_pos,
                button_pos,
                x_pos,
                y_pos,
                coordinate_reference,
                color,
            )

        if mode == "Start/Stop":
            # These positions are always fixed
            checkbox_pos = 0
            tag_pos = 3

            if self.is_next_entry_end is False:  # It is the start position of the entry
                print("Start position")
                button_pos = 1
                x_pos = 4
                y_pos = 5
                coordinate_reference = "Start"
                color = "blue"

                # Add new row -> new entry
                row_count = self.table.rowCount()
                self.table.insertRow(row_count)

                # Add Widgets
                self._add_widgets(
                    tag,
                    x,
                    y,
                    row_count,
                    checkbox_pos,
                    tag_pos,
                    button_pos,
                    x_pos,
                    y_pos,
                    coordinate_reference,
                    color,
                )

                # Next entry will be the end of the current entry
                self.is_next_entry_end = True

            elif self.is_next_entry_end is True:  # It is the end position of the entry
                print("End position")
                row_count = self.table.rowCount() - 1  # Current row
                button_pos = 2
                x_pos = 6
                y_pos = 7
                coordinate_reference = "Stop"
                color = "red"

                # Add Widgets
                self._add_widgets(
                    tag,
                    x,
                    y,
                    row_count,
                    checkbox_pos,
                    tag_pos,
                    button_pos,
                    x_pos,
                    y_pos,
                    coordinate_reference,
                    color,
                )
                self.is_next_entry_end = False  # Next entry will be the start of the new entry

        # Auto table resize
        self.resize_table_auto()

    def _add_widgets(
        self,
        tag: str,
        x: float,
        y: float,
        row: int,
        checkBox_pos: int,
        tag_pos: int,
        button_pos: int,
        x_pos: int,
        y_pos: int,
        coordinate_reference: str,
        color: str,
    ) -> None:
        """
        Add widgets to the table.
        Args:
            tag(str): Tag of the coordinate.
            x(float): X coordinate.
            y(float): Y coordinate.
            row(int): Row of the QTableWidget where to add the widgets.
            checkBox_pos(int): Column where to put CheckBox.
            tag_pos(int): Column where to put Tag.
            button_pos(int): Column where to put Move button.
            x_pos(int): Column where to link x coordinate.
            y_pos(int): Column where to link y coordinate.
            coordinate_reference(str): Reference to the coordinate for MotorMap.
            color(str): Color of the coordinate for MotorMap.
        """
        # Add widgets
        self._add_checkbox(row, checkBox_pos, x_pos, y_pos)
        self._add_move_button(row, button_pos, x_pos, y_pos)
        self.table.setItem(row, tag_pos, QTableWidgetItem(tag))
        self._add_line_edit(x, row, x_pos, x_pos, y_pos, coordinate_reference, color)
        self._add_line_edit(y, row, y_pos, x_pos, y_pos, coordinate_reference, color)

        # # Emit the coordinates to be plotted
        self.emit_plot_coordinates(x_pos, y_pos, coordinate_reference, color)

        # Connect item edit to emit coordinates
        self.table.itemChanged.connect(
            lambda: print(f"item changed from {coordinate_reference} slot \n {x}-{y}-{color}")
        )
        self.table.itemChanged.connect(
            lambda: self.emit_plot_coordinates(x_pos, y_pos, coordinate_reference, color)
        )

    def _add_checkbox(self, row: int, checkBox_pos: int, x_pos: int, y_pos: int):
        """
        Add a checkbox to the table.
        Args:
            row(int): Row of QTableWidget where to add the checkbox.
            checkBox_pos(int): Column where to put CheckBox.
            x_pos(int): Column where to link x coordinate.
            y_pos(int): Column where to link y coordinate.
        """
        show_checkbox = QCheckBox()
        show_checkbox.setChecked(True)
        show_checkbox.stateChanged.connect(lambda: self.emit_plot_coordinates(x_pos, y_pos))
        self.table.setCellWidget(row, checkBox_pos, show_checkbox)

    def _add_move_button(self, row: int, button_pos: int, x_pos: int, y_pos: int) -> None:
        """
        Add a move button to the table.
        Args:
            row(int): Row of QTableWidget where to add the move button.
            button_pos(int): Column where to put move button.
            x_pos(int): Column where to link x coordinate.
            y_pos(int): Column where to link y coordinate.
        """
        move_button = QPushButton("Move")
        move_button.clicked.connect(lambda: self.handle_move_button_click(x_pos, y_pos))
        self.table.setCellWidget(row, button_pos, move_button)

    def _add_line_edit(
        self,
        value: float,
        row: int,
        line_pos: int,
        x_pos: int,
        y_pos: int,
        coordinate_reference: str,
        color: str,
    ) -> None:
        """
        Add a QLineEdit to the table.
        Args:
            value(float): Initial value of the QLineEdit.
            row(int): Row of QTableWidget where to add the QLineEdit.
            line_pos(int): Column where to put QLineEdit.
            x_pos(int): Column where to link x coordinate.
            y_pos(int): Column where to link y coordinate.
            coordinate_reference(str): Reference to the coordinate for MotorMap.
            color(str): Color of the coordinate for MotorMap.
        """
        # Adding validator
        validator = QDoubleValidator()
        validator.setDecimals(self.precision)

        # Create line edit
        edit = QLineEdit(str(f"{value:.{self.precision}f}"))
        edit.setValidator(validator)
        edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add line edit to the table
        self.table.setCellWidget(row, line_pos, edit)
        edit.textChanged.connect(
            lambda: self.emit_plot_coordinates(x_pos, y_pos, coordinate_reference, color)
        )

    def wipe_motor_map_coordinates(self):
        """Wipe the motor map coordinates."""
        try:
            self.table.itemChanged.disconnect()  # Disconnect all previous connections
        except TypeError:
            print("No previous connections to disconnect")
        self.table.setRowCount(0)
        reference_tags = ["Individual", "Start", "Stop"]
        for reference_tag in reference_tags:
            self.plot_coordinates_signal.emit([], reference_tag, "green")

    def handle_move_button_click(self, x_pos: int, y_pos: int) -> None:
        """
        Handle the move button click.
        Args:
            x_pos(int): X position of the coordinate.
            y_pos(int): Y position of the coordinate.
        """
        button = self.sender()
        row = self.table.indexAt(button.pos()).row()

        x = self.get_coordinate(row, x_pos)
        y = self.get_coordinate(row, y_pos)
        self.move_motor(x, y)

    def emit_plot_coordinates(self, x_pos: float, y_pos: float, reference_tag: str, color: str):
        """
        Emit the coordinates to be plotted.
        Args:
            x_pos(float): X position of the coordinate.
            y_pos(float): Y position of the coordinate.
            reference_tag(str): Reference tag of the coordinate.
            color(str): Color of the coordinate.
        """
        print(
            f"Emitting plot coordinates: x_pos={x_pos}, y_pos={y_pos}, reference_tag={reference_tag}, color={color}"
        )
        coordinates = []
        for row in range(self.table.rowCount()):
            show = self.table.cellWidget(row, 0).isChecked()
            x = self.get_coordinate(row, x_pos)
            y = self.get_coordinate(row, y_pos)

            coordinates.append((x, y, show))  # (x, y, show_flag)
        self.plot_coordinates_signal.emit(coordinates, reference_tag, color)

    def get_coordinate(self, row: int, column: int) -> float:
        """
        Helper function to get the coordinate from the table QLineEdit cells.
        Args:
            row(int): Row of the table.
            column(int): Column of the table.
        Returns:
            float: Value of the coordinate.
        """
        edit = self.table.cellWidget(row, column)
        value = float(edit.text()) if edit and edit.text() != "" else None
        if value:
            return value

    def delete_selected_row(self):
        """Delete the selected row from the table."""
        selected_rows = self.table.selectionModel().selectedRows()
        for row in selected_rows:
            self.table.removeRow(row.row())
        if self.comboBox_mode.currentText() == "Start/Stop":
            self.emit_plot_coordinates(x_pos=4, y_pos=5, reference_tag="Start", color="blue")
            self.emit_plot_coordinates(x_pos=6, y_pos=7, reference_tag="Stop", color="red")
            self.is_next_entry_end = False
        elif self.comboBox_mode.currentText() == "Individual":
            self.emit_plot_coordinates(x_pos=3, y_pos=4, reference_tag="Individual", color="green")

    def resize_table_auto(self):
        """Resize the table to fit the contents."""
        if self.checkBox_resize_auto.isChecked():
            self.table.resizeColumnsToContents()

    def move_motor(self, x: float, y: float) -> None:
        """
        Move the motor to the target coordinates.
        Args:
            x(float): Target x coordinate.
            y(float): Target y coordinate.
        """
        self.motor_thread.move_absolute(self.motor_x, self.motor_y, (x, y))

    @pyqtSlot(str, str)
    def change_motors(self, motor_x: str, motor_y: str) -> None:
        """
        Change the active motors and update config.
        Can be connected to the selected_motors_signal from MotorControlSelection.
        Args:
            motor_x(str): New motor X to be controlled.
            motor_y(str): New motor Y to be controlled.
        """
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.config["motor_control"]["motor_x"] = motor_x
        self.config["motor_control"]["motor_y"] = motor_y

    @pyqtSlot(int)
    def set_precision(self, precision: int) -> None:
        """
        Set the precision of the coordinates.
        Args:
            precision(int): Precision of the coordinates.
        """
        self.precision = precision
        self.config["motor_control"]["precision"] = precision


class MotorControlErrors:
    """Class for displaying formatted error messages."""

    @staticmethod
    def display_error_message(error_message: str) -> None:
        """
        Display a critical error message.
        Args:
            error_message(str): Error message to display.
        """
        # Create a QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Critical Error")

        # Format the message
        formatted_message = MotorControlErrors._format_error_message(error_message)
        msg.setText(formatted_message)

        # Display the message box
        msg.exec_()

    @staticmethod
    def _format_error_message(error_message: str) -> str:
        """
        Format the error message.
        Args:
            error_message(str): Error message to format.

        Returns:
            str: Formatted error message.
        """
        # Split the message into lines
        lines = error_message.split("\n")
        formatted_lines = [
            f"<b>{line.strip()}</b>" if i == 0 else line.strip()
            for i, line in enumerate(lines)
            if line.strip()
        ]

        # Join the lines with double breaks for empty lines in between
        formatted_message = "<br><br>".join(formatted_lines)

        return formatted_message


class MotorActions(Enum):
    """Enum for motor actions."""

    MOVE_ABSOLUTE = "move_absolute"
    MOVE_RELATIVE = "move_relative"


class MotorThread(QThread):
    """
    QThread subclass for controlling motor actions asynchronously.

    Signals:
        coordinates_updated (pyqtSignal): Signal to emit current coordinates.
        motor_error (pyqtSignal): Signal to emit when there is an error with the motors.
        lock_gui (pyqtSignal): Signal to lock/unlock the GUI.
    """

    coordinates_updated = pyqtSignal(float, float)  # Signal to emit current coordinates
    motor_error = pyqtSignal(str)  # Signal to emit when there is an error with the motors
    lock_gui = pyqtSignal(bool)  # Signal to lock/unlock the GUI

    def __init__(self, parent=None, client=None):
        super().__init__(parent)

        bec_dispatcher = BECDispatcher()
        self.client = bec_dispatcher.client if client is None else client
        self.dev = self.client.device_manager.devices
        self.scans = self.client.scans
        self.queue = self.client.queue
        self.action = None

        self.motor = None
        self.motor_x = None
        self.motor_y = None
        self.target_coordinates = None
        self.value = None

    def get_all_motors_names(self) -> list:
        """
        Get all the motors names.
        Returns:
            list: List of all the motors names.
        """
        all_devices = self.client.device_manager.devices.enabled_devices
        all_motors_names = [motor.name for motor in all_devices if isinstance(motor, Positioner)]
        return all_motors_names

    def get_coordinates(self, motor_x: str, motor_y: str) -> tuple:
        """
        Get the current coordinates of the motors.
        Args:
            motor_x(str): Motor X to get positions from.
            motor_y(str): Motor Y to get positions from.

        Returns:
            tuple: Current coordinates of the motors.
        """
        x = self.dev[motor_x].readback.get()
        y = self.dev[motor_y].readback.get()
        return x, y

    def move_absolute(self, motor_x: str, motor_y: str, target_coordinates: tuple) -> None:
        """
        Wrapper for moving the motor to the target coordinates.
        Args:
            motor_x(str): Motor X to move.
            motor_y(str): Motor Y to move.
            target_coordinates(tuple): Target coordinates.
        """
        self.action = MotorActions.MOVE_ABSOLUTE
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.target_coordinates = target_coordinates
        self.start()

    def move_relative(self, motor: str, value: float) -> None:
        """
        Wrapper for moving the motor relative to the current position.
        Args:
            motor(str): Motor to move.
            value(float): Value to move.
        """
        self.action = MotorActions.MOVE_RELATIVE
        self.motor = motor
        self.value = value
        self.start()

    def run(self):
        """
        Run the thread.
        Possible actions:
            - Move to coordinates
            - Move relative
        """
        if self.action == MotorActions.MOVE_ABSOLUTE:
            self._move_motor_absolute(self.motor_x, self.motor_y, self.target_coordinates)
        elif self.action == MotorActions.MOVE_RELATIVE:
            self._move_motor_relative(self.motor, self.value)

    def _move_motor_absolute(self, motor_x: str, motor_y: str, target_coordinates: tuple) -> None:
        """
        Move the motor to the target coordinates.
        Args:
            motor_x(str): Motor X to move.
            motor_y(str): Motor Y to move.
            target_coordinates(tuple): Target coordinates.
        """
        self.lock_gui.emit(False)
        try:
            status = self.scans.mv(
                self.dev[motor_x],
                target_coordinates[0],
                self.dev[motor_y],
                target_coordinates[1],
                relative=False,
            )
            status.wait()
        except AlarmBase as e:
            self.motor_error.emit(str(e))
        finally:
            self.lock_gui.emit(True)

    def _move_motor_relative(self, motor, value: float) -> None:
        """
        Move the motor relative to the current position.
        Args:
            motor(str): Motor to move.
            value(float): Value to move.
        """
        self.lock_gui.emit(False)
        try:
            status = self.scans.mv(self.dev[motor], value, relative=True)
            status.wait()
        except AlarmBase as e:
            self.motor_error.emit(str(e))
        finally:
            self.lock_gui.emit(True)

    def stop_movement(self):
        self.queue.request_scan_abortion()
        self.queue.request_queue_reset()
