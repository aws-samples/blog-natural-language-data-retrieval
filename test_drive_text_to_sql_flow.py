import test_cases
import text_to_sql_flow


# test drive the main flow
if __name__ == '__main__':

    test_user_requests = test_cases.TestCases()

    start, end = 0, 7
    for i in range(start, end):
        print("------------------------------------------------------")
        example_input = test_user_requests.get_test_case(i)
        print(f"Test run: {i}, {example_input}\n")
        # run the main flow
        sql_results, sql_status = text_to_sql_flow.TextToSQLFlow().run(example_input)
        print("------------------------------------------------------")
        for row in sql_results:
            print(row)
            pass
        # print(f"sql_status: {sql_status}")
        print("------------------------------------------------------")
