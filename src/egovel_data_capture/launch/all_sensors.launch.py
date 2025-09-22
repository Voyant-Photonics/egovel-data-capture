from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch argument for camera selection and pass it through
    camera_type_arg = DeclareLaunchArgument(
        "camera_type",
        default_value="oakd",
        description="Camera type to use: oakd, realsense",
    )
    camera_type = LaunchConfiguration("camera_type")

    # Include static transforms (foundational - first)
    static_transforms = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "static_transforms.launch.py",
            ]
        )
    )

    # Include camera launch with camera type argument
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

    # Include lidar launch
    lidar_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "lidar.launch.py",
            ]
        )
    )

    # Include GPS launch
    gps_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "gps.launch.py",
            ]
        )
    )

    # Include IMU launch
    imu_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare("egovel_data_capture"),
                "launch",
                "imu.launch.py",
            ]
        )
    )

    return LaunchDescription(
        [
            camera_type_arg,
            static_transforms,
            camera_launch,
            lidar_launch,
            gps_launch,
            imu_launch,
        ]
    )
