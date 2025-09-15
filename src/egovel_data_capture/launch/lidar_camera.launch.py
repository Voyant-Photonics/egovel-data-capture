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
    camera_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "depthai_camera.yaml",
        ]
    )

    # Include static transforms
    static_transforms = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "static_transforms.launch.py",
            ]
        )
    )

    # Sensor nodes
    voyant_sensor = Node(
        package="voyant-ros",
        executable="voyant_sensor_node",
        name="voyant_sensor",
        parameters=[voyant_config],
        remappings=[
            ("/point_cloud", "/voyant/point_cloud")
        ],  # TODO: Remove when this is inherent to ROS node
        output="screen",
    )

    camera_node = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="camera",
        parameters=[camera_config],
        remappings=[
            ("/camera/imu/data", "/imu/data")
        ],  # TODO: Remove when we add VN-200 node
        output="screen",
    )

    return LaunchDescription([static_transforms, voyant_sensor, camera_node])
