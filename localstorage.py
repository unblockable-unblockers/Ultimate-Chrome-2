from selenium.webdriver import Chrome


class LocalStorage:

    def __init__(self, driver: Chrome):
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        return self.driver.execute_script( \
            "var items = {}; " \
            "for (var i = 0, k; i < localStorage.length; ++i) " \
            "  items[k = localStorage.key(i)] = localStorage.getItem(k); " \
            "return items; ")

    def keys(self):
        return self.driver.execute_script( \
            "var keys = []; " \
            "for (var i = 0; i < localStorage.length; ++i) " \
            "  keys[i] = localStorage.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script(
            "return localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script(
            "localStorage.setItem(arguments[0], arguments[1]);", key,
            value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script(
            "window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
