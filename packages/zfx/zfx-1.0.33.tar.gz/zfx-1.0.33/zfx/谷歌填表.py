import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def 谷歌填表_初始化(chrome驱动路径, 浏览器路径, 启动参数=[]):
    """
    初始化谷歌填表驱动器。

    参数:
        chrome驱动路径 (str): Chrome 驱动程序的路径。
        浏览器路径 (str): Chrome 浏览器的路径。
        启动参数 (list): 启动参数列表，每个元素是一个字符串，表示一个启动参数。

    返回:
        WebDriver: Chrome 浏览器的驱动器对象。成功返回 Chrome 浏览器的驱动器对象，失败返回 False。

    使用示例:
        chrome驱动路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chromedriver.exe"
        浏览器路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chrome.exe"
        启动参数 = ["--incognito", "--disable-gpu"]  # 添加启动参数
        driver = 谷歌填表_初始化(chrome驱动路径, 浏览器路径, 启动参数)
    """
    try:
        # 创建 ChromeDriver 服务对象
        chrome服务 = Service(chrome驱动路径)

        # 启动 ChromeDriver 服务
        chrome服务.start()

        # 创建 Chrome 驱动器对象并指定服务
        选项 = webdriver.ChromeOptions()
        选项.binary_location = 浏览器路径

        # 添加启动参数
        for 参数 in 启动参数:
            选项.add_argument(参数)

        驱动器 = webdriver.Chrome(service=chrome服务, options=选项)

        return 驱动器
    except Exception:
        return False


def 谷歌填表_初始化2(chrome驱动路径, 浏览器路径, 启动参数=[], 允许加载图片=True):
    """
    返回一个用于后续浏览器操作的驱动对象。

    参数:
        chrome驱动路径 (str): Chrome 驱动程序的路径。
        浏览器路径 (str): Chrome 浏览器的路径。
        启动参数 (list): 启动参数列表，每个元素是一个字符串，表示一个启动参数。
        允许加载图片 (bool): 是否允许加载图片，默认为 True。

    返回:
        WebDriver: Chrome 浏览器的驱动器对象。成功返回 Chrome 浏览器的驱动器对象，失败返回 False。

    使用示例:
        chrome驱动路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chromedriver.exe"
        浏览器路径 = "C:\\Users\\Administrator\\Desktop\\chrome-win64\\chrome.exe"
        启动参数 = ["--incognito", "--disable-gpu"]  # 添加启动参数
        driver = 谷歌填表_初始化(chrome驱动路径, 浏览器路径, 启动参数)
    """
    try:
        # 创建 ChromeDriver 服务对象
        chrome服务 = Service(chrome驱动路径)

        # 启动 ChromeDriver 服务
        chrome服务.start()

        # 创建 Chrome 驱动器对象并指定服务
        选项 = webdriver.ChromeOptions()
        选项.binary_location = 浏览器路径

        if not 允许加载图片:
            选项.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        # 添加启动参数
        for 参数 in 启动参数:
            选项.add_argument(参数)

        驱动器 = webdriver.Chrome(service=chrome服务, options=选项)

        return 驱动器
    except Exception:
        return False


def 谷歌填表_访问网页(参_driver, 网址):
    """
    使用提供的驱动程序访问指定的网址。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。
        网址: 要访问的网址。

    Returns:
        bool: 访问成功返回 True，访问失败返回 False。
    """
    try:
        参_driver.get(网址)
        return True
    except Exception:
        return False


def 谷歌填表_置浏览器大小和位置(参_driver, 宽度, 高度, x_位置, y_位置):
    """
    设置浏览器窗口的大小和位置。
    参数:
        驱动器: WebDriver 对象，表示浏览器驱动器。
        宽度: int，表示窗口宽度（像素）。
        高度: int，表示窗口高度（像素）。
        x_位置: int，表示窗口左上角的 x 坐标位置。
        y_位置: int，表示窗口左上角的 y 坐标位置。
    """
    参_driver.set_window_size(宽度, 高度)
    参_driver.set_window_position(x_位置, y_位置)


def 谷歌填表_后退(参_driver):
    """
    使用提供的驱动程序执行后退操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.back()


def 谷歌填表_前进(参_driver):
    """
    使用提供的驱动程序执行前进操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.forward()


def 谷歌填表_刷新(参_driver):
    """
    使用提供的驱动程序执行刷新操作。

    Args:
        参_driver: WebDriver 对象，用于控制浏览器的行为。

    Returns:
        无
    """
    参_driver.refresh()


def 谷歌填表_查找元素(参_driver, 定位方法, 定位值):
    """
    参_driver: WebDriver 对象，即浏览器驱动器，用于在网页上执行操作。
    定位方法: 定位方法，指定如何定位元素，可以是 "id"、"name"、"class_name"、"xpath" 等。
    定位值: 定位值，根据定位方法指定的方式，传入相应的定位值。
    返回 查找到的第一个元素，如果找不到则返回 None
    """
    try:
        元素对象 = 参_driver.find_element(by=定位方法, value=定位值)
        time.sleep(1)
        return 元素对象
    except Exception:
        return None


def 谷歌填表_查找多个元素(参_driver, 定位方法, 定位值):
    """
    参_driver: WebDriver 对象，即浏览器驱动器，用于在网页上执行操作。
    定位方法: 定位方法，指定如何定位元素，可以是 "id"、"name"、"class_name"、"xpath" 等。
    定位值: 定位值，根据定位方法指定的方式，传入相应的定位值。
    返回 查找到的所有元素列表，如果找不到任何元素，则返回 None
    """
    try:
        元素对象 = 参_driver.find_elements(by=定位方法, value=定位值)
        time.sleep(1)
        return 元素对象
    except Exception:
        return None


def 谷歌填表_点击元素(元素):
    """
    点击指定的网页元素。

    Args:
        元素: 要点击的元素对象。

    Returns:
        bool: 如果点击成功，则返回 True，否则返回 False。
    """
    try:
        元素.click()
        return True
    except Exception:
        return False


def 谷歌填表_输入文本(元素, 文本):
    """
    在指定的网页元素中输入文本。

    Args:
        元素: 要输入文本的元素对象。
        文本: 要输入的文本内容。

    Returns:
        bool: 输入文本成功返回 True，失败返回 False。
    """
    try:
        元素.send_keys(文本)
        return True
    except Exception:
        return False


def 谷歌填表_清除文本(元素):
    """
    清除元素中的文本。

    Args:
        元素: 要清除文本的元素对象。

    Returns:
        bool: 清除文本成功返回 True，失败返回 False。
    """
    try:
        元素.clear()
        return True
    except Exception:
        return False


def 谷歌填表_获取属性值(元素, 属性名):
    """
    获取元素的属性值。

    Args:
        元素: 要获取属性值的元素对象。
        属性名: 要获取的属性名称。

    Returns:
        str: 元素指定属性的值，如果属性不存在则返回 None。
    """
    try:
        return 元素.get_attribute(属性名)
    except Exception:
        return None


def 谷歌填表_判断可见(元素):
    """
    判断给定元素是否可见。

    Args:
        元素: 要进行可见性检查的元素对象。

    Returns:
        bool: 如果元素可见，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_displayed()
    except Exception:
        return False


def 谷歌填表_判断可用(元素):
    """
    判断给定元素是否可用。

    Args:
        元素: 要进行可用性检查的元素对象。

    Returns:
        bool: 如果元素可用，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_enabled()
    except Exception:
        return False


def 谷歌填表_判断选中(元素):
    """
    判断给定元素是否选中。

    Args:
        元素: 要进行选中状态检查的元素对象。

    Returns:
        bool: 如果元素选中，则返回 True；否则返回 False。
    """
    try:
        return 元素.is_selected()
    except Exception:
        return False


def 谷歌填表_等待元素出现(参_driver, 定位方法, 定位值, 超时时间=10):
    """
    使用提供的WebDriver等待指定元素出现。

    Args:
        参_driver: WebDriver对象，用于控制浏览器的行为。
        定位方法: 用于定位元素的方法，例如 'id', 'class_name', 'xpath'等。
        定位值: 元素的定位值。
        超时时间: 等待元素出现的最长时间，单位为秒，默认为10秒。

    Returns:
        如果元素出现，则返回该元素对象；如果超时未出现，则返回 None。
    """
    try:
        元素对象 = WebDriverWait(参_driver, 超时时间).until(EC.presence_of_element_located((定位方法, 定位值)))
        time.sleep(1)
        return 元素对象
    except Exception:
        return None


def 谷歌填表_等待元素可见(参_driver, 定位方法, 定位值, 超时时间=10):
    """
    使用提供的WebDriver等待指定元素可见。

    Args:
        参_driver: WebDriver对象，用于控制浏览器的行为。
        定位方法: 用于定位元素的方法，例如 'id', 'class_name', 'xpath'等。
        定位值: 元素的定位值。
        超时时间: 等待元素可见的最长时间，单位为秒，默认为10秒。

    Returns:
        如果元素可见，则返回该元素对象；如果超时未可见，则返回 None。
    """
    try:
        元素对象 = WebDriverWait(参_driver, 超时时间).until(EC.visibility_of_element_located((定位方法, 定位值)))
        time.sleep(1)
        return 元素对象
    except Exception:
        return None


def 谷歌填表_等待元素可点击(参_driver, 定位方法, 定位值, 超时时间=10):
    """
    使用提供的WebDriver等待指定元素可点击。

    Args:
        参_driver: WebDriver对象，用于控制浏览器的行为。
        定位方法: 用于定位元素的方法，例如 'id', 'class_name', 'xpath'等。
        定位值: 元素的定位值。
        超时时间: 等待元素可点击的最长时间，单位为秒，默认为10秒。

    Returns:
        如果元素可点击，则返回该元素对象；如果超时未可点击，则返回 None。
    """
    try:
        元素对象 = WebDriverWait(参_driver, 超时时间).until(EC.element_to_be_clickable((定位方法, 定位值)))
        time.sleep(1)
        return 元素对象
    except Exception:
        return None


def 谷歌填表_执行JavaScript(参_driver, 脚本, *参数):
    """
    执行 JavaScript 脚本。

    Args:
        参_driver: WebDriver 对象。
        脚本: 要执行的 JavaScript 脚本。
        *参数: 传递给 JavaScript 脚本的参数。

    Returns:
        执行 JavaScript 脚本后的返回值。
    """
    return 参_driver.execute_script(脚本, *参数)


def 谷歌填表_切换窗口(参_driver, 窗口名称):
    """
    切换到指定名称的窗口。

    Args:
        参_driver: WebDriver 对象。
        窗口名称: 要切换到的窗口的名称。
    """
    参_driver.switch_to.window(窗口名称)


def 谷歌填表_切换框架(参_driver, 框架引用):
    """
    切换到指定的框架。

    Args:
        参_driver: WebDriver 对象。
        框架引用: 要切换到的框架的引用，可以是名称、索引或 WebElement 对象。
    """
    参_driver.switch_to.frame(框架引用)


def 谷歌填表_保存截图(参_driver, 文件名):
    """
    保存当前页面的截图。

    Args:
        参_driver: WebDriver 对象。
        文件名: 要保存的截图文件的名称。
    """
    参_driver.save_screenshot(文件名)


def 谷歌填表_获取页面源代码(参_driver):
    """
    获取当前页面的源代码。

    Args:
        参_driver: WebDriver 对象。

    Returns:
        当前页面的源代码，如果失败则返回 None。
    """
    try:
        return 参_driver.page_source
    except Exception:
        return None


def 谷歌填表_偏移点击(参_driver, 元素, x偏移量=0, y偏移量=0):
    """
    在元素上应用偏移量并点击。

    参数：
    - driver: WebDriver 对象
    - 元素: 要点击的元素
    - x偏移量: X 轴偏移量，默认为 0
    - y偏移量: Y 轴偏移量，默认为 0
    """
    # 创建 ActionChains 对象
    动作 = ActionChains(参_driver)

    # 将鼠标移动到元素位置，并添加偏移量
    动作.move_to_element_with_offset(元素, x偏移量, y偏移量)

    # 执行点击操作
    动作.click().perform()


def 谷歌填表_模拟点击(driver, 元素对象):
    """
    模拟点击元素对象。

    参数:
    - driver: WebDriver 对象，用于执行 JavaScript 脚本。
    - 元素对象: 要模拟点击的 WebElement 对象。
    """
    driver.execute_script("arguments[0].click();", 元素对象)
