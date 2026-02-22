from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration, EnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # namespace = LaunchConfiguration('namespace')
    # frame_prefix = LaunchConfiguration('frame_prefix')
    # server_uri = LaunchConfiguration('server_uri')
    # use_state = LaunchConfiguration('use_state')
    # use_map = LaunchConfiguration('use_map')


    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='kachaka'),
        DeclareLaunchArgument('frame_prefix', default_value=EnvironmentVariable('FRAME_PREFIX', default_value='')),
        DeclareLaunchArgument('server_uri', default_value='localhost:2021'),
        DeclareLaunchArgument('use_state', default_value='true'),
        DeclareLaunchArgument('use_map', default_value='true'),
        OpaqueFunction(function = launch_create_node),
    ])



def launch_create_node(context, *args, **kwargs):
    namespace = LaunchConfiguration('namespace').perform(context)
    frame_prefix = LaunchConfiguration('frame_prefix').perform(context)
    server_uri = LaunchConfiguration('server_uri').perform(context)
    use_state = LaunchConfiguration('use_state').perform(context)
    use_map = LaunchConfiguration('use_map').perform(context)

    def create_node(name, plugin, params=None, remaps=None):
        return ComposableNode(
            package='kachaka_grpc_ros2_bridge',
            plugin=plugin,
            name=name,
            namespace=namespace,
            parameters=params if params else [],
            remappings=remaps if remaps else [],
            extra_arguments=[{'use_intra_process_comms': False}],
        )

    nodes = [

        create_node("auto_homing",
                    "kachaka::grpc_ros2_bridge::AutoHomingComponent",
                    [{"server_uri": server_uri}]),

        create_node("back_camera",
                    "kachaka::grpc_ros2_bridge::BackCameraComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("diagnostics",
                    "kachaka::grpc_ros2_bridge::DiagnosticsComponent",
                    [{"server_uri": server_uri}]),

        create_node("kachaka_command",
                    "kachaka::grpc_ros2_bridge::KachakaCommandComponent",
                    [{"server_uri": server_uri}]),

        create_node("front_camera",
                    "kachaka::grpc_ros2_bridge::FrontCameraComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("goal_pose",
                    "kachaka::grpc_ros2_bridge::GoalPoseComponent",
                    remaps=[("~/goal_pose", "goal_pose")]),

        create_node("imu",
                    "kachaka::grpc_ros2_bridge::ImuComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("layout",
                    "kachaka::grpc_ros2_bridge::LayoutComponent",
                    [{"server_uri": server_uri}]),

        create_node("lidar",
                    "kachaka::grpc_ros2_bridge::LidarComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("manual_control",
                    "kachaka::grpc_ros2_bridge::ManualControlComponent",
                    [{"server_uri": server_uri}]),
    ]


    if ((use_map == 'True') or (use_map == 'true')):
        nodes += [create_node("mapping",
                    "kachaka::grpc_ros2_bridge::MappingComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}])
                ]


    nodes += [

        create_node("robot_info",
                    "kachaka::grpc_ros2_bridge::RobotInfoComponent",
                    [{"server_uri": server_uri}]),

        create_node("object_detection",
                    "kachaka::grpc_ros2_bridge::ObjectDetectionComponent",
                    [{"server_uri": server_uri}]),

        create_node("odometry",
                    "kachaka::grpc_ros2_bridge::OdometryComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("wheel_odometry",
                    "kachaka::grpc_ros2_bridge::WheelOdometryComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("tof_camera",
                    "kachaka::grpc_ros2_bridge::TofCameraComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("torch",
                    "kachaka::grpc_ros2_bridge::TorchComponent",
                    [{"server_uri": server_uri}]),

        create_node("static_tf",
                    "kachaka::grpc_ros2_bridge::StaticTfComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri}]),

        create_node("dynamic_tf",
                    "kachaka::grpc_ros2_bridge::DynamicTfComponent",
                    [{"frame_prefix": frame_prefix},
                     {"server_uri": server_uri},
                     {"use_map": True if (use_map == 'True' or use_map == 'true') else False}]),
    ]

    container = ComposableNodeContainer(
        name='grpc_ros2_bridge_container',
        namespace=namespace,
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=nodes,
        output='screen'
    )



    if ((use_state == 'True') or (use_state == 'true')):
        return [
            container,
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('kachaka_description'), 
                    'launch', 'robot_description.launch.py')
                ),
                launch_arguments={
                    'namespace': namespace,
                    'frame_prefix': frame_prefix
                }.items()
            )
        ]
    else: 
        return [container]