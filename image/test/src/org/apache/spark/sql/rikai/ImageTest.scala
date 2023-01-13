package org.apache.spark.sql.rikai

import org.scalatest.FunSuite

class ImageTest extends FunSuite with SparkTestSession {

  test("image udf") {
    val uri = "s3://path/to/image.png"
    val df = spark.sql(s"select image('${uri}') as image")
    assert(df.collect().head.get(0).toString === s"Image('${uri}')")
  }
}
