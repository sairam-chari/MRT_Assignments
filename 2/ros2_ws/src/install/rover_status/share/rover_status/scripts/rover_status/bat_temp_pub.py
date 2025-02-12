import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import random

class battemppub(Node):
    def __init__(self):
        super().__init__("battery_temperature_publisher")
        self.publisher_ = self.create_publisher(Float32MultiArray, "battery_temperature", 10)
        self.timer = self.create_timer(1.0, self.publish_values)

    def publish_values(self):
        msg = Float32MultiArray()
        msg.data = [random.uniform(0, 100), random.uniform(-20, 80)]
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

def main(args=None):
    global node
    rclpy.init(args=args)
    node = battemppub()
    rclpy.spin(node)
    #node.destroy_node()
    #rclpy.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except:
            pass
