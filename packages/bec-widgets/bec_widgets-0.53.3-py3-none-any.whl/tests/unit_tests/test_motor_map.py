# pylint: disable = no-name-in-module,missing-module-docstring, missing-function-docstring
from unittest.mock import MagicMock

import pytest

from bec_widgets.widgets import MotorMap

from .client_mocks import mocked_client

CONFIG_DEFAULT = {
    "plot_settings": {
        "colormap": "Greys",
        "scatter_size": 5,
        "max_points": 1000,
        "num_dim_points": 100,
        "precision": 2,
        "num_columns": 1,
        "background_value": 25,
    },
    "motors": [
        {
            "plot_name": "Motor Map",
            "x_label": "Motor X",
            "y_label": "Motor Y",
            "signals": {
                "x": [{"name": "samx", "entry": "samx"}],
                "y": [{"name": "samy", "entry": "samy"}],
            },
        },
        {
            "plot_name": "Motor Map 2 ",
            "x_label": "Motor X",
            "y_label": "Motor Y",
            "signals": {
                "x": [{"name": "aptrx", "entry": "aptrx"}],
                "y": [{"name": "aptry", "entry": "aptry"}],
            },
        },
    ],
}

CONFIG_ONE_DEVICE = {
    "plot_settings": {
        "colormap": "Greys",
        "scatter_size": 5,
        "max_points": 1000,
        "num_dim_points": 100,
        "precision": 2,
        "num_columns": 1,
        "background_value": 25,
    },
    "motors": [
        {
            "plot_name": "Motor Map",
            "x_label": "Motor X",
            "y_label": "Motor Y",
            "signals": {
                "x": [{"name": "samx", "entry": "samx"}],
                "y": [{"name": "samy", "entry": "samy"}],
            },
        }
    ],
}


@pytest.fixture(scope="function")
def motor_map(qtbot, mocked_client):
    widget = MotorMap(client=mocked_client)
    qtbot.addWidget(widget)
    qtbot.waitExposed(widget)
    yield widget


def test_motor_limits_initialization(motor_map):
    # Example test to check if motor limits are correctly initialized
    expected_limits = {"samx": [-10, 10], "samy": [-5, 5]}
    for motor_name, expected_limit in expected_limits.items():
        actual_limit = motor_map._get_motor_limit(motor_name)
        assert actual_limit == expected_limit


def test_motor_initial_position(motor_map):
    motor_map.precision = 2

    motor_map_dev = motor_map.client.device_manager.devices

    # Example test to check if motor initial positions are correctly initialized
    expected_positions = {
        ("samx", "samx"): motor_map_dev["samx"].read()["samx"]["value"],
        ("samy", "samy"): motor_map_dev["samy"].read()["samy"]["value"],
        ("aptrx", "aptrx"): motor_map_dev["aptrx"].read()["aptrx"]["value"],
        ("aptry", "aptry"): motor_map_dev["aptry"].read()["aptry"]["value"],
    }
    for (motor_name, entry), expected_position in expected_positions.items():
        actual_position = motor_map._get_motor_init_position(motor_name, entry)
        assert actual_position == expected_position


@pytest.mark.parametrize("config, number_of_plots", [(CONFIG_DEFAULT, 2), (CONFIG_ONE_DEVICE, 1)])
def test_initialization(motor_map, config, number_of_plots):
    config_load = config
    motor_map.on_config_update(config_load)
    assert isinstance(motor_map, MotorMap)
    assert motor_map.client is not None
    assert motor_map.config == config_load
    assert len(motor_map.plot_data) == number_of_plots


def test_motor_movement_updates_position_and_database(motor_map):
    motor_map.on_config_update(CONFIG_DEFAULT)

    # Initial positions
    initial_position_samx = 2.0
    initial_position_samy = 3.0

    # Set initial positions in the mocked database
    motor_map.database["samx"]["samx"] = [initial_position_samx]
    motor_map.database["samy"]["samy"] = [initial_position_samy]

    # Simulate motor movement for 'samx' only
    new_position_samx = 4.0
    motor_map.on_device_readback({"signals": {"samx": {"value": new_position_samx}}})

    # Verify database update for 'samx'
    assert motor_map.database["samx"]["samx"] == [initial_position_samx, new_position_samx]

    # Verify 'samy' retains its last known position
    assert motor_map.database["samy"]["samy"] == [initial_position_samy, initial_position_samy]


def test_scatter_plot_rendering(motor_map):
    motor_map.on_config_update(CONFIG_DEFAULT)
    # Set initial positions
    initial_position_samx = 2.0
    initial_position_samy = 3.0
    motor_map.database["samx"]["samx"] = [initial_position_samx]
    motor_map.database["samy"]["samy"] = [initial_position_samy]

    # Simulate motor movement for 'samx' only
    new_position_samx = 4.0
    motor_map.on_device_readback({"signals": {"samx": {"value": new_position_samx}}})
    motor_map._update_plots()

    # Get the scatter plot item
    plot_name = "Motor Map"  # Update as per your actual plot name
    scatter_plot_item = motor_map.curves_data[plot_name]["pos"]

    # Check the scatter plot item properties
    assert len(scatter_plot_item.data) > 0, "Scatter plot data is empty"
    x_data = scatter_plot_item.data["x"]
    y_data = scatter_plot_item.data["y"]
    assert x_data[-1] == new_position_samx, "Scatter plot X data not updated correctly"
    assert (
        y_data[-1] == initial_position_samy
    ), "Scatter plot Y data should retain last known position"


def test_plot_visualization_consistency(motor_map):
    motor_map.on_config_update(CONFIG_DEFAULT)
    # Simulate updating the plot with new data
    motor_map.on_device_readback({"signals": {"samx": {"value": 5}}})
    motor_map.on_device_readback({"signals": {"samy": {"value": 9}}})
    motor_map._update_plots()

    plot_name = "Motor Map"
    scatter_plot_item = motor_map.curves_data[plot_name]["pos"]

    # Check if the scatter plot reflects the new data correctly
    assert (
        scatter_plot_item.data["x"][-1] == 5 and scatter_plot_item.data["y"][-1] == 9
    ), "Plot not updated correctly with new data"
