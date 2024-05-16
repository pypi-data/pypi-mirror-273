__version__ = '2.5.8'

from mke_sculib.scu import scu as scu_api, plot_tt, print_color, colors
from mke_sculib.sim import scu_sim
from mke_sculib.stellarium_api import stellarium_api as stellar_api
from mke_sculib.sim import plot_motion_pyplot as plot_motion
from mke_sculib.helpers import get_utcnow, make_zulustr, parse_zulutime

def load(antenna_id, post_put_delay=0.0, debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):
    if not "requests" in locals():
        import requests
    if not "json" in locals():
        import json

    assert antenna_id, 'need to give an antenna id'

    if antenna_id == 'test_antenna':
        return scu_sim(antenna_id, debug=debug)
    else:
        dc = requests.get(f'{url_qry}/{antenna_id}').json()
        
        try:
            params = json.loads(dc['params_json'])
            
        except Exception as err:
            print('could not load "params_json" from server')
            params = {}
        dish = scu_api(dc['address'], post_put_delay=post_put_delay, debug=debug)
        for k, v in params.items():
            if hasattr(dish, k):
                setattr(dish, k, v)

        return dish
        