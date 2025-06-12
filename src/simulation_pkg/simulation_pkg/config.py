import torch
import numpy as np
from simulation_pkg import *


class Config: # 자주 바뀌는 항목들
    
    # "driving", "mission", "parking"
    MODE = "driving"  

    # 시뮬레이션 모델 파일(자동으로 기본 모델 파일이 다운로드됨)
    MODEL_NAME = "sim.pt"
    #MODEL_NAME = "yolov8m-ep200-unf-d4 (사본).pt"
    
    # 모델에서 추론할 2차선 class의 이름
    LANE2_CLASS_NAME = "lane2" # lane2 rrline
    
    # 주행 관련 설정
    SPEED = 50    # 속도
    MAX_SPEED = 5  # 최대 속도 (m/s)

    # 디버깅 관련 설정
    DEBUG_SETTINGS = {
        "raw_image_show": True,
        "debugging_image_show": False,  # 이미지 안 띄우려면 False / True
        "lane_info_image_show": True,  # edge, bev, roi 이미지 확인할지 말지
        "traffic_image_show": False
    }
    
    # LIDAR 설정 (모드에 따라 동적으로 바뀌는 부분)
    LIDAR_SETTINGS = {
        "driving": {
            "lidar_start_angle": 0,  # 원하는 각도 범위의 시작 값
            "lidar_end_angle": 30,   # 원하는 각도 범위의 끝 값
            "lidar_range_min": 1.0,  # 원하는 거리 범위의 최소값 [m]
            "lidar_range_max": 12.0  # 원하는 거리 범위의 최대값 [m]
        },
        "mission": {
            "lidar_start_angle": 0,
            "lidar_end_angle": 30,
            "lidar_range_min": 1.0,
            "lidar_range_max": 12.0
        },
        "parking": {
            "lidar_start_angle": 0,
            "lidar_end_angle": 30,
            "lidar_range_min": 1.0,
            "lidar_range_max": 12.0
        }
    }
    
    # 차량 제어 관련 설정
    VEHICLE_CONTROL_SETTINGS = {
        "driving": {
            "steering": -1,   # 좌/우로 움직이는지 확인, 반대로 동작하면 -1
            "direction": 1   # 앞/뒤로 움직이는지 확인, 반대로 동작하면 -1
        },
        "mission": {
            "steering": 1,   
            "direction": 1 
        },
        "parking": {
            "steering": -1,
            "direction": 1
        }
        
    }
    
    @classmethod
    def get_lidar_settings(cls):
        return cls.LIDAR_SETTINGS.get(cls.MODE, cls.LIDAR_SETTINGS["driving"])
    
    @classmethod
    def get_vehicle_control_settings(cls):
        return cls.VEHICLE_CONTROL_SETTINGS.get(cls.MODE, cls.VEHICLE_CONTROL_SETTINGS["driving"])

    @classmethod
    def get_debug_setting(cls, setting_name):
        return cls.DEBUG_SETTINGS.get(setting_name, False)

    
# 카메라 설정
REAL_CAM = "image_raw"               # 실제 차량 이미지 
#SIM_CAM = "/camera/image_raw"        # 시뮬 전방 이미지
SIM_CAM = "image_raw"
SIM_CAM2 = "/rear_camera/image_raw"  # 시뮬 후방 이미지 camera_back
SIM_CAM3 = "/top_camera/image_raw"   # 시뮬 위성 이미지

# lib 기본 제공 함수
camera_perception_func_lib = get_pyc("camera_perception_func_lib.cpython-310.pyc")
#lidar_perception_func_lib = get_pyc("lidar_perception_func_lib.cpython-310.pyc")
decision_making_func_lib = get_pyc("decision_making_func_lib.cpython-310.pyc")
#convert_arduino_msg = get_pyc("convert_protocol_lib.cpython-310.pyc")
#control_motor = get_pyc("control_motor_lib.cpython-310.pyc")


class Yolov8Settings:
    PT_PATH = basic.get_data(file_name=Config.MODEL_NAME)
    basic.check_and_download_model(Config.MODEL_NAME, PT_PATH)
    
    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    # Confidence score가 THRESHOLD 값을 넘었을때 마스킹 이미지에 표시하도록 설정
    THRESHOLD = 0.7
    
    RAW_IMAGE = SIM_CAM
    
    # yolov8_node
    DETECTIONS_TOPIC = "detections" # 추론 결과 토픽 이름
    
    # debug_node
    DEBUG_IMAGE_TOPIC = "yolov8_visualized_img" # 디버깅 이미지 토픽 이름


class LaneInfoExtractorSettings:
    
    DETECTIONS_TOPIC = Yolov8Settings.DETECTIONS_TOPIC
    LANE2_CLASS_NAME = Config.LANE2_CLASS_NAME
    
    SUB_IMAGE = SIM_CAM
    SUB_IMAGE2 = SIM_CAM2
    
    LANE_INFO_IMAGE_SHOW = Config.get_debug_setting("lane_info_image_show")
    
    # 추출한 정보 보낼 토픽 이름
    LANE_INFO_TOPIC = "yolov8_lane_info"


class TrafficLightDetectorSettings:
    
    SUB_IMAGE = SIM_CAM
    DETECTIONS_TOPIC = Yolov8Settings.DETECTIONS_TOPIC
    
    # 모델에서 추론할 class의 이름
    TRAFFIC_CLASS_NAME = "traffic_light"
    
    HSV_RANGES = {
        'red1': (np.array([0, 100, 100]), np.array([10, 255, 255])),
        'red2': (np.array([160, 100, 100]), np.array([179, 255, 255])),
        'yellow': (np.array([20, 100, 100]), np.array([30, 255, 255])),
        'green': (np.array([40, 100, 100]), np.array([90, 255, 255]))
    }
    
    # 신호등의 색상 정보가 넘어가는 토픽
    TRAFFIC_INFO_TOPIC = "yolov8_traffic_light_info"
    
    SHOW_IMAGE = Config.get_debug_setting("traffic_image_show")


class LidarObstacleDetectorSettings:
    
    # 시뮬레이션 LIDAR 토픽
    RAW_LIDAR_TOPIC = "scan"
    
    # 라이다 데이터 전처리 처리 후 토픽
    LIDAR_PREPROC_TOPIC = "lidar_processed"
    
    # 물체 감지 여부를 퍼블리시할 토픽 이름
    LIDAR_OBSTACLE_INFO_TOPIC = "lidar_obstacle_info"
    
    # 동적으로 변경되는 LIDAR 설정
    LIDAR_SETTINGS = Config.get_lidar_settings()
    START_ANGLE = LIDAR_SETTINGS["lidar_start_angle"]
    END_ANGLE = LIDAR_SETTINGS["lidar_end_angle"]
    MIN_RANGE = LIDAR_SETTINGS["lidar_range_min"]
    MAX_RANGE = LIDAR_SETTINGS["lidar_range_max"]
    
    # 연속적으로 몇 번 감지 여부를 확인할지 설정
    STABLE_DETECTED = 5


class MotionPlannerSettings:
    # motion_planner_setting
    
    SUB_DETECTION_TOPIC_NAME = Yolov8Settings.DETECTIONS_TOPIC
    SUB_LANE_TOPIC_NAME = LaneInfoExtractorSettings.LANE_INFO_TOPIC
    SUB_TRAFFIC_LIGHT_TOPIC_NAME = TrafficLightDetectorSettings.TRAFFIC_INFO_TOPIC
    SUB_LIDAR_OBSTACLE_TOPIC_NAME = LidarObstacleDetectorSettings.LIDAR_OBSTACLE_INFO_TOPIC
    
    #MOTION_PLANNER_TOPIC = "motion_planner_signal"
    MOTION_PLANNER_TOPIC = "topic_control_signal"
    

    # 모션 플랜 발행 주기 (초) - 소수점 필요 (int형은 반영되지 않음)
    TIMER = 0.01
    
    QoS_Depth = 3
    
    SPEED = Config.SPEED
    
    # 속도가 급격하게 변하여 모터 고장 방지(클수록 더욱 부드럽게 속도 변화)
    SPEED_CHANGE_SMOOTHNESS = 30


class SimulationSenderSettings:
    # simulation_sender_node
    
    MOTION_PLANNER_TOPIC = MotionPlannerSettings.MOTION_PLANNER_TOPIC
    GAZEBO_CONTROL_TOPIC = "/cmd_vel"
    
    # 주차는 전부 양수/ 주행은 +-
    VEHICLE_SETTINGS = Config.get_vehicle_control_settings()
    STEERING = VEHICLE_SETTINGS["steering"]
    DIRECTION = VEHICLE_SETTINGS["direction"]
    
    MAX_SPEED = Config.MAX_SPEED


class RecordingSettings:
    # video_recording_node
    
    FPS = 30
    IMAGE_SIZE = (640, 480)
    
    # 어떤 시점의 영상을 녹화할 건지(전방/후방/위성)
    RECORD_VIEW1 = SIM_CAM
    RECORD_VIEW2 = SIM_CAM3    
    
    # 비디오 파일의 저장 이름
    RECORD_CAR = basic.get_data("car_view.mp4")
    RECORD_UPPER = basic.get_data("top_view.mp4")
    