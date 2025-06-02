def filter_submitted_tests(tests, responses):
    """This is a function that filters out the already submitted responses of the user from the tests"""
    try:
        available_tests = []
        response_ids = []

        for response in responses:
            response_ids.append(response["test_id"])
        
        for test in tests:
            if test["id"] not in response_ids:
                available_tests.append(test)
        
        return available_tests
    except Exception as e:
        raise e()
