# PyGFF
---
A Python package to read and write Grace Format files (*.gff / .segff*).

## Easiest Way To Install PyGFF
---
```bash
$ pip install pygff
```

## Basic Usage
---
1) **Loading** a *.gff* file:
	```python
	>>> from pygff import load
	>>> img5D = load("tutorials/CT140.gff")
	>>> img5D.shape
	(1, 1, 429, 211, 290)
	>>> img5D.info.voxel_sizes
	[0.14 0.14 0.14]
	```
	GFF objects are five-dimensional [numpy arrays](https://numpy.org/doc/stable/reference/arrays.html) with additional customizable metadata such as voxel sizes and channel units. The shape / indexing convention used is (channel, time, z, y, x).

2) **Saving** a numpy ndarray `np_array` as a *.gff* file:
	```python
	>>> from pygff import GFF, save
	>>> save("image.gff", GFF(np_array))
	```
	The required metadata is automatically added by the `GFF` constructor.
	
3) Saving a numpy array `seg_array` as a *.segff* (**segmentation**) file with metadata for class names, indices, and colors:
	```python
	>>> from pygff import GFF, save
	>>> segff = GFF(seg_array)
	>>> segff.info.set_class_dict(
        {"Heart": {"index": 1, "color": (255, 0, 0, 255)},
          "Liver": {"index": 2, "color": (0, 255, 0, 255)}})
	>>> save("segmentation.segff", segff)
	```
	Note that `seg_array` is converted to `np.uint8` before saving. Colors are specified as RGBA, and class index 0 is reserved for "unclassified" data.

## Tutorials
---
Tutorial notebooks can be found in the `/tutorials/` directory of [this](https://bitbucket.org/felixgremse/gff_file_format/src/master/) repository. They are not included with the PyGFF package. We recommed that you to start with `01_load_and_save.ipynb` to learn more about loading, saving, and GFF objects. More tutorials will be added in the future.

Running the examples requires the packages `jupyter`, `matplotlib`, `numpy`, and `scipy` to be installed. Also, please download the required example datasets if you have not cloned the repository yet.

## What is GFF?
---
GFF is an open source file format for multimodal biomedical images (*.gff*) and segmentations (*.segff*). The format supports datasets with up to five dimensions (three spatial dimensions, time-variant, and multi-channel) and a rich set of metadata key-value pairs. By default, the implementation uses a lossless compression algorithm to reduce file size and cryptographic hashing for secure writing. Multithreading is also used if possible to speed up reading and writing of GFF files.

The PyGFF package is developed by [Gremse-IT GmbH](https://gremse-it.com/) (Aachen, Germany) as a Python interface for [Imalytics Preclinical 3.0](https://gremse-it.com/imalytics-preclinical/) which utilizes *.gff* by default for underlay, overlay, segmentation (*.segff*), and project files (*.imaproj*). 

For more details, please refer to this publication:

> Yamoah, Grace Gyamfuah et al. “Data Curation for Preclinical and Clinical Multimodal Imaging Studies.” 
> Molecular imaging and biology vol. 21,6 (2019): 1034-1043. doi:10.1007/s11307-019-01339-0

Full text: https://pubmed.ncbi.nlm.nih.gov/30868426/

## How to build the package yourself
---
1. Clone the repository
	```bash
	$ git clone git@bitbucket.org:felixgremse/gff_file_format.git
	```
2. (Optional) Create a virtual environment, e.g. with `venv`
	```bash
	$ python -m venv env
	...
	$ source env/bin/activate
	```
	or using `conda`
	```bash
	$ conda env create --file environment.yml
	...
	$ conda activate pygff
	```
3. Then, install `pygff` in editable mode, e.g. using `build`
	```bash
	$ python -m pip install --upgrade build
	...
	$ python -m pip install -e .
	```
	or `conda-build`
	```bash
	$ conda develop .
	```
## How to run package tests
---
Make sure that `pytest` is installed and then simply call it from a shell in the main directory.
```bash
$ pytest
```

## License
---
The PyGFF package is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).

All *.gff* files, *.segff* files, and Jupyter notebooks contained in the `/tutorials/` directory of the repository are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).