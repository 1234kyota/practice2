import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import logging


# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
   # 検索結果の結果の各コンテンツを取得

    company_list = []
    i = 0
    log = 0

    try:
        while True:
            i += 1
            # contents_count = len(contents)
            contents = driver.find_elements_by_class_name("cassetteRecruit__content")

            time.sleep(3)

            #   3つの要素を取得しリスト化


            #   コンテンツ取得
            for content in contents[:3]:
                
                # ログ取得
                log += 1
                logging.basicConfig(filename='debbug.log', level=logging.DEBUG)
                logging.info(f'{log}件目')
                logging.critical('criticalメッセージ')
                logging.error('errorメッセージ')
                logging.warning('warningメッセージ')
                logging.debug('debugメッセージ')
            #  各会社の情報のリスト作成
                company = []
            #  各会社の名前をリストに追加
                name_text = content.find_element_by_class_name("cassetteRecruit__name").text
                company.append(name_text)

            
            #  各会社の仕事内容、初任給をリストか

            #  会社情報を取得
                explanation_list = content.find_elements_by_class_name("tableCondition__head")

            #  会社情報をテキスト化してリスト化
                explanation_text_list = []

                for explanation in explanation_list:
                    explanation_text_list.append(explanation.text)

            #  テキスト化された会社情報をcompanyリストへ追加
                if "仕事内容" in explanation_text_list:
                    work = content.find_elements_by_class_name("tableCondition__body")[0].text
                    company.append(work)
                else:
                    company.append('未記載')

                if "初年度年収" in explanation_text_list:
                    salary = content.find_elements_by_class_name("tableCondition__body")[4].text
                    company.append(salary)
                else:
                    company.append('未記載')
                
                
                company_list.append(company)


                
            if i > 2:
                break        

                # 次へボタンクリック
            driver.find_element_by_class_name("iconFont--arrowLeft").click()
    except:
        pass
    

    word = input('探したい文字列を入力してください >>')
    for conmpany in company_list:
        for explanation in conmpany:
            if word in explanation:
                print(conmpany)
    

    df = pd.DataFrame(company_list, columns=['name', '会社説明','初年度年収'])
    df.to_csv("./company.csv")


    

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
