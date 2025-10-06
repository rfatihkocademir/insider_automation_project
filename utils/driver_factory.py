"""
WebDriver Factory - Selenium WebDriver instance'larını oluşturmak için factory sınıfı.

Chrome ve Firefox browser'larını destekler. webdriver_manager kuruluysa
otomatik olarak driver'ları indirir, yoksa sistem PATH'indeki driver'ları kullanır.
Bu yaklaşım cross-platform uyumluluk ve kolay bakım sağlar.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional

from config.settings import settings
from utils.logger import logger


def get_driver(browser_name: Optional[str] = None) -> WebDriver:
    """
    Belirtilen browser tipine göre Selenium WebDriver instance'ı döndürür.
    
    Bu fonksiyon test framework'ünün ana entry point'idir. Browser seçimi,
    driver yönetimi ve konfigürasyonu burada yapılır.

    Parameters
    ----------
    browser_name : str, optional
        "chrome" veya "firefox" değerlerinden biri. Büyük/küçük harf duyarsız.
        None ise settings.BROWSER değeri kullanılır.

    Returns
    -------
    WebDriver
        Konfigüre edilmiş WebDriver instance'ı

    Raises
    ------
    ValueError
        Desteklenmeyen browser tipi belirtilirse
    """
    # Browser adını normalize et (küçük harfe çevir)
    # Eğer browser_name verilmemişse settings'ten al
    browser = (browser_name or settings.BROWSER).lower()
    logger.info(f"WebDriver başlatılıyor: {browser}")

    # Desteklenen browser'ları kontrol et
    if browser not in {"chrome", "firefox"}:
        raise ValueError(f"Desteklenmeyen browser: {browser}")

    # Eğer Selenium Grid konfigüre edilmişse uzak driver kullan
    if settings.SELENIUM_HUB_URL:
        return _get_remote_driver(browser)

    try:
        # webdriver_manager ile otomatik driver yönetimi dene
        # Bu kütüphane driver'ları otomatik indirir ve yönetir
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager

        if browser == "chrome":
            # Chrome için options ve service oluştur
            options = _get_chrome_options()
            service = webdriver.ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        else:
            # Firefox için options ve service oluştur
            options = _get_firefox_options()
            service = webdriver.FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

    except Exception as e:
        # webdriver_manager başarısız olursa sistem driver'larına geç
        logger.warning(f"WebDriver manager başarısız: {e}. Sistem driver'larına geçiliyor.")
        
        if browser == "chrome":
            # Sistem Chrome driver'ını kullan
            options = _get_chrome_options()
            driver = webdriver.Chrome(options=options)
        else:
            # Sistem Firefox driver'ını kullan
            options = _get_firefox_options()
            driver = webdriver.Firefox(options=options)

    # Implicit wait süresini ayarla
    # Bu, element'lerin bulunması için beklenecek maksimum süreyi belirler
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    logger.info(f"WebDriver başarıyla başlatıldı: {browser}")
    return driver


def _get_chrome_options() -> ChromeOptions:
    """
    Chrome browser için optimize edilmiş seçenekleri döndürür.
    
    Bu fonksiyon Chrome'un test otomasyonu için en uygun şekilde
    çalışmasını sağlayan ayarları yapar.
    """
    options = ChromeOptions()
    
    # Browser'ı tam ekran başlat
    # Bu, element'lerin görünürlüğü için önemli
    options.add_argument("--start-maximized")
    
    # Otomasyon algılamasını devre dışı bırak
    # Bazı siteler bot tespiti yapar, bunu engeller
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Headless mode kontrolü
    if settings.HEADLESS:
        # Görünmez modda çalıştır (CI/CD için ideal)
        options.add_argument("--headless")
        # Headless modda pencere boyutunu manuel ayarla
        options.add_argument("--window-size=1920,1080")

    return options


def _get_firefox_options() -> FirefoxOptions:
    """
    Firefox browser için optimize edilmiş seçenekleri döndürür.
    
    Firefox'un test otomasyonu için uygun şekilde çalışmasını sağlar.
    """
    options = FirefoxOptions()

    # Headless mode kontrolü
    if settings.HEADLESS:
        # Görünmez modda çalıştır
        options.add_argument("--headless")

    # Firefox için pencere boyutunu ayarla
    # Bu ayarlar hem normal hem headless modda çalışır
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    return options


def _get_remote_driver(browser: str) -> WebDriver:
    """
    Selenium Grid için uzak WebDriver instance'ı oluşturur.
    
    Bu fonksiyon testlerin farklı makinelerde paralel olarak
    çalıştırılmasını sağlar.
    
    Parameters
    ----------
    browser : str
        Browser tipi ("chrome" veya "firefox")
        
    Returns
    -------
    WebDriver
        Uzak WebDriver instance'ı
    """
    logger.info(f"Selenium Grid'e bağlanılıyor: {settings.SELENIUM_HUB_URL}")

    if browser == "chrome":
        # Chrome için uzak driver oluştur
        options = _get_chrome_options()
        driver = webdriver.Remote(command_executor=settings.SELENIUM_HUB_URL, options=options)
    else:
        # Firefox için uzak driver oluştur
        options = _get_firefox_options()
        driver = webdriver.Remote(command_executor=settings.SELENIUM_HUB_URL, options=options)

    return driver
