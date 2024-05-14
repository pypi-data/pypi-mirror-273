from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tabulate import tabulate
from pathlib import Path
from pyspark.sql import SparkSession
from tabulate import tabulate

import boto3
import os
import fastparquet
import pydeequ
import pandas as pd
import botocore
import yaml

import re
import os
import logging
import pydeequ
import yaml

from datetime import datetime
from functools import reduce

from pydeequ.checks import (
    Check,
    CheckLevel,
)
from pydeequ.verification import (
    VerificationSuite,
    VerificationResult,
)
from pydeequ.analyzers import *
from pyspark.sql import (
    DataFrame,
    functions as f,
    SparkSession,
)
from pyspark.sql.utils import AnalysisException
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
)
from pyspark.sql.functions import when


class DataQualityValidation:
    """This module contains DataQualityValidation class.

    Contains data quality validation checks on a pyspark dataframe.
    Contains generic methods of data checking like uncity cheks,
    not null checks, consistency checks and others which are still in
    development

    Args:
        spark (pyspark.sql.SparkSession) : Sparksession needed to run pydeequ and read pyspark df
        data_path (str) : s3 path to the table location we want to run checks on
        config (dict) : configuration of which checks to run
        dest_path (str) : path where the deequ checks result will be saved on

    """

    def __init__(
        self,
        spark: SparkSession,
        data_path: str,
        dest_path: str,
        config: dict,
        **kwargs,
    ) -> None:

        super().__init__(**kwargs)

        # initiate spark session
        self.spark = spark or (
            SparkSession.builder.appName("data_quality_validation")
            .enableHiveSupport()
            .config("spark.dynamicAllocation.enabled", "true")
            .config("spark.jars.packages", pydeequ.deequ_maven_coord)
            .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
            .config("spark.default.parallelism", "10")
            .config("spark.sql.shuffle.partitions", "10")
            .config("spark.sql.files.ignoreCorruptFiles", "true")
            .getOrCreate()
        )
        self.data_path = data_path
        self.dest_path = dest_path
        self.config = config

    """
    def _init_dq_results_df(self) -> DataFrame:

        dq_results_schema = StructType(
            [
                StructField("table_name", StringType(), True),
                StructField("dq_assertions", StringType(), True),
                StructField("mode", StringType(), True),
                StructField("status", StringType(), True),
                StructField("message", StringType(), True),
            ]
        )

        dq_results_df = self.spark.createDataFrame(
            data=[],
            schema=dq_results_schema,
        )

        return dq_results_df
    """

    def _get_check_level(
        self,
        mode: str,
    ) -> CheckLevel:
        if mode == "STRICT":
            return CheckLevel.Error
        elif mode == "WARNING":
            return CheckLevel.Warning
        else:
            return CheckLevel.Warning

    def dq_validation_unique(
        self,
        source_cfg_unique: dict,
        verification: VerificationSuite,
    ) -> DataFrame:
        """add check to verify if a column has only unique records"""
        verification = verification.addCheck(
            Check(
                self.spark,
                self._get_check_level(
                    source_cfg_unique["MODE"],
                ),
                "UNIQUE",
            ).hasUniqueness(
                source_cfg_unique["PK"],
                lambda x: x == 1.0,
            )
        )

    def dq_validation_not_null(
        self,
        source_cfg_not_null: dict,
        verification: VerificationSuite,
    ) -> DataFrame:
        """add check if a column has non null records"""
        for column in source_cfg_not_null["COLUMNS"]:
            verification = verification.addCheck(
                Check(
                    self.spark,
                    self._get_check_level(source_cfg_not_null["MODE"]),
                    "NOT_NULL",
                ).isComplete(column)
            )

    def dq_validation_not_missing(
        self,
        source_cfg_not_missing: dict,
        verification: VerificationSuite,
    ) -> DataFrame:
        """Perform data quality checks on expected values."""

        not_missing_values = source_cfg_not_missing["VALUES"]
        not_missing_mode = source_cfg_not_missing["MODE"]

        for condition in not_missing_values:
            verification = verification.addCheck(
                Check(
                    self.spark,
                    self._get_check_level(not_missing_mode),
                    "NOT_MISSING",
                ).satisfies(condition, "NOT_MISSING", lambda x: x > 0.0)
            )

    def dq_validation_consistency(
        self,
        source_cfg_consistency: dict,
        verification: VerificationSuite,
    ) -> DataFrame:
        """Perform data quality checks on data consistency conditions."""

        consistency_conditions = source_cfg_consistency["CONDITIONS"]
        consistency_mode = source_cfg_consistency["MODE"]

        for condition in consistency_conditions:
            verification = verification.addCheck(
                Check(
                    self.spark,
                    self._get_check_level(consistency_mode),
                    "CONSISTENCY",
                ).satisfies(
                    condition,
                    "CONSISTENCY",
                    lambda x: x == 1.0,
                )
            )

    def run_analysis(
        self,
        spark,
        table : DataFrame,
        output_path: str,
    )-> None:

        analysisResult = AnalysisRunner(spark) \
                        .onData(table) \
                        .addAnalyzer(Size()) \
                        .run()
        analysisResult_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysisResult)
        analysisResult_df = analysisResult_df.withColumn("column_name", f.lit(""))
        for column in table.schema.names :
            analysisResult_chunk = (
                AnalysisRunner(spark)
                .onData(table)
                .addAnalyzer(CountDistinct(column))
                .addAnalyzer(Completeness(column))
                .addAnalyzer(DataType(column))
                .addAnalyzer(Distinctness(column))
                .addAnalyzer(Mean(column))
                .addAnalyzer(UniqueValueRatio([column]))
                .addAnalyzer(Uniqueness([column]))
                .run()
            )
            analysisResult_chunk_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysisResult_chunk)
            analysisResult_chunk_df = analysisResult_chunk_df.withColumn("column_name", f.lit(column))
            analysisResult_chunk_df = analysisResult_chunk_df.withColumn("name",
                                                                         when(analysisResult_chunk_df.name == "Distinctness",
                                                                              "Duplicate_Percentage").otherwise(f.col("name")))
            analysisResult_chunk_df = analysisResult_chunk_df.withColumn("value",
                                                                         when(analysisResult_chunk_df.name == "Duplicate_Percentage",
                                                                              (1.00 - f.col("value"))* 100).otherwise(f.col("value"))
                                                                         )
            analysisResult_chunk_df = analysisResult_chunk_df.withColumn("name",
                                                                         when(analysisResult_chunk_df.name == "Completeness",
                                                                              "Null_Percentage").otherwise(f.col("name")))
            analysisResult_chunk_df = analysisResult_chunk_df.withColumn("value",
                                                                         when(analysisResult_chunk_df.name == "Null_Percentage",
                                                                              (1.00 - f.col("value"))* 100).otherwise(f.col("value"))
                                                                         )
            analysisResult_df = analysisResult_df.union(analysisResult_chunk_df)

        analysisResult_df.repartition("column_name").write.partitionBy("column_name").mode("overwrite").parquet(output_path)

    def _save_results(
        self,
        results: list,
        path: str,
    ):
        if results:
            reduce(DataFrame.unionByName, results,).withColumn(
                "created_date", f.lit(datetime.now())
            ).withColumn(
                "snapshot_date", f.lit(datetime.now().strftime("%Y-%m-%d"))
            ).repartition(
                "stg_table",
                "snapshot_date",
            ).write.mode(
                "append"
            ).partitionBy(
                "stg_table",
                "snapshot_date",
            ).parquet(
                path
            )

    def execute(
        self,
    ) -> None:
        """Execute data quality validation key steps and process results."""

        deequ_results = []
        tbl_name = re.sub("^s3://", "", self.data_path,).rstrip("/").split(
            "/"
        )[-1]

        if self.config["ACTIVE"] == 0:
            logging.info(
                "Data Quality checks deactivated for %s.",
                tbl_name,
            )
        else:
            try:
                data_df = self.spark.read.parquet(self.data_path).cache()
            except AnalysisException as exception:
                logging.exception(f"Unable to read staging data (hint: no records?)")
                status = "KO"
                log_msg = (
                    f"{tbl_name} - AVAILABILITY validation " f"completed: {status}."
                )
                logging.error(log_msg)

                temp_results = self.spark.createDataFrame(
                    [
                        (
                            tbl_name,
                            "AVAILABILITY",
                            "STRICT",
                            status,
                            log_msg,
                        )
                    ]
                )
                deequ_results.append(self._init_dq_results_df().union(temp_results))

            verification = VerificationSuite(self.spark).onData(data_df)

            if "UNIQUE" in self.config:
                self.dq_validation_unique(self.config["UNIQUE"], verification)

            if "NOT_NULL" in self.config:
                self.dq_validation_not_null(self.config["NOT_NULL"], verification)

            if "NOT_MISSING" in self.config:
                self.dq_validation_not_missing(self.config["NOT_MISSING"], verification)

            if "CONSISTENCY" in self.config:
                self.dq_validation_consistency(self.config["CONSISTENCY"], verification)


            deequ_results.append(
                VerificationResult.checkResultsAsDataFrame(
                    self.spark,
                    verification.run(),
                ).withColumn("stg_table", f.lit(tbl_name))
            )

        self.run_analysis(
            self.spark,
            data_df,
            f"{self.dest_path}/data_quality_validation/pydeequ/analysis/{tbl_name}"
        )

        if deequ_results:
            self._save_results(
                deequ_results, (f"{self.dest_path}" "/data_quality_validation/pydeequ/checks/{tbl_name}")
            )
            print(deequ_results)
            self.spark.sparkContext._gateway.shutdown_callback_server()
            self.spark.stop()


class sendEmailNotification:
    """ This class is used to send email notifications after validating the Data.
    """
    
    def __init__(
        self, 
        source_path: str, 
        target_path: dict, 
        email_config: dict, 
        **kwargs) -> None:
        """_summary_

        Args:
            source_path (str): Path to source data.
            target_path (str): Path to target data.
            email_config (dict): Email configuration settings.
        """
        os.environ["SPARK_VERSION"] = "3.0.1"
        path = Path(__file__).resolve().parent
        print(path)

        # Perform data quality validation and get result DataFrame
        self.result_df = self.execute_data_quality_validation(target_path)

        # Check if DataFrame is not empty
        if self.result_df is not None and not self.result_df.empty:  
            self.result_str = tabulate(self.result_df, headers='keys', tablefmt='grid')
            self.send_email(email_config, self.result_df)


    def execute_data_quality_validation(
        self, 
        target_path
        ):
        """ converts target data into a DataFrame

        Args:
            target_path (str): Path to target data.

        Returns:
            (pd.DataFrame): Result DataFrame
        """

        result_df = pd.read_parquet(target_path, engine='fastparquet')       
        return  result_df.loc[~result_df['check'].isna()] 


    def send_email(
        self, 
        email_config: dict, 
        result_df: pd.DataFrame
        ) -> None:
        """_summary_

        Args:
            email_config (dict): Email configuration settings.
            result_df (pd.DataFrame):  Result DataFrame
        """
        if result_df is None or result_df.empty:
            print("Error: Result DataFrame is None or empty. Cannot send email.")
            return

        # Save the result DataFrame to a temporary Parquet file
        temp_file_path = "temp_result.parquet"
        result_df.to_parquet(temp_file_path, index=False)

        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = "Data Quality Validation Result"
        msg['From'] = email_config["sender_email"]
        msg['To'] = email_config["receiver_email"]

        # Add the test message to the email body
        body = "Hello,\n\nPlease find the attached data quality validation result in Parquet format.\n\nBest regards,\nYour Team"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the Parquet file to the email
        with open(temp_file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(temp_file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(temp_file_path)}"'
            msg.attach(part)

        # Send the email using SES
        session = boto3.Session(
            aws_access_key_id=email_config["aws_access_key_id"],
            aws_secret_access_key=email_config["aws_secret_access_key"],
            aws_session_token=email_config["aws_session_token"]
        )

        ses = session.client('ses', region_name=email_config["aws_region"])
        response = ses.send_raw_email(RawMessage={'Data': msg.as_string()})

        # Delete the temporary Parquet file after sending the email
        os.remove(temp_file_path)

        print("Email sent successfully!")
        print("Message ID:", response['MessageId'])



class DqvPydeequ:
    """Class for performing data quality validation using PyDeequ"""

    def __init__(
        self,
        config_path: str,
        source_path: str,
        target_path: str,
        **kwargs
    ) -> None:
        """Initialize the DqvPydeequ class.

        Args:
            config_path (str): Path to configuration file.
            source_path (str): Path to source data.
            target_path (str): Path to target data.
        """

        spark = (
            SparkSession.builder.appName("data_quality_validation_pydeequ")
            .enableHiveSupport()
            .config("spark.dynamicAllocation.enabled", "true")
            .config("spark.jars.packages", pydeequ.deequ_maven_coord)
            .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
            .config("spark.default.parallelism", "10")
            .config("spark.sql.shuffle.partitions", "10")
            .config("spark.sql.files.ignoreCorruptFiles", "true")
            .getOrCreate()
        )
        with open(config_path, "r") as stream:
            data = yaml.safe_load(stream)
        config = data["DQ_ASSERTIONS"]["DIR1"]["PRODUCT_FILE"]
        print(config)
        try:
            bolosse = DataQualityValidation(
                spark,
                source_path,
                target_path,
                config,
            )
            bolosse.execute()
            spark.stop()
        except Exception as ex:
            print(ex)
            spark.stop()
