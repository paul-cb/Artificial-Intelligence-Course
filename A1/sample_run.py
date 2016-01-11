from warehouse import *

if __name__ == '__main__':
    s = make_init_state([['prod1', (0,0)], ['prod2', (0,10)], ['prod3', (0, 20)]], 
                        [['pack1', (20,0)], ['pack2', (20,10)], ['pack3', (20,20)]],
                        0, 
                        [['prod1', 'pack1'], ['prod2', 'pack2'], ['prod3', 'pack3']], 
                        [['r1', 'on_delivery', (20,10), 14], 
                         ['r2', 'on_delivery', (20,20), 8], 
                         ['r3', 'on_delivery', (20,0), 8]])
    
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    se.search(s, warehouse_goal_fn, heur_min_completion_time)
    se.set_strategy('breadth_first')
    se.search(s, warehouse_goal_fn)

