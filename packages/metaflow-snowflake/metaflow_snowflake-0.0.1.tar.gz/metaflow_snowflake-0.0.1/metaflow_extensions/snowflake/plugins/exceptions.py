from .constants import SUPPORTED_AUTHENTITACTION_METHODS


class MultipleAuthMethodsSpecified(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AuthenticatorNotSupported(Exception):
    def __init__(self, authenticator):
        self.message = f"{authenticator} authenticator not in the supported authenaticators list {', '.join(SUPPORTED_AUTHENTITACTION_METHODS)}. Please contact Outerbounds for support."
        super().__init__(self.message)


class ConstructorArgumentMissing(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DependencyNotInstalled(Exception):
    def __init__(self, dependency, package_name):
        self.message = f"{dependency} connector not found. Please install the {package_name} package."
        super().__init__(self.message)


class InvalidReturnType(Exception):
    def __init__(self):
        self.message = "Invalid return type. Must be one of: arrow, pandas."
        super().__init__(self.message)


class InvalidFetchStrategy(Exception):
    def __init__(self):
        self.message = "Invalid fetch strategy. Must be one of: all, batches."
        super().__init__(self.message)
