from abc import ABCMeta, abstractmethod
from matplotlib import pyplot as plt
from .data_provider import Provider
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({'font.size': 12})


# 定义绘图功能接口
class PlotContr(metaclass=ABCMeta):
    # 等高线
    @abstractmethod
    def plt_conter(self, mtrix, lat=None, lon=None, name=None):
        """
        :param mtrix: n * p 的array-like
        :param lat: list,如[-10, -5, 0, 5, 10]
        :param lon: list,如[-10, -5, 0, 5, 10]
        :param legend_position:  right or down
        :param name: if None, plt.show else 把图保存到name地址
        :return: None
        """
        pass

    @abstractmethod
    def plt_conterf(self, mtrix, lat=None, lon=None, legend_position='down', name=None):
        """
        :param mtrix: n * p 的array-like
        :param lat: list,如[-10, -5, 0, 5, 10]
        :param lon: list,如[-10, -5, 0, 5, 10]
        :param legend_position:  right or down
        :param name: if None, plt.show else 把图保存到name地址
        :return: None
        """
        pass

    # 3D图
    @abstractmethod
    def plt_3d(self, mtrix, lat=None, lon=None, name=None):
        """
        :param mtrix: n * p 的array-like
        :param lat: list,如[-10, -5, 0, 5, 10]
        :param lon: list,如[-10, -5, 0, 5, 10]
        :param name: if None, plt.show else 把图保存到name地址
        :return: None
        """
        pass

    # layer
    @abstractmethod
    def plt_layer(self, mtrix, lon=None, colors=None, name=None):
        """
        :param mtrix: ncol * layer
        :param lat:
        :param lon:
        :param name:
        :return:
        """
        pass


class PltConter(PlotContr):
    @classmethod
    def plt_conter(cls, mtrix, lat=None, lon=None, name=None):
        nrow, ncol = mtrix.shape
        x, y = np.arange(ncol), nrow - np.arange(nrow) - 1
        xx, yy = np.meshgrid(x, y)
        plt.figure()
        c = plt.contour(xx, yy, mtrix, colors='black')
        plt.clabel(c, inline=True, fontsize=10)
        if lon is not None:
            plt.xticks([item for item in np.linspace(0, ncol, len(lon))], lon)
        if lat is not None:
            plt.yticks([item for item in np.linspace(0, nrow, len(lat))], lat)
        if name is None:
            plt.show()
        else:
            plt.savefig(name)

    @classmethod
    def plt_conterf(cls, mtrix, lat=None, lon=None, legend_position='down', name=None):
        nrow, ncol = mtrix.shape
        x, y = np.arange(ncol), nrow - np.arange(nrow) - 1
        xx, yy = np.meshgrid(x, y)
        plt.figure()
        c = plt.contourf(xx, yy, mtrix)
        plt.clabel(c, inline=False, fontsize=10)
        cbar = plt.colorbar()
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        if lon is not None:
            plt.xticks([item for item in np.linspace(0, ncol, len(lon))], lon)
        if lat is not None:
            plt.yticks([item for item in np.linspace(0, nrow, len(lat))], lat)
        if name is None:
            plt.show()
        else:
            plt.savefig(name)

    @classmethod
    def plt_3d(cls, mtrix, lat=None, lon=None, name=None):
        fig = plt.figure()
        ax3 = plt.axes(projection='3d')
        nrow, ncol = mtrix.shape
        x, y = np.arange(0, ncol), nrow - np.arange(nrow) - 1
        xx, yy = np.meshgrid(x, y)
        ax3.plot_surface(xx, yy, mtrix, cmap='rainbow')

        # ax3.tick_params(labelsize=12)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        if lon is not None:
            plt.xticks([item for item in np.linspace(0, ncol, len(lon))], lon)
        if lat is not None:
            plt.yticks([item for item in np.linspace(0, nrow, len(lat))], lat)
        ax3.dist = 8.5
        if name is None:
            plt.show()
        else:
            plt.savefig(name)

    def plt_layer(self, mtrix, lon=None, colors=None, name=None, texts=[], arrows=[]):
        nrow, ncol = mtrix.shape
        if colors is None:
            colors = ['firebrick', 'sandybrown', 'bisque', 'royalblue']
        plt.figure()
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(-15, 1)
        x = np.arange(mtrix.shape[1])
        for i in range(mtrix.shape[0]):
            if i == 0:
                layer_up = mtrix[i, :]
                layer_down = np.ones(ncol) * mtrix.min() - 1
                plt.fill_between(x, layer_down, layer_up, color=colors[i], edgecolor='black', linewidth=0.5, alpha=0.8)
            else:
                layer_down = mtrix[i - 1, :]
                layer_up = mtrix[i, :]
                plt.fill_between(x, layer_down, layer_up, color=colors[i], edgecolor='black', linewidth=0.5, alpha=0.8)
        if lon is not None:
            plt.xticks([item for item in np.linspace(0, ncol, len(lon))], lon)
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        for arrow in arrows:
            ax.annotate('', xy=arrow[1], xytext=arrow[0], arrowprops=dict(color=arrow[2], arrowstyle=arrow[3]))
        plt.ylabel('Depth', fontdict={'fontsize': 20})
        plt.subplots_adjust(left=0.15)
        for text in texts:
            plt.text(text[0], text[1], text[2], color=text[3], fontdict={'fontsize': 18})
        if name is None:
            plt.show()
        else:
            plt.savefig(name)

    @classmethod
    def plot_twin(cls, _x, _y1, _y2, _xlabel, _ylabel1, _ylabel2, title=None, name=None, texts=[],
                  legend_position='upper right', padding_dict={}):
        fig = plt.figure()
        plt.subplots_adjust(**padding_dict)
        ax1 = fig.add_subplot()
        color = 'tab:blue'
        ax1.set_xlabel(_xlabel, fontdict={'fontsize': 18})
        ax1.set_ylabel(_ylabel1, color=color, fontdict={'fontsize': 18})
        line1 = ax1.plot(_x, _y1, color=color, label=_ylabel1, linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        for text in texts:
            plt.text(text[0], text[1], text[2], color=text[3], fontdict={'fontsize': 18})
        ax2 = ax1.twinx()  # 创建共用x轴的第二个y轴

        color = 'tab:red'
        ax2.set_ylabel(_ylabel2, color=color, fontdict={'fontsize': 18})
        line2 = ax2.plot(_x, _y2, color=color, label=_ylabel2, linestyle='dashed', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color)

        # fig.tight_layout()
        ax_list = line1 + line2
        labels = [l.get_label() for l in ax_list]
        print(labels)
        ax1.legend(ax_list, labels, loc=legend_position)
        if title is not None:
            plt.title(title, fontdict={'fontsize': 18})
        if name is None:
            plt.show()
        else:
            plt.savefig(name)

    @classmethod
    def formater(cls, res_rhos):
        res = []
        for i in range(3):
            mse = res_rhos['mse'][i]
            kl = res_rhos['kl'][i]
            mn, mx = res_rhos['range'][i][0], res_rhos['range'][i][1]
            if mse == min(res_rhos['mse']):
                mse_str = r"& \underline{$%.3f$} " % mse
            else:
                mse_str = r"& $%.3f$ " % mse
            if kl == min(res_rhos['kl']):
                kl_str = r"& \underline{$%.3f$} " % kl
            else:
                kl_str = r"& $%.3f$ " % kl
            if mn == min([item[0] for item in res_rhos['range']]):
                mn_str = r"& \underline{$%.3f$} " % mn
            else:
                mn_str = r"& $%.3f$ " % mn
            if mx == max([item[1] for item in res_rhos['range']]):
                mx_str = r"& \underline{$%.3f$} " % mx
            else:
                mx_str = r"& $%.3f$ " % mx
            st = mse_str + kl_str + mn_str + mx_str
            res.append(st)
        return res


if __name__ == "__main__":
    pcr = PltConter()
    area = {'lat_up': 30, 'lat_down': 20, 'lon_left': 150, 'lon_right': 160, 'delta-vgg': 'delta-g.dg'}
    lon = [r'$150^{\circ}$W', r'$155^{\circ}$W', r'$160^{\circ}$W']
    lat = [r'$20^{\circ}$N', r'$25^{\circ}$N', r'$30^{\circ}$N']
    clr = Provider(area)
    mtrix = clr.format_layer(target_size=(251, 251), layer_number=1)
    pcr.plt_conter(mtrix, lat=lat, lon=lon)
    pcr.plt_conterf(mtrix, lat=lat, lon=lon)
    pcr.plt_3d(mtrix, lat=lat, lon=lon)
    mtrix_cut = np.array([clr.format_layer(target_size=(251, 251), layer_number=8)[-1, :],
                 clr.format_layer(target_size=(251, 251), layer_number=5)[-1, :] - 0.1,
                 clr.format_layer(target_size=(251, 251), layer_number=1)[-1, :] + 0.1,
                 clr.format_layer(target_size=(251, 251), layer_number=0)[-1, :]
                 ])
    pcr.plt_layer(mtrix_cut, lon=lon, name='../figs/crust20.eps')
