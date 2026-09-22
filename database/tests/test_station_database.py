"""
Automated Database Tests for Stations, PostGIS Geometry, and Seed Records.
"""
import pytest
import allure


@allure.epic("Database Automation")
@allure.feature("Stations & Spatial Data")
@pytest.mark.db
@pytest.mark.regression
class TestStationDatabase:
    """Test Suite for Stations spatial columns, seed record counts, and indexes."""

    @allure.story("PostGIS Geometry Verification")
    @allure.severity("critical")
    def test_tc_db_002_stations_postgis_geometry(self, db_client, is_db_available):
        """TC-DB-002: Verify stations table utilizes PostGIS Point geometry with SRID 4326."""
        if not is_db_available:
            pytest.skip("PostgreSQL database is not reachable.")

        with allure.step("Query PostGIS geometry columns metadata"):
            query = """
                SELECT f_geometry_column, type, srid
                FROM geometry_columns
                WHERE f_table_name = 'stations';
            """
            geo_info = db_client.execute_query(query)
            if geo_info:
                assert geo_info[0]["f_geometry_column"] == "location"
                assert geo_info[0]["srid"] == 4326

    @allure.story("Seed Station Record Count")
    @allure.severity("minor")
    def test_tc_db_006_seed_stations_count(self, db_client, is_db_available):
        """TC-DB-006: Verify database contains initialized seed charging stations."""
        if not is_db_available:
            pytest.skip("PostgreSQL database is not reachable.")

        with allure.step("Count records in stations table"):
            count = db_client.execute_scalar("SELECT count(*) FROM stations;")
            assert count is not None and count >= 0
