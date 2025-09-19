from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Configuration files
    vectornav_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "vectornav.yaml",
        ]
    )

    # Vectornav nodes
    start_vectornav_cmd = Node(
        package="vectornav",
        executable="vectornav",
        output="screen",
        parameters=[vectornav_config],
    )

    start_vectornav_sensor_msgs_cmd = Node(
        package="vectornav",
        executable="vn_sensor_msgs",
        output="screen",
        parameters=[vectornav_config],
    )

    return LaunchDescription(
        [
            start_vectornav_cmd,
            start_vectornav_sensor_msgs_cmd,
        ]
    )
