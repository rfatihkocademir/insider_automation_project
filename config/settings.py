"""
Test konfigürasyon ayarları - Environment değişkenlerinden yüklenir.
Bu modül, test framework'ünün tüm konfigürasyon ayarlarını merkezi olarak yönetir.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# .env dosyasından environment değişkenlerini yükle
# Bu sayede test ayarları kod değişikliği olmadan güncellenebilir
load_dotenv()


class Settings:
    """
    Test framework'ü için konfigürasyon ayarları sınıfı.
    Tüm ayarlar environment değişkenlerinden okunur ve varsayılan değerler sağlanır.
    """

    # ==================== BROWSER AYARLARI ====================
    # Hangi browser'ın kullanılacağını belirler (chrome, firefox)
    BROWSER: str = os.getenv("BROWSER", "chrome")
    
    # Browser'ın headless modda (görünmez) çalışıp çalışmayacağını belirler
    # CI/CD ortamlarında genellikle true olarak ayarlanır
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Element'lerin bulunması için implicit wait süresi (saniye)
    # Selenium'un element'i bulmak için bekleyeceği maksimum süre
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    
    # Explicit wait işlemleri için maksimum bekleme süresi (saniye)
    # WebDriverWait ile kullanılan timeout değeri
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "20"))

    # ==================== UYGULAMA AYARLARI ====================
    # Test edilecek uygulamanın ana URL'i
    # Farklı ortamlar için (dev, staging, prod) değiştirilebilir
    BASE_URL: str = os.getenv("BASE_URL", "https://useinsider.com/")
    
    # Test ortamının adı (development, staging, production)
    # Raporlama ve loglama için kullanılır
    TEST_ENV: str = os.getenv("TEST_ENV", "production")

    # ==================== SELENIUM GRID AYARLARI ====================
    # Selenium Grid Hub URL'i (uzak test çalıştırma için)
    # Eğer tanımlanmışsa, testler uzak makinelerde çalıştırılır
    SELENIUM_HUB_URL: Optional[str] = os.getenv("SELENIUM_HUB_URL")

    # ==================== LOGLAMA AYARLARI ====================
    # Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # Hangi seviyedeki logların kaydedileceğini belirler
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Log dosyasının kaydedileceği yol
    # Tüm test aktiviteleri bu dosyaya kaydedilir
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/test.log")

    # ==================== SCREENSHOT AYARLARI ====================
    # Test başarısız olduğunda otomatik screenshot alınıp alınmayacağı
    # Debug için çok önemli, varsayılan olarak açık
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    # Screenshot'ların kaydedileceği klasör
    # Her başarısız test için ayrı screenshot dosyası oluşturulur
    SCREENSHOT_DIR: str = os.getenv("SCREENSHOT_DIR", "screenshots")

    # ==================== RETRY AYARLARI ====================
    # Başarısız testlerin kaç kez tekrar deneneceği
    # Flaky testler için önemli, ağ sorunlarını tolere eder
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Retry denemeleri arasındaki bekleme süresi (saniye)
    # Çok hızlı retry'lar sistem yükü oluşturabilir
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "2"))


# Global settings instance'ı
# Tüm projede bu instance kullanılarak ayarlara erişilir
settings = Settings()
