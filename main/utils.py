import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import itertools
import os
from selenium.webdriver.support import expected_conditions
import requests
from webdriver_manager.chrome import ChromeDriverManager

def web_unblocker (main_link):
    """ Loaded to bypass any captcha issues. """    
    proxies = {
        'http': 'http://USERNAME:PASSWORD@unblock.oxylabs.io:60000',
        'https': 'http://USERNAME:PASSWORD@unblock.oxylabs.io:60000',
    }
    
    requests.get(
        main_link,
        verify=False,
        proxies=proxies
    )
    
    

def press_button(XPATH_button):
    """Presses the button whilst it is visible. Function applicable if contents are loaded into one page only """
    try:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,XPATH_button)))
        load_more = driver.find_element(By.XPATH, XPATH_button)
        string_unfound = False
        while load_more.is_displayed() and string_unfound == False:
            
            
            try:
                url_strings = driver.find_elements(By.XPATH,XPATH_break)
                
                for url_string in url_strings:
                    if url_string.text == string_blocker:
                        string_unfound = True
                        break
            except Exception as e:
                # print(e)
                pass

            driver.execute_script("arguments[0].click();", load_more)
            time.sleep(int(time_sleep)) # extremely slow-loading website
            WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,XPATH_button)))
            load_more = driver.find_element(By.XPATH, XPATH_button) # searches and clicks the load more button
    except Exception as e:
        print(e)


def get_spyder_links(XPATH_element):
    """Main function that collects spyder links"""
    # time.sleep()
    
    if load == "scroll_all_page":
        # pages where you have to scroll down to load all the links
        time_start = time.time()
        # time_sleep is hardcoded and must be identified after manually going through the site
        while time.time() < int(time_sleep) + time_start:
            var_check = 0
            if var_check == 5: 
                break
            var_check -= 1
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);') # scrolls to the bottom of the page
        # page now completely loaded
        urls_list = collect_links(XPATH_element)
        
    elif load == "load_more":
        # collects website (1 page) with load_more button
        # presses the 'load more' button 
        press_button(XPATH_passed)
        # collects all the links after a page has loaded
        urls_list = collect_links(XPATH_element)
        
    elif load == "load_next":
        # collects links where there is a next page (loads a new page)
        urls_list = next_page(XPATH_element)
        
    elif load == "all_page":   
        urls_list = collect_links(XPATH_element)
    else:
        # catches any undefined or wrongly defined load variable
        urls_list = collect_links(XPATH_element)
        
    return urls_list

def collect_links (XPATH_element):
    """Collect links based on the given xpath element"""
    urls_list = []
    
    elements = driver.find_elements(By.XPATH,XPATH_element)
    
    links = (elems.get_attribute("href") for elems in elements)
    if links == None:
        links = (elems.get_attribute("data-href") for elems in elements)    
    for link in links:
        urls_list.append(link)
        
    return urls_list
    
    
def next_page(XPATH_element):
    """Presses next page button in pagination and downloads links till last page is reached"""
    all_links = []
    try:

        WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,XPATH_passed)))

        # time.sleep(10)
        next_button = driver.find_element(By.XPATH, XPATH_passed)
        while next_button.is_displayed():
            urls_list = collect_links(XPATH_element)            
            all_links.append(urls_list)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)
            next_button = driver.find_element(By.XPATH, XPATH_passed)
            try:
                if site_name == "SECUREWORKS":
                    # the string_to_compare is in the value attribute, not text
                    string_to_compare=driver.find_element(By.XPATH,XPATH_break).get_attribute("value")
                    if string_to_compare == string_blocker:
                        break
                else:
                    # if last assign button is found, loop would break
                    string_to_compare=driver.find_element(By.XPATH,XPATH_break)
                    if int(string_to_compare.text) == int(float(string_blocker)):
                        break  
            except Exception as e:
                # print(e)
                pass
            

    except Exception as e:
        # collects the links in the last page
        urls_list = collect_links(XPATH_element)
        all_links.append(urls_list)
        print(e)

    
    # collects the lists of lists of links
    all_links = itertools.chain(all_links)
    all_links = list(all_links)
    # merge all links into one link
    all_links = [link for links in all_links for link in links]
    # collect the unique sets of links to return
    all_links = set(all_links)
    
    return all_links
    
def merge_files(name,file_list):
    """Merge multiple txt files to 1 txt file"""
    # create the file
    with open(f"{name}_spyder.txt","w", encoding="utf-8") as file:
        # open each file in file_list
        for files in file_list:
            with open(files) as file_to_save:
                for line in file_to_save:
                    file.write(line)
                    
def delete_files(file_list):
    for file in file_list:
        # deletes files in file_list because it has now been saved to a concatenated file above
        os.remove(file)

    
def main(df):
    """
        Main function to collect spyder links from specific websites (see df)
        File format via csv. See columns below for value:
            df["site_name"] : string format (upper case) to assign file name when saved externally, i.e. "ELEMENDAR"
            df["website"] : string value of the website to direct the driver, i.e. "https://elemendar.com/blog/"
            df["load"] : string to assign which function to use for scraping purposes, see function get_spyder_links() for usage
            df["XPATH_passed"] : XPATH string of pagination or 'load more' button
            df["string_blocker"] : string used in next_page() to compare whether current page is the last page
            df["XPATH_break"] : XPATH string to check if current pagination number == string_blocker
            df["time_sleep"] : int (in seconds) to wait for the page to load
            df["XPATH_element"]: XPATH of spyder link 
    
    """
    
    # global values to assign over passing variables 
    global load 
    global website 
    global site_name
    global time_sleep 
    global XPATH_passed 
    global driver # passed through globally to prevent messy code given it is similar throughout the code
    global string_blocker
    global XPATH_break 
    
    # loop throught the df
    for i in df.index:
        df = df.astype(str)
        # assign variables before calling any other function because these functions reference these variables
        site_name = df.at[i,"site_name"]
        website = df.at[i,"website"]
        load = df.at[i,"load"]
        XPATH_passed = df.at[i,"XPATH_passed"]
        XPATH_break = df.at[i,"XPATH_break"]
        string_blocker = str(df.at[i,"string_blocker"])
        time_sleep = df.at[i,"time_sleep"]
        # initiate browser window
        driver = webdriver.Chrome()
        # unblocker to override window blockers or possible robots.txt issues
        web_unblocker(website)
        # collect the site
        driver.get(website)
        
        # collect each spyder links
        urls_list = get_spyder_links(df.at[i,"XPATH_element"])
        
        # save collected links (.txt) to a specific directory
        save_txt_file(site_name,urls_list)
        # closes the browser window to prevent having too many browser open
        # driver.close()
        

def save_txt_file(name,urls_list):
    """Save links to a text file"""
    try:
        # open old file
        with open(f"{name}_spyder.txt","r", encoding="utf-8") as file:
            lines = [line for line in file] # old file   
        # new file
        for x in urls_list:
            lines.append(x+"\n")
        
        # get the unique values in the url list string
        lines = set(lines)
            
        with open(f"{name}_spyder.txt", "w", encoding="utf-8") as output:
            for line in lines:
                output.write(str(line))
    except Exception as e:
        # for first download, create a new file with all collected spyder
        file = open(f'{name}_spyder.txt', 'w', encoding="utf-8")
        for x in urls_list:
            """ urls_list passed through to be saved. """
            file.write(x+"\n")
        file.close()