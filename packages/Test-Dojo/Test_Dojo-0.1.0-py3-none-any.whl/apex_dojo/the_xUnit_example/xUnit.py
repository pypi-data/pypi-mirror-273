# TODO:
# - Invoke tearDown even if the test method fails;
# - Run multiple tests;
# - Catch and report setup errors;.


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.error_count = 0

    def summery(self):
        return "{} ran, {} failed".format(self.run_count, self.error_count)

    def test_started(self):
        self.run_count += 1

    def test_failed(self):
        self.error_count += 1


class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self, result: TestResult) -> None:
        result.test_started()
        self.setup()

        # SAME AS: method = self.test_method
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.test_failed()
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass


class WasRun(TestCase):
    def __init__(self, name):
        self.was_run = None
        # self.name = name
        TestCase.__init__(self, name)

    def test_method(self):
        self.log += "test_method "

    def test_broken_method(self):
        raise Exception

    def setup(self):
        self.log = "setup "

    def teardown(self):
        self.log += "teardown "


class TestSuite:
    def __init__(self):
        self.tests: list[TestCase] = []

    def add(self, test: TestCase):
        self.tests.append(test)

    def run(self, result: TestResult):
        for test in self.tests:
            test.run(result)


class TestCaseTest(TestCase):
    def test_template_method(self):
        test = WasRun("test_method")
        test.run(TestResult())
        assert test.log == "setup test_method teardown "

    def test_result(self):
        test = WasRun("test_method")
        result = TestResult()
        test.run(result)
        assert result.summery() == "1 ran, 0 failed"

    def test_fail_result(self):
        test = WasRun("test_broken_method")
        result = TestResult()
        test.run(result)
        assert result.summery() == "1 ran, 1 failed"

    def test_failed_result_formatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert result.summery() == "1 ran, 1 failed"

    def test_suite(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        result = TestResult()
        suite.run(result)
        assert result.summery() == "2 ran, 1 failed"
