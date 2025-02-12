from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'grid_x',
            default_value='10',
            description='Number of columns in the obstacle grid',
        ),
        DeclareLaunchArgument(
            'grid_y',
            default_value='10',
            description='Number of rows in the obstacle grid',
        ),
        DeclareLaunchArgument(
            'grid_string',
            default_value='0000010000100010000010000100001000010001000000010000100010000',
            description='Flattened binary grid representing obstacles',
        ),
        DeclareLaunchArgument(
            'start_x',
            default_value='0',
            description='Starting x-coordinate of the rover',
        ),
        DeclareLaunchArgument(
            'start_y',
            default_value='0',
            description='Starting y-coordinate of the rover',
        ),
        DeclareLaunchArgument(
            'goal_x',
            default_value='9',
            description='Goal x-coordinate of the rover',
        ),
        DeclareLaunchArgument(
            'goal_y',
            default_value='9',
            description='Goal y-coordinate of the rover',
        ),

        Node(
            package='walle', 
            executable='rover_navigation',  
            parameters=[{
                'grid_x': LaunchConfiguration('grid_x'),
                'grid_y': LaunchConfiguration('grid_y'),
                'grid_string': LaunchConfiguration('grid_string'),
            }],
            output='screen',
        ),

        
        Node(
            package='walle',  
            executable='obstacle_avoidance',  
            name='obstacle_avoidance',
            parameters=[{
                'start_x': LaunchConfiguration('start_x'),
                'start_y': LaunchConfiguration('start_y'),
                'goal_x': LaunchConfiguration('goal_x'),
                'goal_y': LaunchConfiguration('goal_y'),
            }],
            output='screen',
        ),
    ])
