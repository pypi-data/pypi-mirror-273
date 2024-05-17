#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#

from dataclasses import dataclass, field
from ...DataModels.Geosteering.Horizon import Horizon
from ...DataModels.Geosteering.Pick import Pick
from shapely.geometry import Polygon, LineString
from typing import List, Optional, Tuple, Union
from vectormath import Vector3, Vector2
from ...DataModels.Geospatial.GeoLocation import GeoLocation
from ...DataModels.Geospatial.Coordinate import Coordinate
from ...DataModels.Geosteering.Interpretation import Interpretation
import math
import numpy as np
from itertools import groupby
from abc import ABC, abstractmethod


@dataclass
class GeosteerItem(ABC):
    @property
    @abstractmethod
    def kind(self) -> str:
        pass

    @property
    @abstractmethod
    def next(self) -> 'GeosteerItem':
        pass


class GeosteerIter:
    """
    Iterator to easily iterate through the block and faults in MD order of a geosteering interpretation.
    """
    def __init__(self, interp: Interpretation):
        blocks, faults = make_blocks_and_faults(interp)
        self._item = blocks[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self._item.next is None:
            raise StopIteration
        else:
            item = self._item
            self._item = self._item.next
            return item


@dataclass
class Layer:
    """
    A layer in a geosteering block corresponding to a horizon in a geosteering interpretation
    """
    block: 'Block'
    horz: Horizon
    tvd_start: float
    tvd_end: float
    thickness: float

    @property
    def polygon(self) -> Polygon:
        """
        A polygon in (md, tvd) space that is a layer in a geosteering block
        :return:
        """
        s = self
        x1 = s.block.md_start
        x2 = s.block.md_end
        y1a = s.tvd_start
        y1b = y1a + s.thickness
        y2a = s.tvd_end
        y2b = y2a + s.thickness
        coordinates = [(x1, y1a), (x2, y2a), (x2, y2b), (x1, y1b)]
        p = Polygon(coordinates)
        return p


@dataclass
class Block(GeosteerItem):
    """
    A geosteering block derived from a pair of geosteering interpretation pick
    NOTE: start = the heel-ward direction, and end = the toe-ward direction
    NOTE: in the interpretation, each block is followed by either a block or a fault.
    """
    start_pick: Pick
    end_pick: Pick
    layers: List[Layer] = field(default_factory=list[Layer])
    target_layer: Optional[Layer] = None
    next_block: Optional['Block'] = None
    next_fault: Optional['Fault'] = None

    @property
    def kind(self) -> str:
        return 'Block'

    @property
    def next(self) -> 'GeosteerItem':
        next_item = self.next_fault if self.next_block is None else self.next_block
        return next_item

    @property
    def md_start(self) -> float:
        return self.start_pick.md

    @property
    def md_end(self) -> float:
        return self.end_pick.md

    @property
    def location_start(self) -> GeoLocation:
        return GeoLocation(self.start_pick.latitude, self.start_pick.longitude)

    @property
    def location_end(self) -> GeoLocation:
        return GeoLocation(self.end_pick.latitude, self.end_pick.longitude)

    @property
    def xyz_start(self) -> Coordinate:
        return Coordinate(self.start_pick.x, self.start_pick.y, self.start_pick.target_tvd)

    @property
    def xyz_end(self) -> Coordinate:
        return Coordinate(self.end_pick.x, self.end_pick.y, self.end_pick.target_tvd)

    @property
    def elevation_start(self) -> float:
        """
        Get elevation of target formation at start of block
        :return:
        """
        return self.start_pick.target_elevation

    @property
    def elevation_end(self) -> float:
        """
        Get elevation of target formation at end of block
        :return:
        """
        return self.end_pick.target_elevation

    @property
    def dip(self) -> float:
        """
        Get dip of block in direction of increasing MD
        :return:
        """
        c1 = self.xyz_start.vector
        c2 = self.xyz_end.vector
        v: Vector3 = c2 - c1  # Vector pointing along top of block
        h = Vector3(v.x, v.y, 0)  # Vector pointing along plane in direction of block
        cos_theta = v.dot(h) / (v.length * h.length)
        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        try:
            dip_radians = math.acos(cos_theta)
            dip_degrees = math.degrees(dip_radians)
            return dip_degrees
        except ValueError as err:
            return np.nan

    @property
    def inclination(self) -> float:
        dHX = self.end_pick.md - self.start_pick.md
        dTVD = self.end_pick.target_tvd - self.start_pick.target_tvd
        incl = 90 + math.atan2(-dTVD, dHX) * 180 / math.pi
        return incl

    @property
    def length(self) -> float:
        """
        Get length of block
        :return:
        """
        c1 = self.xyz_start.vector
        c2 = self.xyz_end.vector
        v: Vector3 = c2 - c1  # Vector pointing along top of block
        return v.length

    @property
    def md_length(self) -> float:
        md_len = self.md_end - self.md_start
        return md_len

    def find_next_block(self) -> Union['Block', None]:
        next_item = self.next
        if next_item is None:
            return None
        next_next_item = next_item.next
        if isinstance(next_item, Block):
            return next_item
        elif isinstance(next_next_item, Block):
            return next_next_item
        else:
            return None

    def contains_md(self, md: float):
        if self.md_start <= md < self.md_end:
            return True
        return False

    def make_pick(self, md: float) -> Pick:
        p1 = self.start_pick
        p2 = self.end_pick
        m = (md - p1.md) / (p2.md - p1.md)

        def lerp(a, b):
            return a + (b - a) * m

        c = lerp(self.xyz_start.vector, self.xyz_end.vector)
        g1 = Vector3(self.location_start.longitude, self.location_start.latitude, self.elevation_start)
        g2 = Vector3(self.location_end.longitude, self.location_end.latitude, self.elevation_start)
        g = lerp(g1, g2)
        d = lerp(Vector2(p1.dx, p1.dy), Vector2(p2.dx, p2.dy))
        tvt = lerp(p1.target_tvt, p2.target_tvt)
        elev = lerp(p1.elevation, p2.elevation)
        tvd = lerp(p1.tvd, p2.tvd)
        vx = lerp(p1.vx, p2.vx)
        p = Pick(target_tvd=c.z, x=c.x, y=c.y, md=md, block_flag=True, type_wellbore_id=p1.type_wellbore_id,
                 type_curve_def_id=p1.type_curve_def_id, latitude=g.y, longitude=g.x, target_elevation=g.z,
                 dx=d.x, dy=d.y, target_tvt=tvt, elevation=elev, tvd=tvd, vx=vx)
        return p


@dataclass
class Throw:
    """
    A throw in a geosteering fault corresponding to a horizon in a geosteering interpretation
    """
    fault: 'Fault'
    horz: Horizon
    tvd_start: float
    tvd_end: float
    throw_amt: float

    @property
    def line(self) -> LineString:
        line = LineString([(self.fault.md, self.tvd_start), (self.fault.md, self.tvd_end)])
        return line


@dataclass
class Fault:
    """
    A geosteering fault derived from a pair of geosteering interpretation picks
    NOTE: in the interpretation, each fault is followed by a block.
    """
    pick: Pick
    throws: List[Throw] = field(default_factory=list[Throw])
    target_throw: Optional[Throw] = None
    next_block: Optional[Block] = None

    @property
    def kind(self) -> str:
        return 'Fault'

    @property
    def next(self) -> 'GeosteerItem':
        return self.next_block

    @property
    def md(self) -> float:
        return self.pick.md

    @property
    def location(self) -> GeoLocation:
        return GeoLocation(self.pick.latitude, self.pick.longitude)

    def xyz(self) -> Coordinate:
        """
        XYZ of the top of target on heel-ward side of fault.
        :return:
        """
        return Coordinate(self.pick.x, self.pick.y, self.pick.target_tvd)

    @property
    def elevation(self) -> float:
        """
        Elevation of the top of target on heel-ward side of fault.
        :return:
        """
        return self.pick.target_elevation

    @property
    def trace(self) -> LineString:
        pts = [(self.md, min(t.tvd_start, t.tvd_end)) for t in self.throws]
        last_t = self.throws[-1]
        max_tvd = max(last_t.tvd_start, last_t.tvd_end)
        pts.append((self.md, max_tvd))
        return LineString(pts)


def make_blocks_and_faults(interp: Interpretation) -> Tuple[List[Block], List[Fault]]:
    """
    Computes the blocks and faults for a geosteering interpretation
    :param interp: A geosteering interpretation
    :return: a list of geosteering blocks and faults
    """
    # Make a list of layer thicknesses for each employed typewell
    interp.typewell_horizon_depths.sort(key=lambda d: d.type_wellbore_id)  # Make sure horz depths in type well order
    target_formation = interp.target_formation_id
    type_well_groups = groupby(interp.typewell_horizon_depths, key=lambda d: d.type_wellbore_id)  # Group by type well
    type_well_depth_dict = {key: list(group) for key, group in type_well_groups}  # Make depth list LUT by type well id
    for wellbore_id, h_depths in type_well_depth_dict.items():
        h_depths.sort(key=lambda h_depth: h_depth.tvt)  # Make sure lists are in TVT order

    # Create a list of geosteering blocks
    horizons_dict = {h.id: h for h in interp.horizons}  # Make a horizon lookup dictionary
    picks = interp.picks
    blocks: List[Block] = []
    faults: List[Fault] = []

    p1 = picks[0]
    last_block_or_fault: Union[Block, Fault, None] = None
    for p2 in picks[1:]:
        h_depths = type_well_depth_dict[p1.type_wellbore_id]  # Get type well horizon depths for this pick
        depth_pairs = zip(h_depths, h_depths[1:])
        if p1.block_flag:   # Create block
            block = Block(p1, p2)
            blocks.append(block)
            if last_block_or_fault is not None:
                last_block_or_fault.next_block = block
            last_block_or_fault = block
            for d, d2 in depth_pairs:
                tvd1 = p1.target_tvd + d.tvt  # Compute geometry of the layer for this horizon pair
                tvd2 = p2.target_tvd + d.tvt
                thickness = d2.tvt - d.tvt
                horizon = horizons_dict[d.horizon_id]  # Find horizon for this type well depth
                layer = Layer(block, horizon, tvd1, tvd2, thickness)
                block.layers.append(layer)  # Create layer and add to block for this pick
                if horizon.formation_id == target_formation:
                    block.target_layer = layer
        elif p1.fault_flag:  # Create fault
            fault = Fault(p1)
            faults.append(fault)
            if last_block_or_fault is not None:
                last_block_or_fault.next_fault = fault
            last_block_or_fault = fault
            for d in h_depths:
                tvd1 = p1.target_tvd + d.tvt  # Compute geometry of the layer for this horizon pair
                tvd2 = p2.target_tvd + d.tvt
                throw_amt = tvd2 - tvd1
                if math.fabs(throw_amt) > 0:
                    horizon = horizons_dict[d.horizon_id]  # Find horizon for this type well depth
                    throw = Throw(fault, horizon, tvd1, tvd2, throw_amt)
                    fault.throws.append(throw)  # Create fault throw and add to block for this pick
                    if horizon.formation_id == target_formation:
                        fault.target_throw = throw
        p1 = p2

    return blocks, faults
