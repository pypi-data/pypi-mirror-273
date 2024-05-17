import numpy as np
import copy

__all__ = ["GFF", "StepInfo", "GFFInfo"]


class StepInfo:
    """Class for timestep and channel metadata."""

    def __init__(self, equidistant=True, centers=None, widths=None):
        self.equidistant = equidistant
        self.centers = [0] if centers is None else centers
        self.widths = [0] if widths is None else widths
        if len(self.centers) != len(self.widths):
            raise ValueError(
                "Centers ({}) and widths ({}) lengths are not equal.".format(
                    len(self.centers), len(self.widths)
                )
            )

    def len(self):
        return len(self.centers)

    def __str__(self):
        return "Equidistant: {}\nCenters: {}\nWidths: {}".format(
            self.equidistant, self.centers, self.widths
        )

    def __repr__(self):
        return "StepInfo({},{},{})".format(
            self.equidistant, self.centers.__repr__(), self.widths.__repr__()
        )


class GFFInfo:
    """Class for all necessary GFF metadata."""

    def __init__(
        self,
        meta=None,
        affine=None,
        voxel_sizes=None,
        intensity_scale=1.0,
        intensity_offset=0.0,
        times=None,
        channels=None,
    ):
        if isinstance(meta, GFFInfo):
            raise TypeError(
                "Metadata must be a dictionary. Please use the .copy() method for a deep copy of a GFFInfo object."
            )
        self.meta = {} if meta is None else meta
        self.affine = np.eye(N=4, M=4) if affine is None else affine
        self.voxel_sizes = (
            np.array([1.0, 1.0, 1.0]) if voxel_sizes is None else voxel_sizes
        )
        self.intensity_scale = intensity_scale
        self.intensity_offset = intensity_offset
        self.times = StepInfo() if times is None else times
        self.channels = StepInfo() if channels is None else channels
        # self.shape is not required as it already is an attribute of the ndarray.

    def __str__(self):
        return "--- self.info --- \n\
Meta: {meta}\n\
Affine: {affine}\n\
Voxel sizes: {voxel_sizes}\n\
Intensity scale: {intensity_scale}\n\
Intensity offset: {intensity_offset}\n\
Timepoints: {times}\n\
Channels: {channels}\n".format(
            meta=self.meta,
            affine=self.affine,
            voxel_sizes=self.voxel_sizes,
            intensity_scale=self.intensity_scale,
            intensity_offset=self.intensity_offset,
            times=self.times,
            channels=self.channels,
        )

    def get_rotation(self):
        """Returns the 3x3 rotation matrix from the metadata."""
        return self.affine[0:3, 0:3]

    def set_rotation(self, rotation):
        """Sets the rotation matrix in the metadata"""
        if rotation.shape != (3, 3):
            raise ValueError("Rotation matrix must be 3-by-3.")
        res = np.matmul(self.affine[0:3, 0:3], rotation)
        self.affine[0:3, 0:3] = res

    def get_translation(self):
        """Returns the 3x1 translation vector from the metadata."""
        return np.array(self.affine[0:3, 3])

    def set_translation(self, translation):
        """Sets the 3x1 translation vector in the metadata."""
        if len(translation) != 3:
            raise ValueError("Translation matrix must have three entries.")
        self.affine[0:3, 3] = translation

    def copy(self):
        """Returns a deep copy of GFFInfo object."""
        return copy.deepcopy(self)

    def get_class_names(self):
        """Returns a list of class names from the metadata."""
        try:
            proj_info = self.meta["Project info"]
            class_names = proj_info["ClassNames"]  # A|B|C...
            names_list = class_names.split("|")
            return names_list
        except KeyError:
            raise ValueError("No segmentation classes.")

    def get_class_indices(self):
        """Returns a list of class indices from the metadata."""
        try:
            proj_info = self.meta["Project info"]
            class_names = proj_info["ClassIndices"]
            ind_list = class_names.split("|")
            return [int(i) for i in ind_list]
        except KeyError:
            raise ValueError("No segmentation classes.")

    def get_class_colors(self):
        """Returns a list of class colors (rgba) from the metadata."""
        try:
            proj_info = self.meta["Project info"]
            class_names = proj_info["ClassColors"]
            col_list = class_names.split("|")  # b g r a
            new_list = []
            for c in col_list:
                tmp = c.split(" ")
                new_list.append((int(tmp[2]), int(tmp[1]), int(tmp[0]), int(tmp[3])))
            return new_list

        except KeyError:
            raise ValueError("No segmentation classes.")

    def get_class_dict(self):
        """Returns a dictionary with class names as keys and a dictionary of 'color' and 'index' as value."""
        class_dict = {}
        try:
            names = self.get_class_names()
            indices = self.get_class_indices()
            colors = self.get_class_colors()

            for i in range(len(names)):
                class_dict[names[i]] = {"index": indices[i], "color": colors[i]}
            return class_dict

        except:
            raise ValueError("No segmentation classes.")

    def __set_default_segmentation_dict(self):
        if self.meta.get("Project info") is None:
            self.meta["Project info"] = {
                "ClassColors": "0 0 0 255",
                "ClassIndices": "0",
                "ClassNames": "unclassified",
            }

    def __add_class(
        self, prof_dict: dict, class_name: str, class_color: tuple, class_index: int
    ) -> None:
        try:
            prof_dict["ClassNames"] += "|" + str(class_name)
            assert len(class_color) == 4
            for c in class_color:
                if not 0 <= c <= 255:
                    raise ValueError(f"Class color values must be between 0 and 255.")
            prof_dict["ClassColors"] += "|" + " ".join(
                [
                    str(class_color[2]),
                    str(class_color[1]),
                    str(class_color[0]),
                    str(class_color[3]),
                ]
            )  # stored as BGRA
            prof_dict["ClassIndices"] += "|" + str(class_index)
        except:
            raise ValueError("Invalid new class.")

    def set_class_dict(self, class_dict: dict) -> None:
        """Sets the class dictionary in the metadata.
        Keys are class names and values are a nested dictionary of 'color' (RGBA) and 'index' (uchar) values.
        """
        try:
            self.__set_default_segmentation_dict()

            proj_info = self.meta["Project info"]

            for k, v in class_dict.items():
                self.__add_class(proj_info, str(k), v["color"], v["index"])
        except:
            raise ValueError("Invalid class dictionary.")

    def add_class(self, new_class: dict) -> None:
        """Adds a new class to the metadata dictionary.
        Keys must be "name", "color", and "index".
        """
        try:
            proj_info = self.meta["Project info"]
        except KeyError:
            print("No classes configured yet. Please use 'set_class_dict'.")
        self.__add_class(
            proj_info, new_class["name"], new_class["color"], new_class["index"]
        )

    def _correct_times_and_channels(self, shape: tuple) -> None:
        """generates required StepInfo metadata for channels and times if not set"""
        if len(self.channels.centers) != shape[0]:
            self.channels = StepInfo(
                equidistant=True,
                centers=[i for i in range(shape[0])],
                widths=shape[0] * [0],  # not required
            )
        if len(self.times.centers) != shape[1]:
            self.times = StepInfo(
                equidistant=True,
                centers=[i for i in range(shape[1])],
                widths=shape[1] * [0],
            )


class GFF(np.ndarray):
    """Representation of a GFF dataset with associated metadata ("info")."""

    def __new__(cls, input_array=None, info=None):
        obj = (
            np.zeros(5 * (1,)).view(cls)
            if input_array is None
            else np.asarray(input_array).view(cls)
        )
        obj.info = GFFInfo() if info is None else info

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.info = getattr(obj, "info", GFFInfo())

    def __str__(self):
        return str(self.info) + "Dimensions: {shape}\nArray: {array}".format(
            shape=super().shape, array=super().__str__()
        )
