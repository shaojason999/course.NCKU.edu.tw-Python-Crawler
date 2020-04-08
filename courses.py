from selenium import webdriver
import csv
import time

f_csv = open('ncku_course.csv','w')
writer = csv.writer(f_csv)

course_list_name = ['學院','系所名稱','系號-序號','年級','類別','科目名稱','學分選必修','教師姓名','已選課人數/餘額','時間/教室','課程大綱']
writer.writerow(course_list_name)

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-CN')    # query chinese page
browser = webdriver.Firefox(firefox_profile = profile)

browser.get('https://course.ncku.edu.tw/index.php?c=qry_all') 

college_list = []
depart_list = []
panels = browser.find_elements_by_class_name('panel-default')
panels = panels[:int(len(panels)/2)]  # cut in half

for panel in panels:
    college = panel.find_element_by_class_name('panel-heading')
    departs = panel.find_elements_by_class_name('btn_dept')
    college_list.extend([college.text]*len(departs))
    for depart in departs:
        depart_list.append(depart.text)

for i in range(len(depart_list)):
    time.sleep(3)   # wait for 5 seconds
    college_name = college_list[i]
    depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])[0]  # use the first one
    depart_name = depart.text
    course_list = [college_name,depart_name]

    depart.click()
    time.sleep(3)   # wait for 5 seconds
    courses_elements = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")

    for i,element in enumerate(courses_elements):
        if (i%10 == 0): # discard first one
            continue
        elif (i%10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            if (len(href) == 0):    # no href exits
                course_list.append('')
            else:
                url = href[0].get_attribute('href')
                if (url[0] != 'h'):    # not a url
                    course_list.append('')
                else:
                    course_list.append(url)

            # output                    
            writer.writerow(course_list)
            course_list = [college_name,depart_name]
        else:   # we don't need the text of the last one (when i%10 == 9)
            split_list = element.text.split()
            if (len(split_list) == 0):
                course_list.append('')
            else:
                course_list.append(split_list)

    browser.back()

f_csv.close()
browser.quit()

