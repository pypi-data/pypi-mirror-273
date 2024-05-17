# {# pkglts, glabpkg_dev
import chalhoub2017


def test_package_exists():
    assert chalhoub2017.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert chalhoub2017.pth_clean.exists()
    try:
        assert chalhoub2017.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
