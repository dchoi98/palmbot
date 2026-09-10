import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    description_pkg_share = get_package_share_directory('palmbot_description')
    sim_package_share = get_package_share_directory('palmbot_simulation')
    bridge_config_path = os.path.join(sim_package_share, 'config', 'gz_bridge.yaml')
    world_path = os.path.join(sim_package_share, 'worlds', 'my_world.sdf')

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("ros_gz_sim"), "launch"
                ),
                "/gz_sim.launch.py",
            ]
        ),
        launch_arguments={
            "gz_args": ["-v 4 ", world_path]
        }.items(),
    )

    load_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(description_pkg_share, "launch", "load_description_launch.py")
        )
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'palmbot'
        ]
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        parameters=[{
            'config_file': bridge_config_path
        }]
    )

    return LaunchDescription([
        launch_gazebo,
        load_description,
        spawn_robot,
        gz_bridge_node
    ])