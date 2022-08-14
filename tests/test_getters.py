import pytest
from randomizer.utils import (
    filter_handles_by_exe_name,
    get_all_handles,
    get_exe_from_process_id,
    get_half_handles,
    get_process_id_from_handle,
)


@pytest.mark.unit
def test_get_all_handles():
    """Checks that at least one handle is returned, test invalid direction"""
    handles = get_all_handles()
    assert len(handles) > 0
    with pytest.raises(Exception):
        get_half_handles(0, None)


@pytest.mark.unit
def test_filter_by_exe():
    """Does a second run through the scummvm handles, tests that they
    belong to scummvm"""
    handles = get_all_handles()
    filtered_handles, _ = filter_handles_by_exe_name(handles)
    # This will fail there is no ScummVM instance open.
    assert len(filtered_handles) > 0
    for handle in filtered_handles:
        id = get_process_id_from_handle(handle)
        exe = get_exe_from_process_id(id)
        assert "scummvm" in exe
