import os
from datetime import datetime
from launch import LaunchDescription
from launch.actions import  ExecuteProcess


def generate_launch_description():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '/point_cloud', '/tf_static',
                 '-o', f'data/bags/lidar_capture_{timestamp}'],
            output='screen'
        )
    ])