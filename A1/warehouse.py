#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
import copy

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class warehouse(StateSpace):
    def __init__(self, action, gval, product_list, packing_station_list, current_time, open_orders, robot_status, parent=None): 
#IMPLEMENT
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.product_list = product_list
        self.packing_station_list = packing_station_list
        self.current_time = current_time
        self.open_orders = open_orders
        self.robot_status = robot_status 

    def successors(self): 
#IMPLEMENT
        '''Return list of warehouse objects that are the successors of the current object
    
        1. Check open orders (so I know what possible orders can be assigned to a robot)
        2. Check robot statuses (so I know what robot's are idle, which are doing a delivery)
              - If there is a robot currently doing a delivery then another possible successor 
                would be moving time forward. 
        '''

        successor_states = list()
        idle_robots = list()
        robots_on_delivery = list()
        product_list_dict = dict()
        packing_station_list_dict = dict()

        '''Store products and packing stations in a dictionary for looking up 
           coordinates of their locations.
        '''

        for product in self.product_list:
            product_list_dict[product[0]] = product[1]

        for packing_station in self.packing_station_list:
            packing_station_list_dict[packing_station[0]] = packing_station[1]

        #print(packing_station_list_dict)
        for robot in self.robot_status:
            if robot[1] == "idle":
              idle_robots.append(robot)
            elif robot[1] == "on_delivery":
              robots_on_delivery.append(robot)

        open_orders_copy = copy.deepcopy(self.open_orders)
        #open_orders_copy = self.open_orders.copy()

        "If there are orders then map each robot to a order covering all combinations"
        if len(open_orders_copy) != 0 and len(idle_robots) !=0 :
            for robot in idle_robots:
                for order in open_orders_copy: 
                    action_str_deliver = "deliver({},{},{})".format(robot[0], order[0], order[1])
                    robot_location = robot[2]
                    product_location = product_list_dict[order[0]]
                    packing_station_location = packing_station_list_dict[order[1]]
                    cost_robot_to_product =  abs(robot_location[(0)] - product_location[(0)]) + abs(robot_location[(1)] - product_location[(1)]) 
                    cost_product_to_packing_station = abs(product_location[(0)] - packing_station_location[(0)]) + abs(product_location[(1)] - packing_station_location[(1)])
                    g_value_cost = cost_robot_to_product + cost_product_to_packing_station
                      
                    open_orders_alias = copy.deepcopy(self.open_orders)
                    open_orders_alias.remove(order)

                    robot_status_alias = copy.deepcopy(self.robot_status)
                    robot_status_alias2 = copy.deepcopy(self.robot_status)
                    for robot1 in robot_status_alias:
                        if robot1[0] == robot[0]:
                            robot_temp = [robot[0], "on_delivery", packing_station_location, self.current_time + g_value_cost]
                            robot_status_alias2.remove(robot1)
                            robot_status_alias2.append(robot_temp)

                    '''
                       Remove possible order from open_orders, 
                       Update robot status 
                    '''
                    warehouse_obj = warehouse(action_str_deliver, self.gval, self.product_list, self.packing_station_list, self.current_time, open_orders_alias, robot_status_alias2, self)
                    successor_states.append(warehouse_obj)

        if robots_on_delivery != []:
            earliest_delivery_time_robot = dict()
            earliest_delivery_time_robot[robots_on_delivery[0][0]] = robots_on_delivery[0]
            earliest_delivery_time_robot_key = robots_on_delivery[0][0]
            for delivering_robot in robots_on_delivery[1:]:
                if delivering_robot[3] < earliest_delivery_time_robot[earliest_delivery_time_robot_key][3]:
                    earliest_delivery_time_robot = dict()
                    earliest_delivery_time_robot[delivering_robot[0]] = delivering_robot
                    earliest_delivery_time_robot_key = delivering_robot[0]

                elif delivering_robot[3] == earliest_delivery_time_robot[earliest_delivery_time_robot_key][3]:
                    earliest_delivery_time_robot[delivering_robot[0]] = delivering_robot

            '''
            Update robot status to idle not on delivery. 
            Update the time of the new state
            '''
            robot_status_shallow = copy.deepcopy(self.robot_status)
            for x in earliest_delivery_time_robot:
                spot = robot_status_shallow.index(earliest_delivery_time_robot[x])
                robot_status_shallow[spot][1] = "idle"
                finish_time = earliest_delivery_time_robot[x][3]
                move_forward_time = robot_status_shallow[spot][3] - self.current_time
                move_forward_time = move_forward_time + self.current_time
                robot_temp = robot_status_shallow[spot][:-1]
                robot_status_shallow.remove(robot_status_shallow[spot])
                robot_status_shallow.append(robot_temp)
                action_str_move_forward = "move_forward({})".format(finish_time)
                      
            warehouse_mf_state = warehouse(action_str_move_forward, self.gval + (finish_time - self.current_time), self.product_list, self.packing_station_list, finish_time, self.open_orders, robot_status_shallow, self)
            successor_states.append(warehouse_mf_state)

        #print(successor_states)
        return successor_states

    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        #L = [self.current_time, map(tuple, self.robot_status), map(tuple, self.open_orders)]
        rcpy = copy.deepcopy(self.robot_status)
        scpy = copy.deepcopy(self.open_orders)
        for i in rcpy:
           tuple(i)
            
        for j in scpy:
            tuple(j)
        #return (str([self.current_time, tuple(rcpy), tuple(scpy)]))
        #return (tuple((str(self.index))))
        return tuple(str([self.current_time, tuple(rcpy), tuple(scpy)]))
        #L.append(self.current_time)
        #L.append(self.current_time)
        #L.append(tuple(self.robot_status))
        #L.append(tuple(self.open_orders))
        #L.extend([self.gval, tuple(self.product_list), tuple(self.packing_station_list), tuple(self.open_orders), tuple(self.robot_status)])
        #unique = str(self.index)
        #return tuple(L)  

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("Time = {}".format(self.get_time())) #added extra bracket
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))

#Data accessor routines.

    def get_robot_status(self):
#IMPLEMENT
        '''Return list containing status of each robot
           This list has to be in the format: [rs_1, rs_2, ..., rs_k]
           with one status list for each robot in the state. 
           Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
           Where <name> is the name of the robot (a string)
                 <status> is either the string "idle" or the string "on_delivery"
                 <loc> is a location (a pair (x,y)) 
                       if <status> == "idle" then loc is the robot's current location
                       if <status> == "on_delivery" then loc is the robot's future location
                <ftime> 
                       if <status> == "idle" this item is missing (i.e., the list is of 
                                      length 3)
                       if <status> == "on_delivery" then this is a number that is the 
                                      time that the robot will complete its current delivery
        '''
        return self.robot_status

    def get_time(self):
#IMPLEMENT
        '''Return the current time of this state (a number)'''
        return self.current_time

    def get_orders(self):
#IMPLEMENT
        '''Return list of unfulfilled orders of this state
           This list is in the format [o1, o2, ..., om]
           one item for each unfulfilled order. 
           Each oi is itself a list [<product_name>, <packing_station_name>]
           where <product_name> is the name of the product to be delivered
           and  <packing_station_name> is the name of the packing station it is to be delivered to'''

        return self.open_orders
#############################################
# heuristics                                #
#############################################
    
def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_min_completion_time(state):
#IMPLEMENT
    '''warehouse heuristic'''
    #We want an admissible heuristic. Since the aim is to delivery all
    #of the products to their packing station in as short as a time as
    #possible. 
    #NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    #Consider all of the possible delays in moving from this state to
    #a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    #
    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max TIME2
    #    Clearly we cannot finish before TIME2
    #
    # Finally we return as a the heuristic value the MAXIMUM of TIME1 and TIME2

    time1_temp = []
    TIME1 = 0
    TIME2 = 0
    for robot in state.robot_status:
        if robot[1] == "on_delivery":
            delivery_time = robot[3] - state.current_time
            time1_temp.append(delivery_time)

    if time1_temp == []:
        TIME1 = 0
    else:
        TIME1 = max(time1_temp)

    time2_temp = []
    product_list_dict = dict()
    packing_station_list_dict = dict()

    ## Dictionary lookup - product name to it's location
    for product in state.product_list:
        product_list_dict[product[0]] = product[1]

    for packing_station in state.packing_station_list:
        packing_station_list_dict[packing_station[0]] = packing_station[1]

    #print(product_list_dict)
    #print(packing_station_list_dict)

    for order in state.open_orders:
        #print(order)
        product_location = product_list_dict[order[0]]
        packing_station_location = packing_station_list_dict[order[1]]
        cost_product_to_packing_station = abs(product_location[(0)] - packing_station_location[(0)]) + abs(product_location[(1)] - packing_station_location[(1)])
        #print(cost_product_to_packing_station)
        time2_temp.append(cost_product_to_packing_station)
        #print(time2_temp)

    #print("outside for loop")
    #print(time2_temp)  
    if time2_temp == []:
        TIME2 = 0
    else:
        TIME2 = max(time2_temp)

    final_heuristic_value = max(TIME1, TIME2)
    return final_heuristic_value

def warehouse_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal when all orders have been delivered'''
    if (state.open_orders == []):
        for i in state.robot_status:
            if (i[1] != "idle"):
               return False

        return True
        
    else: return False       

def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):
#IMPLEMENT
    '''Input the following items which specify a state and return a warehouse object 
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

   NOTE: for simplicity you may assume that 
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
    '''
    action = "START"
    gval = 0
    parent = None
    start_state_space = warehouse(action, gval, product_list, packing_station_list, current_time, open_orders, robot_status, parent)
    return start_state_space 

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0,50), randint(0,50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0,50), randint(0,50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0,nprods-1)][0], packs[randint(0,npacks-1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0,50), randint(0,50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


def test(nprods, npacks, norders, nrobots):
    s0 = make_rand_init_state(nprods, npacks, norders, nrobots)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, warehouse_goal_fn, heur_min_completion_time)
