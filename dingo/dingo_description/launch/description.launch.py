import launch
from launch import action
from launch import actions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    # get necessary addresses
    pkg_share = launch_ros.substitutions.FindPackageShare(package='dingo_description').find('dingo_description')
    default_model_path = os.path.join(pkg_share, 'urdf/dingo.urdf.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
    
    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', LaunchConfiguration('model')])
            }]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )
    spawn_entity = launch_ros.actions.Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        arguments=['-entity', 'dingo',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0',
            '-z', '0.01'
        ],
        output='screen'
    )
    robot_localization_node = launch_ros.actions.Node(
         package='robot_localization',
         executable='ekf_node',
         name='ekf_filter_node',
         output='screen',
         parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )
    
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Use simulation (Gazebo) clock if true'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], output='screen'),

        robot_state_publisher_node,
        spawn_entity
        #robot_localization_node
        #rviz_node
    ])