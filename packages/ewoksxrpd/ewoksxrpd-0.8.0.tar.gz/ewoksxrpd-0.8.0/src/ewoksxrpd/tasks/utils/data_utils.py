import os
from typing import Mapping, Union, Optional
from typing_extensions import TypeGuard
from numbers import Number

import numpy
import h5py
from silx.io.url import DataUrl
from blissdata.h5api import dynamic_hdf5
import fabio.edfimage
import fabio.tifimage


def hdf5_url(file_name: str, data_path: str) -> str:
    if not os.path.isabs(file_name):
        file_name = os.path.abspath(file_name)
    return f"silx://{file_name}?path={data_path}"


def is_data(data) -> TypeGuard[Union[numpy.ndarray, Number, str, list]]:
    if isinstance(data, (numpy.ndarray, Number)):
        return True
    if isinstance(data, (str, list)) and data:
        return True
    return False


def data_from_storage(data, remove_numpy=True):
    if isinstance(data, numpy.ndarray):
        if not remove_numpy:
            return data
        elif data.ndim == 0:
            return data.item()
        else:
            return data.tolist()
    elif isinstance(data, Mapping):
        return {
            k: data_from_storage(v, remove_numpy=remove_numpy)
            for k, v in data.items()
            if not k.startswith("@")
        }
    else:
        return data


def link_bliss_scan(
    outentry: h5py.Group, bliss_scan_url: Union[str, DataUrl], **options
):
    if isinstance(bliss_scan_url, str):
        bliss_scan_url = DataUrl(bliss_scan_url)
    file_path = bliss_scan_url.file_path()
    data_path = bliss_scan_url.data_path()
    out_filename = outentry.file.filename
    ext_filename = os.path.relpath(out_filename, os.path.dirname(file_path))
    if ".." in ext_filename:
        ext_filename = file_path
    with dynamic_hdf5.File(file_path, mode="r", **options) as root:
        inentry = root[data_path]
        # Link to the entire group
        for groupname in ("instrument", "sample"):
            try:
                if groupname in outentry or groupname not in inentry:
                    continue
            except Exception:  # fixed by bliss PR !5435
                continue
            outentry[groupname] = h5py.ExternalLink(
                ext_filename, inentry[groupname].name
            )
        # Link to all sub groups
        for groupname in ("measurement",):
            if groupname not in inentry:
                continue
            igroup = inentry[groupname]
            if groupname in outentry:
                ogroup = outentry[groupname]
            else:
                ogroup = outentry.create_group(groupname)
                ogroup.attrs["NX_class"] = igroup.attrs["NX_class"]
            for name in igroup.keys():
                if name in ogroup:
                    continue
                if name not in ogroup:
                    ogroup[name] = h5py.ExternalLink(ext_filename, igroup[name].name)


def convert_to_3d(data: Union[numpy.ndarray, Number, str, list]):
    data_arr = numpy.array(data)

    if data_arr.ndim >= 3:
        return data_arr

    if data_arr.ndim == 2:
        return data_arr.reshape(1, *data_arr.shape)

    if data_arr.ndim == 1:
        return data_arr.reshape(1, 1, *data_arr.shape)

    return data_arr.reshape(1, 1, 1)


def save_image(
    data: numpy.ndarray,
    save_path: str,
    save_name: str,
    monitor_data: Optional[Number] = None,
    metadata: Optional[dict] = None,
    ext: str = "edf",
) -> str:
    normalized_data = data / monitor_data if monitor_data else data

    header = dict(
        Summed_monitor_counts=str(monitor_data) if monitor_data else "nan",
        **(metadata if metadata else {}),
    )

    ext = ext.lower()
    img_filepath = f"{save_path}/{save_name}.{ext}"
    if ext.lower() == "edf":
        Image = fabio.edfimage.EdfImage
    elif ext == "tiff" or ext == "tif":
        Image = fabio.tifimage.TifImage
    else:
        raise ValueError(f"Unsupported ext {ext}. Only supports EDF and TIFF.")

    img = Image(data=normalized_data, header=header)
    img.write(img_filepath)

    return img_filepath
