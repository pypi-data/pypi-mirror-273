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

from typing import List
from zonevu.zonevu.DataModels.Geosteering.Pick import Pick
from zonevu.zonevu.DataModels.Geospatial.GeoLocation import GeoLocation
from zonevu.zonevu.DataModels.Geospatial.Coordinate import Coordinate
from zonevu.zonevu.Zonevu import Zonevu
from zonevu.zonevu.Services.Client import ZonevuError
from zonevu.zonevu.Services.WellService import WellData
from zonevu.zonevu.DataModels.Geosteering.Calcs import create_extended_picks
from zonevu.zonevu.Services.GeosteeringService import PickAdjustEnum
from tabulate import tabulate
from ...DataModels.Geosteering.Calcs import make_evenly_spaced_picks
from ...DataModels.Geosteering.Blocks import make_blocks_and_faults, Block, Fault


def main_evenly_spaced(zonevu: Zonevu, well_name: str):
    """
    Retrieve well data from ZoneVu
    For the first geosteering interpretation, create flattened geosteering picks.
    """
    well_svc = zonevu.well_service
    well = well_svc.get_first_named(well_name)
    if well is None:
        raise ZonevuError.local('Could not find the well "%s"' % well_name)

    well_name = well.full_name
    print('Well named "%s" was successfully found' % well_name)
    well_svc.load_well(well)  # Load surveys and geosteering into well
    wellbore = well.primary_wellbore  # Get reference to wellbore
    if wellbore is None:
        print('Well has no wellbores, so exiting')
        return

    # Get geosteering interpretation using geosteering service, so we can specify special parameters for sampling
    geosteer_svc = zonevu.geosteering_service
    interp_entries = geosteer_svc.get_interpretations(wellbore.id)
    has_geosteering = len(interp_entries) > 0
    if has_geosteering:
        interp_entry = next((g for g in interp_entries if g.starred),
                            interp_entries[0])  # Get starred or first interpretation
        # Get interpretation with picks interpolated to every 1 ft (or meters)
        interp = geosteer_svc.get_interpretation(interp_entry.id)
        evenly_spaced_picks = make_evenly_spaced_picks(interp=interp, interval=1, first_md=9000)

        print('%s evenly spaced geosteering picks created with an interval of %s %s' %
              (len(evenly_spaced_picks), 1, zonevu.distance_units))
        print()
