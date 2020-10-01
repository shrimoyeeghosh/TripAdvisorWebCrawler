import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# import the webdriver, chrome driver is recommended
driver = webdriver.Chrome("/usr/bin/chromedriver")

# insert the tripadvisor's website of one attraction
driver.get("https://www.tripadvisor.in/Attraction_Review-g503703-d666591-Reviews-Jagannath_Temple-Puri_Puri_District_Odisha.html")

# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
# code for selecting the review rating?
"""time.sleep(2)
driver.find_element_by_xpath('//label[@for="ReviewRatingFilter_5"]').click()
time.sleep(2) """

# open the file to save the review
with open('jtreviews.tsv', 'a') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')


    # write the column name and shit
    tsv_writer.writerow(
        ["score", "location", "review"])

    # change the value inside the range to save more or less

    # this part controls the number of pages in the TripAdvisor place
    for i in range(0, 538):
        # PRINT THE CURRENT PAGE
        print(i)

        #click on link read more
        if (check_exists_by_xpath("//span[@class='_3maEfNCR']")):
            time.sleep(5)
            driver.find_element_by_xpath("//span[@class='_3maEfNCR']").click()

        # find the number of reviews in one page
        container = driver.find_elements_by_xpath("//div[@class='Dq9MAugU T870kzTX LnVzGwUB']")
        num_page_items = len(container)
        print(num_page_items)

        #make a loop for the numbers of elements found
        for j in range(num_page_items):
            # to save the rating
            string = container[j].find_element_by_xpath(
                ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            data = string.split("_")
            #print(data)

            # to save the location
            locstring = container[j].find_element_by_xpath(
                "//span[@class='default _3J15flPT small']").get_attribute("innerHTML")
            location = locstring.split(">")
            # print(location)

            # to expand review
            """if (check_exists_by_xpath("//span[@class='_3maEfNCR']")):
                print("yipee")
                container[j].find_element_by_xpath("//span[@class='_3maEfNCR']").click()"""


            # to get review
            review = container[j].find_element_by_xpath(".//q[@class='IRsGHoPm']").get_attribute("innerHTML")
            # Note- Probably a better way to this exists, but I'm not patient enough to find it.
            reviewsmall = review.split(">")
            reviewsmaller = reviewsmall[1].split('<')
            freview = reviewsmaller[0]
            #print(reviewsmaller)

            # to save in a csv file readable the star and the review [Ex: 50,"I love this place"]
            tsv_writer.writerow(
              [data[3], location[2], freview])
            #tsv_writer.writerow(
               #[data[3], location[2], container[j].find_element_by_xpath(".//q[@class='IRsGHoPm']").text.replace("\n", "")])

        # to change the page
        if (check_exists_by_xpath('//a[@class="ui_button nav next primary "]')):
            driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]').click()
        time.sleep(5)

driver.close()

