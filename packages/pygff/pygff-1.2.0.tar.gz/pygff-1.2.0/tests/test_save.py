from pygff import load, save, GFF, GFFInfo
import numpy as np
import pathlib
import pytest
from tests.datadir import datadir


def test_saving(datadir):
    path = datadir / "minimal.gff"
    gff = load(path)

    output_path = datadir / "minimal_out.gff"

    with open(output_path, "wb") as f:
        save(f, gff)

    gff_new = load(output_path)

    assert np.array_equal(gff, gff_new)


def test_saving_array(datadir):
    test_array = np.ndarray((1, 1, 1, 1, 1))
    test_info = GFFInfo()
    test_gff = GFF(test_array, test_info)
    arr_path = datadir / "minimal_arr.gff"
    save(open(arr_path, "wb"), test_gff)
    assert np.array_equal(test_gff, load(arr_path))


def test_empty_segff(datadir):
    gff = GFF()
    metadata = gff.info

    with pytest.raises(ValueError):  # no "ProjectInfo" set
        metadata.get_class_dict()

    save(datadir / "minimal_out.segff", gff)

    segff = load(datadir / "minimal_out.segff")
    # assert np.array_equal(gff, segff) # fails as GFF is always loaded as 5D

    assert segff.info.get_class_dict() == {
        "unclassified": {"index": 0, "color": (0, 0, 0, 255)}
    }


def test_add_class(datadir):
    gff = GFF()
    gff.info.set_class_dict({"test": {"index": 1, "color": (255, 0, 0, 255)}})
    class_dict = gff.info.get_class_dict()
    assert class_dict == {
        "unclassified": {"index": 0, "color": (0, 0, 0, 255)},
        "test": {"index": 1, "color": (255, 0, 0, 255)},
    }

    gff.info.add_class(
        new_class={"name": "test2", "index": 2, "color": (0, 255, 0, 255)}
    )
    assert gff.info.get_class_dict() == {
        "unclassified": {"index": 0, "color": (0, 0, 0, 255)},
        "test": {"index": 1, "color": (255, 0, 0, 255)},
        "test2": {"index": 2, "color": (0, 255, 0, 255)},
    }

    save(datadir / "add_class.segff", gff)


if __name__ == "__main__":
    tmp_dir = pathlib.Path("tests/testdata")
    test_saving(tmp_dir)
    test_saving_array(tmp_dir)
    test_empty_segff(tmp_dir)
    test_add_class(tmp_dir)
