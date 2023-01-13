#  Copyright 2021 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Vision related Spark UDFs.
"""

# Standard library
import os
from pathlib import Path
from typing import List, Optional, Union

# Third Party
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import (
    ArrayType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

# Liga
from liga.io import copy as _copy
from liga.logging import logger
from liga.numpy import ndarray
from ligavision.spark.types.vision import ImageType
from ligavision.types.geometry import Box2d
from ligavision.types.video import (
    Segment,
    SingleFrameSampler,
    VideoStream,
    YouTubeVideo,
)
from ligavision.types.vision import Image

__all__ = [
    "crop",
    "to_image",
    "image_copy",
    "numpy_to_image",
    "video_metadata",
    "video_metadata_schema",
]


@udf(returnType=ImageType())
def to_image(image_data: Union[bytes, bytearray, str, Path]) -> Image:
    """Build an :py:class:`Image` from
    bytes, file-like object, str, or :py:class:`~pathlib.Path`.

    Parameters
    ----------
    image_data : bytes, bytearray, str, Path
        The resource identifier or bytes of the source image.

    Return
    ------
    img: Image
        An Image from the given embedded data or URI

    Example
    -------

    >>> df = spark.read.format("image").load("<path-to-data>")
    >>>
    >>> df.withColumn("new_image", to_image("image.data"))
    """
    return Image(image_data)


@udf(returnType=ImageType())
def image_copy(img: Image, uri: str) -> Image:
    """Copy the image to a new destination, specified by the URI.

    Parameters
    ----------
    img : Image
        An image object
    uri : str
        The base directory to copy the image to.

    Return
    ------
    Image
        Return a new image pointed to the new URI
    """
    logger.info("Copying image src=%s dest=%s", img.uri, uri)
    return Image(_copy(img.uri, uri))


@udf(returnType=ImageType())
def numpy_to_image(
    array: ndarray, uri: str, format: str = None, **kwargs
) -> Image:
    """Convert a numpy array to image, and upload to external storage.

    Parameters
    ----------
    array : :py:class:`numpy.ndarray`
        Image data.
    uri : str
        The base directory to copy the image to.
    format : str, optional
        The image format to save as. See
        `supported formats <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save>`_ for details.
    kwargs : dict, optional
        Optional arguments to pass to `PIL.Image.save <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save>`_.

    Return
    ------
    Image
        Return a new image pointed to the new URI.

    Example
    -------

    >>> spark.createDataFrame(..).registerTempTable("df")
    >>>
    >>> spark.sql(\"\"\"SELECT numpy_to_image(
    ...        resize(grayscale(image)),
    ...        lit('s3://asset')
    ...    ) AS new_image FROM df\"\"\")

    See Also
    --------
    :py:meth:`ligavision.types.vision.Image.from_array`
    """  # noqa: E501
    return Image.from_array(array, uri, format=format, **kwargs)


video_metadata_schema = StructType(
    [
        StructField("width", IntegerType(), True),
        StructField("height", IntegerType(), True),
        StructField("num_frames", IntegerType(), True),
        StructField("duration", FloatType(), True),
        StructField("bit_rate", IntegerType(), True),
        StructField("frame_rate", IntegerType(), True),
        StructField("codec", StringType(), True),
        StructField("size", IntegerType(), True),
        StructField(
            "_errors",
            StructType(
                [
                    StructField("message", StringType(), True),
                    StructField("stderr", StringType(), True),
                    StructField("probe", StringType(), True),
                ]
            ),
            True,
        ),
    ]
)


@udf(returnType=video_metadata_schema)
def video_metadata(video: Union[str, VideoStream]) -> dict:
    """Return useful video stream metadata like width, height, num_frames,
    duration, bit_rate, frame_rate, codec, and size about the given video

    Parameters
    ----------
    video: str or VideoStream
        The video uri or the Video object

    Returns
    -------
    result: dict
        The keys are: width, height, num_frames, duration, bit_rate,
        frame_rate, codec, size, and _errors

    Notes
    -----
    The frame_rate is rounded to the nearest whole number of frames per sec

    Examples
    --------
    The following returns the fps rounded to the nearest integer:

    import ligavision.spark.functions as RF
    (spark.createDataFrame([(VideoStream(<uri>),)], ['video'])
    .withColumn('meta', RF.video_metadata('video'))
    .select('meta.data.frame_rate'))

    """
    probe_result = _probe(video)
    if probe_result.get("_errors", None):
        return probe_result

    video_stream = next(
        (
            stream
            for stream in probe_result.get("streams", [])
            if stream.get("codec_type", None) == "video"
        ),
        None,
    )
    if video_stream is None:
        return _error("No video stream found", probe=probe_result)

    try:
        return {
            "width": _int_or_none(video_stream, "width"),
            "height": _int_or_none(video_stream, "height"),
            "num_frames": _int_or_none(video_stream, "nb_frames"),
            "frame_rate": _fps_or_none(video_stream),
            "duration": _float_or_none(video_stream, "duration"),
            "bit_rate": _int_or_none(video_stream, "bit_rate"),
            "codec": video_stream.get("codec_name", None),
            "size": _int_or_none(probe_result.get("format", {}), "size"),
        }
    except Exception as e:
        return _error(str(e))


def _probe(video):
    try:
        import ffmpeg
    except ImportError as e:
        raise ImportError(
            "Couldn't import ffmpeg. Please make sure to "
            "`pip install ffmpeg-python` explicitly or install "
            "the correct extras like `pip install ligavision[video]`"
        ) from e

    uri = video.uri if isinstance(video, VideoStream) else video
    try:
        return ffmpeg.probe(uri)
    except Exception as e:
        return _error(str(e), stderr=getattr(e, "stderr", None))


def _int_or_none(data, key):
    return int(data[key]) if key in data else None


def _float_or_none(data, key):
    return float(data[key] if key in data else None)


def _fps_or_none(data: dict) -> Optional[int]:
    # ffprobe returns frame rate in timebase units (as a fraction)
    avg_frame_rate = data.get("avg_frame_rate", None)
    if avg_frame_rate is None:
        return None
    n, d = [int(x) for x in avg_frame_rate.split("/")]
    if d == 0:
        raise ValueError("avg_frame_rate had 0 time base")
    return int(round(n / d))


def _error(message, stderr=None, probe=None):
    err = {"message": message}
    if stderr is not None:
        err["stderr"] = stderr.decode("utf-8", "backslashreplace")
    if probe is not None:
        err["probe"] = str(probe)
    return {"_errors": err}


@udf(returnType=ArrayType(ImageType(), True))
def crop(img: Image, box: Union[Box2d, List[Box2d]]):
    """Crop image specified by the bounding boxes, and returns the cropped
    images.

    Parameters
    ----------
    img : Image
        An image object to be cropped.
    box : Box2d or List of Box2d
        One bound-2d box or a list of such boxes.

    Returns
    -------
    [Image]
        Return a list of cropped images.

    Examples
    --------

    >>> spark.sql("SELECT crop(img, boxes) as patches FROM detections")

    """
    return img.crop(box)
