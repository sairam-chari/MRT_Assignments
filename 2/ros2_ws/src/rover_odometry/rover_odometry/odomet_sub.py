import rclpy
from rclpy.node import Node
from mars_msgs.msg import RoverOdometry
import math

class OdometrySubscriber(Node):
    def __init__(self):
        super().__init__("odometry_subscriber")
        self.subscription = self.create_subscription(RoverOdometry, "rover_odometry", self.listener_callback, 10)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def listener_callback(self, msg):
        self.theta = msg.orientation
        dt = 1  # Assuming 1 second interval
        self.x += msg.linear_velocity.linear.x * math.cos(self.theta) * dt
        self.y += msg.linear_velocity.linear.x * math.sin(self.theta) * dt
        self.get_logger().info(f"Position: ({self.x}, {self.y}), Orientation: {self.theta}, Linear Velocity: {msg.linear_velocity.linear.x}, Angular Velocity: {msg.angular_velocity}")
        if msg.linear_velocity.linear.x > 3:
            self.get_logger().warn("Warning: High linear velocity!")

def main(args=None):
    rclpy.init(args=args)
    node = OdometrySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
