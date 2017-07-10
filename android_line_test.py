import re
import unittest
from telnetlib import EC
from time import sleep

import os
from appium import webdriver

# Returns abs path relative to this file and not cwd
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class ComplexAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['noReset'] = 'true'
        desired_caps['fullReset'] = 'false'
        desired_caps['app'] = PATH('../../../sample-code/apps/line.apk')
        desired_caps['appPackage'] = 'jp.naver.line.android'
        # desired_caps['appActivity'] = 'com.android.packageinstaller.permission.ui.GrantPermissionsActivity'
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = '4.2'
        # desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['deviceName'] = 'LGMG600Sbefb676a'

        # desired_caps['avd'] = 'Nexus_5X_API_25_2'
        # desired_caps['app'] = PATH('../../../sample-code/apps/ApiDemos/bin/ApiDemos-debug.apk')


        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_line_initial_settings(self):
        sleep(1)

        # 탭정보 받아오기
        tabs = self.driver.find_elements_by_id('jp.naver.line.android:id/gnb_menu_item_icon')

        # 친구 탭 클릭
        tabs[0].click()
        # 친구를 포함한 TextView를 찾는다
        el = self.driver.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "친구")]')
        # 친구 (35명) 이라는 포맷의 TextView가 있는지 확인
        self.assertEqual(True, bool(re.match(r'^친구 \([0-9]+명\)$', el.text)))

        # 프로필 두번 클릭해서 내 프로필을 접었다가 펴기
        el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"프로필")]')
        self.assertIsNotNone(el)
        el.click()
        el.click()

        # 임지훈 프로필 클릭 (xpath로 이미지를 싸고있는 FrameLayout 찾아서 클릭)
        els = self.driver.find_elements_by_xpath(
            '//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView')
        self.assertIsNotNone(els)
        els[0].click()

        # 뒤로 (임지훈 프로필 끄기)
        self.driver.back()

        # 대화 탭 클릭
        tabs[1].click()
        # 대화를 포함한 TextView를 찾는다
        el = self.driver.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "대화")]')
        # 대화라는 이름의 TextView가 있는지 확인
        self.assertEqual(el.text, '대화')
        #
        els = self.driver.find_elements_by_xpath(
            '//android.widget.ListView/android.widget.FrameLayout/android.widget.RelativeLayout')
        try:
            # 맨 위에있는 대화창 하나 클릭
            els[0].click()
            # 뒤로 (대화창 끄기)
            self.driver.back()
        except IndexError:
            # 만약 대화창이 없으면 "대화 시작"이라는 버튼이 있어야 한다
            el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"대화 시작")]')
            self.assertIsNotNone(el)

        # 타임라인 탭 클릭
        tabs[2].click()
        # "타임라인"을 포함한 TextView를 찾는다
        el = self.driver.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "타임라인")]')
        # "타임라인"라는 이름의 TextView가 있는지 확인
        self.assertEqual(el.text, '타임라인')

        # 통화 탭 클릭
        tabs[3].click()
        # "통화"을 포함한 TextView를 찾는다
        el = self.driver.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "통화")]')
        # "통화"라는 이름의 TextView가 있는지 확인
        self.assertEqual(el.text, '통화')

        # 더보기 탭 클릭
        tabs[4].click()
        # "더보기"을 포함한 TextView를 찾는다
        el = self.driver.find_element_by_xpath(
            '//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@text, "더보기")]')
        # "더보기"라는 이름의 TextView가 있는지 확인
        self.assertEqual(el.text, '더보기')
        # 라인페이 클릭
        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"LINE Pay")]')
        except:
            self.driver.swipe(470, 1500, 470, 1000, 400)
            el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"LINE Pay")]')

        self.assertIsNotNone(el)
        el.click()
        sleep(1)




        els = self.driver.find_elements_by_xpath(
            '//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView')
        wait = WebDriverWait(self.driver, 1)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView')))
        self.assertEqual(len(els), 5)

        print("size : " + str(len(els)))
        for el in els:
            print(el)
            el.click()
            self.driver.implicitly_wait(4)


        print("size : " + str(len(els)))



        els = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
        self.assertIsInstance(els, list)
        for el in els:
            print(el)

        self.driver.find
        els = self.driver.find_elements_by_xpath("//*[@class='android.widget.TextView']")
        print(els)



        # 염정은 클릭
        el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "염정은")]')
        el.click();
        self.assertIsNotNone(el)


        # 대화 클릭
        el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "김도윤")]')

        self.assertIsNotNone(el)
        # 클릭가능한것 찾기


        sleep(5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ComplexAndroidTests)
    # suite2 = unittest.TestLoader().loadTestsFromName('android_complex.ComplexAndroidTests.test_smiley_face')
    unittest.TextTestRunner(verbosity=2).run(suite)
