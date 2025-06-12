import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TimerBasedObstacleMover(Node):
    def __init__(self):
        super().__init__('timer_based_obstacle_mover')
        
        # 두 개의 장애물 cmd_vel 퍼블리셔 생성
        self.ob1_pub = self.create_publisher(Twist, '/ob1/cmd_vel', 10)
        self.ob2_pub = self.create_publisher(Twist, '/ob2/cmd_vel', 10)
        
        # 타이머 설정 (5초마다 움직임 전환)
        self.timer = self.create_timer(7.0, self.timer_callback)
        
        # 현재 방향 (1: 전진, -1: 후진)
        self.direction = 1
    
    def timer_callback(self):
        # Twist 메시지 생성
        ob1_twist = Twist()
        ob2_twist = Twist()
        
        if self.direction == -1:
            ob1_twist.linear.x = 1.0  # ob1 전진
            ob2_twist.linear.x = -2.5  # ob2 후진
        else:
            ob1_twist.linear.x = -2.5  # ob1 후진
            ob2_twist.linear.x = 1.0  # ob2 전진
        
        ob1_twist.angular.z = 0.0  # 조향은 직진
        ob2_twist.angular.z = 0.0  # 조향은 직진
        
        # 메시지 퍼블리시
        self.ob1_pub.publish(ob1_twist)
        self.ob2_pub.publish(ob2_twist)
        
        self.get_logger().info(f'Published velocities - ob1: {ob1_twist.linear.x} m/s, ob2: {ob2_twist.linear.x} m/s')
        
        # 방향 반전
        self.direction *= -1


def main(args=None):
    rclpy.init(args=args)
    node = TimerBasedObstacleMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()