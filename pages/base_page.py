"""
Base Page Sınıfı - Insider POM projesi için temel sayfa sınıfı.

Bu sınıf, tıklama, element bekleme ve metin alma gibi yaygın Selenium
işlemlerini sarmalayarak kod tekrarını önler. Tüm diğer page object'ler
bu temel sınıftan miras alır ve ortak fonksiyonları kullanır.

Page Object Model (POM) design pattern'inin temel taşıdır.
"""

from typing import List, Optional
import time

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from utils.logger import logger
from utils.retry_decorator import retry
from config.settings import settings


class BasePage:
    """
    Tüm page object'lerin miras aldığı temel sınıf.
    
    Bu sınıf, web sayfalarıyla etkileşim için gerekli olan temel
    Selenium işlemlerini sağlar. Her page object bu sınıftan miras
    alarak ortak fonksiyonları kullanabilir.
    """

    def __init__(self, driver: WebDriver, timeout: Optional[int] = None) -> None:
        """
        BasePage instance'ını başlatır.
        
        Args:
            driver: Selenium WebDriver instance'ı
            timeout: Element bekleme süresi (None ise settings'ten alınır)
        """
        # WebDriver instance'ını sakla
        self.driver = driver
        # Timeout değerini ayarla (verilmemişse settings'ten al)
        self.timeout = timeout or settings.EXPLICIT_WAIT
        # WebDriverWait instance'ını oluştur (explicit wait için)
        self.wait = WebDriverWait(driver, self.timeout)
        # Hangi page object'in başlatıldığını logla
        logger.debug(f"{self.__class__.__name__} sınıfı başlatıldı")

    @retry(exceptions=(ElementClickInterceptedException, StaleElementReferenceException))
    def click(self, by: By, locator: str) -> None:
        """
        Element'in tıklanabilir olmasını bekler ve retry logic ile tıklar.
        
        Bu metod, element'in tıklanabilir duruma gelmesini bekler ve
        geçici hatalar durumunda otomatik olarak tekrar dener.
        
        Args:
            by: Element bulma yöntemi (By.ID, By.XPATH, vb.)
            locator: Element'in locator değeri
            
        Raises:
            TimeoutException: Element belirtilen sürede tıklanabilir olmadıysa
        """
        logger.debug(f"Element tıklanıyor: {by}={locator}")
        # Element'in tıklanabilir olmasını bekle
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))

        try:
            # Normal tıklama işlemini dene
            element.click()
        except ElementClickInterceptedException:
            # Normal tıklama başarısız olursa JavaScript ile tıkla
            logger.warning(f"Normal tıklama başarısız: {locator}, JavaScript ile deneniyor")
            self.driver.execute_script("arguments[0].click();", element)

    def click_with_js(self, by: By, locator: str) -> None:
        """
        Element'i JavaScript kullanarak tıklar.
        
        Normal tıklama işlemi çalışmadığında alternatif olarak kullanılır.
        Özellikle overlay'ler veya gizli element'ler için faydalıdır.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
        """
        logger.debug(f"JavaScript ile element tıklanıyor: {by}={locator}")
        element = self.find(by, locator)
        self.driver.execute_script("arguments[0].click();", element)

    def hover(self, by: By, locator: str) -> None:
        """
        Element'in üzerine mouse ile hover yapar.
        
        Dropdown menüler veya hover efektleri için kullanılır.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
        """
        logger.debug(f"Element üzerine hover yapılıyor: {by}={locator}")
        element = self.find(by, locator)
        ActionChains(self.driver).move_to_element(element).perform()

    @retry(exceptions=(StaleElementReferenceException,))
    def type(self, by: By, locator: str, text: str, clear_first: bool = True) -> None:
        """
        Element'in görünür olmasını bekler ve metin girer.
        
        Input field'lara metin girmek için kullanılır.
        Varsayılan olarak önce mevcut metni temizler.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            text: Girilecek metin
            clear_first: Önce mevcut metni temizle (varsayılan: True)
        """
        logger.debug(f"'{text}' metni giriliyor: {by}={locator}")
        # Element'in görünür olmasını bekle
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))

        if clear_first:
            # Mevcut metni temizle
            element.clear()
        # Yeni metni gir
        element.send_keys(text)

    @retry(exceptions=(StaleElementReferenceException,))
    def find(self, by: By, locator: str) -> WebElement:
        """
        Tek bir WebElement döndürür, varlığını bekler.
        
        Element'in DOM'da bulunmasını bekler ve döndürür.
        En temel element bulma metodudur.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            
        Returns:
            WebElement: Bulunan element
            
        Raises:
            TimeoutException: Element belirtilen sürede bulunamazsa
        """
        logger.debug(f"Element aranıyor: {by}={locator}")
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def finds(self, by: By, locator: str) -> List[WebElement]:
        """
        Birden fazla WebElement döndürür, bekleme yapmaz.
        
        Aynı locator'a sahip birden fazla element bulmak için kullanılır.
        Liste halinde döndürür, boş liste de olabilir.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            
        Returns:
            List[WebElement]: Bulunan element'lerin listesi
        """
        logger.debug(f"Çoklu element aranıyor: {by}={locator}")
        return self.driver.find_elements(by, locator)

    def exists(self, by: By, locator: str, timeout: Optional[int] = None) -> bool:
        """
        Element'in belirtilen süre içinde var olup olmadığını kontrol eder.
        
        Element'in varlığını kontrol etmek için kullanılır.
        Exception fırlatmaz, sadece True/False döndürür.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            timeout: Bekleme süresi (None ise varsayılan timeout kullanılır)
            
        Returns:
            bool: Element varsa True, yoksa False
        """
        wait_time = timeout or self.timeout
        temp_wait = WebDriverWait(self.driver, wait_time)

        try:
            temp_wait.until(EC.presence_of_element_located((by, locator)))
            logger.debug(f"Element mevcut: {by}={locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element mevcut değil: {by}={locator}")
            return False

    def wait_for_element_visible(
        self, by: By, locator: str, timeout: Optional[int] = None
    ) -> WebElement:
        """
        Element'in görünür olmasını bekler ve döndürür.
        
        Element'in sadece DOM'da değil, aynı zamanda görünür olmasını bekler.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            timeout: Bekleme süresi
            
        Returns:
            WebElement: Görünür hale gelen element
        """
        wait_time = timeout or self.timeout
        temp_wait = WebDriverWait(self.driver, wait_time)
        logger.debug(f"Element'in görünür olması bekleniyor: {by}={locator}")
        return temp_wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_for_element_clickable(
        self, by: By, locator: str, timeout: Optional[int] = None
    ) -> WebElement:
        """
        Element'in tıklanabilir olmasını bekler ve döndürür.
        
        Element'in hem görünür hem de tıklanabilir durumda olmasını bekler.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            timeout: Bekleme süresi
            
        Returns:
            WebElement: Tıklanabilir hale gelen element
        """
        wait_time = timeout or self.timeout
        temp_wait = WebDriverWait(self.driver, wait_time)
        logger.debug(f"Element'in tıklanabilir olması bekleniyor: {by}={locator}")
        return temp_wait.until(EC.element_to_be_clickable((by, locator)))

    def get_text(self, by: By, locator: str) -> str:
        """
        Element'in metnini alır.
        
        Element'in görünür metnini döndürür.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            
        Returns:
            str: Element'in metni
        """
        logger.debug(f"Element'in metni alınıyor: {by}={locator}")
        element = self.find(by, locator)
        return element.text

    def get_attribute(self, by: By, locator: str, attribute: str) -> Optional[str]:
        """
        Element'in belirtilen attribute değerini alır.
        
        HTML attribute'larını (href, class, id vb.) almak için kullanılır.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
            attribute: Alınacak attribute adı
            
        Returns:
            Optional[str]: Attribute değeri (yoksa None)
        """
        logger.debug(f"'{attribute}' attribute'u alınıyor: {by}={locator}")
        element = self.find(by, locator)
        return element.get_attribute(attribute)

    def scroll_to_element(self, by: By, locator: str) -> None:
        """
        Element'e kadar scroll yapar.
        
        Element'in görünür alana gelmesi için sayfa kaydırır.
        
        Args:
            by: Element bulma yöntemi
            locator: Element'in locator değeri
        """
        logger.debug(f"Element'e scroll yapılıyor: {by}={locator}")
        element = self.find(by, locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Smooth scrolling için kısa bekleme

    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Sayfanın tamamen yüklenmesini bekler.
        
        JavaScript'in document.readyState kontrolü ile
        sayfanın tamamen yüklendiğinden emin olur.
        
        Args:
            timeout: Bekleme süresi
        """
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.debug("Sayfa tamamen yüklendi")

    def switch_to_new_window(self) -> None:
        """
        En yeni pencere/tab'a geçiş yapar.
        
        Yeni açılan pencere veya tab'a odaklanmak için kullanılır.
        """
        logger.debug("Yeni pencereye geçiş yapılıyor")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_window_and_switch_back(self) -> None:
        """
        Mevcut pencereyi kapatır ve ana pencereye geri döner.
        
        Pop-up veya yeni tab'ları kapatmak için kullanılır.
        """
        logger.debug("Mevcut pencere kapatılıyor ve ana pencereye dönülüyor")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
