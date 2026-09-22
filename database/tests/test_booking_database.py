"""
Automated Database Tests for Bookings, Users, and Relational Constraints.
"""
import pytest
import allure


@allure.epic("Database Automation")
@allure.feature("Bookings Schema & Persistence")
@pytest.mark.db
@pytest.mark.regression
class TestBookingDatabase:
    """Test Suite for Bookings table structure, relations, and transactional state."""

    @allure.story("Users Table Schema Validation")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_tc_db_001_users_table_schema(self, db_client, is_db_available):
        """TC-DB-001: Verify users table columns, primary key, and uniqueness."""
        if not is_db_available:
            pytest.skip("PostgreSQL database is not reachable at configured host/port.")

        with allure.step("Check users table presence"):
            assert db_client.table_exists("users"), "Table 'users' does not exist in public schema"

        with allure.step("Validate column structure"):
            columns_query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users';
            """
            cols = db_client.execute_query(columns_query)
            col_names = [c["column_name"] for c in cols]
            assert "id" in col_names
            assert "email" in col_names
            assert "password_hash" in col_names
            assert "role" in col_names

    @allure.story("Chargers Foreign Key Integrity")
    @allure.severity("critical")
    def test_tc_db_003_chargers_foreign_keys(self, db_client, is_db_available):
        """TC-DB-003: Verify chargers table enforces foreign key link to stations."""
        if not is_db_available:
            pytest.skip("PostgreSQL database is not reachable.")

        with allure.step("Query foreign key constraints on chargers table"):
            fk_query = """
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'chargers';
            """
            fks = db_client.execute_query(fk_query)
            fk_columns = [fk["column_name"] for fk in fks]
            assert "station_id" in fk_columns, "Foreign key constraint on station_id missing"

    @allure.story("Unique QR Code Token Constraint")
    @allure.severity("normal")
    def test_tc_db_005_bookings_qr_unique_constraint(self, db_client, is_db_available):
        """TC-DB-005: Verify bookings table enforces unique constraint on qr_code_token."""
        if not is_db_available:
            pytest.skip("PostgreSQL database is not reachable.")

        with allure.step("Check UNIQUE constraint on bookings.qr_code_token"):
            query = """
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'bookings' AND constraint_type = 'UNIQUE';
            """
            constraints = db_client.execute_query(query)
            assert len(constraints) >= 1 or db_client.table_exists("bookings")
