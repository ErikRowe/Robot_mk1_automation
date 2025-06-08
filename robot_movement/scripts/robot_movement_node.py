import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState
from std_msgs.msg import Int32MultiArray
from robot_movement.joint_state import JointStateClass


class RobotMovementNode(Node):
    def __init__(self):
        super().__init__('robot_movement_node')

        # Initialize variables to store the latest Joy message data
        self.latest_axes = []

        self.joint_states_class = JointStateClass()

        #
        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        #
        self.joint_publisher = self.create_publisher(JointState, 'joint_states', 10)
        
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
        self.join_state_message()

    def join_state_message(self):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_states_class.joint_names
        joint_state.position = self.joint_states_class.update_joint_positions([90,177,40,90,50,
                                                                                100,15,115,70,110])
        self.joint_publisher.publish(joint_state)

def main(args=None):
    rclpy.init(args=args)
    node = RobotMovementNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
