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
#
#

import copy
from ...Zonevu import Zonevu
from ...Services.WellService import WellData
from ...Services.Error import ZonevuError
from typing import Dict


def main_copy_well(zonevu: Zonevu, well_name: str, delete_code: str):
    """
    Retrieve a well and its surveys and make a copy
    :param zonevu: Zonevu instance
    :param well_name: Name of well to work with
    :param delete_code: delete code to use if an existing copy will be deleted
    :return:
    NOTES:
    1- we are copying a well and all of its constituent child data, including surveys, well logs, tops, etc. We will do
       a "Phase I" copy of all of this, except the geosteering interpretations.
    2- we will also copy the geosteering interpretations -- this will be "Phase II".
       This is a special case because these refer to other wells, namely, type wells.
       We will assume that those wells are not being copied, therefore the references in the
       geosteering interpretations to those wells will remain valid.
    3- The geosteering interpretations also refer to LWD well log curves on this well that is being copied. Those
       references need to be updated since we have copied in Phase I the well logs on this very well.
    """
    well_svc = zonevu.well_service
    geosteer_svc = zonevu.geosteering_service

    well = well_svc.get_first_named(well_name, True)
    well_svc.load_well(well, {WellData.all})  # Load well and its surveys
    print('Copying Well %s%s (id=%d, UWI=%s)' % (well.name, well.number, well.id, well.uwi))
    print()

    well_copy_name = '%s_Copy' % well.name
    well_copy_uwi = '%s 3' % well_copy_name
    print('Copy will be named "%s"' % well_copy_name)

    # Delete well
    try:
        existing_copy = well_svc.find_by_uwi(well_copy_uwi)
        if existing_copy is not None:
            well_svc.delete_well(existing_copy.id, delete_code)
            print("Successfully deleted existing copy of the well named '%s'" % well_copy_name)
    except ZonevuError as error:
        print("Execution failed because %s" % error.message)
        raise error

    # Phase I - create and save a copy of the well and all its child data, except interpretations
    # NOTE: well_svc.create_well updates all the system ids on the well and all of its children to the new saved ids.
    #       We will use those new system ids below.
    well_copy = copy.deepcopy(well)
    well_copy.name = well_copy_name
    well_copy.uwi = well_copy_uwi
    well_svc.create_well(well_copy, {WellData.surveys, WellData.logs, WellData.curves, WellData.tops,
                                     WellData.notes, WellData.fracs})

    # Phase II - copy the geosteering interpretations, update curve defs that refer to this wellbores logs, & save.
    # Make a lookup dict that relates the well log curves in the original well to the curves in the copied well.
    wb_orig = well.primary_wellbore
    wb_copy = well_copy.primary_wellbore
    curve_lut = {orig.id: cpy.id for orig, cpy in zip(wb_orig.well_log_curves, wb_copy.well_log_curves)}
    grp_lut = {orig.id: cpy.id for orig, cpy in zip(wb_orig.well_log_curve_groups, wb_copy.well_log_curve_groups)}

    # Update curve defs in geosteering interpretations that refer to this wellbores logs
    for interp in wb_orig.interpretations:
        interp_copy = copy.deepcopy(interp)  # Make a copy of the interpretation
        curve_defs = [d for d in interp_copy.curve_defs if d.curve_id in curve_lut or d.curve_group_id in grp_lut]

        for d in curve_defs:    # For curve defs that refer to this well, and update them to correct system ids
            if d.curve_id is not None:
                d.curve_id = curve_lut[d.curve_id]   # Update the curve def curve id reference
            if d.curve_group_id is not None:
                d.curve_group_id = grp_lut[d.curve_group_id]  # Update the curve def curve id reference

        geosteer_svc.add_interpretation(wb_copy.id, interp_copy)  # Save interp onto well copy

    print('Well copy for %s%s (id=%d, UWI=%s) succeeded' % (well_copy.name, well_copy.number, well_copy.id, well_copy.uwi))
    print()

