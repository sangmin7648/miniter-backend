# miniter-backend
backend api application for miniter

# API 

| 엔드포인트                | 메서드  | 응답형식   | 설명                          |
|-------------------------|--------|---------|-------------------------------|
| <code>/ping</code>     | GET    |  text    | 정상 작동시 "pong"을 반환합니다     |
| <code>/sign-up</code>  | POST   |  INT     | name, email, profile, password를 받아 사용자를 저장하고 사용자 id 숫자를 반환합니다|
| <code>/login</code>    | POST   |  JSON    | email, password를 받아 로그인을 하고 엑세스 토큰을 반환합니다     |
| <code>/tweet</code>    | POST   | 200      | tweet을 받아 저장하고 완료 시 status code 200을 반환합니다     |
| <code>/follow</code>   | POST   | 200      | 사용자 id 숫자로된 follow를 받아 팔로우하고 status code 200을 반환합니다  |
| <code>/unfollow</code> | POST   | 200      | 사용자 id 숫자로된 unfollow를 받아 언팔로우하고 status code 200을 반환합니다  |
| <code>/timeline</code> | GET    | JSON     | 사용자나 사용자가 팔로우한 사용자의 트윗을 JSON으로 반환합니다            |
| <code>/timeline/<user_id></code> | GET    | JSON     | user_id 사용자나 사용자가 팔로우한 사용자의 트윗을 JSON으로 반환합니다 | 
