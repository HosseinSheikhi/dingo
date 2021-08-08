#! /usr/bin/env python3

# Author: Hossein S.D <hsa150@sfu.ca>


import os

from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
import launch_ros

def generate_launch_description():
    DINGO_MODEL = os.environ['DINGO_MODEL'] #d - o
    dingo_urdf_file_name = 'dingo-' + DINGO_MODEL + '.urdf.xacro'
    dingo_urdf_file_address = os.path.join(get_package_share_directory('dingo_gazebo'),'urdf',dingo_urdf_file_name)

     # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')

     # Declare the launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    robot_state_publisher_node = launch_ros.actions.Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    output='screen',
    parameters=[{
        'use_sim_time': use_sim_time,
        'robot_description': Command(['xacro ', dingo_urdf_file_address])
        }]
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Use simulation (Gazebo) clock if true'),
        robot_state_publisher_node
    ])