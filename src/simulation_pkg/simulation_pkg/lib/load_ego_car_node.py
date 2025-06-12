import rclpy
from rclpy.node import Node
from simulation_pkg import basic


class EgoCarLoader(Node):
    def __init__(self):
        super().__init__('ego_car_loader')
        
        # 4초 후에 한 번만 실행되는 타이머 생성
        self.timer = self.create_timer(4.5, self.load_model_callback)
        
    def load_model_callback(self):
        self.get_logger().info('Loading Prius Hybrid after 2 secs')
        basic.load_model("ego_vehicle", "prius_hybrid", basic.driving_ego())
        self.timer.cancel()  
def main():
    rclpy.init()
    ego_car_loader = EgoCarLoader()
    
    try:
        rclpy.spin(ego_car_loader)
    except KeyboardInterrupt:
        pass
    finally:
        ego_car_loader.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
