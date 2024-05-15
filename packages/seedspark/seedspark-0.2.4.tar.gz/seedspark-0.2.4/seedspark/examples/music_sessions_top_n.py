from typing import Optional

import sqlglot
from pyspark.sql.types import StringType, StructField, StructType, TimestampType
from sqlglot.errors import ErrorLevel

from seedspark.sparkapp import SparkApps


class LastFMSessionsApp(SparkApps):
    """
    Session Top 50 approach:
    ------------------------
    Session - One or More songs by UserID
        Song started 20min of prevSong start_time
        Time delta between two rows is not greather than 20mins


    Find Top 50 longest sessions by tracks count
        Top 50 longest sesions = Sessions with highest Count
    # Also Remove duplicates before doing track count top 50 filter

    List of Top 10 songs in Top 50

    """

    def load_data(self, data_path: Optional[str] = None):
        if not data_path:
            data_path = (
                "/Users/chethanuk//Downloads/lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv"
            )
            # TODO: Update or Replace with actual path of music_sessions_data.tsv
            # data_path = "./tests/fm_music_top_songs/it/it_music_sessions_data.tsv"
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

    @staticmethod
    def generate_sessions_sql():
        return """
                WITH song_prev_data AS (
                                SELECT
                                    userid,
                                    timestamp,
                                    song_name,
                                    LAG(timestamp) OVER (PARTITION BY userid ORDER BY timestamp) as prev_timestamp
                                FROM
                                    songs_raw
                            ),
                    session_differences AS (
                        SELECT
                            userid,
                            timestamp,
                            song_name,
                            prev_timestamp,
                            CASE
                                WHEN prev_timestamp IS NULL OR
                                    (unix_timestamp(timestamp) - unix_timestamp(prev_timestamp)) / 60 > 20 THEN 1
                                ELSE 0
                            END as new_session_flag
                        FROM
                            song_prev_data
                    ),
                    sessions_with_marking AS (
                        SELECT
                            *,
                            SUM(new_session_flag) OVER (PARTITION BY userid ORDER BY timestamp) as session_id
                        FROM
                            session_differences
                    )
                """

    @staticmethod
    def top_50_sessions_sql():
        return """
            session_counts AS (
                SELECT
                    userid,
                    session_id,
                    COUNT(*) as song_count
                FROM
                    sessions_with_marking
                GROUP BY
                    userid, session_id
            ),
            top_sessions AS (
                SELECT
                    userid,
                    session_id,
                    song_count,
                    -- TODO: Based on requirment change Rank to DENSE_RANK
                    DENSE_RANK() OVER (PARTITION BY userid ORDER BY song_count DESC) as rank
                FROM
                    session_counts
                WHERE
                    song_count > 1 -- Verify: Filter sessions with at least more than one song
            ),
            filtered_sessions AS (
                SELECT
                    a.userid,
                    a.session_id,
                    -- a.artist_name,
                    a.song_name,
                    a.timestamp
                FROM
                    sessions_with_marking a
                JOIN
                    top_sessions b
                ON
                    a.userid = b.userid AND a.session_id = b.session_id
                WHERE
                    b.rank <= 50
            )
        """

    def parse_query(self, query: str):
        return sqlglot.transpile(query, read="spark", write="spark", error_level=ErrorLevel.RAISE)[0]

    def query(self, top_n: int = 10):
        sql_query = f"""
            {self.generate_sessions_sql()},\n
            {self.top_50_sessions_sql()}\n
            SELECT
                song_name,
                COUNT(song_name) as song_count
            FROM
                filtered_sessions
            GROUP BY song_name
            ORDER BY
                song_count DESC
            LIMIT {top_n}
            """

        return self.parse_query(sql_query)

    def execute(self, data_path: Optional[str] = None, output_path: Optional[str] = None, top_n: int = 10):
        df = self.load_data(data_path)
        df.createOrReplaceTempView("songs_raw")

        df_top_n_sessions = self.spark.sql(self.query(top_n))
        print(f"Query: {self.query()}")

        # df_top_n_sessions.explain(mode='simple')
        df_top_n_sessions.explain(mode="formatted")

        df_top_n_sessions.cache().show(100, truncate=False)

        # Write as JSON
        if output_path:
            # df_top_n_sessions.write.mode("overwrite").json(output_path)
            # For local testing - writing as single file
            # json.decoder.JSONDecodeError: Extra data: line 2 column 1
            df_top_n_sessions.coalesce(1).toPandas().to_json(output_path, orient="records")


if __name__ == "__main__":
    LastFMSessionsApp(app_name="ExploreMusicDatasetApp").execute(output_path="./datasets/top_n_songs.json", top_n=15)
