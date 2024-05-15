from pyspark.sql.types import StringType, StructField, StructType, TimestampType

from seedspark.sparkapp import SparkApps


class ExploreMusicDatasetApp(SparkApps):
    # def __init__(
    #     self,
    #     app_name: str = "ExploreMusicDatasetApp",
    #     extra_packages: Optional[List[str]] = None,
    #     extra_jars: Optional[List[str]] = None,
    #     extra_configs: Optional[Dict[str, Any]] = None,
    #     spark_master: Optional[str] = None,
    #     environment="staging",
    #     log_env: bool = True,
    #     existing_spark_session: Optional[SparkSession] = None,  # New parameter to accept an existing session
    # ):
    #     super().__init__(
    #         app_name,
    #         extra_packages=extra_packages,
    #         extra_jars=extra_jars,
    #         extra_configs=extra_configs,
    #         spark_master=spark_master,
    #         environment=environment,
    #         log_env=log_env,
    #         existing_spark_session=existing_spark_session,
    #     )

    def load_data(self):
        data_path = "/Users/chethanuk/Downloads/lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv"
        schema = StructType(
            [
                StructField("userid", StringType(), True),
                StructField("timestamp", TimestampType(), True),
                StructField("artist_id", StringType(), True),
                StructField("artist_name", StringType(), True),
                StructField("song_id", StringType(), True),
                StructField("song_name", StringType(), True),
            ]
        )

        data = self.spark.read.option("sep", "\t").option("header", "false").schema(schema).csv(data_path)
        print(f"Columns: {data.columns}")
        print(f"Schema: {data.schema}")
        return data

    def execute(self, profile=False):
        df = self.load_data()

        df.registerTempTable("songs_raw")

        self.spark.sql(
            """
                       SELECT userid, COUNT(1)
                       FROM songs_raw
                       GROUP BY userid
                       """
        ).show()

        df.show(100, truncate=False)
        if profile:
            from ydata_profiling import ProfileReport

            report = ProfileReport(
                df, title="Music dataset", infer_dtypes=False, interactions=None, missing_diagrams=None
            )
            report_html = report.to_html()
            with open("report.html", "w") as f:
                f.write(report_html)

            # Count the number of lines
            line_count = df.count()

            print(f"Number of lines in the file: {line_count}")
            return line_count


__main__ = ExploreMusicDatasetApp(app_name="ExploreMusicDatasetApp").execute()
