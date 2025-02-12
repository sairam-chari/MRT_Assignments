
cmake_minimum_required(VERSION 3.5)
project(rover_status)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Install Python packages
install(
  DIRECTORY
    scripts
  DESTINATION share/${PROJECT_NAME}
)

# Declare the package for ament
ament_package()
