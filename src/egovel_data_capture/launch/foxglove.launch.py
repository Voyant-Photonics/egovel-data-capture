from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    # Launch arg to control where to open Foxglove: 'desktop' or 'web'
    open_in_arg = DeclareLaunchArgument(
        'open_in',
        default_value='desktop',
        description="Where to open Foxglove: 'desktop' (foxglove-studio app) or 'web' (browser)",
    )

    foxglove_bridge = Node(
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
    )

    # Deep link base that connects to local foxglove-websocket (from foxglove_bridge)
    # Note: ds.url is intentionally not URL-encoded; Foxglove handles this form too.
    deep_link_base = "https://app.foxglove.dev/~/view?ds=foxglove-websocket&ds.url=ws://localhost:8765"
    app_deep_link_base = "foxglove://open?ds=foxglove-websocket&ds.url=ws://localhost:8765"

    # Open in Foxglove desktop app
    foxglove_desktop = ExecuteProcess(
        cmd=[
            "foxglove-studio",
            PythonExpression([f"'{app_deep_link_base}'"]),
        ],
        condition=IfCondition(PythonExpression(
            ["'", LaunchConfiguration('open_in'), "' == 'desktop'"])),
    )

    # Open in default web browser
    foxglove_web = ExecuteProcess(
        cmd=[
            "xdg-open",
            PythonExpression([f"'{deep_link_base}'"]),
        ],
        condition=IfCondition(PythonExpression(
            ["'", LaunchConfiguration('open_in'), "' == 'web'"])),
    )

    return LaunchDescription([
        open_in_arg,
        foxglove_bridge,
        foxglove_desktop,
        foxglove_web,
    ])
