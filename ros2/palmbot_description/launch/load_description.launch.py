import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    description_pkg_share = get_package_share_directory('palmbot_description')
    default_model_path = os.path.join(
        description_pkg_share, 'urdf', 'palmbot_description.xacro'
    )
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': Command(
                    ['xacro ', LaunchConfiguration('model')]
                ),
                'use_sim_time': use_sim_time,
            }
        ],
    )
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[
            {
                'robot_description': Command(['xacro ', default_model_path]),
                'use_sim_time': use_sim_time,
            }
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name='model',
                default_value=default_model_path,
                description='Absolute path to robot model file',
            ),
            robot_state_publisher_node,
            joint_state_publisher_node,
        ]
    )
