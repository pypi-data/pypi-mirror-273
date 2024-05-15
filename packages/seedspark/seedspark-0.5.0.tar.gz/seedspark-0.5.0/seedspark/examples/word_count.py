from typing import Any, Dict, List, Optional

from pyspark.sql import SparkSession

from seedspark.sparkapp import SparkApps


class SimpleLineCountApp(SparkApps):
    def __init__(  # noqa: PLR0913
        self,
        app_name: str,
        file_path: str,
        extra_packages: Optional[List[str]] = None,
        extra_jars: Optional[List[str]] = None,
        extra_configs: Optional[Dict[str, Any]] = None,
        spark_master: Optional[str] = None,
        environment="staging",
        log_env: bool = True,
        existing_spark_session: Optional[SparkSession] = None,  # New parameter to accept an existing session
    ):
        self.file_path = file_path
        super().__init__(
            app_name,
            extra_packages=extra_packages,
            extra_jars=extra_jars,
            extra_configs=extra_configs,
            spark_master=spark_master,
            environment=environment,
            log_env=log_env,
            existing_spark_session=existing_spark_session,
        )

    def execute(self):
        # Load data
        data = self.spark.read.text(self.file_path)
        # Count the number of lines
        line_count = data.count()
        print(f"Number of lines in the file: {line_count}")
        return line_count


# line_count_app = SimpleLineCountApp(app_name="a",
#                                     file_path = ".")
# line_count_app.execute()
