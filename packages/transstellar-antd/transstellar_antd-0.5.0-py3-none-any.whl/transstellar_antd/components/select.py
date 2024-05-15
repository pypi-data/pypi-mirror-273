from selenium.webdriver.common.keys import Keys
from transstellar.framework import Element


class Select(Element):
    XPATH_CURRENT = '//div[contains(@class, "ant-select ")]'
    XPATH_SELECT_SEARCH = (
        '//input[contains(@class, "ant-select-selection-search-input")]'
    )

    def select(self, text):
        self.logger.info(f"selecting text: {text}")

        self.get_current_dom_element().click()

        search_input = self.find_dom_element_by_xpath(self.XPATH_SELECT_SEARCH)
        search_input.send_keys(text)
        search_input.send_keys(Keys.RETURN)

        # NOTE: need to find a better way to assert account has been totally changed
        self.sleep(0.5)
