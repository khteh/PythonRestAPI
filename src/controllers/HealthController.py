import re, jsonpickle, logging
from psycopg_pool import AsyncConnectionPool, ConnectionPool
from quart import (
    Blueprint,
    Response,
    ResponseReturnValue,
    current_app,
    make_response,
    render_template,
    session
)
health_api = Blueprint("health", __name__)
@health_api.route("/ready")
def readiness() -> ResponseReturnValue:
    try:
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        with ConnectionPool(
            conninfo = current_app.config["POSTGRESQL_DATABASE_URI"],
            max_size = current_app.config["DB_MAX_CONNECTIONS"],
            kwargs = connection_kwargs,
        ) as pool:
            # Check if the checkpoints table exists
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE  table_schema = 'public'
                                AND    table_name   = 'library'
                            );
                        """)
                    except Exception as e:
                        logging.exception(f"Error checking for library table: Exception: {e}")
                        raise e
                        # Optionally, you might want to raise this error
                        # raise
        logging.debug("Ready!")
        return "OK", 200
    except Exception as e:
        logging.exception(f"{readiness.__name__} Exception: {e}")
        return "Exceptions!", 500

@health_api.route("/live")
def liveness():
    logging.debug("Alive!")
    return "OK", 200

