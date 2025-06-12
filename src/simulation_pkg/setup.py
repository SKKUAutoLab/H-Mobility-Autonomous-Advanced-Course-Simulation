import os
from glob import glob
from setuptools import setup

package_name = 'simulation_pkg'
sub_package_name = 'simulation_pkg/lib'

setup(
    name=package_name,
    version='0.0.0',
    
    packages=[package_name, sub_package_name],
    
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name,'launch'), glob('launch/*')),
        (os.path.join('share', package_name,'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name,'rviz'), glob('rviz/*')),
    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jinsun-Lee',
    maintainer_email='012vision@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                
        # 시뮬레이션 세팅
        'load_ego_car_node = simulation_pkg.lib.load_ego_car_node:main',
        'load_obstable_car_node = simulation_pkg.lib.load_obstable_car_node:main',
        'load_traffic_light_node = simulation_pkg.lib.load_traffic_light_node:main',
        'load_parking_car_node = simulation_pkg.lib.load_parking_car_node:main',
        
        # 실제 환경과 동일한 구성의 노드
        'sim_lane_info_extractor_node = simulation_pkg.lane_info_extractor_node:main',
        'sim_motion_planner_node = simulation_pkg.motion_planner_node:main',
        'sim_simulation_sender_node = simulation_pkg.simulation_sender_node:main',
        'timer_based_obstacle_mover = simulation_pkg.timer_based_obstacle_mover:main',
        
        'sim_yolov8_node = simulation_pkg.lib.yolov8_node:main',
        'sim_debug_node = simulation_pkg.lib.debug_node:main',
        
        'sim_traffic_light_detector_node = simulation_pkg.traffic_light_detector_node:main',
        
        'sim_lidar_processor_node = simulation_pkg.lidar_processor_node:main',
        'sim_lidar_obstacle_detector_node = simulation_pkg.lidar_obstacle_detector_node:main',       
    
        # 추가 노드
        'data_collection_node = simulation_pkg.data_collection_node:main',
        'video_recording_node = simulation_pkg.lib.video_recording_node:main', # 비디오 녹화
        
        'sonar_processor_node = simulation_pkg.sonar_processor_node:main', # 초음파 센서 처리
        
        'draw_trajectory_node = simulation_pkg.lib.draw_trajectory_node:main', # 궤적 시각화
        
        
        
        ],
    },
)