"""
Insider kariyer ana sayfası için Page Object sınıfı.

Bu sayfa, anahtar bölümlerin görünür olduğunu doğrular (Locations,
Teams ve Life at Insider) ve Quality Assurance sayfasına navigasyon sağlar.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class CareersPage(BasePage):
    """
    Ana kariyer landing sayfasını modelleyen sınıf.
    
    Bu sınıf kariyer sayfasındaki temel bölümlerin varlığını kontrol eder
    ve Quality Assurance sayfasına yönlendirme işlemlerini yönetir.
    """

    # ==================== BAŞLIK LOCATOR'LARI ====================
    # Metin kontrollerini daha sağlam yapmak için küçük harf dönüşümü kullanır
    
    # "Our Locations" veya "Locations" içeren başlıklar
    LOCATIONS_HEADING = (
        By.XPATH,
        "//h3[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'our locations') or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'locations')] | //h2[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'our locations')]",
    )
    
    # "Find Your Calling" veya "Teams" içeren başlıklar
    TEAMS_HEADING = (
        By.XPATH,
        "//h3[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'find your calling') or contains(.,'Teams')]",
    )
    
    # "Life at Insider" içeren başlıklar
    LIFE_AT_INSIDER_HEADING = (
        By.XPATH,
        "//h2[contains(.,'Life at Insider')] | //h3[contains(.,'Life at Insider')]",
    )

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        CareersPage instance'ını başlatır.
        
        Args:
            driver: Selenium WebDriver instance'ı
            timeout: Element bekleme süresi (varsayılan: 10 saniye)
        """
        super().__init__(driver, timeout)

    def verify_sections_present(self) -> None:
        """
        Sayfadaki kritik bölümlerin görünür olduğunu doğrular.
        
        Bu metod kariyer sayfasının temel bölümlerinin (Locations, Teams,
        Life at Insider) mevcut olduğunu kontrol eder. Eksik bölüm varsa
        assertion hatası fırlatır.
        
        Raises:
            AssertionError: Gerekli bölümlerden biri eksikse
        """
        assert self.exists(*self.LOCATIONS_HEADING), "Locations bölümü eksik"
        assert self.exists(*self.TEAMS_HEADING), "Teams bölümü eksik"
        assert self.exists(*self.LIFE_AT_INSIDER_HEADING), "Life at Insider bölümü eksik"

    def go_to_quality_assurance(self):
        """
        Link metni üzerinden Quality Assurance landing sayfasına navigasyon yapar.
        
        "Quality Assurance" link metnine tıklayarak QA sayfasına yönlendirir.
        
        Returns:
            QualityAssurancePage: Quality Assurance sayfası page object instance'ı
        """
        from .quality_assurance_page import QualityAssurancePage
        self.click(By.LINK_TEXT, "Quality Assurance")
        return QualityAssurancePage(self.driver)