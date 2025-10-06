"""
Insider ana sayfası için Page Object sınıfı.

Bu sınıf Insider ana sayfasının element'lerini ve navigasyon metodlarını içerir.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class HomePage(BasePage):
    """
    Insider ana sayfasını modelleyen ve navigasyon metodları sağlayan sınıf.
    
    Bu sınıf ana sayfadaki temel işlemleri (çerez kabul etme, menü navigasyonu)
    ve kariyer sayfasına yönlendirme işlemlerini yönetir.
    """

    # Ana sayfa URL'i
    URL = "https://useinsider.com/"

    # ==================== LOCATOR'LAR ====================
    # Çerez kabul etme butonu - farklı varyasyonları destekler
    ACCEPT_COOKIES_BTN = (
        By.XPATH,
        "//a[contains(@class,'accept')] | //button[contains(@class,'accept') and contains(text(),'Accept')]",
    )
    # Ana navigasyon menüsündeki Company linki
    COMPANY_MENU = (By.XPATH, "//nav//a[normalize-space()='Company']")
    # Company dropdown menüsündeki Careers linki
    CAREERS_LINK = (By.XPATH, "//nav//a[normalize-space()='Careers']")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        HomePage instance'ını başlatır.
        
        Args:
            driver: Selenium WebDriver instance'ı
            timeout: Element bekleme süresi (varsayılan: 10 saniye)
        """
        super().__init__(driver, timeout)

    def open(self) -> None:
        """
        Ana sayfaya navigasyon yapar.
        
        Browser'ı Insider ana sayfasına yönlendirir.
        """
        self.driver.get(self.URL)

    def accept_cookies_if_present(self) -> None:
        """
        Çerez banner'ı varsa kapatır.
        
        Çerez onay popup'ı görünürse kabul eder. Eğer popup yoksa
        veya tıklanamıyorsa sessizce devam eder.
        """
        try:
            self.click(*self.ACCEPT_COOKIES_BTN)
        except Exception:
            # Banner mevcut değil veya element tıklanamıyor - sorun yok
            pass

    def go_to_careers(self):
        """
        Company menüsü üzerinden kariyer sayfasına navigasyon yapar.
        
        Bu metod önce Company menüsüne hover yapar, dropdown'ı açar
        ve Careers linkine tıklar. Eğer UI navigasyonu başarısız olursa
        direkt URL ile kariyer sayfasına gider.
        
        Returns:
            CareersPage: Kariyer sayfası page object instance'ı
        """
        from .careers_page import CareersPage
        
        try:
            # Company menüsüne hover yaparak dropdown'ı aç
            company = self.find(*self.COMPANY_MENU)
            ActionChains(self.driver).move_to_element(company).perform()

            # Dropdown'ın açılması için kısa bir süre bekle
            import time
            time.sleep(1)

            # Careers linkini bul ve tıkla
            if self.exists(*self.CAREERS_LINK, timeout=3):
                careers_element = self.find(*self.CAREERS_LINK)
                if careers_element.is_displayed():
                    # Element görünürse normal tıklama yap
                    careers_element.click()
                else:
                    # Element gizliyse JavaScript ile tıkla
                    self.driver.execute_script("arguments[0].click();", careers_element)
            else:
                # Link bulunamazsa direkt URL'e git
                self.driver.get("https://useinsider.com/careers/")

        except Exception:
            # Herhangi bir hata durumunda direkt navigasyon yap
            self.driver.get("https://useinsider.com/careers/")

        # Kariyer sayfası page object'ini döndür
        return CareersPage(self.driver)
