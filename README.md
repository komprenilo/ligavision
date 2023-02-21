# Liga Vision: Let Data Dance with Computer Vision Models
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
| Image Overlays | `\|` | [DSL for Image Overlays](notebooks/DSLImageOverlays.ipynb) |
| Overlay Attributes | `*` | [DSL for Overlay Attributes](notebooks/DSLOverlayAttribute.ipynb)


## History
The initial Liga Vision is consisted of [spark-video](https://github.com/eto-ai/spark-video) and the vision DSL/UDT/UDF part of [Rikai](https://github.com/eto-ai/rikai).
