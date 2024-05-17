# {# pkglts, glabpkg_dev
import alsina2011


def test_package_exists():
    assert alsina2011.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert alsina2011.pth_clean.exists()
    try:
        assert alsina2011.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
