import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('status_subscriber')
        self.create_subscription(Float32MultiArray, 'battery_temperature', self.battery_temp_callback, 10)
        self.create_subscription(String, 'health_status', self.health_status_callback, 10)

    def battery_temp_callback(self, msg):
        self.get_logger().info(f'Received battery and temperature: {msg.data}')

    def health_status_callback(self, msg):
        self.get_logger().info(f'Received health status: {msg.data}')

def main(args=None):
    global node
    rclpy.init(args=args)
    node = StatusSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
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