from launch import LaunchDescription
from launch.actions import  IncludeLaunchDescription
from launch.substitutions import  PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Configuration files
    voyant_config = PathJoinSubstitution([
        FindPackageShare('egovel_data_capture'),
        'config', 'sensors', 'voyant_lidar.yaml'
    ])

    return LaunchDescription([
        
        # Include static transforms
        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('egovel_data_capture'),
                'launch', 'static_transforms.launch.py'
            ])
        ),
        
        # Sensor nodes
        Node(
            package='voyant-ros',
            executable='voyant_sensor_node',
            name='voyant_sensor',
            parameters=[voyant_config],
            output='screen'
        ),
        
        
    ])
