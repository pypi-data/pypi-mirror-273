# pylint: disable = no-name-in-module,missing-class-docstring, missing-module-docstring
import os
from unittest.mock import MagicMock

import pytest
import yaml

from bec_widgets.widgets import BECMonitor

from .client_mocks import mocked_client


def load_test_config(config_name):
    """Helper function to load config from yaml file."""
    config_path = os.path.join(os.path.dirname(__file__), "test_configs", f"{config_name}.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


@pytest.fixture(scope="function")
def monitor(bec_dispatcher, qtbot, mocked_client):
    # client = MagicMock()
    widget = BECMonitor(client=mocked_client)
    qtbot.addWidget(widget)
    qtbot.waitExposed(widget)
    yield widget


@pytest.mark.parametrize(
    "config_name, scan_type, number_of_plots",
    [
        ("config_device", False, 2),
        ("config_device_no_entry", False, 2),
        # ("config_scan", True, 4),
    ],
)
def test_initialization_with_device_config(monitor, config_name, scan_type, number_of_plots):
    config = load_test_config(config_name)
    monitor.on_config_update(config)
    assert isinstance(monitor, BECMonitor)
    assert monitor.client is not None
    assert len(monitor.plot_data) == number_of_plots
    assert monitor.scan_types == scan_type


@pytest.mark.parametrize(
    "config_initial,config_update",
    [("config_device", "config_scan"), ("config_scan", "config_device")],
)
def test_on_config_update(monitor, config_initial, config_update):
    config_initial = load_test_config(config_initial)
    config_update = load_test_config(config_update)
    # validated config has to be compared
    config_initial_validated = monitor.validator.validate_monitor_config(
        config_initial
    ).model_dump()
    config_update_validated = monitor.validator.validate_monitor_config(config_update).model_dump()
    monitor.on_config_update(config_initial)
    assert monitor.config == config_initial_validated
    monitor.on_config_update(config_update)
    assert monitor.config == config_update_validated


@pytest.mark.parametrize(
    "config_name, expected_num_columns, expected_plot_names, expected_coordinates",
    [
        ("config_device", 1, ["BPM4i plots vs samx", "Gauss plots vs samx"], [(0, 0), (1, 0)]),
        (
            "config_scan",
            3,
            ["Grid plot 1", "Grid plot 2", "Grid plot 3", "Grid plot 4"],
            [(0, 0), (0, 1), (0, 2), (1, 0)],
        ),
    ],
)
def test_render_initial_plots(
    monitor, config_name, expected_num_columns, expected_plot_names, expected_coordinates
):
    config = load_test_config(config_name)
    monitor.on_config_update(config)

    # Validate number of columns
    assert monitor.plot_settings["num_columns"] == expected_num_columns

    # Validate the plots are created correctly
    for expected_name in expected_plot_names:
        assert expected_name in monitor.plots.keys()

    # Validate the grid_coordinates
    assert monitor.grid_coordinates == expected_coordinates


def mock_getitem(dev_name):
    """Helper function to mock the __getitem__ method of the 'dev'."""
    mock_instance = MagicMock()
    if dev_name == "samx":
        mock_instance._hints = "samx"
    elif dev_name == "bpm4i":
        mock_instance._hints = "bpm4i"
    elif dev_name == "gauss_bpm":
        mock_instance._hints = "gauss_bpm"

    return mock_instance


def mock_get_scan_storage(scan_id, data):
    """Helper function to mock the __getitem__ method of the 'dev'."""
    mock_instance = MagicMock()
    mock_instance.get_scan_storage.return_value = data
    return mock_instance


# mocked messages and metadata
msg_1 = {
    "data": {
        "samx": {"samx": {"value": 10}},
        "bpm4i": {"bpm4i": {"value": 5}},
        "gauss_bpm": {"gauss_bpm": {"value": 6}},
        "gauss_adc1": {"gauss_adc1": {"value": 8}},
        "gauss_adc2": {"gauss_adc2": {"value": 9}},
    },
    "scan_id": 1,
}
metadata_grid = {"scan_name": "grid_scan"}
metadata_line = {"scan_name": "line_scan"}


@pytest.mark.parametrize(
    "config_name, msg, metadata, expected_data",
    [
        # case: msg does not have 'scan_id'
        (
            "config_device",
            {"data": {}},
            {},
            {
                "scan_segment": {
                    "bpm4i": {"bpm4i": []},
                    "gauss_adc1": {"gauss_adc1": []},
                    "gauss_adc2": {"gauss_adc2": []},
                    "samx": {"samx": []},
                }
            },
        ),
        # case: scan_types is false, msg contains all valid fields, and entry is present in config
        (
            "config_device",
            msg_1,
            {},
            {
                "scan_segment": {
                    "bpm4i": {"bpm4i": [5]},
                    "gauss_adc1": {"gauss_adc1": [8]},
                    "gauss_adc2": {"gauss_adc2": [9]},
                    "samx": {"samx": [10]},
                }
            },
        ),
        # case: scan_types is false, msg contains all valid fields and entry is missing in config, should use hints
        (
            "config_device_no_entry",
            msg_1,
            {},
            {
                "scan_segment": {
                    "bpm4i": {"bpm4i": [5]},
                    "gauss_bpm": {"gauss_bpm": [6]},
                    "samx": {"samx": [10]},
                }
            },
        ),
        # case: scan_types is true, msg contains all valid fields, metadata contains scan "line_scan:"
        (
            "config_scan",
            msg_1,
            metadata_line,
            {
                "scan_segment": {
                    "bpm4i": {"bpm4i": [5]},
                    "gauss_adc1": {"gauss_adc1": [8]},
                    "gauss_adc2": {"gauss_adc2": [9]},
                    "gauss_bpm": {"gauss_bpm": [6]},
                    "samx": {"samx": [10]},
                }
            },
        ),
        (
            "config_scan",
            msg_1,
            metadata_grid,
            {
                "scan_segment": {
                    "bpm4i": {"bpm4i": [5]},
                    "gauss_adc1": {"gauss_adc1": [8]},
                    "gauss_adc2": {"gauss_adc2": [9]},
                    "gauss_bpm": {"gauss_bpm": [6]},
                    "samx": {"samx": [10]},
                }
            },
        ),
    ],
)
def test_on_scan_segment(monitor, config_name, msg, metadata, expected_data):
    config = load_test_config(config_name)
    monitor.on_config_update(config)

    # Mock scan_storage.find_scan_by_ID
    mock_scan_data = MagicMock()
    mock_scan_data.data = {
        device_name: {
            entry: MagicMock(val=[msg["data"][device_name][entry]["value"]])
            for entry in msg["data"][device_name]
        }
        for device_name in msg["data"]
    }
    monitor.queue.scan_storage.find_scan_by_ID.return_value = mock_scan_data

    monitor.on_scan_segment(msg, metadata)
    assert monitor.database == expected_data
