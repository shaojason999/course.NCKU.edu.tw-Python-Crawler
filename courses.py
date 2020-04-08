from selenium import webdriver
import csv
import time

f_csv = open('ncku_course.csv','w')
writer = csv.writer(f_csv)
#f = open('ncku_course_data','w')

course_list_name = ['系所名稱','系號-序號','年級','類別','科目名稱','學分選必修','教師姓名','已選課人數/餘額','時間/教室','課程大綱']
writer.writerow(course_list_name)

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-CN')    # query chinese page
browser = webdriver.Firefox(firefox_profile = profile)

browser.get('https://course.ncku.edu.tw/index.php?c=qry_all') 

departs = browser.find_elements_by_xpath("//*[@class='btn_dept']") # have to type in the complete class=' '
depart_list = []
for depart in departs:
    depart_list.append(depart.text)

for i in range(int(len(depart_list)/2)):
#for i in range(3):
    time.sleep(3)   # wait for 5 seconds
    depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
    depart_name = depart[0].text
    depart[0].click()
    time.sleep(3)   # wait for 5 seconds
    courses_elements = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")

    course_list = [depart_name]

    """ used for write csv (start)"""
    for i,element in enumerate(courses_elements):
        if (i%10 == 0): # discard first one
            continue
        elif (i%10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            if (len(href) == 0):    # no href exits
                course_list.append([])
            else:
                url = href[0].get_attribute('href')
                if (url[0] != 'h'):    # not a url
                    course_list.append([])
                else:
                    course_list.append(url)
        else:   # we don't need the text of the last one (when i%10 == 9)
            course_list.append(element.text.split())
        if (i%10 == 9):    # last one
            writer.writerow(course_list)
            course_list = [depart_name]
    """ used for write csv (end) """

    """ used for write txt file
    for i,element in enumerate(courses_elements):
        if (i%10 == 0): # discard first one
            continue
        elif (i%10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            href = [href[0].get_attribute('href')] # convert from string to list, because .extend() accept list
            course_list.extend(href)
        else:   # we don't need the text of the last one (when i%10 == 9)
            course_list.extend(element.text.split())
        if (i%10 == 9):    # last one
            for j,item in enumerate(course_list):
                if (j == len(course_list)-1):
                    f.write(item + '\n')
                    break 
                else:
                    f.write(item + ',')
            course_list = [depart_name]
    """
    browser.back()

f_csv.close()
# f.close()
browser.quit()

