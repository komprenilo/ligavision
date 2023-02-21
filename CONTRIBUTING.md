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
