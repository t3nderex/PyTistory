# PyTistory

**[Tistory Open API](https://tistory.github.io/document-tistory-apis/) Python Wrapper**

파이썬을 이용해서 Tistory Open API를 사용할 수 있습니다.


## 사용 방법

함수 인자에 대한 설명은 [Tistory Open API](https://tistory.github.io/document-tistory-apis/) 참고
```python
# 인스턴스 초기화
tistory = PyTistory(Access Token)

# 게시글 목록 가져오기
post_list = tistory.get_post_list(page_num =)

# 게시글 읽기
content = tistory.read_post(post_id =)

# 게시글 작성
tistory.write_post(title = ,content = ,visibility = ,category_id = ,published = ,slogan = ,tag = ,accept_comment = ,password = )

# 게시글 수정
#tistory.modify_post(post_id = , title = ,content = ,visibility = ,category_id = ,published = ,slogan = ,tag = ,accept_comment = ,password = )

# 카테고리 목록 가져오기
category = tistory.get_category()

# 파일 업로드
tistory.post_attach(file_path ='')

# 댓글 삭제
# tistory.comment_delete(post_id = ,comment_id = )

# 댓글 수정
tistory.comment_modify(post_id = comment_id = ,content = ,secret = ,parent_id = )

# 댓글 작성
tistory.comment_write(post_id = ,content = ,secret = ,parent_id = )

# 댓글 목록 가져오기
tistory.get_comment_list(post_id = )

# 최신 댓글 가져오기
tistory.get_comment_newest(count = ,page = )
```


## 📢 TOD 
 - 예외처리
 - 패키지 구성(PyPi 업로드)
