# egovel-data-capture

A ROS repo for capturing the data streams required of the Ego Velocity / Super Resolution project

## Setup

### Clone the repo

```bash
# Clone the repo with submodules
git clone --recurse-submodules https://github.com/Voyant-Photonics/egovel-data-capture.git
```

If ever new submodules are added or existing submodules are updated, run:

```bash
# Update submodules
git submodule update --init --recursive
```

### Depthai UDEV rules

These are required to connect to Luxonis OAK cameras over USB.

```bash
# Download and install the udev rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Manual Setup

> NOTE: This is a WIP. Start dumping dependencies here.

#### ROS2 Humble

Follow the [ROS2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

#### `ros-humble-voyant-ros`

##### Dep: Cap'n Proto v1.1.0

Install Cap'n Proto from source following the **Installation: Unix** > **From Release Tarball** instructions
found at [Cap'n Proto](https://capnproto.org/install.html).

> At the time of writing, these instructions were:
>
> ```bash
> curl -O https://capnproto.org/capnproto-c++-1.1.0.tar.gz
> tar zxf capnproto-c++-1.1.0.tar.gz
> cd capnproto-c++-1.1.0
> ./configure
> make -j6 check
> sudo make install
> ```

See also:
[Cap'n Proto install](https://capnproto.org/install.html)

##### Dep: `voyant-api` & `voyant-api-dev`

Download `voyant-api` & `voyant-api-dev` packages from
[voyant-sdk/releases/latest](https://github.com/Voyant-Photonics/voyant-sdk/releases/latest)
and place them in a `debs/` dir in your relative path.

> For more info see official [Voyant SDK Installation Guide](https://voyant-photonics.github.io/02_getting-started/installation.html#option-1-native-installation-recommended)

#### Install

Download `ros-humble-voyant-ros` package from
[voyant-ros/releases/latest](https://github.com/Voyant-Photonics/voyant-ros/releases/latest)
and place it in a `debs/` dir in your relative path.

```bash
sudo apt update
sudo apt install -y ./debs/voyant-api*.deb
sudo apt install -y ./debs/ros-humble-voyant-ros*.deb
```

#### Intel realsense-ros

> ⚠️ If you are only using a Luxonis OAK-D camera, then you can skip this section!

Follow the latest `realsense-ros` installation instructions for ROS2 found at:
https://github.com/IntelRealSense/realsense-ros

> At the time of writing this involves a few steps,
> including installing their native drivers before installing the ros packages.
>
> They provide a few different options, but it is recommended to use the simplest (typically Option 1 for each step).
> There is probably no reason to install from source.
>
> If you try to go direct with `sudo apt install ros-humble-realsense2-*`, you may experience some issues.

#### Other ROS2 deps

```bash
sudo apt install -y ros-humble-foxglove-bridge  # for visualization
sudo apt install -y ros-humble-foxglove-msgs   # for visualization
sudo apt install -y ros-humble-depthai-ros     # for OAK-D camera
sudo apt install -y ros-humble-rtcm-msgs       # for GPS
sudo apt install -y ros-humble-nmea-msgs       # for GPS
```

#### Other deps

Install `asio`; required for `ublox` node.

```bash
sudo apt install -y libasio-dev
```

### Docker setup

Build:

```bash
docker build -t voyant-egovel-container .
```

Run:

```bash
docker run -it --rm \
    --network host \
    --name voyant_egovel_container \
    -v $(pwd):/workspace/ros2_ws \
    -v $(pwd)/debs:/debs \
    voyant-egovel-container
```

> TEMPORARY UNTIL THIS IS HOSTED AND BUILT INTO DOCKER CONTAINER
>
> Requires: `debs/ros-humble-voyant-ros_0.2.1-0jammy_amd64.deb` exists in repo root
>
> ```bash
> apt update && apt install -y /debs/ros-humble-voyant-ros*.deb
> ```

Exec in (access running container):

```bash
docker exec -it voyant_egovel_container bash
```

## Build and run [WIP]

```bash
source /opt/ros/humble/setup.bash
colcon build # Optionally, use --parallel-workers $(nproc) to speed up build
```

**Terminal 1:** Start the sensors

```bash
source install/setup.bash
ros2 launch egovel_data_capture lidar_camera.launch.py
```

By default, this uses the `oakd` camera. You can switch to `realsense` with:

```bash
ros2 launch egovel_data_capture lidar_camera.launch.py camera_type:=realsense
```

Start the GPS Node. The RTK corrections are provided through a NTRIP connection with [`NYSNET`](https://cors.dot.ny.gov/sbc/Account/Index?returnUrl=%2Fsbc) VRS on `/rtcm` topic.

```bash
source install/setup.bash
ros2 launch egovel_data_capture gps.launch.py
```

The GPS sensor and NTRIP client can be configured in [`gps.yaml`](./src/egovel_data_capture/config/sensors/gps.yaml).

**Terminal 2:** Visualize the data streams

```bash
source install/setup.bash
ros2 launch egovel_data_capture foxglove.launch.py open_in:=web # or open_in:=desktop default is desktop
```

Then load [`egovel_data_view.json`](./src/egovel_data_capture/config/visualization/egovel_data_view.json)

**Terminal 3:** Log the data

```bash
source install/setup.bash
ros2 launch egovel_data_capture recording.launch.py
```

This will use the `full_capture` recording profile in
[`bag_config.yaml`](./src/egovel_data_capture/config/recording/bag_config.yaml)
as the default.

To select a different profile, specify the `RECORDING_PROFILE` environment variable:

```bash
RECORDING_PROFILE=lidar_only ros2 launch egovel_data_capture recording.launch.py
```

### Playback

The recording system writes sensor data to separate bag files in parallel to optimize I/O performance.
Use `ros2 bag convert` to merge specific bags into a single file for playback when needed.

**For example:**

Create a file called `merge_config.yaml` with contents like:

```bash
output_bags:
  - uri: data/bags/merged_full_capture_20250912_160110
    storage_id: mcap
    all: true
```

Run `ros2 bag convert` command with desired inputs:

```bash
ros2 bag convert \
    --input data/bags/full_capture_20250912_160110/lidar_20250912_160110 \
    --input data/bags/full_capture_20250912_160110/metadata_20250912_160110 \
    --input data/bags/full_capture_20250912_160110/navigation_20250912_160110 \
    --input data/bags/full_capture_20250912_160110/rgb_camera_20250912_160110 \
    --input data/bags/full_capture_20250912_160110/stereo_cameras_20250912_160110 \
    --output merge_config.yaml
```

Playback the merged bag file with `ros2 bag play`:

```bash
ros2 bag play data/bags/merged_full_capture_20250912_160110/
```

> You *may* also be able to play this file back directly in foxglove.
