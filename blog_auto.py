import json
import time
import requests
import os
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from seleniumbase import Driver

from webdriver_manager.chrome import ChromeDriverManager

# MongoDB 연결
uri = "mongodb+srv://admin:admin12341234@cluster0.3e37l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['tistory']

# 'posts' 컬렉션을 지정
postsDB = db['posts']

print("Connected to MongoDB")

# 만약에 ChromeDriverManager를 install 해야 할 상황이 오면 아래의 옵션으로 인스톨 한번 해준 후 다시 주석처리 해주기
# options = ChromeOptions()
# options.add_argument(r"user-data-dir=C:\\selenium_data\\Chrome")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 역사 썰
history_story = ['category-item-1201184', 'https://chatgpt.com/g/g-GB6qPTSIt-yeogsa-sseol-blog-json']
science_story = ['category-item-1201410', 'https://chatgpt.com/g/g-G6PYOE1TE-gwahag-sseol-blog-json']
health_story = ['category-item-1204403', 'https://chatgpt.com/g/g-cEdBDA8JR-geongang-gwanryeon-sseol-json']

postings = [history_story, science_story, health_story]
posting = history_story

# driver = uc.Chrome(service=Service(ChromeDriverManager().install()), user_data_dir='C:\\selenium_data\\Chrome', port=54806, disable_logging=True, detach=True, excludeSwitches=["enable-logging"])
driver = Driver(uc=True, user_data_dir='C:\\selenium_data\\Chrome', port=54806)
driver.get("https://www.google.com")

def write_tistory_post(title, content, keywords):
    def get_recent_file_path():
        files_path = r".\\downloaded_files"
        # files_path = r"C:\Users\Jinyo3090\Downloads"

        file_name_and_time_lst = []
        # 해당 경로에 있는 파일들의 생성시간을 함께 리스트로 넣어줌. 
        for f_name in os.listdir(f"{files_path}"):
            written_time = os.path.getctime(f"{files_path}\\{f_name}")
            file_name_and_time_lst.append((f_name, written_time))
        # 생성시간 역순으로 정렬하고, 
        sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)
        # 가장 앞에 이는 놈을 넣어준다.
        recent_file = sorted_file_lst[0]
        recent_file_name = recent_file[0]

        return os.path.abspath(f"{files_path}\\{recent_file_name}")
    # tistory_driver = uc.Chrome(user_data_dir='C:\\selenium_data\\Chrome', port=54806)
    tistory_driver = driver
    # 셀레니움으로 티스토리 포스팅 url로 넘어가기
    tistory_driver.implicitly_wait(4)
    tistory_driver.get("https://dropdrop.tistory.com/manage/posts")
    tistory_driver.implicitly_wait(10)
    
    # 로그인 창으로 넘어갈 경우 로그인하기
    try :
        login_button = tistory_driver.find_element(By.CLASS_NAME, "btn_login")
        ActionChains(tistory_driver).click(login_button).perform()
        tistory_driver.implicitly_wait(10)

        id_input = tistory_driver.find_element(By.NAME, "loginId")
        pw_input = tistory_driver.find_element(By.NAME, "password")

        ActionChains(tistory_driver).send_keys_to_element(id_input, "solomoj94@naver.com").perform()
        tistory_driver.implicitly_wait(1)
        ActionChains(tistory_driver).send_keys_to_element(pw_input, "skfrosla131").perform()
        tistory_driver.implicitly_wait(1)

        login_button = tistory_driver.find_element(By.CLASS_NAME, "submit")
        ActionChains(tistory_driver).click(login_button).perform()
        tistory_driver.implicitly_wait(4)
    except NoSuchElementException as e :
        print("이미 로그인 되어 있습니다.")
        # 로그인 되어 있는 경우에는 계정 버튼을 눌러서 들어가기
        try :
            time.sleep(1)
            account_button = tistory_driver.find_element(By.CLASS_NAME, "wrap_profile")
            ActionChains(tistory_driver).click(account_button).perform()
            tistory_driver.implicitly_wait(4)
        except Exception as e:
            print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(3)
    # 글 쓰기 버튼 클릭하기
    # write_button = tistory_driver.find_element(By.CLASS_NAME, "link_write")
    # ActionChains(tistory_driver).click(write_button).perform()
    # 글쓰기버튼 안클릭해도 바로 다이렉트 URL이 있더라
    tistory_driver.get("https://dropdrop.tistory.com/manage/newpost/?type=post&returnURL=%2Fmanage%2Fposts%2F")
    tistory_driver.implicitly_wait(10)

    # 혹시나 임시저장글 어쩌고가 나올 때를 대비해서
    try :
        alert_present = WebDriverWait(tistory_driver, 5).until(EC.alert_is_present())
        if alert_present:
            tistory_alert = Alert(tistory_driver)
            tistory_alert.dismiss()
            tistory_driver.implicitly_wait(1)
    except TimeoutException as e :
        print("임시저장글 어쩌고가 나오지 않았습니다.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 글 카테고리 선택하기
    category_button = tistory_driver.find_element(By.ID, "category-btn")
    ActionChains(tistory_driver).click(category_button).perform()
    tistory_driver.implicitly_wait(10)
    # 역사시간 순삭 카테고리
    science_category_list_btn = tistory_driver.find_element(By.ID, posting[0])
    ActionChains(tistory_driver).click(science_category_list_btn).perform()
    tistory_driver.implicitly_wait(1)

    # 글 입력 형식 바꾸기
    category_button = tistory_driver.find_element(By.ID, "editor-mode-layer-btn-open")
    ActionChains(tistory_driver).click(category_button).perform()
    tistory_driver.implicitly_wait(10)
    # HTML 형식으로 바꾸기
    science_category_list_btn = tistory_driver.find_element(By.ID, 'editor-mode-html')
    ActionChains(tistory_driver).click(science_category_list_btn).perform()
    tistory_driver.implicitly_wait(1)
    # 경고창이 뜨면 확인 버튼 누르기
    alert_present = WebDriverWait(tistory_driver, 5).until(EC.alert_is_present())
    if alert_present:
        tistory_alert = Alert(tistory_driver)
        tistory_alert.accept()
        tistory_driver.implicitly_wait(1)

    #글 제목 입력하기
    title_input = tistory_driver.find_element(By.CLASS_NAME, "textarea_tit")
    ActionChains(tistory_driver).send_keys_to_element(title_input, title).perform()
    tistory_driver.implicitly_wait(1)

    # 사진 업로드 할 공간 만들어주기 (글 내용 입력 클릭시에 안눌리게)
    content_input = tistory_driver.find_element(By.CLASS_NAME, "mce-edit-area")
    ActionChains(tistory_driver).click(content_input).perform()
    ActionChains(tistory_driver).send_keys(Keys.ENTER).send_keys(Keys.ENTER).send_keys(Keys.ARROW_UP).send_keys(Keys.ARROW_UP).perform()
    tistory_driver.implicitly_wait(3)

    #사진 업로드하기
    attach_layer_button = tistory_driver.find_element(By.ID, "attach-layer-btn")
    ActionChains(tistory_driver).click(attach_layer_button).perform()
    tistory_driver.implicitly_wait(1)
    image_input = tistory_driver.find_element(By.ID, "attach-image")
    image_input.send_keys(get_recent_file_path())
    tistory_driver.implicitly_wait(1)
    time.sleep(3)
    
    #글 내용 입력하기 (HTML)
    #클립보드에 content 복사
    pyperclip.copy(content)
    content_input = tistory_driver.find_element(By.CLASS_NAME, "mce-edit-area")
    ActionChains(tistory_driver).click(content_input).perform()
    ActionChains(tistory_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    tistory_driver.implicitly_wait(10)

    #태그 내용 입력하기
    tag_input = tistory_driver.find_element(By.ID, "tagText")
    if (type(keywords) == type([])) :
        keywords = ", ".join(map(str, keywords))
    ActionChains(driver).send_keys_to_element(tag_input, keywords).perform()
    tistory_driver.implicitly_wait(1)
    

    
    # 글 입력 형식 바꾸기
    category_button = tistory_driver.find_element(By.XPATH, "//*[@id='html-editor-container']/div[1]/div/div/div/div/div/div[5]/div/div/button")
    ActionChains(tistory_driver).click(category_button).perform()
    tistory_driver.implicitly_wait(10)
    time.sleep(1)

    # 기본 형식으로 바꾸기 (대표 이미지 자동 설정을 위해)
    science_category_list_btn = tistory_driver.find_element(By.ID, 'editor-mode-kakao-tistory')
    ActionChains(tistory_driver).click(science_category_list_btn).perform()
    tistory_driver.implicitly_wait(1)
    time.sleep(1)
    # 경고창이 뜨면 확인 버튼 누르기
    alert_present = WebDriverWait(tistory_driver, 5).until(EC.alert_is_present())
    if alert_present:
        tistory_alert = Alert(tistory_driver)
        tistory_alert.accept()
        tistory_driver.implicitly_wait(1)
        
    time.sleep(3)

    #완료 버튼 누르기
    publish_layer_button = tistory_driver.find_element(By.ID, "publish-layer-btn")
    ActionChains(tistory_driver).click(publish_layer_button).perform()
    tistory_driver.implicitly_wait(1)

    time.sleep(3)

    # 공개 버튼 누르기 (티스토리 기본 설정에서 변경 가능)
    # public_button = tistory_driver.find_element(By.XPATH, "//*[@id='editor-root']/div[5]/div/div/div/form/fieldset/div[2]/div/dl[1]/dd/div[1]")
    # ActionChains(tistory_driver).click(public_button).perform()
    # tistory_driver.implicitly_wait(1)
    # public_button = tistory_driver.find_element(By.XPATH, "//*[@id='editor-root']/div[5]/div/div/div/form/fieldset/div[2]/div/dl[1]/dd/div[1]")
    # ActionChains(tistory_driver).click(public_button).perform()
    # tistory_driver.implicitly_wait(1)

    # 대표이미지 설정하기 안됨..
    # image_input = tistory_driver.find_element(By.CLASS_NAME, "inp_g")
    # image_input.send_keys(get_recent_file_path())
    # tistory_driver.implicitly_wait(2)

    # #발행 버튼 누르기
    publish_button = tistory_driver.find_element(By.ID, "publish-btn")
    ActionChains(tistory_driver).click(publish_button).perform()
    tistory_driver.implicitly_wait(1)

    time.sleep(2)

    # DB에 저장하기
    postsDB.insert_one({"title":title, "category": posting[0], "created_at": time.time()})
    
    

def get_post_from_gpt():
    
    def replace_markdown_bold_with_html(text):
        # 정규식 패턴: **로 감싸진 문자열 찾기
        pattern = r"\*\*(.*?)\*\*"
        
        # 매치된 문자열을 <b> </b>로 감싸는 함수
        def replace_with_bold(match):
            return f"<b>{match.group(1)}</b>"
        
        # 전체 텍스트에서 패턴에 매치되는 모든 부분을 찾아 replace_with_bold 함수로 변환
        return re.sub(pattern, replace_with_bold, text)

        
    chatgpt_driver = driver
    chatgpt_driver.implicitly_wait(4)
    chatgpt_driver.get(posting[1])
    chatgpt_driver.implicitly_wait(10)
    time.sleep(5)

    results = postsDB.find({"category": posting[0]})
    names = [result["title"] for result in results]

    gpt_chat_input = chatgpt_driver.find_element(By.ID, "prompt-textarea")
    # ActionChains(chatgpt_driver).send_keys_to_element(gpt_chat_input, "Create new content while avoiding following listings as much as possible. [" + ", ".join(map(str,names)) + "]").perform()
    pyperclip.copy("Create new content while avoiding following listings as much as possible. [" + ", ".join(map(str,names)) + "]")
    ActionChains(chatgpt_driver).click(gpt_chat_input).perform()
    ActionChains(chatgpt_driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    chatgpt_driver.implicitly_wait(10)

    gpt_chat_input.send_keys(Keys.ENTER)
    time.sleep(1)
    WebDriverWait(chatgpt_driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='프롬프트 보내기']")))
    # gpt_chat_output_element = chatgpt_driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]/div/div/div/p")
    # gpt_chat_output_json_text = gpt_chat_output_element.text
    # gpt_chat_output_dict = json.loads(gpt_chat_output_json_text)


    gpt_chat_output_element = driver.find_element(By.TAG_NAME, 'code')
    # <code> 태그 내부의 모든 <span> 태그들 찾기
    span_elements = gpt_chat_output_element.find_elements(By.TAG_NAME, 'span')
    # <span> 태그들의 텍스트를 하나의 문자열로 조합
    gpt_chat_output_json_text = ''.join([replace_markdown_bold_with_html(span.text) for span in span_elements])
    gpt_chat_output_dict = json.loads(gpt_chat_output_json_text)

    gpt_chat_input = chatgpt_driver.find_element(By.ID, "prompt-textarea")
    ActionChains(chatgpt_driver).send_keys_to_element(gpt_chat_input, "위 내용의 커버사진으로 쓸만한 이미지 정책에 걸리지 않게 하나 만들어 줘").perform()
    gpt_chat_input.send_keys(Keys.ENTER)
    time.sleep(25)
    images = chatgpt_driver.find_elements(By.TAG_NAME, "img")
    last_image = images[-1]
    ActionChains(chatgpt_driver).click(last_image).perform()

    chatgpt_driver.implicitly_wait(5)
    gpt_img_download_element = chatgpt_driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/span[2]/button")
    ActionChains(chatgpt_driver).click(gpt_img_download_element).perform()

    time.sleep(5)

    return gpt_chat_output_dict

def main_process():
    gpt_chat_output_dict = get_post_from_gpt()
    print(gpt_chat_output_dict)
    write_tistory_post(gpt_chat_output_dict['title'], gpt_chat_output_dict['content'], gpt_chat_output_dict['keywords'])

for _posting in postings:
    posting = _posting
    for i in range(5):
        try:
            main_process()
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

def restart():
    return os.system("shutdown /r /t 1")

def shutdown():
    return os.system("shutdown /s /t 1")

restart()