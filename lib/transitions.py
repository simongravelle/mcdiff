#!/usr/bin/env python
#
# copyright: Gerhard Hummer (NIH, July 2012)
# An Ghysels (August 2012)
#

import numpy as np
from reading import guess_dim_transition_square, read_transition_square
from reading import read_transition_header
from reading import guess_dim_transition_cube, read_transition_cube

"""
lt  --  lag time between snapshots [in ps]
dt  --  time between two subsequent frames [in ps] (as if time unit)
dn  --  number of frames between two snapshots [type: int]
        so lt = dn*dt
dim_lt  --  number of lag times
dim_trans  --  dimension of transition matrix
count  --  how transitions were counted [pbc, cut, ...]
"""

class Transitions(object):
    def __init__(self,list_filenames):
        self.started = False
        self.dim_lt = len(list_filenames)  # number of lagtimes (lt)
        assert self.dim_lt > 0
        self.list_filenames = list_filenames
        # initialize
        self.list_lt = []
        self.list_dt = []
        self.list_dn = []
        self.list_trans = []
        for filename in list_filenames:
            self.read_transition(filename)
        # convert
        self.list_lt = np.array(self.list_lt)
        self.list_dt = np.array(self.list_dt)
        self.list_dn = np.array(self.list_dn)
        self.list_trans = np.array(self.list_trans)
        print "trans:",self.list_trans.shape
        self.min_lt = min(self.list_lt)

    def read_transition(self,filename):
        dim_trans = guess_dim_transition_square(filename)
        header = read_transition_header(filename)
        transmatrix = read_transition_square(filename,dim_trans)

        if not self.started: # initialize settings
            self.started = True
            self.count = header['count']
            self.dim_trans = dim_trans
            if 'edges' in header:
                self.edges = header['edges']
            else:
                self.edges = np.arange(self.dim_trans+1.)
        else: # assert same settings
            assert self.count == header['count']
            assert self.dim_trans == dim_trans
            if 'edges' in header:
                assert (self.edges == header['edges']).all()

        self.list_lt.append(header['lt'])
        self.list_dt.append(header['dt'])
        self.list_dn.append(header['dn'])
        self.list_trans.append(transmatrix)

class RadTransitions(object):
    def __init__(self,list_filenames):
        self.started = False
        self.dim_lt = len(list_filenames)  # number of lagtimes (lt)
        assert self.dim_lt > 0
        self.list_filenames = list_filenames
        # initialize
        self.list_lt = []
        self.list_dt = []
        self.list_dn = []
        self.list_trans = []
        for filename in list_filenames:
            self.read_transition(filename)
        # convert
        self.list_lt = np.array(self.list_lt)
        self.list_dt = np.array(self.list_dt)
        self.list_dn = np.array(self.list_dn)
        self.list_trans = np.array(self.list_trans)
        print "trans:",self.list_trans.shape
        self.min_lt = min(self.list_lt)

    def read_transition(self,filename):
        dim_rad,dim_trans = guess_dim_transition_cube(filename)
        header = read_transition_header(filename)   # same function....
        transmatrix = read_transition_cube(filename,dim_rad,dim_trans)

        if not self.started: # initialize settings
            self.started = True
            self.count = header['count']
            self.dim_trans = dim_trans
            self.dim_rad = dim_rad
            if 'edges' in header:
                self.edges = header['edges']
            else:
                self.edges = np.arange(self.dim_trans+1.)
            if 'redges' in header:
                self.redges = header['redges']
            else:
                raise Error("I should have had radial edges in header")
        else: # assert same settings
            assert self.count == header['count']
            assert self.dim_trans == dim_trans
            assert self.dim_rad == dim_rad
            if 'edges' in header:
                assert (self.edges == header['edges']).all()
            if 'redges' in header:
                assert (self.redges == header['redges']).all()

        self.list_lt.append(header['lt'])
        self.list_dt.append(header['dt'])
        self.list_dn.append(header['dn'])
        self.list_trans.append(transmatrix)
