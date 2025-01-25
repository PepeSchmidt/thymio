import argparse
import time
import random
from thymiodirect import Connection 
from thymiodirect import Thymio
portvar = 30166                    #set port to 1234 if not using in simulation

def main(use_sim=False, ip='127.0.0.1', port=portvar):
    ''' Main function '''
    
    print(ip)
    try:
        # Configure Interface to Thymio robot
        if use_sim:
            th = Thymio(use_tcp=True, host=ip, tcp_port=port, 
                        on_connect=lambda node_id: print(f' Thymio {node_id} is connected'))
        else:
            port = Connection.serial_default_port()
            th = Thymio(serial_port=port, 
                        on_connect=lambda node_id: print(f'Thymio {node_id} is connected'))

        # Connect to Robot
        th.connect()
        robot = th[th.first_node()]
        # Delay to allow robot initialization of all variables
        time.sleep(1)

        # Initialize the state variable
        state = 'stop'
        
        # Initialize the motors
        robot['motor.left.target'] = 0
        robot['motor.right.target'] = 0 
        x1 = robot['prox.horizontal'] [2]
        # Main loop
        while True:
            # Required to slow down the loop
            x2 = robot['prox.horizontal'] [2]
            #if x2 != 0:
            print(x2)
                #x1 = x2
            #    pass
            #else:
            #    pass
            time.sleep(0.1)
            
            # Start the robot
            if state == 'stop' and robot['button.forward']:
                # TODO
                state = 'explore'
                pass
            
            # Stop the robot
            elif state != 'stop' and robot['button.center']:
                # TODO
                robot['motor.left.target'] = 0
                robot['motor.right.target'] = 0
                state = 'stop'
                pass
            
            # Handle the explore state
            elif state == 'explore':
                # TODO
                if robot['prox.horizontal'] [2] <= 100:
                    robot['motor.left.target'] = 500
                    robot['motor.right.target'] = 500
                    if robot['prox.ground.reflected'] [0] >= 800 or robot['prox.ground.reflected'] [1] > 800:
                        state = 'follow'
                else:
                    robot['motor.left.target'] = 0
                    robot['motor.right.target'] = 0

                    Drehung = random.random()
                    while Drehung > 0:
                        robot['motor.right.target'] = 500
                        robot['motor.left.target'] = -500
                        time.sleep(0.01)
                        Drehung = Drehung - 0.5
                    

                pass

            # Handle the follow state
            elif state == 'follow':
                # TODO
                if robot['prox.horizontal'] [2] >= 4450:
                    state = 'avoid'
                elif robot['prox.ground.reflected'] [0] < 800 and robot['prox.ground.reflected'] [1] >= 800:
                    robot['motor.left.target'] = 200
                    robot['motor.right.target'] = 0
                elif robot['prox.ground.reflected'] [0] >= 800 and robot['prox.ground.reflected'] [1] < 800:
                    robot['motor.left.target'] = 0
                    robot['motor.right.target'] = 200
                elif robot['prox.ground.reflected'] [0] >= 800 and robot['prox.ground.reflected'] [1] >= 800:
                    robot['motor.left.target'] = 200
                    robot['motor.right.target'] = 200
                elif robot['prox.ground.reflected'] [0] < 800 and robot['prox.ground.reflected'] [1] < 800:
                    robot['motor.left.target'] = 200
                    robot['motor.right.target'] = 200
                    time.sleep(5)
                    if robot['prox.ground.reflected'] [0] < 800 and robot['prox.ground.reflected'] [1] < 800:
                        state = 'explore'
                
                pass
            elif state == 'avoid':
                #robot['motor.right.target'] = 500
                #robot['motor.left.target'] = -500
                #time.sleep(1)
                #state = 'explore'
                robot['motor.right.target'] = 0
                robot['motor.left.target'] = 0
                x1 = 0
                pass
                

    except Exception as err:
        # Stop robot
        robot['motor.left.target'] = 0
        robot['motor.right.target'] = 0 
        print(err)


if __name__ == '__main__':
    # Parse commandline arguments to cofigure the interface for a simulation (default = real robot)
    parser = argparse.ArgumentParser(description='Configure optional arguments to run the code with simulated Thymio. '
                                                    'If no arguments are given, the code will run with a real Thymio.')
    
    # Add optional arguments
    parser.add_argument('-s', '--sim', action='store_true', help='set this flag to use simulation', default=False)
    parser.add_argument('-i', '--ip', help='set the TCP host ip for simulation. default=localhost', default='localhost')
    parser.add_argument('-p', '--port', help='set the TCP port for simulation. default=1234', default=portvar, type=int)

    # Parse arguments and pass them to main function
    args = parser.parse_args()

    if args.sim:
        main(use_sim=True, ip=args.ip, port=args.port)
    else:
        main(use_sim=False)