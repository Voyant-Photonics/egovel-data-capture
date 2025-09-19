from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
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

    # Include vectornav launch file
    vectornav_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("vectornav"),
                "launch",
                "vectornav.launch.py",
            ]
        ),
        launch_arguments={
            "config_file": vectornav_config,
        }.items(),
    )

    return LaunchDescription([vectornav_launch])
