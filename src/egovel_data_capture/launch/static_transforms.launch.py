import yaml
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Load static transforms config
    config_file = os.path.join(
        get_package_share_directory("egovel_data_capture"),
        "config",
        "transforms",
        "static_transforms.yaml",
    )

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    transforms = config["static_transforms"]
    nodes = []

    # Add map -> front_axle transform as Identity
    nodes.append(
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="map_to_vehicle_publisher",
            arguments=["0", "0", "0", "0", "0", "0", "map", "front_axle"],
            output="screen",
        )
    )

    # Process wheel transforms
    for wheel_name, wheel_data in transforms["wheels"].items():
        trans = wheel_data["translation"]
        rot = wheel_data["rotation"]
        nodes.append(
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name=f"{wheel_name}_publisher",
                arguments=[
                    str(trans[0]),
                    str(trans[1]),
                    str(trans[2]),  # x, y, z
                    str(rot[0]),
                    str(rot[1]),
                    str(rot[2]),
                    str(rot[3]),  # qx, qy, qz, qw
                    wheel_data["parent"],
                    wheel_data["child"],
                ],
                output="screen",
            )
        )

    # Process collection rig transform
    rig_data = transforms["collection_rig"]
    trans = rig_data["translation"]
    rot = rig_data["rotation"]
    nodes.append(
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="collection_rig_publisher",
            arguments=[
                str(trans[0]),
                str(trans[1]),
                str(trans[2]),
                str(rot[0]),
                str(rot[1]),
                str(rot[2]),
                str(rot[3]),
                rig_data["parent"],
                rig_data["child"],
            ],
            output="screen",
        )
    )

    # Process sensor transforms
    for sensor_name, sensor_data in transforms["sensors"].items():
        trans = sensor_data["translation"]
        rot = sensor_data["rotation"]
        nodes.append(
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name=f"{sensor_name}_publisher",
                arguments=[
                    str(trans[0]),
                    str(trans[1]),
                    str(trans[2]),
                    str(rot[0]),
                    str(rot[1]),
                    str(rot[2]),
                    str(rot[3]),
                    sensor_data["parent"],
                    sensor_data["child"],
                ],
                output="screen",
            )
        )

    return LaunchDescription(nodes)
