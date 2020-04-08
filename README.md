# course.NCKU.edu.tw-Python-Crawler

### 使用工具
1. selenium: 可以實際開啟 browser 去開啟網站，做到點選、上一頁...等動作
    * 解決抓取網頁原始碼問題: js 產生網頁碼用 reqeusts 工具抓不到
        * browser 右鍵，點選"檢視網頁原始碼看不到"
        * 按 F12 才看的到
2. Firefox(真的 browser), [geckodriver](https://github.com/mozilla/geckodriver/releases)
2. xpath: 節點搜尋

### 一些注意的點
1. 先搜尋某些節點，再搜尋下一個節點的方法: xpath 好像不能連續搜尋，.find_elements_by_xxx 這種才可以(我沒有仔細查，不過用起來是這樣)
```python=
browser = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")
```
* 拆解上面程式碼的方法: 不能用第二句，會搜尋到整篇的 \<td> (所以底下的第一句如同不存在)，解決辦法是用第三句
```python=
browser = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr")
wrong = browser.find_elements_by_xpath("//td")
correct = browser.find_elements_by_css_selector('a')
```
2. 當點選頁面之後，回到上一頁，原本搜尋的東西都不能用了，要重新搜尋
```python=
depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
depart[0].click()
.
.
browser.back()
depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
```
3. 解決出現英文頁面問題: 要求中文 'zh-CN'
```python=
profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-CN')    # query chinese page
browser = webdriver.Firefox(firefox_profile = profile)
```
4. 頁面還沒跑完就執行下一步: 我很粗略地只要換頁面就強迫等待3秒才繼續做事 (會受網速影響)
    * 錯誤訊息像是 `is not clickable at point (x,y)`
    * 或是還沒進到新頁面就已經開始爬，這樣會爬不到，頁面跳轉也會出問題
5. 注意 Locating Elements 的名字有沒有加 s: 底下一個有加一個沒加，其中有加的那個會返回 list()
```python=
college = panel.find_element_by_class_name('panel-heading')
departs = panel.find_elements_by_class_name('btn_dept')
```

### 參考資料(紀錄幾個不錯的網站，但不見得有用到)
[BeautifulSoup](https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/)
[requests](https://blog.gtwang.org/programming/python-requests-module-tutorial/)

