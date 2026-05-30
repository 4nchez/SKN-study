-- MySQL_Day01.sql (SQL Script File)
-- 작성된 쿼리문 저장한 파일임
/*
여러 줄 주석(comment)
Changing Font Size : Edit - Prefernces - Fonts & Colors
Query 메뉴 - 메뉴와 단축키 확인함 :
	- 쿼리문 하나만 실행 : 문장에 커서 두고 ctrl + enter (툴 버튼에 I자 있는 번개 아이콘)
    - 선택한(범위 지정한) 쿼리 실행 : ctrl + shift + enter (번개 아이콘)
    - 그냥 번개 아이콘 클릭 : 스크립트 전체 실행
*/

/*
WorkBench 처음 실행 시 root (관리자계정, MySQL 설치 시 기본 제공됨) 계정 접속 방법
	- 방법 1: 아래쪽의 보여지는 Local Instance MySQL80 을 더블 클릭
    - 방법 2: 상단의 메뉴바의 Database 메뉴 - Connect to database... 선택
*/

-- root 계정에서 할 일 : 사용자 계정 생성, 권한 추가 (2가지 방법)
-- 방법 1: Server 메뉴 - Users and Privileges 메뉴 선택
-- 수업용 계정 만들기 : 
-- Login name : studnet
-- Host : %
-- Password : Student80*
-- Schema Privileges 탭 클릭 > Add Entry > 추가하고 싶은 권한 선택 > Apply

-- 방법 2 : sql 구분 직접 작성
-- CREATE USER '계정명' IDENTIFIED BY '암호'; -- 공유서버에서 적용
-- CREATE USER '계정명'@'localhost' IDENTIFIED BY '암호';
-- 과제용 계정 만들기 :
CREATE USER 'homework' IDENTIFIED BY 'Homework80*';
-- 권한 부여 : GRANT 권한종류 | 롤이름  ON 데이터베이스 이름 TO 사용자계정;
SHOW DATABASES;
-- GRANT 권한종류, 권한종류, 권한종류 ON mysql.* TO 'homework';
GRANT ALL PRIVILEGES ON homeworkdb.* TO 'homework'; -- 모든 권한 부여
-- 아래에서 만든 데이터베이스 homeworkdb 에 대해 모든 권한을 부여함

-- 데이터베이스 생성 명령 (root 계정)
-- CREATE DATABASE '데이터베이스 이름';
CREATE DATABASE mydb;
CREATE DATABASE homeworkdb;

-- ROOT 계정에서 만들어진 데이터베이스 확인할 수 있음
SHOW DATABASES;

-- 데이터베이스 제거
-- DROP '데이터베이스이름';

-- RDBMS 종작 구조
/*
Client(db 서버 사용자) --> sql 쿼리문 작성 --> 실행 --> RDBMS : SQL 해석기 --> RDBMS : 자료 관리기 --|
--> 데이터 저장소(하드디스크) --> SQL 처리한 결과 --> RDBMS : SQL 응답 --> 사용자 결과 보기
*/

-- MySQL 설치 후 root 계정 접속 --> 데이터베이스 구조 Set-Up 절차
/*
사용자 계정과 암호 생성 --> 사용할 데이터베이스 생성 --> 생성한 데이터베이스와 계정으로 권한 부여
--> 생성한 데이터베이스에 테이블 만들기 --> 테이블에 데이터 저장
*/

-- SQL 문 작성 규칙
/*
1. 명령문 끝에는 반드시 새미콜론(;) 붙일 것
2. 명령문에 대소문자 구분 안 함
*/
