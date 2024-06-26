import pandas as pd
import pytest
from fyskemqc.parameter import Parameter
from fyskemqc.qc_configuration import QcConfiguration


def given_parameter_with_data(data: dict):
    parameter_series = pd.Series(data)
    return Parameter(parameter_series)


@pytest.mark.parametrize(
    "given_parameter_name, expected_min, expected_max",
    (
        ("ALKY", 0, 5000),
        ("AMON", 0, 1500),
        ("CNDC_CTD", 0, 5),
        ("CPHL", 0, 150),
        ("DEPH", 0, 4000),
        ("DOXY_BTL", 0, 12),
        ("DOXY_CTD", 0, 12),
        ("H2S", 0, 2000),
        ("HUMUS", 0, 100),
        ("NTOT", 0, 1500),
        ("NTRA", 0, 300),
        ("NTRI", 0, 20),
        ("NTRZ", 0, 350),
        ("PRES_CTD", 0, 1000),
        ("SALT_BTL", 0, 36),
        ("SALT_CTD", 0, 36),
        ("TEMP_BTL", -1, 24),
        ("TEMP_CTD", -1, 24),
        ("TOC", 0, 10),
    ),
)
def test_range_check_default_qc_configuration(
    given_parameter_name, expected_min, expected_max
):
    # Given a parameter
    parameter = given_parameter_with_data({"parameter": given_parameter_name})

    # When creating a configuration
    given_configuration = QcConfiguration()

    # Then the default values can be retrieved
    retrieved_configuration = given_configuration.get("range_check", parameter)

    assert retrieved_configuration.min_range_value == expected_min
    assert retrieved_configuration.max_range_value == expected_max


@pytest.mark.parametrize(
    "given_parameter_name, expected_limit",
    (
        (
            "ALKY",
            0.5,
        ),
        ("AMON", 0.2),
        ("CPHL", 0.2),
        ("DOXY_BTL", 0.1),
        ("DOXY_CTD", 0.2),
        ("H2S", 4),
        ("NTOT", 5),
        ("NTRA", 0.1),
        ("NTRI", 0.02),
        ("NTRZ", 0.1),
    ),
)
def test_limit_detection_check_default_qc_configuration(
    given_parameter_name, expected_limit
):
    # Given a parameter
    parameter = given_parameter_with_data({"parameter": given_parameter_name})

    # When creating a configuration
    given_configuration = QcConfiguration()

    # Then the default value can be retrieved
    retrieved_configuration = given_configuration.get("detection_limit_check", parameter)

    assert retrieved_configuration.limit == expected_limit
