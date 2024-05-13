from .data_provider import Provider
from .mult_interface import MultiInverser
import numpy as np
import os

dir = os.path.dirname(__file__)


"""generate the vgg of 3-interface model and 5-interface model by the coordinates"""


class Generater:
    @classmethod
    def generate_vgg3(cls, lat_up=30, lat_down=20, lon_left=150, lon_right=160, n=16, order=3, name='temp.dg'):
        target_size = (251, 251)
        kwargs = {'lat_up': lat_up, 'lat_down': lat_down, 'lon_left': lon_left, 'lon_right': lon_right, 'delta-vgg': 'delta-g.dg'}
        clr = Provider(kwargs)
        layers = [clr.format_layer(target_size=target_size, layer_number=i, order=order) for i in [8, 5, 1, 0]]
        observation_plane = 0
        rho_s = [clr.rho_mean(i) for i in [8, 6, 2, 0]]
        kwargs.update({'delta-bnds': {i: item - item.mean() for i, item in enumerate(layers)}})
        kwargs.update({'ave-depths': {i: item.mean() for i, item in enumerate(layers)}})
        kwargs.update({'rhos': rho_s + [0]})
        kwargs.update({'delta-gravity': clr.format_vgg(target_size=target_size, order=order) - clr.format_vgg(target_size=target_size, order=order).mean()})
        kwargs.update({'longrkm': 1100, 'longckm': 1100, 'observation-plane': observation_plane, 'target-layer': 2})
        """查看数据情况"""
        mir = MultiInverser(kwargs)
        delta_g = mir.for_ward(n=n)
        np.savetxt(dir + '/crust1.0/{}'.format(name), delta_g)
        return delta_g

    @classmethod
    def generate_vgg5(cls, lat_up=30, lat_down=20, lon_left=150, lon_right=160, n=16, order=3, name='temp.dg'):
        target_size = (251, 251)
        kwargs = {'lat_up': lat_up, 'lat_down': lat_down, 'lon_left': lon_left, 'lon_right': lon_right, 'delta-vgg': 'delta-g5.dg'}
        clr = Provider(kwargs)
        layers = [clr.format_layer(target_size=target_size, layer_number=i, order=3) for i in [8, 7, 6, 5, 1, 0]]
        observation_plane = 0
        rho_s = [clr.rho_mean(i) for i in [8, 7, 6, 5, 2, 0]]
        kwargs.update({'delta-bnds': {i: item - item.mean() for i, item in enumerate(layers)}})
        kwargs.update({'ave-depths': {i: item.mean() for i, item in enumerate(layers)}})
        kwargs.update({'rhos': rho_s + [0]})
        kwargs.update({'delta-gravity': clr.format_vgg(target_size=target_size, order=order) - clr.format_vgg(
            target_size=target_size, order=order).mean()})
        kwargs.update({'longrkm': 1100, 'longckm': 1100, 'observation-plane': observation_plane, 'target-layer': 4})
        """查看数据情况"""
        mir = MultiInverser(kwargs)
        delta5_g = mir.for_ward(n=n)
        np.savetxt(dir + '/crust1.0/{}'.format(name), delta5_g)
        return delta5_g

    @classmethod
    def generate_vgg(cls, kwargs, n=16, name='temp.dg'):
        mir = MultiInverser(kwargs=kwargs)
        delta_g = mir.for_ward(n=n)
        np.savetxt(name, delta_g)
        return delta_g

