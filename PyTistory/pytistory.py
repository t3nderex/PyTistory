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
        """블로그 정보 얻어오기

        Returns:
            dict: {'url' : url, 'params' : params}
        """
        url = 'https://www.tistory.com/apis/blog/info'
        params ={'access_token':self.__access_token,
                'output':self.__output_type}
        return {'url':url, 'params':params}


    @call_api('GET', 'text')
    def get_post_list(self, page_num):
        """게시글 목록 얻어오기
        Args:
            access_token (str): Tistory Access Token_
            output_type (str): 출력 타입(json or json or xml)
            blog_name (str): 게시글을 얻어올 블로그 이름
            page_num (str): 게시글을 얻어올 페이지

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
        """게시글 읽기

        Args:
            post_id (str): 게시글의 id

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
        """게시글 작성

        Args:
            title (str): 게시글 제목
            content (str): 게시글 내용
            visibility (int, optional): visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행). Defaults to 0.
            category_id (int, optional): 카테고리 아이디 (기본값: 0). Defaults to 0.
            published (str, optional): 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간). Defaults to None.
            slogan (str, optional): 문자 주소. Defaults to None.
            tag (str, optional): 태그 (',' 로 구분). Defaults to None.
            accept_comment (int, optional): 댓글 허용 (0, 1 - 기본값). Defaults to 1.
            password (str, optional): 보호글 비밀번호. Defaults to None.

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
        """게시글 수정

        Args:
            post_id (str): 게시글 id
            title (str): 게시글 제목
            content (str): 게시글 내용
            visibility (int, optional): 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행). Defaults to 0.
            category_id (int, optional): 카테고리 아이디 (기본값: 0). Defaults to 0.
            published (str, optional): 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간). Defaults to None.
            slogan (str, optional): 문자 주소. Defaults to None.
            tag (str, optional): 태그 (',' 로 구분). Defaults to None.
            accept_comment (int, optional): 댓글 허용 (0, 1 - 기본값). Defaults to 1.
            password (str, optional): 보호글 비밀번호. Defaults to None.

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
        """카테고리 목록 얻기

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
        """파일 업로드

        Args:
            file_path (str): 업로드할 파일 경로

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
        """최근 댓글 목록 얻어오기

        Args:
            count (int): _description_
            page (int, optional): 가져올 페이지. Defaults to 1.

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
        """게시글 댓글 목록 얻어오기

        Args:
            post_id (int): 게시글 id

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
        """댓글 작성

        Args:
            post_id (str): 글 ID
            content (str): 댓글 내용
            secret (int, optional): 비밀 댓글 여부 (1: 비밀댓글, 0: 공개댓글 - 기본 값). Defaults to 0.
            parent_id (str, optional): 부모 댓글 ID (대댓글인 경우 사용). Defaults to None.

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
        """댓글 수정

        Args:
            post_id (str): 게시글 ID
            comment_id (str): 댓글 ID
            content (str): 댓글 내용
            parent_id (str, optional): 부모 댓글 ID (대댓글인 경우 사용). Defaults to None.
            secret (int, optional): 비밀 댓글 여부 (1: 비밀댓글, 0: 공개댓글 - 기본 값). Defaults to 0.

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
        """댓글 삭제

        Args:
            post_id (str): 게시글 ID
            comment_id (str): 댓글 ID

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