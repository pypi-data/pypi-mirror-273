# {# pkglts, glabpkg_dev
import allen1989


def test_package_exists():
    assert allen1989.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert allen1989.pth_clean.exists()
    try:
        assert allen1989.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
