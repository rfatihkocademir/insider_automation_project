"""
Retry Decorator - Flaky test operasyonlarını yönetmek için decorator.

Bu modül, geçici hatalar nedeniyle başarısız olan fonksiyonları
otomatik olarak tekrar denemeyi sağlar. Web testlerinde ağ sorunları,
timing sorunları ve element yükleme gecikmeleri gibi durumlar için kritiktir.
"""

import time
import functools
from typing import Callable, Any, Type, Tuple

from utils.logger import logger
from config.settings import settings


def retry(
    max_attempts: int = None,
    delay: float = None,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """
    Geçici hatalar için fonksiyonları tekrar deneyen decorator.
    
    Bu decorator, belirtilen exception türleri yakalandığında
    fonksiyonu belirlenen sayıda tekrar dener. Web testlerinde
    StaleElementReferenceException, TimeoutException gibi geçici
    hatalar için çok faydalıdır.

    Args:
        max_attempts: Maksimum deneme sayısı (None ise settings'ten alınır)
        delay: Denemeler arası bekleme süresi saniye cinsinden (None ise settings'ten alınır)
        exceptions: Yakalanacak exception türlerinin tuple'ı (varsayılan: tüm exception'lar)
        
    Returns:
        Callable: Retry logic'i eklenmiş decorator fonksiyonu
        
    Example:
        @retry(max_attempts=3, delay=1, exceptions=(TimeoutException,))
        def click_element(self, locator):
            element = self.find_element(locator)
            element.click()
    """
    # Eğer parametreler verilmemişse settings'ten al
    if max_attempts is None:
        max_attempts = settings.MAX_RETRIES
    if delay is None:
        delay = settings.RETRY_DELAY

    def decorator(func: Callable) -> Callable:
        """
        Asıl decorator fonksiyonu.
        
        Args:
            func: Retry logic'i eklenecek fonksiyon
            
        Returns:
            Callable: Wrapper fonksiyon
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            Fonksiyonu retry logic'i ile sarmalayan wrapper.
            
            Args:
                *args: Orijinal fonksiyonun pozisyonel argümanları
                **kwargs: Orijinal fonksiyonun keyword argümanları
                
            Returns:
                Any: Orijinal fonksiyonun dönüş değeri
                
            Raises:
                Exception: Tüm denemeler başarısız olursa son exception'ı fırlatır
            """
            last_exception = None

            # Belirtilen sayıda deneme yap (max_attempts + 1 = ilk deneme + retry'lar)
            for attempt in range(max_attempts + 1):
                try:
                    # Fonksiyonu çalıştırmayı dene
                    return func(*args, **kwargs)
                except exceptions as e:
                    # Belirtilen exception türlerinden biri yakalandı
                    last_exception = e
                    
                    if attempt < max_attempts:
                        # Henüz maksimum deneme sayısına ulaşılmadı, tekrar dene
                        logger.warning(
                            f"Deneme {attempt + 1} başarısız - {func.__name__}: {e}. "
                            f"{delay} saniye sonra tekrar denenecek..."
                        )
                        time.sleep(delay)
                    else:
                        # Tüm denemeler tükendi
                        logger.error(
                            f"Tüm {max_attempts + 1} deneme başarısız - {func.__name__}"
                        )

            # Tüm denemeler başarısız oldu, son exception'ı fırlat
            raise last_exception

        return wrapper

    return decorator
