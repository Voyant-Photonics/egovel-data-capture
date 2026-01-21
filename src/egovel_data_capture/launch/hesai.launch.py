from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Hesai configuration file path
    hesai_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "hesai.yaml",
        ]
    )

    # Hesai LiDAR node with topic remapping
    hesai_node = Node(
        namespace="hesai_ros_driver",
        package="hesai_ros_driver",
        executable="hesai_ros_driver_node",
        name="hesai_driver",
        parameters=[{"config_path": hesai_config}],
        output="screen",
        remappings=[
            ("/lidar_points", "/hesai/lidar_points"),
            ("/lidar_imu", "/hesai/lidar_imu"),
        ],
    )

    return LaunchDescription([hesai_node])
 