from matchkit.core import hello_world


class TestHelloWorld:
    def test_it(self):
        assert hello_world() == "Hello, world!"
