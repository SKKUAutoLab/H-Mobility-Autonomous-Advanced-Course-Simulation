from simulation_pkg import basic

def main():
    basic.load_model( "traffic_light_stand", "traffic" , basic.traffic_light_stand() )

if __name__ == "__main__":
    main()