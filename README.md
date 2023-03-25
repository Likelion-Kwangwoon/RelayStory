# team2-BE


# 🔥 Git 규칙 

## ① 브랜치(branch) 이름 
- 기능 개발  
  git branch **feature**/기능요약  
  `ex) git branch feature/login`   
  `ex) git branch feature/ad_memberAll` 
 
- 버그/오류 수정
  git branch **hotfix**/기능요약  
  `ex) git branch hotfix/mypage_myArticle`   
  `ex) git branch hotfix/u_faqList`  

## ② 커밋(commit)
- 하나의 커밋에는 한 단위의 작업 넣기  
  ◽ 한 작업을 여러 버전에 걸쳐 커밋 ❌  
  ◽ 여러 작업을 한 버전에 커밋 ❌   
    → 여러 개 같이 커밋하면, 나중에 그것들 중 하나만 취소해야 될 일 발생할 수 있으니까⋯⋯!   
  ◽ 커밋 최소 단위로 하기, 하나의 의도만 가지고 !  
    → 버그 수정 + 새 기능 추가 를 같이 커밋 ❌ 

## ③ 커밋 메시지
🌟 어떤 작업이 이뤄졌는지 알아볼 수 있게 작성 !  
→ 이름 아무렇게나 작성해놓으면, 나중에 본인도 거기서 무슨 작업했는지 기억 못함⋯!   
`ex) git commit -m 'haha'` 

``` 
type : subject

body 

footer
``` 
구조로 작성

### type
- 명령문 형태로, 제목 첫 글자는 대문자로 (타입 말고 제목을!)
- 아래에서 필요한 타입 사용 
  
|타입|내용|
|------|------|
|feat|새로운 기능 추가|
|fix| 버그/오류 수정|
|docs| 문서 수정 |
|style| 코드 포맷 변경, 세미콜론 누락, 코드 변경 없음|
|design| 사용자 UI 디자인 변경 (CSS 등)|
|move| 코드나 파일의 이동|
|rename| 이름 변경|
|remove| 삭제|  
### subject
완전한 서술형 문장이 아니라, 간결하고 요점적인 서술로 작성한다.


### body
본문은 한 줄 당 72자 내로 작성한다.
본문 내용은 양에 구애받지 않고 최대한 상세히 작성한다.
본문 내용은 어떻게 변경했는지 보다 무엇을 변경했는지 또는 왜 변경했는지를 설명한다.

### footer
footer는 "유형: #이슈 번호" 형식으로 사용한다
- Fixes: 이슈 수정중 (아직 해결되지 않은 경우)
- Resolves: 이슈를 해결했을 때 사용
- Ref: 참고할 이슈가 있을 때 사용
- Related to: 해당 커밋에 관련된 이슈번호 (아직 해결되지 않은 경우)


### 커밋 메세지 예시 


``` 
feat: "회원 가입 기능 구현"

SMS, 이메일 중복확인 API 개발

Resolves: #123

Ref: #456

Related to: #48, #45
```  

커밋 메세지의 줄을 띄우는 법은 그냥 따옴표를 닫지 않고 엔터를 눌러 줄 띄우고 쓰면 된다.
