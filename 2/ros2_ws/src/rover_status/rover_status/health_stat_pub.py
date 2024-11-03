import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray

class HealthStatusPublisher(Node):
    def __init__(self):
        super().__init__("health_status_publisher")
        self.publisher_ = self.create_publisher(String, "health_status", 10)
        self.subscription = self.create_subscription(Float32MultiArray, "battery_temperature", self.listener_callback, 10)

    def listener_callback(self, msg):
        battery_level = msg.data[0]
        status = "Healthy" if battery_level > 40 else "Warning" if battery_level > 15 else "Critical"
        status_msg = String()
        status_msg.data = status
        self.publisher_.publish(status_msg)
        self.get_logger().info(f"Battery: {battery_level}, Health Status: {status}")

def main(args=None):
    global node
    rclpy.init(args=args)
    node = HealthStatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

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