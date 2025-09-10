FROM ros:humble-ros-base-jammy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    apt-utils \
    build-essential \
    cmake \
    curl \
    g++ \
    pkg-config \
    jq \
    wget \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Install Cap'n Proto from source
WORKDIR /tmp
RUN curl -O https://capnproto.org/capnproto-c++-1.1.0.tar.gz && \
    tar zxf capnproto-c++-1.1.0.tar.gz && \
    cd capnproto-c++-1.1.0 && \
    ./configure && \
    make -j$(nproc) check && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf capnproto-c++-1.1.0*

# Create workspace directories
WORKDIR /workspace
RUN mkdir -p debs src

# Download and install Voyant SDK packages
RUN LATEST_RELEASE_URL=$(curl -s https://api.github.com/repos/Voyant-Photonics/voyant-sdk/releases/latest | jq -r '.assets[].browser_download_url') && \
    for url in $LATEST_RELEASE_URL; do \
        wget -P ./debs/ $url; \
    done && \
    apt-get update && \
    apt-get install -y ./debs/voyant-api*.deb && \
    rm -rf /var/lib/apt/lists/*

# # Download and install Voyant ROS packages
# RUN VOYANT_ROS_RELEASE_URL=$(curl -s https://api.github.com/repos/Voyant-Photonics/voyant-ros/releases/latest | jq -r '.assets[].browser_download_url') && \
#     for url in $VOYANT_ROS_RELEASE_URL; do \
#         wget -P ./debs/ $url; \
#     done && \
#     apt-get update && \
#     apt-get install -y ./debs/ros-humble-voyant-ros*.deb && \
#     rm -rf /var/lib/apt/lists/*

# Install additional ROS2 dependencies
RUN apt-get update && \
    apt-get install -y \
    ros-humble-foxglove-bridge \
    ros-humble-foxglove-msgs \
    ros-humble-depthai-ros \
    && rm -rf /var/lib/apt/lists/*

# Source ROS2 setup in bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Create a ROS2 workspace
RUN mkdir -p /workspace/ros2_ws/src
WORKDIR /workspace/ros2_ws

# Set up entrypoint to source ROS2
# Create entrypoint script using RUN and echo
RUN echo '#!/bin/bash' > /ros_entrypoint.sh && \
    echo 'set -e' >> /ros_entrypoint.sh && \
    echo '' >> /ros_entrypoint.sh && \
    echo '# setup ros2 environment' >> /ros_entrypoint.sh && \
    echo 'source "/opt/ros/$ROS_DISTRO/setup.bash" --' >> /ros_entrypoint.sh && \
    echo 'exec "$@"' >> /ros_entrypoint.sh && \
    chmod +x /ros_entrypoint.sh

# Clean up debs directory
RUN rm -rf /workspace/debs

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]