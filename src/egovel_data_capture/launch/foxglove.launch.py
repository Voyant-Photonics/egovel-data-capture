from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    foxglove_bridge = (
        Node(
            package="foxglove_bridge",
            executable="foxglove_bridge",
            name="foxglove_bridge",
            parameters=[
                {
                    "port": 8765,
                    "address": "0.0.0.0",
                    "tls": False,
                    "topic_whitelist": [".*"],  # Allow all topics
                    "send_buffer_limit": 10000000,
                    "use_compression": True,
                }
            ],
            output="screen",
        ),
    )
    return LaunchDescription([foxglove_bridge])
