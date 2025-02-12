import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool
from std_msgs.msg import Float32MultiArray

class CollectionClient(Node):
    def __init__(self):
        super().__init__('collection_client')
        self.cli = self.create_client(SetBool, 'soil_collection')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service to be available...')
        self.get_logger().info("Service available. Ready to send requests.")

    def send_request(self, target_x, target_y):
        # Creating a request to the service
        request = SetBool.Request()
        # Here, using a simple method where `data` contains the success/failure state
        request.data = True  # Example: just confirming that we want to request collection

        # Sending the request
        self.future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result() is not None:
            self.get_logger().info(f"Service response: {self.future.result().message}")
        else:
            self.get_logger().error("Failed to call service")


def main(args=None):
    rclpy.init(args=args)
    node = CollectionClient()
    try:
        # Example targets
        targets = [(1, 0), (2, 0), (3, 0)]
        for x, y in targets:
            node.send_request(x, y)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
