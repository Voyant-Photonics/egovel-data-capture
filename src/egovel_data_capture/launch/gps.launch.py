import os
import yaml

import ament_index_python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import SetRemap


def generate_launch_description():
    # Get the path to the ublox_gps package and ntrip_client package
    ntrip_client_pkg = ament_index_python.get_package_share_directory("ntrip_client")

    default_config = os.path.join(
        ament_index_python.get_package_share_directory("egovel_data_capture"),
        "config",
        "sensors",
        "gps.yaml",
    )

    with open(default_config, "r") as f:
        config = yaml.safe_load(f)

    # Declare the config file argument
    config_file_arg = DeclareLaunchArgument(
        "config_file",
        default_value=default_config,
        description="Path to the ublox_gps_node config file",
    )

    # Include the ublox_gps_node launch file with the config file argument
    params = config["ublox_gps_node"]["ros__parameters"]
    ublox_launch = ComposableNodeContainer(
        name="ublox_gps_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[
            ComposableNode(
                package="ublox_gps",
                plugin="ublox_node::UbloxNode",
                name="ublox_gps_node",
                parameters=[params],
            ),
        ],
        output="both",
    )
    # Launch the ntrip client node with the appropriate arguments
    ntrip_configs = config["ntrip_client_config"]["ros__parameters"]
    ntrip_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(ntrip_client_pkg, "ntrip_client_launch.py")]
        ),
        launch_arguments={
            "host": ntrip_configs["host"],
            "port": ntrip_configs["port"],
            "mountpoint": ntrip_configs["mountpoint"],
            "username": ntrip_configs["username"],
            "password": ntrip_configs["password"],
        }.items(),
    )
    # Remap the topics expected by ntrip_client to the ublox node outputs
    ntrip_with_remaps = GroupAction(
        [
            SetRemap(src="fix", dst="/ublox_gps_node/fix"),
            ntrip_launch,
        ]
    )

    return LaunchDescription(
        [
            config_file_arg,
            ublox_launch,
            ntrip_with_remaps,
        ]
    )
