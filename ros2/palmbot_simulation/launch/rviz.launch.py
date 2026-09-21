import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    simulation_pkg_share = get_package_share_directory('palmbot_simulation')
    default_rviz_config_path = os.path.join(
        simulation_pkg_share, 'rviz', 'config.rviz'
    )
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name='rvizconfig',
                default_value=default_rviz_config_path,
                description='Absolute path to rviz config file',
            ),
            rviz_node,
        ]
    )
