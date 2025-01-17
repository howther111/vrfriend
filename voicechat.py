from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chromedriverのパスを指定
CHROMEDRIVER_PATH = ""

# Seleniumの設定
options = Options()
#options.add_argument("--headless")  # 必要に応じてヘッドレスモードを解除
options.add_argument("--disable-gpu")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # URLをmiibo_voicechat_url.txtから読み込む
    with open("miibo_voicechat_url.txt", "r") as file:
        url = file.readline().strip()  # ファイルの最初の行を読み取る

    if not url:
        raise ValueError("miibo_voicechat_url.txtに有効なURLが記載されていません。")

    # 読み込んだURLを開く
    driver.get(url)

    while True:
        try:
            # 条件を満たすbuttonタグを取得
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//button[img[@src='/assets/images/mike.png'] and not(contains(@style, 'display:none'))]"))
            )

            # ボタンをクリック
            button.click()
            print("ボタンをクリックしました")

        except Exception as e:
            print("条件を満たすボタンが見つかりません:", str(e))

        # 10秒待機
        time.sleep(10)

finally:
    # ブラウザを閉じる
    driver.quit()