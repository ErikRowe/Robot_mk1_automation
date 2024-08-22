import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray

class JoyToArrayNode(Node):
    def __init__(self):
        super().__init__('robot_movement_node')

        # Initialize variables to store the latest Joy message data
        self.latest_axes = []

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        
        # Publisher for 'int32_array' topic
        self.publisher = self.create_publisher(Int32MultiArray, 'motors_array', 10)

        # Create a timer to publish at regular intervals (e.g., every 0.5 seconds)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.publisher_interval)

        self.get_logger().info('Node has been started.')

    def joy_callback(self, msg):
        # Store joy data
        self.latest_axes = [int(axis * 100) for axis in msg.axes]

    def publisher_interval(self):
        # Convert the Joy message's axes to an Int32MultiArray
        int_array_msg = Int32MultiArray()
        int_array_msg.data = [90, 170, 25, 155, 55,
                            90, 25, 140, 25, 105-10]

        self.publisher.publish(int_array_msg)

def main(args=None):
    rclpy.init(args=args)
    node = JoyToArrayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
