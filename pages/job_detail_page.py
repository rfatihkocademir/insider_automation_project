"""Lever İş Detay Sayfası Modülü.

Bu modül Lever.co platformundaki iş detay sayfasını temsil eden
JobDetailPage sınıfını içerir. Bu sınıfın temel sorumluluğu,
kullanıcının doğru üçüncü taraf sayfasına yönlendirildiğini ve
başvuru bölümünün mevcut olduğunu doğrulamaktır.

Lever.co, Insider'ın iş başvuruları için kullandığı harici platformdur.
"""

# Selenium import'ları
from selenium.webdriver.common.by import By  # Element bulma stratejileri
from selenium.webdriver.remote.webdriver import WebDriver  # WebDriver sınıfı

# Proje içi import'lar
from .base_page import BasePage  # Temel sayfa sınıfı


class JobDetailPage(BasePage):
    """Lever İş Detay Sayfası Sınıfı.
    
    Bu sınıf Lever.co platformundaki iş detay sayfasını temsil eder.
    İş başvuru formunun bulunduğu sayfanın doğruluğunu kontrol eder.
    """

    # LOCATOR'LAR - Sayfadaki elementleri bulmak için tanımlayıcılar
    
    # Başvuru bölümünü bulan XPath
    # "Apply for this job" başlığı veya "Apply" butonu arar
    # Lever sayfasının farklı versiyonlarını desteklemek için iki seçenek
    APPLY_SECTION = (
        By.XPATH,
        "//h2[contains(.,'Apply for this job')] | //button[contains(.,'Apply')]",
    )

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """JobDetailPage sınıfını başlat.
        
        Args:
            driver: WebDriver instance'ı
            timeout: Element bekleme süresi (varsayılan: 10 saniye)
        """
        super().__init__(driver, timeout)  # BasePage constructor'ını çağır
        print(" İş detay sayfası page object'i oluşturuldu")

    def verify_on_lever(self) -> None:
        """Lever sayfasında olduğumuzu ve başvuru bölümünün mevcut olduğunu doğrula.
        
        Bu method test senaryosunun son adımıdır. İki önemli kontrolü yapar:
        1. URL'in jobs.lever.co domain'ini içerdiğini kontrol eder
        2. Sayfada başvuru bölümünün (Apply section) bulunduğunu kontrol eder
        
        Raises:
            AssertionError: URL Lever domain'ini içermiyorsa veya başvuru bölümü yoksa
        """
        print("🔍 Lever sayfası doğrulaması yapılıyor...")
        
        # Mevcut URL'i al
        current_url = self.driver.current_url
        print(f" Mevcut URL: {current_url}")
        
        # URL'in Lever domain'ini içerdiğini kontrol et
        print(" URL kontrolü yapılıyor...")
        assert "jobs.lever.co" in current_url, (
            f" Beklenmeyen domain! "
            f"Beklenen: 'jobs.lever.co' içeren URL, "
            f"Mevcut: {current_url}"
        )
        print(" URL kontrolü başarılı - Lever sayfasındayız")
        
        # Başvuru bölümünün varlığını kontrol et
        print(" Başvuru bölümü kontrolü yapılıyor...")
        assert self.exists(*self.APPLY_SECTION), (
            "Başvuru bölümü bulunamadı! "
            "Lever sayfasında 'Apply for this job' başlığı veya 'Apply' butonu olmalı. "
            "Sayfa yapısı değişmiş olabilir."
        )
        print("Başvuru bölümü bulundu")
        
        print("Lever sayfası doğrulaması başarıyla tamamlandı!")