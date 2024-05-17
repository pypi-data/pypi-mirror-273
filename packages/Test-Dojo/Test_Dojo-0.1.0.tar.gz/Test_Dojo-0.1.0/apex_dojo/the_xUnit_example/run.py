from apex_dojo.the_xUnit_example.xUnit import TestCaseTest, TestSuite, TestResult

suite = TestSuite()
suite.add(TestCaseTest("test_template_method"))
suite.add(TestCaseTest("test_result"))
suite.add(TestCaseTest("test_failed_result_formatting"))
suite.add(TestCaseTest("test_fail_result"))
suite.add(TestCaseTest("test_suite"))

result = TestResult()
suite.run(result)

print(result.summery())
