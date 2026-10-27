from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    config = PathJoinSubstitution([
        FindPackageShare('carla_monitoring'),
        'config',
        'carla_monitoring.yaml',
    ])

    return LaunchDescription([
        Node(
            package='carla_monitoring',
            executable='carla_monitor_node',
            name='carla_monitor',
            output='screen',
            emulate_tty=True,
            parameters=[config],
        ),
    ])