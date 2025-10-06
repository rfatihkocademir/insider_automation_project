from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage

class OpenPositionsPage(BasePage):
    LOCATION_FILTER = (By.ID, "location")
    DEPARTMENT_FILTER = (By.ID, "department")
    LISTING_ITEM = (By.CSS_SELECTOR, "div.position-list-item")
    LISTING_TITLE = (By.CSS_SELECTOR, "div.position-title")
    LISTING_DEPARTMENT = (By.CSS_SELECTOR, "div.position-department")
    LISTING_LOCATION = (By.CSS_SELECTOR, "div.position-location")
    VIEW_ROLE_BUTTON = (By.XPATH, ".//a[contains(@href,'jobs.lever.co') and (contains(text(),'View Role') or contains(text(),'Apply'))]")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)

    def set_filters(self, location: str, department: str) -> None:
        try:
            select_location = Select(self.find(*self.LOCATION_FILTER))
            select_location.select_by_visible_text(location)
        except Exception:
            self.click(*self.LOCATION_FILTER)
            option_locator = (By.XPATH, f"//div[contains(@class,'dropdown')]//span[normalize-space()='{location}']")
            self.click(*option_locator)
        
        try:
            select_dept = Select(self.find(*self.DEPARTMENT_FILTER))
            select_dept.select_by_visible_text(department)
        except Exception:
            self.click(*self.DEPARTMENT_FILTER)
            option_locator = (By.XPATH, f"//div[contains(@class,'dropdown')]//span[normalize-space()='{department}']")
            self.click(*option_locator)

    def get_listings(self) -> List[Dict[str, any]]:
        cards = self.finds(*self.LISTING_ITEM)
        listings = []
        
        for card in cards:
            try:
                title = card.find_element(*self.LISTING_TITLE).text
                department = card.find_element(*self.LISTING_DEPARTMENT).text
                location = card.find_element(*self.LISTING_LOCATION).text
                button = card.find_element(*self.VIEW_ROLE_BUTTON)
                
                listings.append({
                    "element": card,
                    "title": title,
                    "department": department,
                    "location": location,
                    "button": button,
                })
            except Exception:
                continue
        
        return listings

    def open_first_job(self):
        from .job_detail_page import JobDetailPage
        
        jobs = self.get_listings()
        assert jobs, "Hiç iş ilanı yok"
        
        jobs[0]["button"].click()
        
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        
        return JobDetailPage(self.driver)
