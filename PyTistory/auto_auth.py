import re
from xmlrpc.client import ResponseError



import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager



def set_driver(load_wait_time = 10):
    """selenium 드라이버 세팅

    Returns:
        <class 'selenium.webdriver.chrome.webdriver.WebDriver'>: 셀레니움 드라이버
    """
    driver_opts = webdriver.ChromeOptions()
    driver_opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=driver_opts
                            )
    driver.implicitly_wait(load_wait_time)

    return driver


def authorize_api(id, pw, client_id, redirect_uri, state_param = None):
    """ 초기 인증 요청
    Args:
        client_id (str): 클라이언트 정보의 Client ID 입니다.
        redirect_uri (str): 사용자가 인증 후에 리디렉션할 URI입니다. 클라이언트 정보의 Callback 경로로 등록하여야 하며 등록되지 않은 URI를 사용하는 경우 인증이 거부됩니다.
        response_type: 항상 code를 사용합니다.
        mstate_param (str): 사이트간 요청 위조 공격을 보호하기 위한 임의의 고유한 문자열이며 리디렉션시 해당 값이 전달됩니다. (필수아님)
        
    Returns:
        str: auth_code
    """
    if state_param is None:
        import random, string
        length_of_string = 64
        state_param =''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    
    url = 'https://www.tistory.com/oauth/authorize'
    params = f'''?client_id={client_id}
                &redirect_uri={redirect_uri}
                &response_type=code
                &state={state_param}'''.replace(' ', '')

    driver = set_driver()
    driver.get(url+params)
    driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[1]/span[2]').click()
    driver.find_element(By.XPATH, '//*[@id="id_email_2"]').send_keys(id)
    driver.find_element(By.XPATH, '//*[@id="id_password_3"]').send_keys(pw)
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    driver.find_element(By.XPATH, '//*[@id="contents"]/div[4]/button[1]').click()
    
    try:
        if 'error' in driver.current_url:
            raise ResponseError
    except ResponseError as e:
        pass
        
    code = re.search('\w{72}',driver.current_url).group()
    return code


def get_access_token(id, pw, client_id, client_secret, redirect_uri, state_param = None):
    if not state_param:
        code = authorize_api(id, pw, client_id, redirect_uri)
    elif state_param: 
        code = authorize_api(id, pw, client_id, redirect_uri, state_param)
    
    url = 'https://www.tistory.com/oauth/access_token?'
    params = {'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':redirect_uri,
            'code':code,                    #1198cf4305a03ac2c154932f7306fe4114e34de1164d747a07d3e5c98ac5e31c3b083934
            'grant_type':'authorization_code'}

    response = requests.get(url, params = params)
    
    try:
        if 'error' in  response.text:
            raise ResponseError
    except ResponseError as e:
        print("")
    
    return response.text.split('=')[1]
    
