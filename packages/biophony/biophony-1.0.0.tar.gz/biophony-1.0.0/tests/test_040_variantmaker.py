# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
import biophony

def test_rates_sum():

    # Rates sum is 1.0 ==> OK
    _ = biophony.VariantMaker(ins_rate = 0.4, del_rate = 0.4,
                            mut_rate = 0.2)

    # Rates sum > 1.0 ==> ERROR
    with pytest.raises(ValueError):
        _ = biophony.VariantMaker(ins_rate = 0.4, del_rate = 0.4,
                                mut_rate = 0.200001)
