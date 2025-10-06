"""
Test Framework Logging Konfigürasyonu.

Bu modül, test framework'ü için merkezi logging sistemi sağlar.
Hem dosyaya hem de konsola log yazma, farklı log seviyeleri ve
formatlanmış çıktı desteği sunar.
"""

import logging
import os

from config.settings import settings


class TestLogger:
    """
    Test framework'ü için özelleştirilmiş logger sınıfı.
    
    Bu sınıf, test çalıştırma sürecinde oluşan tüm olayları
    hem dosyaya hem de konsola kaydetmek için tasarlanmıştır.
    Debug, bilgi, uyarı ve hata mesajlarını organize eder.
    """

    def __init__(self, name: str = "test_framework"):
        """
        TestLogger instance'ını başlatır.
        
        Args:
            name: Logger'ın adı (varsayılan: "test_framework")
                 Bu ad log mesajlarında görünür ve logger'ı tanımlar
        """
        # Python'un built-in logging sisteminden logger al
        self.logger = logging.getLogger(name)
        # Logger'ı konfigüre et
        self._setup_logger()

    def _setup_logger(self) -> None:
        """
        Logger'ı file ve console handler'ları ile konfigüre eder.
        
        Bu metod logger'ın sadece bir kez konfigüre edilmesini sağlar
        ve hem dosyaya hem konsola log yazacak şekilde ayarlar.
        """
        # Eğer logger zaten konfigüre edilmişse tekrar yapma
        if self.logger.handlers:
            return  # Logger zaten konfigüre edilmiş

        # Settings'ten log seviyesini al ve ayarla
        # DEBUG, INFO, WARNING, ERROR, CRITICAL seviyelerinden biri
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))

        # Log dosyasının bulunacağı klasörü oluştur
        log_dir = os.path.dirname(settings.LOG_FILE)
        if log_dir:
            # Klasör yoksa oluştur (exist_ok=True ile hata vermez)
            os.makedirs(log_dir, exist_ok=True)

        # ==================== FILE HANDLER ====================
        # Log mesajlarını dosyaya yazan handler
        file_handler = logging.FileHandler(settings.LOG_FILE)
        # Dosya için detaylı format: tarih-saat, logger adı, seviye, mesaj
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # ==================== CONSOLE HANDLER ====================
        # Log mesajlarını konsola yazan handler
        console_handler = logging.StreamHandler()
        # Konsol için basit format: sadece seviye ve mesaj
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        # Handler'ları logger'a ekle
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        """
        Bilgi seviyesinde log mesajı yazar.
        
        Genel bilgilendirme mesajları için kullanılır.
        Örnek: "Test başlatıldı", "Sayfa yüklendi"
        
        Args:
            message: Log edilecek mesaj
        """
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """
        Debug seviyesinde log mesajı yazar.
        
        Detaylı debug bilgileri için kullanılır.
        Sadece LOG_LEVEL=DEBUG olduğunda görünür.
        Örnek: "Element bulundu: xpath=//button", "Click işlemi yapıldı"
        
        Args:
            message: Log edilecek mesaj
        """
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Uyarı seviyesinde log mesajı yazar.
        
        Potansiyel sorunlar için kullanılır.
        Örnek: "Element geç yüklendi", "Retry yapılıyor"
        
        Args:
            message: Log edilecek mesaj
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Hata seviyesinde log mesajı yazar.
        
        Ciddi hatalar için kullanılır.
        Örnek: "Element bulunamadı", "Test başarısız"
        
        Args:
            message: Log edilecek mesaj
        """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Kritik seviyesinde log mesajı yazar.
        
        Sistem durdurucu hatalar için kullanılır.
        Örnek: "WebDriver başlatılamadı", "Konfigürasyon hatası"
        
        Args:
            message: Log edilecek mesaj
        """
        self.logger.critical(message)


# Global logger instance'ı
# Tüm projede bu instance kullanılarak log işlemleri yapılır
# Import edilerek kullanılır: from utils.logger import logger
logger = TestLogger()
