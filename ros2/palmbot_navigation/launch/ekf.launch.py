import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
import launch_ros.actions


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription(
        [
            launch_ros.actions.Node(
                package='robot_localization',
                executable='ekf_node',
                name='ekf_filter_node',
                output='screen',
                parameters=[
                    os.path.join(
                        get_package_share_directory('palmbot_navigation'),
                        'config',
                        'ekf.yaml',
                    ),
                    {'use_sim_time': use_sim_time}
                ],
            ),
        ]
    )
