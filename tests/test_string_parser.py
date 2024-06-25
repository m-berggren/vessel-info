from src.string_parser import compare_vessel_names


def test_compare_vessel_names():
    # Test cases
    name1 = "X-PRESS%20MULHACEN"
    name2 = "X_PRESS_MULHACEN"
    name3 = "X PRESS MULHACEN"
    name4 = "XPRESS MULHACEN"

    assert compare_vessel_names(name1, name2) == True
    assert compare_vessel_names(name1, name3) == True
    assert compare_vessel_names(name1, name4) == True
    assert compare_vessel_names(name2, name3) == True
    assert compare_vessel_names(name2, name4) == True
    assert compare_vessel_names(name3, name4) == True

    assert compare_vessel_names("", "") == True
    assert compare_vessel_names("%20", "") == True
    assert compare_vessel_names(" X-PRESS", "XPRESS") == True
    assert compare_vessel_names("X-PRESS", "Y-PRESS") == False