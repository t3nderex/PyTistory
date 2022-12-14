import json



import requests
from requests.exceptions import HTTPError



def call_api(req_method,return_type = 'text'):
    if req_method =='GET':
        requests_api = requests.get
    elif req_method =='POST':
        requests_api = requests.post
    def wrapper(api_func):
        def request_(*args, **kwargs):
            data = api_func(*args,**kwargs)
            url = data['url']
            params = data['params']
            try:
                if 'files' in data:
                    files = data['files']
                    resp = requests_api(url, params = params, files = files)
                else:
                    resp = requests_api(url, params = params)   
                if resp.status_code == 200:
                    if return_type =='text':
                        return json.loads(resp.text)
                    elif return_type == 'content':
                        return json.loads(resp.content)
                    else:
                        return resp
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')
        return request_
    return wrapper



class PyTistory():
    def __init__(self, access_token) -> None:
        try:
            self.__access_token = access_token
            self.__output_type = 'json'
            self.blog_info = self.__get_blog_info()  
            self.__blog_name = self.blog_info['tistory']['item']['blogs'][0]['name']
        except BaseException as e:
            print(e)        
    

    @property
    def access_token(self):
        return self.__access_token


    @access_token.setter
    def access_token(self, access_token):
        self.__access_token = access_token


    @property
    def output_type(self):
        return self.__output_type


    @output_type.setter
    def output_type(self, output_type):
        self.__output_type = output_type


    @call_api('GET','text')
    def __get_blog_info(self):
        """????????? ?????? ????????????

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/blog/info'
        params ={'access_token':self.__access_token,
                'output':self.__output_type}
        return {'url':url, 'params':params}


    @call_api('GET', 'text')
    def get_post_list(self, page_num):
        """????????? ?????? ????????????
        Args:
            access_token (str): Tistory Access Token_
            output_type (str): ?????? ??????(json or json or xml)
            blog_name (str): ???????????? ????????? ????????? ??????
            page_num (str): ???????????? ????????? ?????????

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = f'https://www.tistory.com/apis/post/list'
        params = {'access_token':self.access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'page':page_num
                }
        return {'url':url, 'params':params}


    @call_api('GET', 'text')
    def read_post(self, post_id):
        """????????? ??????

        Args:
            post_id (str): ???????????? id

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/post/read'
        params ={'access_token':self.__access_token,
                'blogName':self.__blog_name,
                'postId':post_id,
                'output':self.__output_type}
        return {'url':url, 'params':params}


    @call_api('POST', 'text')
    def write_post(self, title, content, visibility = 0,
                    category_id = 0, published = None, slogan = None,
                    tag=None, accept_comment = 1, password = None):
        """????????? ??????

        Args:
            title (str): ????????? ??????
            content (str): ????????? ??????
            visibility (int, optional): visibility: ???????????? (0: ????????? - ?????????, 1: ??????, 3: ??????). Defaults to 0.
            category_id (int, optional): ???????????? ????????? (?????????: 0). Defaults to 0.
            published (str, optional): ???????????? (TIMESTAMP ?????? ????????? ????????? ?????? ?????? ??????. ?????????: ????????????). Defaults to None.
            slogan (str, optional): ?????? ??????. Defaults to None.
            tag (str, optional): ?????? (',' ??? ??????). Defaults to None.
            accept_comment (int, optional): ?????? ?????? (0, 1 - ?????????). Defaults to 1.
            password (str, optional): ????????? ????????????. Defaults to None.

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/post/write'
        params = {'access_token':self.__access_token,
                    'output':self.__output_type,
                    'blogName':self.__blog_name,
                    'title':title,
                    'content':content,
                    'visibility':visibility,
                    'category':category_id,
                    'published':published,
                    'slogan':slogan,
                    'tag':tag,
                    'acceptComment':accept_comment,
                    'password':password}
        return {'url':url, 'params':params}


    @call_api('POST', 'text')
    def modify_post(self, post_id, title, content, visibility = 0,
                    category_id = 0, published = None, slogan =  None,
                    tag = None, accept_comment = 1, password = None):
        """????????? ??????

        Args:
            post_id (str): ????????? id
            title (str): ????????? ??????
            content (str): ????????? ??????
            visibility (int, optional): ???????????? (0: ????????? - ?????????, 1: ??????, 3: ??????). Defaults to 0.
            category_id (int, optional): ???????????? ????????? (?????????: 0). Defaults to 0.
            published (str, optional): ???????????? (TIMESTAMP ?????? ????????? ????????? ?????? ?????? ??????. ?????????: ????????????). Defaults to None.
            slogan (str, optional): ?????? ??????. Defaults to None.
            tag (str, optional): ?????? (',' ??? ??????). Defaults to None.
            accept_comment (int, optional): ?????? ?????? (0, 1 - ?????????). Defaults to 1.
            password (str, optional): ????????? ????????????. Defaults to None.

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/post/modify'
        params = {'access_token':self.__access_token,
                    'output':self.__output_type,
                    'blogName':self.__blog_name,
                    'postId':post_id,
                    'title':title,
                    'content':content,
                    'visibility':visibility,
                    'category':category_id,
                    'published':published,
                    'slogan':slogan,
                    'tag':tag,
                    'acceptComment':accept_comment,
                    'password':password}
        return {'url':url, 'params':params}


    @call_api('GET', 'text')
    def get_category(self):
        """???????????? ?????? ??????

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/category/list'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name
                }
        return {'url':url, 'params':params}
    

    @call_api('POST', 'text')
    def post_attach(self,file_path):
        """?????? ?????????

        Args:
            file_path (str): ???????????? ?????? ??????

        Returns:
            dict: {'url' : url, 'params' : params, 'uploadedfile' : file_path}
        """
        url = 'https://www.tistory.com/apis/post/attach?'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                }
        return {'url':url, 'params':params, 'files' : {'uploadedfile':open(file_path, 'rb')}}


    @call_api('GET', 'text')
    def get_comment_newest(self, count, page = 1):
        """?????? ?????? ?????? ????????????

        Args:
            count (int): _description_
            page (int, optional): ????????? ?????????. Defaults to 1.

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/comment/newest'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'page':page,
                'count':count}
        return {'url':url, 'params':params}    


    @call_api('GET', 'text')
    def get_comment_list(self, post_id):
        """????????? ?????? ?????? ????????????

        Args:
            post_id (int): ????????? id

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/comment/list'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'postId':post_id}
        return {'url':url, 'params':params}
    
    
    @call_api('POST', 'text')
    def comment_write(self, post_id, content, secret = 0, parent_id = None):
        """?????? ??????

        Args:
            post_id (str): ??? ID
            content (str): ?????? ??????
            secret (int, optional): ?????? ?????? ?????? (1: ????????????, 0: ???????????? - ?????? ???). Defaults to 0.
            parent_id (str, optional): ?????? ?????? ID (???????????? ?????? ??????). Defaults to None.

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/comment/write'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'postId':post_id,
                'parentId':parent_id,
                'content':content,
                'secret':secret}
        return {'url':url, 'params':params}


    @call_api('POST', 'text')
    def comment_modify(self, post_id, comment_id, content, secret = 0, parent_id = None):
        """?????? ??????

        Args:
            post_id (str): ????????? ID
            comment_id (str): ?????? ID
            content (str): ?????? ??????
            parent_id (str, optional): ?????? ?????? ID (???????????? ?????? ??????). Defaults to None.
            secret (int, optional): ?????? ?????? ?????? (1: ????????????, 0: ???????????? - ?????? ???). Defaults to 0.

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/comment/modify'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'postId':post_id,
                'parentId':parent_id,
                'commentId':comment_id,
                'content':content,
                'secret':secret}
        return {'url':url, 'params':params}


    @call_api('POST', 'text')
    def comment_delete(self, post_id, comment_id):
        """?????? ??????

        Args:
            post_id (str): ????????? ID
            comment_id (str): ?????? ID

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/comment/delete'
        params = {'access_token':self.__access_token,
                'output':self.__output_type,
                'blogName':self.__blog_name,
                'postId':post_id,
                'commentId':comment_id}
        return {'url':url, 'params':params}
