import os
import yaml
from datetime import datetime
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    profile_name = os.environ.get("RECORDING_PROFILE", "full_capture")

    # Load config
    config_file = os.path.join(
        get_package_share_directory("egovel_data_capture"),
        "config",
        "recording",
        "bag_config.yaml",
    )

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    profile = config["recording"]["profiles"][profile_name]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Calculate max bag size in bytes
    max_bag_size_mb = config["recording"]["max_bag_size_mb"]
    max_bag_size_bytes = max_bag_size_mb * 1024 * 1024

    # Get base path from config
    base_path = config["recording"]["base_path"]

    # Group topics by bag_name
    bag_groups = {}
    for topic_info in profile["topics"]:
        bag_name = topic_info["bag_name"]
        if bag_name not in bag_groups:
            bag_groups[bag_name] = []
        bag_groups[bag_name].append(topic_info["topic"])

    # Create separate recording processes for each bag
    recording_processes = []
    for bag_name, topics in bag_groups.items():
        recording_processes.append(
            ExecuteProcess(
                cmd=[
                    "ros2",
                    "bag",
                    "record",
                    *topics,
                    "-o",
                    f"{base_path}/{profile_name}_{timestamp}/{bag_name}_{timestamp}",
                    "--storage",
                    "mcap",
                    "--max-bag-size",
                    str(max_bag_size_bytes),
                ],
                output="screen",
            )
        )

    return LaunchDescription(recording_processes)
