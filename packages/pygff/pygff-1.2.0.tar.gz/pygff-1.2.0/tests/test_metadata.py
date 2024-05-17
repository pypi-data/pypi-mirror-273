from pygff import load, GFFInfo
from .datadir import datadir


def test_get_metadata(datadir):
    path = datadir / "minimal_seg.segff"
    with open(path, "rb") as f:
        seg = load(f)
        info = seg.info
        assert info is not None

        assert info.get_rotation() is not None
        assert info.get_rotation().shape == (3, 3)
        info.set_rotation(info.get_rotation())

        assert info.get_translation() is not None
        assert info.get_translation().shape == (3,)
        info.set_translation(info.get_translation())

        assert info.get_class_names() == ["unclassified"]
        assert info.get_class_indices() == [0]
        assert info.get_class_colors() == [(0, 0, 0, 255)]
        assert info.get_class_dict() == {
            "unclassified": {"index": 0, "color": (0, 0, 0, 255)}
        }
