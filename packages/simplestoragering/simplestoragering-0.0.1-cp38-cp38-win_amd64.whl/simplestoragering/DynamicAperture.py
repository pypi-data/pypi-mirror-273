# -*- coding: utf-8 -*-
import numpy as np
from .track import symplectic_track
from .CSLattice import CSLattice
from .exceptions import ParticleLost
from .components import Mark


class Grid:

    def particles(self):
        """generate particles to track"""
        pass

    def run(self):
        pass


# def parallel_search_inner(vv):
#     set_ref_energy(3500)
#     try:
#         symplectic_track([vv[0], 0, vv[1], 0, 0, vv[2]], vv[4], vv[3], record = False)
#         return [vv[0], vv[1], 0, np.inf, np.inf]
#     except ParticleLost as p:
#         return [vv[0], vv[1], 1, p.location, p.location]


class XDeltaGrid(Grid):
    """generate 2d grid on x-delta plane.

    generate a grid in the range of (-xmax, xmax)x(-delta_max, delta_max).
    then use XDeltaGrid.search() to track particles in this grid.

    attributes:
    delta: momentum deviation.
    data: particle data with 5 columns, (x, dp, is_lost, survive_turn, lost_location)"""
    def __init__(self, xmax=None, nx=None, delta_max=None, ndelta=None, y=1e-6, xlist=None, delta_list=None) -> None:
        self.xrange = np.linspace(-xmax, xmax, nx * 2 + 1) if xlist is None else xlist
        self.delta_range = np.linspace(-delta_max, delta_max, ndelta * 2 + 1) if delta_list is None else delta_list
        self.y = y
        self.data = None

    def search(self, lattice: CSLattice, n_turns=100, with_rf=False):
        """"""
        if with_rf:
            raise Exception('Unfinished. 4D tracking only.')
        self.data = np.zeros((len(self.xrange) * len(self.delta_range), 5))
        i = 0
        for dp in self.delta_range:
            for x in self.xrange:
                try:
                    symplectic_track([x, 0, self.y, 0, 0, dp], lattice, n_turns, record = False)
                    self.data[i, :] = [x, dp, 0, np.inf, np.inf]
                    i += 1
                except ParticleLost as p:
                    self.data[i, :3] = [x, dp, 1]
                    self.data[i, 3] = int(p.location / lattice.length)
                    self.data[i, 4] = p.location % (lattice.length / lattice.n_periods)
                    i += 1

    def save_data(self):
        pass


class XYGrid:
    """generate 2d grid on xy plane.

    generate a grid in the range of (-xmax, xmax)x(1e-6, ymax).
    then use XYGrid.search() to track particles in this grid.

    attributes:
    delta: momentum deviation.
    data: particle data with 5 columns, (x, y, is_lost, survive_turn, lost_location)"""
    def __init__(self, xmax=None, nx=None, ymax=None, ny=None, delta=0, xlist=None, ylist=None) -> None:
        self.xrange = np.linspace(-xmax, xmax, nx * 2 + 1) if xlist is None else xlist
        self.yrange = np.linspace(1e-6, ymax, ny + 1) if ylist is None else ylist
        self.delta = delta
        self.data = None

    def search(self, lattice: CSLattice, n_turns=100, with_rf=False):
        """"""
        if with_rf:
            raise Exception('Unfinished. 4D tracking only.')
        self.data = np.zeros((len(self.xrange) * len(self.yrange), 5))
        i = 0
        for y in self.yrange:
            for x in self.xrange:
                try:
                    symplectic_track([x, 0, y, 0, 0, self.delta], lattice, n_turns, record = False)
                    self.data[i, :] = [x, y, 0, np.inf, np.inf]
                    i += 1
                except ParticleLost as p:
                    self.data[i, :3] = [x, y, 1]
                    self.data[i, 3] = int(p.location / lattice.length)
                    self.data[i, 4] = p.location % (lattice.length / lattice.n_periods)
                    i += 1

    def save_data(self):
        pass


class NLine:
    """n-line mode to find dynamic aperture.

    generate n_lines, search along the lines, and split n_splits times once the particle is lost for preciser result.
    similar to ELEGANT.

    Params:
        n_lines: int = 5,
        xmax: float = 0.01,
        ymax: float = 0.01,
        n_points: int = 10,
        n_splits: int = 0,
        split_fraction=0.5,
        delta=0, momentum deviation.
        verbose=True, print details.

    Attributes:
        aperture, np.ndarray, (n_lines, 2) shape.
        area, m^2
        n_lines
        n_splits
        nx
        split_fraction
        xmax
        ymax
        delta
        verbose
    """
    def __init__(self,
                 n_lines: int = 5,
                 xmax: float = 0.01,
                 ymax: float = 0.01,
                 n_points: int = 10,
                 n_splits: int = 0,
                 split_fraction=0.5,
                 delta=0,
                 verbose=True) -> None:
        assert n_lines >= 3, 'n_lines at least 5.'
        self.aperture = np.zeros((n_lines, 2))
        self.area = 0
        self.n_lines = n_lines
        self.n_splits = n_splits
        self.nx = n_points
        self.split_fraction = split_fraction
        self.xmax = xmax
        self.ymax = ymax
        self.delta = delta
        self.verbose = verbose

    def search(self, lattice: CSLattice, n_turns=100, with_rf=False):
        if with_rf:
            raise Exception('Unfinished. 4D tracking only.')
        for i, theta in enumerate(np.linspace(-np.pi / 2, np.pi / 2, self.n_lines)):
            if self.verbose:
                print(f'start line {i+1}...')
            xy0 = np.zeros(2) + 1e-6
            xymax = np.array([self.xmax * np.sin(theta), self.ymax * np.cos(theta)])
            self.aperture[i, :] = self._search_line(xy0, xymax, self.nx, self.n_splits, n_turns, lattice)

        area = 0
        for i in range(self.aperture.shape[0] - 1):
            area += abs(self.aperture[i, 0] * self.aperture[i + 1, 1] - self.aperture[i, 1] * self.aperture[i+1, 0])
        self.area = area / 2

    def _search_line(self, xy0, xymax, nx, n_splits, n_turns, lattice):
        is_lost = False
        xy = np.linspace(xy0, xymax, nx + 1)
        for i in range(nx):
            try:
                symplectic_track([xy[i+1, 0], 0, xy[i+1, 1], 0, 0, self.delta], lattice, n_turns, record=False)
            except ParticleLost as p:
                xy0 = xy[i, :]
                nx = int(1 / self.split_fraction)
                xymax = xy[i+1, :]
                is_lost = True
                if n_splits > 0:
                    return self._search_line(xy0, xymax, nx, n_splits - 1, n_turns, lattice)
        if is_lost:
            if self.verbose:
                print(f'    Particle lost at ({xymax[0]*1e3:.1f}, {xymax[1]*1e3:.1f}) mm.')
            return xy0
        else:
            if self.verbose:
                print('    Particle survived.')
            return xymax
    
    def save(self, filename=None, header=None):
        """header: String that will be written at the beginning of the file."""
        filename = 'DynamicAperture.csv' if filename is None else filename
        if header is None:
            header = ''
        else:
            header += '\n'
        header += f'{self.n_lines} lines, search range: ({self.xmax}, {self.ymax}), n_points: {self.nx}, number of split: {self.n_splits}, split fraction: {self.split_fraction}\n'
        header += f'x y area={self.area}'
        np.savetxt(filename, self.aperture, fmt='%10.6f', comments='#', header=header)


class DynamicAperture(object):
    """find dynamic aperture of lattice"""

    def __init__(self, lattice, grid) -> None:
        pass

    def search(self):
        pass


class LocalMomentumAperture(object):
    """local momentum aperture.

    generate n_lines, search along the lines, and split n_splits times once the particle is lost for preciser result.
    similar to ELEGANT.

    Params:
        ds: float or a dictionary {'Drift': float, 'HBend': float, 'Quadrupole': float, 'Sextupole': float, 'Octupole': float}.
        delta_negative_start: float = 0.0,
        delta_positive_start: float = 0.0,
        delta_negative_limit: float = -0.05,
        delta_positive_limit: float = 0.05,
        delta_step = 0.01,
        n_splits: int = 1,
        split_fraction=0.5,
        verbose=True, print details.

    Attributes:
        s: np.array.
        min_delta: np.array.
        max_delta: np.array.
    """

    def __init__(self, lattice: CSLattice, ds=None,
            delta_negative_start=0, delta_positive_start=0, delta_negative_limit=-0.1, delta_positive_limit=0.1, delta_step=0.01,
            n_splits=1, split_fraction=0.5, verbose=True):
        if ds is None:
            ds = 0.1
            ele_slices = lattice.slice_elements(ds, ds, ds, ds, ds)
        elif isinstance(ds, float):
            ele_slices = lattice.slice_elements(ds, ds, ds, ds, ds)
        elif isinstance(ds, dict):
            ele_slices = lattice.slice_elements(ds['Drift'], ds['HBend'], ds['Quadrupole'], ds['Sextupole'], ds['Octupole'])
        else:
            raise Exception("ds: float or a dictionary {'Drift': float, 'HBend': float, 'Quadrupole': float, 'Sextupole': float, 'Octupole': float}")
        self.newlattice = CSLattice(ele_slices[:-1])
        self.newlattice.linear_optics()
        self.n_periods = lattice.n_periods
        self.delta_negative_start=delta_negative_start
        self.delta_positive_start=delta_positive_start
        self.delta_negative_limit=delta_negative_limit
        self.delta_positive_limit=delta_positive_limit
        self.delta_step=delta_step
        self.n_splits=n_splits
        self.split_fraction=split_fraction
        self.verbose=verbose
        nums_ = len(self.newlattice.elements)
        self.s = np.zeros(nums_)
        self.max_delta = np.zeros(nums_)
        self.min_delta = np.zeros(nums_)

    def search(self, n_turns=100, parallel=False):
        if parallel:
            pass
        else:
            nums_ = len(self.s) - 1
            for i in range(nums_):
                sub_lattice = self.newlattice.elements[i:-1] + self.newlattice.elements[:i]
                self.s[i] = sub_lattice[0].s
                if isinstance(sub_lattice[0], Mark) and (i > 0):
                    self.min_delta[i] = self.min_delta[i-1]
                    self.max_delta[i] = self.max_delta[i-1]
                else:
                    if self.verbose:
                        print(f'Start search MA at s={sub_lattice[0].s:.3f} m ({sub_lattice[0].name})............... {i + 1} / {nums_}')
                    self.min_delta[i] = self._search_one_position(n_turns * self.n_periods, sub_lattice, 
                                              self.delta_negative_start, self.delta_negative_limit, -self.delta_step, self.n_splits)
                    self.max_delta[i] = self._search_one_position(n_turns * self.n_periods, sub_lattice, 
                                              self.delta_positive_start, self.delta_positive_limit, self.delta_step, self.n_splits)
            self.s[-1] = self.newlattice.elements[-1].s
            self.min_delta[-1] = self.min_delta[0]
            self.max_delta[-1] = self.max_delta[0]


    def _search_one_position(self, n_turns, sub_lattice, delta_init, delta_end, delta_step, n_splits):
        delta_survive = delta_init
        for dp in np.arange(delta_init, delta_end + delta_step, delta_step):
            try:
                symplectic_track([0, 0, 0, 0, 0, dp], sub_lattice, n_turns, record=False)
                delta_survive = dp
            except ParticleLost:
                if n_splits > 0:
                    return self._search_one_position(n_turns, sub_lattice, delta_survive, dp, delta_step * self.split_fraction, n_splits - 1)
                else:
                    break
        if self.verbose:
            print(f'    Particle survived at delta={delta_survive * 100:.2f}%.')
        return delta_survive
    
    def save(self, filename=None, header=None):
        """header: String that will be written at the beginning of the file."""
        filename = 'LocalMA.csv' if filename is None else filename
        if header is None:
            header = ''
        else:
            header += '\n'
        header += f'search range: ({self.delta_negative_start}, {self.delta_negative_limit}) + ({self.delta_positive_start}, {self.delta_positive_limit}), step: {self.delta_step}, number of split: {self.n_splits}, split fraction: {self.split_fraction}\n'
        header += 's delta_min delta_max'
        ma_data = np.vstack((self.s, self.min_delta, self.max_delta)).T
        np.savetxt(filename, ma_data, fmt='%10.6f', comments='#', header=header)


