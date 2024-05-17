# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert {{ base.pkg_full_name }}.pth_clean.exists()
    try:
        assert {{ base.pkg_full_name }}.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
