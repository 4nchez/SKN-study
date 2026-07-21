-- Django 프로젝트가 사용할 DB 생성
CREATE DATABASE IF NOT EXISTS django_member_board
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Django 전용 사용자계정 만듦
CREATE USER IF NOT EXISTS 'django_user'@'localhost' IDENTIFIED BY 'django1234!';
CREATE USER IF NOT EXISTS 'django_user'@'127.0.0.1' IDENTIFIED BY 'django1234!';

-- 권한을 부여함
GRANT ALL PRIVILEGES ON django_member_board.* TO 'django_user'@'localhost' ;
GRANT ALL PRIVILEGES ON django_member_board.* TO 'django_user'@'127.0.0.1' ;

-- 적용
FLUSH PRIVILEGES;