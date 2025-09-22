from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Configuration files
    voyant_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "voyant_lidar.yaml",
        ]
    )

    # Sensor nodes
    voyant_sensor = Node(
        package="voyant_ros",
        executable="voyant_sensor_node",
        name="voyant_sensor",
        parameters=[voyant_config],
        remappings=[
            ("/device_metadata", "/voyant/device_metadata"),
            ("/point_cloud", "/voyant/point_cloud"),
        ],  # TODO: Remove when this is inherent to ROS node
        output="screen",
    )

    return LaunchDescription([voyant_sensor])
