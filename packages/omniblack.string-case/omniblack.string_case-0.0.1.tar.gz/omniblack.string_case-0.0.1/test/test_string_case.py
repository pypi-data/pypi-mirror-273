from omniblack.string_case import Cases


class Base:
    def test_from_kebab(self):
        assert self.case.to('test-test') == self.result

    def test_from_snake(self):
        assert self.case.to('test_test') == self.result

    def test_from_camel(self):
        assert self.case.to('testTest') == self.result

    def test_from_pascal(self):
        assert self.case.to('TestTest') == self.result

    def test_from_title(self):
        assert self.case.to('Test Test') == self.result

    def test_repeated_seperator(self):
        assert self.case.to('test___test') == self.result

    def test_mixed_seperator(self):
        assert self.case.to('test.-_test') == self.result

    def test_mixed_case(self):
        assert self.case.to('testTest_test-Test') == self.long_result

class TestToKebabCase(Base):
    case = Cases.Kebab
    result = 'test-test'
    long_result = 'test-test-test-test'

class TestToCapKebabCase(Base):
    case = Cases.CapKebab
    result = 'TEST-TEST'
    long_result = 'TEST-TEST-TEST-TEST'

class TestToSnakeCase(Base):
    case = Cases.Snake
    result = 'test_test'
    long_result = 'test_test_test_test'

class TestToCapSnakeCase(Base):
    case = Cases.CapSnake
    result = 'TEST_TEST'
    long_result = 'TEST_TEST_TEST_TEST'

class TestToCamelCase(Base):
    case = Cases.Camel
    result = 'testTest'
    long_result = 'testTestTestTest'

class TestToPascalCase(Base):
    case = Cases.Pascal
    result = 'TestTest'
    long_result = 'TestTestTestTest'

class TestToTitleCase(Base):
    case = Cases.Title
    result = 'Test Test'
    long_result = 'Test Test Test Test'
