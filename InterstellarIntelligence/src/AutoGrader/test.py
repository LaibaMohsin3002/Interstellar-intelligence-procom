import os
import sys

import pytest

FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def update_path():
    """
    Sets the path for submission directory. This is necessary to
    import submission.py in Github workflow.
    """

    directory = FILE_DIR
    parent = os.path.abspath(os.path.join(directory, "..", 'Submission'))

    if parent not in sys.path:
        sys.path.insert(0, parent)


update_path()

import submission
import calculation


variable_strings = [
    "temperature",
    "cloud_density",
    "photosynthesis",
    "plants_density",
    "oxygen",
    "carbon_dioxide",
    "asi",
    "rainfall_intensity",
    "radius_of_wet_ground",
    "rainfall_area",
    "power",
    "uv_index",
    "pollution",
    "health_risk",
    "crop_yield",
    "hunger",
    "water_resources",
    "thirst",
]

def test_team_name():
    teams = [
        "Team 1",
        "Team 2",
        "Team 3",
        "Team 4",
        "Team 5",
        "Team 6",
        "Team 7",
        "Team 8",
        "Team 9",
        "Team 10",
    ]

    assert hasattr(submission, "TEAM_NAME"), "TEAM_NAME not found in submission.py"
    assert submission.TEAM_NAME in teams, "TEAM_NAME is not valid"

def test_computation():
    """
    Tests the computation of variables using the engine built from the evaluation order
    defined in the submission module.
    The test performs the following checks:
    1. Ensures that the 'evaluation_order' attribute exists in the submission module.
    2. Initializes a dictionary of independent variables.
    3. Builds the computation engine using the evaluation order.
    4. Computes the variables using the engine and the independent variables.
    5. Asserts that the computation does not raise any exceptions.
    6. Asserts that the computed variables are not None.
    7. Asserts that the independent variables are not modified.
    8. Checks that all expected variable strings are present in the computed variables.
    9. Asserts that the number of computed variables is correct (18 plus the number of independent variables).
    Raises:
        AssertionError: If any of the assertions fail.
    """
    
    assert hasattr(
        submission, "evaluation_order"
    ), "evaluation_order not found in submission.py"

    indep_vars = {
        "solar_intensity": 0, 
        "humidity": 0, 
        "wind_speed": 0, 
        "population": 0
    }

    engine = calculation.build_engine(submission.evaluation_order)
    vars = None
    try:
        vars = engine.compute(indep_vars)
    except Exception as e:
        assert False, f"Error in compute method: {e}"

    assert vars is not None, "No variables computed"
    assert vars is not indep_vars, "indep_vars should not be modified"

    for variable in variable_strings:
        assert variable in vars, f"{variable} not found in computed variables"

    assert len(vars) == 18 + len(indep_vars), "Incorrect number of variables computed"