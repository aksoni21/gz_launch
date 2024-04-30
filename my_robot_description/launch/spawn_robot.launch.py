import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    #urdf = get_package_share_directory('my_robot_description') + '/urdf/simple_robot.urdf'
    urdf = os.path.join(get_package_share_directory('my_robot_description') , 'urdf','simple_robot.urdf')
    print("-----------------URDF file path:---=================================", urdf)  # Print the URDF file path
    #Environment Variable
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(get_package_prefix("my_robot_description"), "share")

    # gazebo = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory("gazebo_ros"),"launch","gazebo.launch.py")
    #     )
    # )

    start_gazebo_server_cmd = ExecuteProcess(
       cmd=[
            'gzserver',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            
        ],        
        output='screen',
    )
    start_gazebo_client_cmd = ExecuteProcess(
        cmd=[
            'gzclient',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            
        ],
        output='screen',
    )

    robot_description = {'robot_description': open(urdf).read()}

    #gazebo needs spawn node, server and client(gui) node
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description],
        ),
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'my_robot', '-topic',"robot_description"],
            name='spawn_entity',
            output='screen',
        )
    ])
