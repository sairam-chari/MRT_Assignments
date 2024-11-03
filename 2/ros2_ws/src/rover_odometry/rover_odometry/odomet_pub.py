import rclpy
from rclpy.node import Node
from mars_msgs.msg import RoverOdometry
from geometry_msgs.msg import Twist
import random

class OdometryPublisher(Node):
    def __init__(self):
        super().__init__("odometry_publisher")
        self.publisher_ = self.create_publisher(RoverOdometry, "rover_odometry", 10)
        self.timer = self.create_timer(1.0, self.publish_odometry)
        self.orientation = 0.0

    def publish_odometry(self):
        msg = RoverOdometry()
        msg.rover_id = 0
        msg.orientation = self.orientation
        msg.linear_velocity = Twist()
        msg.linear_velocity.linear.x = random.uniform(0, 5)
        msg.angular_velocity = random.uniform(-1, 1)
        self.publisher_.publish(msg)
        self.orientation += 0.05

def main(args=None):
    global node
    rclpy.init(args=args)
    node = OdometryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
