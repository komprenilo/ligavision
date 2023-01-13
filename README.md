# Liga Vision: the Liga solution for Computer Vision
## Developers' Guide
### Cheatsheet for mill
``` bash
## video
./mill 'video[2.12].test'
./mill 'video[2.12].test.testOnly' '**.MLImageTest.scala'
./mill 'video[2.12].assembly'

## image
./mill 'image[2.12].test'
./mill 'image[2.12].assembly'

## format
./mill mill.scalalib.scalafmt.ScalafmtModule/checkFormatAll __.sources
./mill mill.scalalib.scalafmt.ScalafmtModule/reformatAll __.sources
```

## History
The initial Liga Vision is consisted of [spark-video](https://github.com/eto-ai/spark-video) and the vision DSL/UDT/UDF part of [Rikai](https://github.com/eto-ai/rikai).
