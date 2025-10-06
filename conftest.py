"""
Insider Selenium projesi için Pytest konfigürasyonu ve fixture'ları.

Bu modül, ``--browser`` komut satırı seçeneğine göre WebDriver başlatan
``driver`` fixture'ını tanımlar. Test başarısızlığında screenshot alır
ve her testten sonra browser'ın kapatılmasını sağlar.
"""

import os
import pytest
import allure
from datetime import datetime
from typing import Generator

from utils.driver_factory import get_driver
from utils.logger import logger
from config.settings import settings


def pytest_addoption(parser) -> None:
    """
    Pytest için özel komut satırı seçeneklerini kaydet.
    
    Bu fonksiyon pytest'in komut satırından browser seçimi yapılmasını sağlar.
    Örnek kullanım: pytest --browser=firefox
    """
    parser.addoption(
        "--browser",
        action="store",
        default=os.environ.get("BROWSER", "chrome"),
        help="Testlerin çalıştırılacağı browser: chrome veya firefox (varsayılan: chrome)",
    )


@pytest.fixture(scope="function")
def driver(request) -> Generator:
    """
    Selenium WebDriver döndürür ve temizlik ile başarısızlık durumunda screenshot işlemlerini yönetir.
    
    Bu fixture her test fonksiyonu için yeni bir WebDriver instance'ı oluşturur.
    Test başarısız olursa otomatik screenshot alır ve driver'ı kapatır.
    """
    # Komut satırından browser seçeneğini al
    browser = request.config.getoption("--browser")
    logger.info(f"Test başlatılıyor: {request.node.name}")
    
    # WebDriver instance'ını oluştur
    driver_instance = get_driver(browser)
    
    # Test fonksiyonuna driver'ı ver
    yield driver_instance
    
    # Test sonucunu kontrol et ve başarısızlık durumunda screenshot al
    test_failed = False
    for rep in (getattr(request.node, "rep_setup", None), 
                getattr(request.node, "rep_call", None)):
        if rep and rep.failed:
            test_failed = True
            break
    
    # Eğer test başarısız olduysa ve screenshot ayarı açıksa screenshot al
    if test_failed and settings.SCREENSHOT_ON_FAILURE:
        _capture_failure_screenshot(driver_instance, request.node.name)
    
    # Driver'ı kapat ve kaynakları temizle
    logger.info(f"Test için driver kapatılıyor: {request.node.name}")
    driver_instance.quit()


def _capture_failure_screenshot(driver_instance, test_name: str) -> None:
    """
    Test başarısızlığında screenshot yakalar.
    
    Bu fonksiyon başarısız olan testler için otomatik screenshot alır,
    dosyaya kaydeder ve Allure raporuna ekler.
    """
    try:
        # Screenshot klasörünü oluştur (yoksa)
        os.makedirs(settings.SCREENSHOT_DIR, exist_ok=True)
        
        # Zaman damgası ile benzersiz dosya adı oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"failure_{test_name}_{timestamp}.png"
        filepath = os.path.join(settings.SCREENSHOT_DIR, filename)
        
        # Screenshot'ı kaydet
        driver_instance.save_screenshot(filepath)
        logger.info(f"Screenshot kaydedildi: {filepath}")
        
        # Allure raporuna ekle (mevcut ise)
        try:
            with open(filepath, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Screenshot_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            logger.warning(f"Screenshot Allure'a eklenemedi: {e}")
            
    except Exception as e:
        logger.error(f"Screenshot alınamadı: {e}")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Test rapor nesnesini test item'ında sonradan kullanım için açığa çıkarır.
    
    Bu hook, test sonuçlarının (başarılı/başarısız) fixture'larda
    kullanılabilmesi için gereklidir.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
