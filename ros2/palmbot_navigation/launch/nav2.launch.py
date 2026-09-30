import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import LaunchConfigAsBool

bond_heartbeat_period = 0.25
node_names = [
    'controller_server',
    'planner_server',
    'behavior_server',
    'velocity_smoother',
    'bt_navigator',
]


def generate_launch_description() -> LaunchDescription:
    """Launch the Nav2 stack for autonomous navigation."""
    nav2_params_file = LaunchConfiguration('nav2_params_file')
    autostart = LaunchConfigAsBool('autostart')
    use_respawn = LaunchConfigAsBool('use_respawn')
    use_sim_time = LaunchConfigAsBool('use_sim_time')

    nav2_params_file_w_subst = ParameterFile(
        param_file=nav2_params_file,
        allow_substs=True,
    )

    declare_use_sim_time_argument = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock',
    )
    declare_params_file_argument = DeclareLaunchArgument(
        name='nav2_params_file',
        default_value=os.path.join(
            get_package_share_directory('palmbot_navigation'),
            'config',
            'nav2_params.yaml',
        ),
        description='Full path to the ROS 2 parameters file to use for all launched nodes',
    )
    declare_autostart_argument = DeclareLaunchArgument(
        name='autostart',
        default_value='true',
        description='Automatically startup the Nav2 stack',
    )
    declare_use_respawn_argument = DeclareLaunchArgument(
        name='use_respawn',
        default_value='False',
        description='Whether to respawn if a node crashes. Applied when composition is disabled.',
    )

    nav2_lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[
            {
                'autostart': autostart,
                'node_names': node_names,
                'use_sim_time': use_sim_time,
                'bond_heartbeat_period': bond_heartbeat_period,
            }
        ],
    )
    controller_server_node = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[nav2_params_file_w_subst, {'use_sim_time': use_sim_time}],
        remappings=[('cmd_vel', 'cmd_vel_nav')],
    )
    planner_server_node = Node(
        package='nav2_planner',
        executable='planner_server',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[nav2_params_file_w_subst, {'use_sim_time': use_sim_time}],
    )
    behavior_server_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[nav2_params_file_w_subst, {'use_sim_time': use_sim_time}],
        remappings=[('cmd_vel', 'cmd_vel_nav')],
    )
    velocity_smoother_node = Node(
        package='nav2_velocity_smoother',
        executable='velocity_smoother',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[nav2_params_file_w_subst, {'use_sim_time': use_sim_time}],
        remappings=[
            ('cmd_vel', 'cmd_vel_nav'),
            ('cmd_vel_smoothed', 'cmd_vel'),
        ],
    )
    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        output='screen',
        respawn=use_respawn,
        respawn_delay=2.0,
        parameters=[nav2_params_file_w_subst, {'use_sim_time': use_sim_time}],
    )

    return LaunchDescription(
        [
            declare_use_sim_time_argument,
            declare_params_file_argument,
            declare_autostart_argument,
            declare_use_respawn_argument,
            nav2_lifecycle_manager,
            controller_server_node,
            planner_server_node,
            behavior_server_node,
            bt_navigator_node,
            velocity_smoother_node,
        ]
    )
