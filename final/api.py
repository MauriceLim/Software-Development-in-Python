"""
API Routes for Zen Nilpferd
"""
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from mysql.connector import MySQLConnection, Error as MySQLError

import models

app = FastAPI()

class BasicChecksMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, conn: MySQLConnection):
        super().__init__(app)
        self._conn = conn

    async def dispatch(self, request, call_next):
        if not self._conn.is_connected():
            try:
                # We expect the environment variable MYSQL_HOST will to be
                # present if we're running within a container.
                host = os.environ.get("MYSQL_HOST", "127.0.0.1")
                # Port is always the within container network default port, even
                # if another, e.g. 3307, is exposed to the Docker host.
                port = 3306
                print(f"Connecting to host '{host}', port '{port}'")
                self._conn.connect(host=host, port=port, user="root",database='zen_nilpferd')
            except Exception as e:
                return JSONResponse(
                    status_code=503, content=f"Database unavailable: {e}"
                )

        result = await call_next(request)
        # ensure we commit each time to avoid select statement caching
        self._conn.commit()
        return result 


conn: MySQLConnection = MySQLConnection()
middleware = [Middleware(BasicChecksMiddleware, conn=conn)]
app = FastAPI(title="Zen Nilpferd's Quant API", version="0.0.1", middleware=middleware)

# ==========================================================================
#                            YOUR IMPLEMENTATION
#                               BELOW HERE!!!
# NOTES:
#   - Use the global `conn` variable for the MySQL connection
# ==========================================================================


@app.get("/")
def root():
    if conn.is_connected():
        return "All is well!"


@app.get("/assumptions/{id}")
def assumptions(id: int) -> models.ProjectionAssumptions:
    cursor = conn.cursor(dictionary=True)
    try:
        query = f"SELECT mortality_multiplier, wd_age, min_wd_delay FROM assumptions WHERE id = {id};"
        
        cursor.execute(query)
        result = cursor.fetchone()

        # Check if the result is not None (record found)
        if result is not None:
            return models.ProjectionAssumptions(**result)
        else:
            # Return 404 if the record is not found
            raise HTTPException(
                status_code=404,
                detail="Assumption not found",
            )

    except MySQLError as e:
        # Handle database errors
        return JSONResponse(content={"error": str(e)}, status_code=404)


@app.get("/parameters/{id}")
def parameters(id: int) -> models.ProjectionParameters:
    cursor = conn.cursor(dictionary=True)
    try:
        query = f"SELECT proj_periods, num_paths, seed FROM parameters WHERE id = {id};"
        
        cursor.execute(query)
        result = cursor.fetchone()

        # Check if the result is not None (record found)
        if result is not None:
            return models.ProjectionParameters(**result)
        else:
          
            raise HTTPException(
                status_code=404,
                detail="Parameters not found",
            )

    except MySQLError as e:
        # Handle database errors
        return JSONResponse(content={"error": str(e)}, status_code=500)


def policies(id: Optional[int] = None) -> list[models.PolicyholderRecord]:

    cursor = conn.cursor(dictionary=True)

    try:
        if id is not None:
            # Fetch policies for a specific ID
            query = f"SELECT id, issue_age, initial_premium, fee_pct_av, benefit_type, ratchet_type, guarantee_wd_rate FROM policies WHERE id = {id};"
        
        else:
            # Fetch all policies
            query = "SELECT id, issue_age, initial_premium, fee_pct_av, benefit_type, ratchet_type, guarantee_wd_rate FROM policies;"

        
        cursor.execute(query)
        results = cursor.fetchall()

        if id is not None and not results:
            return []

        all_records = []
        if results is not None:
            for result in results:
                all_records.append(models.PolicyholderRecord(**result))
            
        return all_records

    except MySQLError as e:
        # Handle database errors
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/policies")
def get_policies_without_id():
    return policies()

@app.get("/policies/{id}")
def get_policies_with_id(id: int):
    return policies(id=id)


@app.get("/scenario/{id}")
def scenario(id: int) -> models.ScenarioParameters:
    
    cursor = conn.cursor(dictionary=True)
    
    try:      
        query = f"SELECT risk_free_rate, dividend_yield, volatility FROM scenarios WHERE id = {id};"
        
        cursor.execute(query)
        result = cursor.fetchone()

        # Check if the result is not None (record found)
        if result is not None:
            return models.ScenarioParameters(**result)
        else:
            
            raise HTTPException(
                status_code=404,
                detail="Scenarios not found",
            )

    except MySQLError as e:
        # Handle database errors
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/mortality")
def mortality() -> models.MortalityTable:
    cursor = conn.cursor(dictionary=True)
        
    try:      
        query = f"SELECT qx FROM mortality;"
        
        cursor.execute(query)
        results = cursor.fetchall()
        qx_values = [result["qx"] for result in results]

        # Check if the result is not None (record found)
        if results is not None:
            return models.MortalityTable(qx=qx_values)
        else:
            
            raise HTTPException(
                status_code=404,
                detail="Mortality not found",
            )

    except MySQLError as e:
        # Handle database errors
        return JSONResponse(content={"error": str(e)}, status_code=500)
    ...