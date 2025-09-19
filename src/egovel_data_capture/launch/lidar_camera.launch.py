from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch argument for camera selection and pass it through
    camera_type_arg = DeclareLaunchArgument(
        "camera_type",
        default_value="oakd",
        description="Camera type to use: oakd, realsense",
    )
    camera_type = LaunchConfiguration("camera_type")

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

    # ===============================
    # Define the sensor nodes
    # ===============================
    # Voyant sensor node
    voyant_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "voyant_lidar.yaml",
        ]
    )
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

    # Launch camera, forwarding the camera_type arg
    camera_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "camera.launch.py",
            ]
        ),
        launch_arguments={"camera_type": camera_type}.items(),
    )

    return LaunchDescription(
        [
            camera_type_arg,
            static_transforms,
            voyant_sensor,
            camera_launch,
        ]
    )
