import mill._
import mill.scalalib._
import mill.scalalib.publish._
import mill.scalalib.scalafmt._
import mill.modules.Assembly
import mill.modules.Assembly.Rule.ExcludePattern
import $ivy.`org.bytedeco:javacpp:1.5.6`

class ImageModule(majorVersion: String) extends CrossScalaModule with PublishModule with ScalafmtModule {
  override def crossScalaVersion: String = majorVersion match {
    case "2.12" => "2.12.13"
    case "2.13" => "2.13.7"
    case _ => ???
  }

  override def publishVersion = "0.2.0"

  override def artifactId = s"liga-image_${majorVersion}"

  override def pomSettings = PomSettings(
    description = "Image related UDT/UDF on Apache Spark",
    organization = "ligaai",
    licenses = Seq(License.Common.Apache2),
    url = "https://github.com/liga-ai/liga-vision",
    versionControl = VersionControl.github("liga-ai", "liga-vision"),
    developers = Seq(
      Developer("da-tubi", "Darcy Shen", "https://github.com/da-tubi")
    )
  )

  override def compileIvyDeps = Agg(
    ivy"org.apache.spark::spark-sql:3.2.0",
  )

  def assemblyRules = Assembly.defaultRules ++ Seq(ExcludePattern("scala/.*"))

  object test extends Tests with TestModule.ScalaTest {
    override def ivyDeps = Agg(
      ivy"org.apache.spark::spark-sql:3.2.0",
      ivy"org.scalatest::scalatest:3.0.8",
      ivy"ch.qos.logback:logback-classic:1.2.3",
    )

    override def forkEnv = Map("LOG_LEVEL" -> "ERROR")
  }
}

object image extends mill.Cross[ImageModule]("2.12", "2.13")


class VideoModule(majorVersion: String) extends CrossScalaModule with PublishModule with ScalafmtModule {
  override def crossScalaVersion: String = majorVersion match {
    case "2.12" => "2.12.13"
    case "2.13" => "2.13.7"
    case _ => ???
  }

  override def publishVersion = "0.2.0"

  override def artifactId = s"liga-video_${majorVersion}"

  override def pomSettings = PomSettings(
    description = "Processing Videos on Apache Spark",
    organization = "eto.ai.rikai",
    licenses = Seq(License.Common.Apache2),
    url = "https://github.com/liga-ai/liga-vision",
    versionControl = VersionControl.github("liga-ai", "spark-vision"),
    developers = Seq(
      Developer("da-tubi", "Darcy Shen", "https://github.com/da-tubi")
    )
  )

  def javacppVersion = "1.5.6"

  override def compileIvyDeps = Agg(
    ivy"org.apache.spark::spark-mllib:3.2.0",
    ivy"com.amazonaws:aws-java-sdk-s3:1.11.173"
  )

  override def ivyDeps = Agg(
    ivy"org.bytedeco:javacv:${javacppVersion}",
    ivy"org.bytedeco:ffmpeg:4.4-${javacppVersion}",
    ivy"com.typesafe.scala-logging::scala-logging:3.9.4"
  )

  def assemblyRules = Assembly.defaultRules ++ Seq(ExcludePattern("scala/.*"))

  object test extends Tests with TestModule.ScalaTest {
    def javacppPlatform = org.bytedeco.javacpp.Loader.Detector.getPlatform

    override def ivyDeps = Agg(
      ivy"org.bytedeco:ffmpeg:4.4-${javacppVersion};classifier=${javacppPlatform}",
      ivy"org.apache.spark::spark-mllib:3.2.0",
      ivy"com.amazonaws:aws-java-sdk-s3:1.11.173",
      ivy"org.scalatest::scalatest:3.0.8",
      ivy"ch.qos.logback:logback-classic:1.2.3",
      ivy"com.typesafe.scala-logging::scala-logging:3.9.4"
    )

    override def forkEnv = Map("LOG_LEVEL" -> "ERROR")
  }
}

object video extends mill.Cross[VideoModule]("2.12", "2.13")