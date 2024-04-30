from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf = get_package_share_directory('my_robot_description') + '/simple_robot.urdf'
    print("-----------------URDF file path:-------------------------------=================================", urdf)  # Print the URDF file path

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': urdf}],
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'my_robot', '-file', urdf, '-x', '0', '-y', '0', '-z', '0'],
            name='spawn_entity',
            output='screen',
        ),
        Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d',"/home/aksoni/Documents/projects/ros2/rviz_all.rviz"]
    )
    ])
