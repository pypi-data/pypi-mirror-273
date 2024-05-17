from pygff import load
from .datadir import datadir


def test_loading(datadir):
    path = datadir / "minimal.gff"

    with open(path, "rb") as f:
        gff = load(f)
        assert gff[0] == 0


def test_loading_segmentation(datadir):
    path = datadir / "minimal_seg.segff"
    with open(path, "rb") as f:
        segff = load(f)
        assert segff[0] == 0
        assert segff.info is not None
        meta_dict = segff.info.meta
        assert meta_dict["Project info"] is not None
        assert meta_dict["Project info"]["ClassColors"] == "0 0 0 255"
        assert meta_dict["Project info"]["ClassIndices"] == "0"
        assert meta_dict["Project info"]["ClassNames"] == "unclassified"
