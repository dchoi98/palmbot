import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    description_pkg_share = get_package_share_directory('palmbot_description')
    default_model_path = os.path.join(
        description_pkg_share, "urdf", "palmbot_description.xacro"
    )
    default_rviz_config_path = os.path.join(
        description_pkg_share, "rviz", "config.rviz"
    )
    load_description_path = os.path.join(
        description_pkg_share, "launch", "load_description.launch.py"
    )
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[
            {
                "robot_description": Command(["xacro ", default_model_path]),
                "use_sim_time": use_sim_time,
            }
        ],
    )
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
                name="model",
                default_value=default_model_path,
                description="Absolute path to robot model file",
            ),
            DeclareLaunchArgument(
                name="rvizconfig",
                default_value=default_rviz_config_path,
                description="Absolute path to rviz config file",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(load_description_path)
            ),
            joint_state_publisher_node,
            rviz_node,
        ]
    )