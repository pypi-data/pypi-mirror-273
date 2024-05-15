class InvalidOutput(Exception):
    """Exception raised for errors in output format.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Output format wasn't expected"):
        self.message = message
        super().__init__(self.message)