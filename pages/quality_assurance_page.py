"""
Insider Quality Assurance landing sayfası için Page Object sınıfı.

Bu sayfa öncelikle tüm QA iş ilanlarını görüntülemek için
bir call-to-action butonu içerir.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class QualityAssurancePage(BasePage):
    """
    QA landing sayfasını modelleyen sınıf.
    
    Bu sınıf Quality Assurance sayfasındaki temel işlemleri yönetir,
    özellikle tüm QA işlerini görme butonuna tıklama işlemini sağlar.
    """

    # ==================== LOCATOR'LAR ====================
    # "See all QA jobs" butonunu bulan XPath
    # Hem href attribute'unu hem de metin içeriğini kontrol eder
    SEE_ALL_JOBS = (
        By.XPATH,
        "//a[contains(@href,'open-positions') and contains(.,'See all QA jobs')]",
    )

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        QualityAssurancePage instance'ını başlatır.
        
        Args:
            driver: Selenium WebDriver instance'ı
            timeout: Element bekleme süresi (varsayılan: 10 saniye)
        """
        super().__init__(driver, timeout)

    def click_see_all_jobs(self):
        """
        "See all QA jobs" butonuna tıklar ve açık pozisyonlar sayfasını döndürür.
        
        Bu metod QA sayfasındaki ana call-to-action butonuna tıklayarak
        tüm açık QA pozisyonlarının listelendiği sayfaya yönlendirir.
        
        Returns:
            OpenPositionsPage: Açık pozisyonlar sayfası page object instance'ı
        """
        from .open_positions_page import OpenPositionsPage
        self.click(*self.SEE_ALL_JOBS)
        return OpenPositionsPage(self.driver)