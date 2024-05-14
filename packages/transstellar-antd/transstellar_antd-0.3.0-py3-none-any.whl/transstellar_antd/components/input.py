from transstellar.framework import Element


class Input(Element):
    XPATH_CURRENT = '//input[contains(@class, "ant-input")]'

    def input(self, value: str):
        self.logger.info(f"input to value: {value}")

        self.get_current_dom_element().send_keys(value)

        new_value = self.get_value()

        assert new_value == value

    def get_value(self):
        return self.dom_element.get_attribute("value")
