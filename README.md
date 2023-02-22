# Liga Vision: Let Data Dance with Computer Vision Models
+ `ligavision-dsl`: A clean DSL library to manipulate Image/Video
+ `ligavision`: Apache Spark UDTs and UDFs for Computer Vision on Liga

## Image DSL
### Syntax
``` python
# image scaling
image * scale_factor
image * (width_scale_factor, height_scale_factor)

# image overlays
image | box2d
image | text
image | mask
image | box2d | text

# overlay attributes
image | box2d @ {"color": "#000000"}
image | mask @ {"color": "#FFF6B0"}
image | text @ {"color": "#000000"} | box2d
```

### Notebooks
| Purpose | Operator | Notebook | Google Colab Notebook |
|---------|----------|----------|-----------------------|
| Image Scaling | `*` | [DSL for Image Scaling](notebooks/DSLImageScale.ipynb) | <a href="https://colab.research.google.com/github/liga-ai/ligavision/blob/main/notebooks/DSLImageScale.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> |
| Image Overlays | `\|` | [DSL for Image Overlays](notebooks/DSLImageOverlay.ipynb) | <a href="https://colab.research.google.com/github/liga-ai/ligavision/blob/main/notebooks/DSLImageOverlay.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> |
| Overlay Attributes | `@` | [DSL for Overlay Attributes](notebooks/DSLOverlayAttribute.ipynb) | <a href="https://colab.research.google.com/github/liga-ai/ligavision/blob/main/notebooks/DSLOverlayAttribute.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> |

## Apache Spark UDTs and UDFs
### UDTs
| UDT | What |
|---------|-----------------|
| `box2d` | 2D bounding box |
| `box3d` | 3D bounding box |
| `mask` | 2D mask |
| `image` | Image |

UDT schema name could be used as part of the model type schema name. For example:
``` python
class ObjectDetectionModelType(TorchModelType):
    def schema(self) -> str:
        return (
            "array<struct<
              box:box2d,
              score:float,
              label_id:int,
              label:string
            >>"
        )

    ...

```

### UDFs
| UDF | Syntax | Notebooks | Google Colab |
|-----|--------|-----------|--------------|
| `crop` | `select crop(image, array(box2d))` | [crop](notebooks/UDF_crop.ipynb) | <a href="https://colab.research.google.com/github/liga-ai/ligavision/blob/main/notebooks/UDF_crop.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> |

> TODO: more live notebooks for UDFs.

## History
The initial Liga Vision is consisted of [spark-video](https://github.com/eto-ai/spark-video) and the vision DSL/UDT/UDF part of [Rikai](https://github.com/eto-ai/rikai).
