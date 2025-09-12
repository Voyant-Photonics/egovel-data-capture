# egovel-data-capture

A ROS repo for capturing the data streams required of the Ego Velocity / Super Resolution project

## Docker setup

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

## Manual Setup

> NOTE: This is a WIP. Start dumping dependencies here.

### ROS2 Humble

Follow the [ROS2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

### `ros-humble-voyant-ros`

#### Dep: Cap'n Proto v1.1.0

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

#### Dep: `voyant-api` & `voyant-api-dev`

Download `voyant-api` & `voyant-api-dev` packages from
[voyant-sdk/releases/latest](https://github.com/Voyant-Photonics/voyant-sdk/releases/latest).

> For more info see official [Voyant SDK Installation Guide](https://voyant-photonics.github.io/02_getting-started/installation.html#option-1-native-installation-recommended)

### Install

Download `ros-humble-voyant-ros` package from
[voyant-ros/releases/latest](https://github.com/Voyant-Photonics/voyant-ros/releases/latest).

```bash
sudo apt update
sudo apt install -y /workspace/debs/voyant-api*.deb
sudo apt install -y /workspace/debs/ros-humble-voyant-ros*.deb
```

### Other ROS2 deps

```bash
sudo apt install -y ros-humble-foxglove-* # for visualization
sudo apt install -y ros-humble-depthai-ros # for OAK-D camera
```
