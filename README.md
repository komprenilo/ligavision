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
| Purpose | Operator | Notebook |
|---------|----------|----------|
| Image Scaling | `*` | [DSL for Image Scaling](notebooks/DSLImageScale.ipynb) |
| Image Overlays | `\|` | [DSL for Image Overlays](notebooks/DSLImageOverlay.ipynb) |
| Overlay Attributes | `@` | [DSL for Overlay Attributes](notebooks/DSLOverlayAttribute.ipynb)

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
| UDF | Syntax | Notebooks |
|-----|--------|-----------|
| `crop` | `select crop(image, box2d)` | [crop.ipynb](notebooks/crop.ipynb) |

> TODO: more live notebooks for UDFs.

## History
The initial Liga Vision is consisted of [spark-video](https://github.com/eto-ai/spark-video) and the vision DSL/UDT/UDF part of [Rikai](https://github.com/eto-ai/rikai).
