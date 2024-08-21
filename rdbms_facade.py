import sqlite3
import app_constants as app_consts


# The class RdbmsFacade wraps the SQL Database Engines(s) to provide a consistent interface
# independent of the underlying implementation

class RdbmsFacade:
    # A method to execute SQL
    def execute_sql(self, database: str, rdbms_results: [str]):

        # execute the SQL script
        rdbms_results, rdbms_status = self.execute_sql_script(database, rdbms_results)

        # create a dictionary to store the RDBMS results
        results = {app_consts.RDBMS_OUTPUT: rdbms_results, app_consts.PROCESSING_STATUS: rdbms_status}

        # return the executed SQL
        return results

    # A method to execute the generated SQL script against a sqlite database
    @staticmethod
    def execute_sql_script(database: str, sql_script: [str]):
        """
        This method executes the SQL script against a sqlite database.
        It will execute each statement in the SQL script and return the results of the last statement.
        Success is defined as a valid query execution for the last statement.
        This is determined by checking if the cursor did not throw an error, and it has a row description.
        :param database: the database to execute the SQL script against
        :param sql_script: the SQL script to execute
        :return:
        """

        status, verbose = "failed", False
        results, iterations = [], 1

        connection = sqlite3.connect(database)
        with connection:
            cursor = connection.cursor()
            try:
                for stmt in sql_script:
                    if stmt == '':
                        iterations += 1
                        continue
                    cursor.execute(stmt)
                    result = cursor.fetchall()

                    if result:
                        if verbose:
                            print(f"Rows resulting from SQL statement '{stmt}':")
                            for res in result:
                                print(res)
                    else:
                        if verbose:
                            print(f"No rows resulting from SQL statement '{stmt}'\n")

                    if iterations == len(sql_script):
                        if len(cursor.description) > 0:
                            column_names = [x[0] for x in cursor.description]
                            results = [tuple(column_names)]
                            for r in result:
                                results.append(r)
                            status = app_consts.SUCCESS
                    else:
                        iterations += 1
            finally:
                cursor.close()

        return results, status
