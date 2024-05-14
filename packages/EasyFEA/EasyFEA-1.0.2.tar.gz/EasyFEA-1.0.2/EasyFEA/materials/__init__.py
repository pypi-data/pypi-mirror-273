# Copyright (C) 2021-2024 Université Gustave Eiffel. All rights reserved.
# This file is part of the EasyFEA project.
# EasyFEA is distributed under the terms of the GNU General Public License, Version 3 or later, see LICENSE.txt and CREDITS.txt for more information.

from ._utils import (ModelType, _IModel,
                     Reshape_variable, Heterogeneous_Array,
                     Tensor_Product,
                     KelvinMandel_Matrix, Project_Kelvin,
                     Result_in_Strain_or_Stress_field,
                     Get_Pmat, Apply_Pmat)