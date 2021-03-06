
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program,  If not, see <http://www.gnu.org/licenses/>.


import pandas
from openfisca_france.reforms import reform_cd

from openfisca_france.tests import base

from openfisca_france_data.input_data_builders import get_input_data_frame
from openfisca_france_data.surveys import SurveyScenario
import openfisca_france_data


def simulate_reform_cd(year):
    assert year is not None
    TaxBenefitSystem = openfisca_france_data.init_country()
    tax_benefit_system = TaxBenefitSystem()
    reform = reform_cd.build_reform(tax_benefit_system)
    input_data_frame = get_input_data_frame(year)
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        used_as_input_variables = ['sal', 'cho', 'rst', 'age_en_mois', 'smic55'],
        year = year,
        tax_benefit_system = reform
        )
    reference_simulation = survey_scenario.new_simulation(debug = True, reference = True)
    reform_simulation = survey_scenario.new_simulation(debug = True)

    reform_data_frame_by_entity_key_plural = dict(
        foyers = pandas.DataFrame(
            dict([(name, reference_simulation.calculate_add(name)) for name in [
                'impo',
                'rfr',
                ]])
            ),
        )

    return reform_data_frame_by_entity_key_plural, reference_simulation


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    year = 2009

    data_frame_by_entity_key_plural, simulation = simulate_reform_cd(year)
    data_frame_individus = data_frame_by_entity_key_plural['individus']
    data_frame_foyers = data_frame_by_entity_key_plural['foyers']
