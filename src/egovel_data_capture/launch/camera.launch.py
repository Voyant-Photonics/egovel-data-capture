from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    EqualsSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch argument for camera selection
    camera_type_arg = DeclareLaunchArgument(
        "camera_type",
        default_value="oakd",
        description="Camera type to use: oakd, realsense",
    )

    # Get launch configuration
    camera_type = LaunchConfiguration("camera_type")

    # Configuration files
    oakd_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "depthai_camera.yaml",
        ]
    )

    realsense_config = PathJoinSubstitution(
        [
            FindPackageShare("egovel_data_capture"),
            "config",
            "sensors",
            "realsense_camera.yaml",
        ]
    )

    # OAK-D camera node (conditional)
    oakd_camera_node = Node(
        package="depthai_ros_driver",
        executable="camera_node",
        name="camera",
        parameters=[oakd_config],
        output="screen",
        condition=IfCondition(EqualsSubstitution(camera_type, "oakd")),
    )

    # RealSense camera node (conditional) with topics remapped to match OAK-D
    realsense_camera_node = Node(
        package="realsense2_camera",
        executable="realsense2_camera_node",
        name="camera",
        parameters=[realsense_config],
        output="screen",
        condition=IfCondition(EqualsSubstitution(camera_type, "realsense")),
        remappings=[
            # RGB camera remapping (RealSense color -> standard RGB)
            (
                "/camera/camera/color/image_raw/compressed",
                "/camera/rgb/image_raw/compressed",
            ),
            ("/camera/camera/color/camera_info", "/camera/rgb/camera_info"),
            # Stereo cameras remapping (RealSense infrared -> standard left/right)
            (
                "/camera/camera/infra1/image_rect_raw/compressed",
                "/camera/left/image_raw/compressed",
            ),
            (
                "/camera/camera/infra2/image_rect_raw/compressed",
                "/camera/right/image_raw/compressed",
            ),
            ("/camera/camera/infra1/camera_info", "/camera/left/camera_info"),
            ("/camera/camera/infra2/camera_info", "/camera/right/camera_info"),
        ],
    )

    return LaunchDescription(
        [
            camera_type_arg,
            oakd_camera_node,
            realsense_camera_node,
        ]
    )
