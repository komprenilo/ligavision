/*
 * Copyright 2022 Rikai authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.spark.sql.rikai

import org.apache.spark.sql.catalyst.FunctionIdentifier
import org.apache.spark.sql.catalyst.analysis.{
  UnresolvedAttribute,
  UnresolvedFunction
}
import org.apache.spark.sql.catalyst.expressions.{
  Expression,
  ExpressionInfo,
  Literal
}
import org.apache.spark.sql.catalyst.plans.logical.LogicalPlan
import org.apache.spark.sql.rikai.expressions.{Area, IOU, Image, ToStruct}
import org.apache.spark.sql.{SparkSession, SparkSessionExtensions}


/** Rikai SparkSession extensions to enable Spark SQL ML.
  */
class LigaImageExtensions extends (SparkSessionExtensions => Unit) {

  override def apply(extensions: SparkSessionExtensions): Unit = {
    extensions.injectFunction(
      new FunctionIdentifier("area"),
      new ExpressionInfo("org.apache.spark.sql.rikai.expressions", "Area"),
      (exprs: Seq[Expression]) => Area(exprs.head)
    )

    extensions.injectFunction(
      new FunctionIdentifier("iou"),
      new ExpressionInfo("org.apache.spark.sql.rikai.expressions", "IOU"),
      (exprs: Seq[Expression]) => IOU(exprs.head, exprs(1))
    )

    extensions.injectFunction(
      new FunctionIdentifier("to_struct"),
      new ExpressionInfo("org.apache.spark.sql.rikai.expressions", "ToStruct"),
      (exprs: Seq[Expression]) => ToStruct(exprs.head)
    )

    extensions.injectFunction(
      new FunctionIdentifier("image"),
      new ExpressionInfo("org.apache.spark.sql.rikai.expressions", "Image"),
      (exprs: Seq[Expression]) => Image(exprs.head)
    )
  }
}
