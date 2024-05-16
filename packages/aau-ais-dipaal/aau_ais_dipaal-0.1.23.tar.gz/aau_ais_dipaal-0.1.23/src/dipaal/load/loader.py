"""This module contains the Loader class, which is used to load data from the DIPAAL schema into the depth schema."""
from datetime import datetime, timedelta
from pathlib import Path
from calendar import monthrange

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError

from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.settings import get_dipaal_admin_engine


class Loader:
    """Base class for DIPAAL loaders."""

    def __init__(self, engine: Engine = get_dipaal_admin_engine(), *, update: bool = False):
        self.connection = PostgreSQLConnection(engine)
        self.update = update
        self.sql_folder = Path(__file__).parent / 'sql'

    def load_depth(
            self,
            start_date: int,
            end_date: int,
            confidence_scores: list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    ):
        """Load data into the depth schema from the DIPAAL schema.

        For the method to work,
         the following tables must exist in the DIPAAL schema and be populated with appropriate data:
            - dim_ship
            - dim_date
            - dim_time
            - dim_ship_type
            - dim_nav_status
            - dim_cell_50m
            - spatial_partition
            - fact_cell_5000m

        Args:
            start_date: The start date to load data from, in the format YYYYMMDD.
            end_date: The end date to load data to, in the format YYYYMMDD.
            confidence_scores: A list of confidence values to load data for into the raster aggregation.
             Default is [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1].
        """
        min_time = '000000'
        max_time = '235959'

        date_range = self._get_date_range(start_date, end_date)

        for day in date_range:
            print(f'Loading data for {day} into the fact_depth_50m table...')
            self._attempt_sql_execution(
                sql=Path(self.sql_folder, 'dipaal_to_depth/02.load.fact_depth_50m.sql'),
                params={'start_date': day, 'end_date': day,
                        'start_time': min_time, 'end_time': max_time}
            )

            print(f"Updating confidence in the fact_depth_50m table for {day}...")
            self._attempt_sql_execution(
                sql="""CALL depth.update_confidence_depth_01(:start_date, :end_date);""",
                params={'start_date': day, 'end_date': day}
            )

            for confidence in confidence_scores:
                print(f'Loading data for {day} and confidence {confidence} into the fact_raster_cfd table...')
                self._attempt_sql_execution(
                    sql=Path(self.sql_folder, 'dipaal_to_depth/06.load.fact_raster_confidence.sql'),
                    params={'date_key': day, 'confidence': confidence}
                )

            print(f"Testing if all days in month {day[:6]} have been loaded into the fact_raster_cfd_month table...")
            days_in_month = monthrange(int(day[:4]), int(day[4:6]))[1]
            year = day[:4]
            month = day[4:6]

            result = self.connection.execute(
                sql="""SELECT count(DISTINCT date_id) FROM depth.fact_raster_cfd 
                WHERE EXTRACT(YEAR FROM to_date(date_id::text, 'YYYYMMDD')) = :year
                AND EXTRACT(MONTH FROM to_date(date_id::text, 'YYYYMMDD')) = :month;""",
                params={'year': year, 'month': month}
            ).fetchone()

            if result[0] == days_in_month:
                print(f'Loading data for {day} into the fact_raster_cfd_month table...')
                self._attempt_sql_execution(
                    sql=Path(self.sql_folder, 'dipaal_to_depth/08.load.fact_raster_confidence_month.sql'),
                    params={'start_date': day, 'end_date': day}
                )

    def _attempt_sql_execution(self, *, sql: str | Path, params: dict):
        """Attempt to execute SQL and raise an exception if it fails."""
        try:
            self.connection.execute(
                sql=sql,
                params=params
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            raise Exception(error)

    @staticmethod
    def _get_date_range(start_date, end_date):
        """Get a range of dates."""
        date_range = []
        current_date = datetime.strptime(str(start_date), '%Y%m%d')
        while current_date <= datetime.strptime(str(end_date), '%Y%m%d'):
            date_range.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)
        return date_range
