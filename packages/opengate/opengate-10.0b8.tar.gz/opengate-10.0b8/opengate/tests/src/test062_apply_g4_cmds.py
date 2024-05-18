#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from box import Box
import opengate as gate
import opengate_core as g4
from opengate.tests import utility


def print_em_parameters(simulation_engine):
    em = g4.G4EmParameters.Instance()
    sec_model = str(em.PIXECrossSectionModel())
    esec_model = str(em.PIXEElectronCrossSectionModel())
    simulation_engine.hook_log = Box(
        {
            "bearden": em.FluoDirectory(),
            "pixe_sec_model": sec_model,
            "epixe_sec_model": esec_model,
        }
    )


if __name__ == "__main__":
    paths = utility.get_default_test_paths(__file__)

    # create simulation
    sim = gate.Simulation()

    # physics
    mm = gate.g4_units.mm
    eV = gate.g4_units.eV
    MeV = gate.g4_units.keV

    # fake source
    source = sim.add_source("GenericSource", "source")
    source.particle = "gamma"
    source.energy.mono = 1 * MeV
    source.direction.type = "iso"
    source.n = 1

    # physics
    sim.physics_manager.physics_list_name = "QGSP_BERT_EMZ"
    sim.user_hook_after_init = print_em_parameters

    # start simulation
    sim.run(start_new_process=True)
    h = sim.output.hook_log
    print("output", h)
    is_ok = h.bearden == 0 and h.pixe_sec_model == "Empirical"

    # redo with different fluo dir
    sim.add_g4_command_after_init("/process/em/pixeXSmodel ECPSSR_ANSTO")
    sim.add_g4_command_before_init("/process/em/fluoBearden true")
    sim.run(start_new_process=True)
    h = sim.output.hook_log
    print("output", h)
    is_ok = h.bearden == 1 and h.pixe_sec_model == "ECPSSR_ANSTO" and is_ok

    # redo with different fluo dir
    try:
        sim.add_g4_command_after_init("/process/em/fluoBearden true")
        sim.run(start_new_process=True)
        # The above should have caused an exception
        # not OK if it has not.
        is_ok = False
    except:
        print("This is CORRECT if it throws an exception")

    utility.test_ok(is_ok)
