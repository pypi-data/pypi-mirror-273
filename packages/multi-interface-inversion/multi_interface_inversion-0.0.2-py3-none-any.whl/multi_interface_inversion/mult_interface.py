import numpy as np
from scipy.fftpack import fft2, ifft2
# from .data_provider import Provider
from abc import ABCMeta, abstractmethod
from scipy.signal.windows import tukey
from math import factorial


class MultiInversion(metaclass=ABCMeta):
    @abstractmethod
    def down_ward(self, target_layer, n=0):
        pass

    @abstractmethod
    def for_ward(self, n):
        pass


class MultiInverser(MultiInversion):
    def __init__(self, kwargs):
        super(MultiInverser, self).__init__()
        self.bnds = kwargs.get('delta-bnds')
        self.mean_depths = kwargs.get('ave-depths')
        self.rhos = kwargs.get('rhos')
        self.observation_plane = kwargs.get('observation-plane')
        self.vgg = kwargs.get('delta-gravity')

        self.target_layer = kwargs.get('target-layer')
        self.longrkm, self.longckm = kwargs.get('longrkm'), kwargs.get('longckm')
        self.G = 6.67
        self.wh, self.sh = kwargs.get('wh', 0.3), kwargs.get('sh', 0.4)
        self.alpha = kwargs.get('alpha', 8)
        # second initialize
        self.__second_init__(truncate=0.1)
        # temp
        self.temp = {}
        self.target_bnd = None

    def __second_init__(self, truncate=0.1):
        nrow, ncol = self.vgg.shape
        # wave number
        self.omga = np.zeros((nrow, ncol))
        for i in range(nrow):
            for j in range(ncol):
                i_changed = i if i <= nrow / 2 else i - nrow
                j_changed = j if j <= ncol / 2 else j - ncol
                self.omga[i, j] = np.sqrt(i_changed ** 2 / self.longrkm ** 2 + j_changed ** 2 / self.longckm ** 2) * 2 * np.pi
        # rho * A
        self.K = len(self.rhos) - 1
        self.mean_depths[self.K] = 0
        self.rhod = {item: self.rhos[item] for item in range(self.K)}
        self.a_ks = {item: np.exp(-self.omga * (self.observation_plane - self.mean_depths[item])) for item in range(self.K)}
        # filter
        b = self.omga.max()
        wh, sh = b * self.wh, b * self.sh
        alpha = self.alpha
        self.filtor = np.ones((nrow, ncol))
        # alph = self.alpha
        for i in range(nrow):
            for j in range(ncol):
                if self.omga[i, j] > wh:
                    swh = self.omga[i, j] / wh
                    self.filtor[i, j] = swh ** (1 - alpha) - (1 - alpha) * np.log(swh) * swh ** (1 - alpha)

                # if wh < self.omga[i, j] < sh:
                #     self.filtor[i, j] = 0.5 * (1 + np.cos(np.pi * (self.omga[i, j] - wh) / (sh - wh)))
                #     # self.filtor[i, j] = ((sh - wh) ** alpha - (self.omga[i, j] - wh) ** alpha) / \
                #     #                     ((sh - wh) ** alpha - (self.omga[i, j] + wh) ** alpha)
                # elif self.omga[i, j] >= sh:
                #     self.filtor[i, j] = 0
        # delta g
        twkey_vgg = self.twkey(self.vgg, truncate=truncate)
        self.delta_g_fourier = fft2(twkey_vgg)

    @classmethod
    def twkey(cls, layer, truncate=0.1):
        nrow, ncol = layer.shape
        twk = np.array([item1 * item2 for item1 in tukey(nrow, truncate) for item2 in tukey(ncol, truncate)]).reshape((nrow, ncol))
        return twk * layer

    def for_ward(self, n):
        factor_constant = -2 * np.pi * self.G
        fft_bands = 0
        for k in range(self.K - 1):
            factor_rhok = (self.rhod[k] - self.rhod[k + 1]) * self.a_ks[k]
            delta_h = np.zeros(self.omga.shape)
            for m in range(1, n + 1):
                delta_h = delta_h + self.omga ** (m - 1) / factorial(m) * fft2(self.bnds[k] ** m)
            fft_bands = fft_bands + factor_rhok * delta_h
        fft_delta_g = factor_constant * fft_bands
        return ifft2(fft_delta_g).real

    def get_fourier_bnd_k_n(self, k, n, truncate=0.1):
        fourier_twkey_bnd_k_n = self.temp.get(k, None)
        if fourier_twkey_bnd_k_n is not None:
            fourier_twkey_bnd_k_n = fourier_twkey_bnd_k_n.get(n, None)
        if fourier_twkey_bnd_k_n is None:
            if k != self.target_layer:
                bnd_k = self.bnds[k]
                twkey_bnd_k = self.twkey(bnd_k, truncate=truncate)
                twkey_bnd_k_n = twkey_bnd_k ** n
                fourier_twkey_bnd_k_n = fft2(twkey_bnd_k_n)
                fourier_twkey_bnd_ks = self.temp.get(k, {})
                fourier_twkey_bnd_ks[n] = fourier_twkey_bnd_k_n
                self.temp[k] = fourier_twkey_bnd_ks
            else:
                bnd_k = self.target_bnd - self.target_bnd.mean()
                twkey_bnd_k = self.twkey(bnd_k, truncate=truncate)
                twkey_bnd_k_n = twkey_bnd_k ** n
                fourier_twkey_bnd_k_n = fft2(twkey_bnd_k_n)
        return fourier_twkey_bnd_k_n

    def down_ward(self, target_layer, n=1, truncate=0.1):
        delta_rhoa_target = (self.rhod[target_layer] - self.rhod[target_layer + 1]) * self.a_ks[target_layer]
        # first inversion ----------------------------------------------------------------------------------------------
        delta_g_factor = -2 * np.pi * self.G * delta_rhoa_target
        fourier = self.delta_g_fourier / delta_g_factor
        for k in range(self.K - 1):
            if k != target_layer:
                fft_k_bnd = (self.rhod[k] - self.rhod[k + 1]) * self.a_ks[k] / delta_rhoa_target * self.get_fourier_bnd_k_n(k=k, n=1, truncate=truncate)
                fourier -= fft_k_bnd
        # filter
        fourier_filtered = fourier * self.filtor
        # target_bnd
        bnd_target = ifft2(fourier_filtered).real
        # doward
        for m in range(1, n):
            for k in range(self.K - 1):
                if k != target_layer:
                    fourier -= (self.rhod[k] - self.rhod[k + 1]) * self.a_ks[k] / delta_rhoa_target * \
                               self.omga ** m / factorial(m+1)\
                               * self.get_fourier_bnd_k_n(k=k, n=m+1, truncate=truncate)
            # filter
            fourier[0, 0] = 0
            target_fourier = fourier - self.calculate_m_fourier_target(bnd_target, m=m+1, truncate=truncate)
            filter_target_fourier = target_fourier * self.filtor
            bnd_target = ifft2(filter_target_fourier).real
            # self.target_bnd[m + 1] = bnd_target

        delta = bnd_target.real - bnd_target.real.mean()  # + self.mean_depths[target_layer]
        predict = delta + self.mean_depths[target_layer]
        return predict, delta

    def calculate_m_fourier_target(self, bnd_target, m=2, truncate=0.0):
        bnd_target_center = bnd_target - bnd_target.mean()
        twkey_bnd_target = self.twkey(bnd_target_center, truncate=truncate)
        fourier_twkey_bnd_target_ms = 0
        for n in range(2, m):
            twkey_bnd_target_n = twkey_bnd_target ** n
            fourier_twkey_bnd_target_n = fft2(twkey_bnd_target_n)
            fourier_twkey_bnd_target_ms += self.omga ** (n - 1) / factorial(n) * fourier_twkey_bnd_target_n
        return fourier_twkey_bnd_target_ms

#
# if __name__ == "__main__":
#     """parameters"""
#     target_size = (251, 251)
#     kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160, 'delta-vgg': 'delta-g.dg'}
#     clr = Provider(kwargs)
#     layers = [clr.format_layer(target_size=target_size, layer_number=i, order=3) for i in [8, 5, 1, 0]]
#     observation_plane = 0
#     rho_s = [clr.rho_mean(i) for i in [8, 6, 2, 0]]
#     kwargs.update({'delta-bnds': {i: item - item.mean() for i, item in enumerate(layers)}})
#     kwargs.update({'ave-depths': {i: item.mean() for i, item in enumerate(layers)}})
#     kwargs.update({'rhos': rho_s + [0]})
#     kwargs.update({'delta-gravity': clr.format_vgg(target_size=target_size, order=3) - clr.format_vgg(target_size=target_size, order=3).mean()})
#     kwargs.update({'longrkm': 1100, 'longckm': 1100, 'observation-plane': observation_plane, 'target-layer': 2})
#     """查看数据情况"""
#     mir = MultiInverser(kwargs)
#     # h2 = mir.down_ward(target_layer=2, n=1, truncate=0.1)
#     # clr.show_matrix(layers[2])
#     # clr.show_matrix(h2)
#     # clr.show_matrix(kwargs['vgg'])
#     delta_g = mir.for_ward(n=16)
#     np.savetxt('../crust1.0/delta-g.dg', delta_g)
#     # clr.show_matrix(delta_g)
#     # kwargs.update({'delta-gravity': delta_g - delta_g.mean()})
#     # mir2 = MultiInversor(kwargs)
#     # h2 = mir2.down_ward(target_layer=2, n=6, truncate=0.1)
#     # cf = 15
#     # clr.show_matrix(h2[cf:-cf, cf:-cf], name="prediction")
#     # clr.show_matrix(layers[2][cf:-cf, cf:-cf], name='truth')
#     """------------------------------------------------------layer5-----------------------------------------"""
#     """parameters"""
#     target_size = (251, 251)
#     kwargs = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160, 'delta-vgg': 'delta-g5.dg'}
#     clr = Provider(kwargs)
#     layers = [clr.format_layer(target_size=target_size, layer_number=i, order=3) for i in [8, 7, 6, 5, 1, 0]]
#     observation_plane = 0
#     rho_s = [clr.rho_mean(i) for i in [8, 7, 6, 5, 2, 0]]
#     kwargs.update({'delta-bnds': {i: item - item.mean() for i, item in enumerate(layers)}})
#     kwargs.update({'ave-depths': {i: item.mean() for i, item in enumerate(layers)}})
#     kwargs.update({'rhos': rho_s + [0]})
#     kwargs.update({'delta-gravity': clr.format_vgg(target_size=target_size, order=3) - clr.format_vgg(
#         target_size=target_size, order=3).mean()})
#     kwargs.update({'longrkm': 1100, 'longckm': 1100, 'observation-plane': observation_plane, 'target-layer': 2})
#     """查看数据情况"""
#     mir = MultiInverser(kwargs)
#     delta5_g = mir.for_ward(n=16)
#     np.savetxt('../crust1.0/delta-g5.dg', delta5_g)

