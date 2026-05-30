-- student/Student80*
select user(); -- 접속 계정 확인
-- 사용자계정 처음 접속시, 사용할 db 지정 확인할 것
use mydb;

-- DDL (Data Definition Language : 데이터 정의어)
-- 명령어 : CREATE, ALTER, DROP
-- 데이터베이스 객체 생성, 변경, 제거하는 구문
-- 데이터베이스 객체 : 테이블(table), 뷰(view), 인덱스(index), 함수(function), 프로시저(procedure), 트리거(trigger)

-- 테이블 만들기
/*
CREATE TABLE 테이블명 (
	컬럼명 자료형 comment '컬럼설명',
    컬럼명 자료형 DEFAULT 기록할 기본값,
    컬럼명 자료형 제약조건,
    컬럼명 자료형 DEFAULT 기본값 제약조건,
    [CONSTARAINT 제약조건이름] 제약조건종류 (적용할 컬럼명)
);
-- 테이블은 반드시 최소 1개의 컬럼을 가져야 함
*/

-- CREATE TABLE EXAM();	-- ERROR : 컬럼 없는 빈 테이블 생성 못함

CREATE TABLE MANAGE (
	MARKET VARCHAR(20), -- 영업소명
    BUY INT, -- 입고량
    SELL INT, -- 판매량
    STOCK INT, -- 재고량
	IN_DAY DATE -- 날짜
);

-- 테이블 생성에 사용되는 컬럼 자료형
-- 문자형
/*
- 문자열과 문자하나 구분 없음
- 문자값은 반드시 '문자값' (작은 따옴표로 묶을 것) 표시함
- 종류 : CHAR(), VARCHAR(), TINYTEXT, TEXT 등
	CHAR(바이트수) : 고정 길이 문자열
				컬럼에 기록되는 글자수 고정
                예) CHAR(2) : 컬럼에 글자는 반드시 2바이트임
                기록시 'AB', 'ab'
                만약, 'a' 기록시 'a공백문자' 무조건 2바이트로 기록되게 함
                'abc' 기록은 에러임
	VARCHAR(최대 기록 바이트 수) : 가변길이 문자열
				컬럼에 0개 <= 글자 <= 최대 기록 바이트 수 로 글자 기록함
				입력한 문자값만 기록됨 (공백으로 채우지 않음)
	TINYTEXT : 최대 255 바이트 문자 기록할 수 있음
    TEXT : 최대 65,535 바이트 문자 기록할 수 있음 (본문 내용 저장시)
*/

-- 숫자형
/*
- TINYINT(최대자릿수) : -128 ~ 127 사이의 정수
				UNSIGNED (음수를 앙수로 전환) 사용 : 0 ~ 255 정수
- INT(최대자릿수) : -2147483648 ~ 2147483647 사이의 정수
				UNSIGNED 사용 : 0 ~ 429477295 사이의 정수
- FLOAT : 부동소수형 실수
- DECIMAL(전체자릿수, 소숫점아래 자릿수) : 부동소수형 실수나 정수
*/

-- 날짜형
/*
- DATE : YYYY-MM-DD 날짜만 기록
				현재 날짜 입력 함수 : NOW()
- DATETIME : YYYY-MM-DD HH:MM:SS 날짜와 시간 기록
				현재 시간 입력 : NOW()
- TIME : HH:MM:SS 시간만 기록
*/

-- 기타 자료형 : ENUM(값, 값, ....) 정해진 값만 강제 사용할 때

-- 현재 데이터베이스안에 만들어진 테이블 보기
USE MYDB;
SHOW TABLES; -- 현재 DB에 만들어진 테이블 이름 리스트로 확인할 수 있음

EXPLAIN MANAGE;
-- 테이블의 컬럼 구성 정보를 보여줌
-- EXPLAIN 테이블명;

-- 테이블 구조 확인 명령어 : DESC 테이블명;
-- DESCRIBE 축약한 명령어임 : DESCRIBE 테이블명;
DESC MANAGE;
DESCRIBE MANAGE;

-- 테이블 제거 : DROP TABLE 테이블명;
DROP TABLE MANAGE; -- 없는 테이블 삭제시 에러 발생함
-- 조건부 테이블 삭제 명령 사용할 수 있음
-- DROP TABLE IF EXISTS 테이블명;
DROP TABLE IF EXISTS MANAGE2;

-- 테이블 정보 변경 : ALTER TABLE 사용
-- 테이블명 변경, 컬럼 추가/제거/자료형변경/컬럼명바꾸기/DEFAULT추가|제거/제약조건 추가|제거
-- 1. 테이블명 변경
/*
ALTER TABLE 원래이름 RENAME 바꿀이름 -- 테이블 1개 이름 변경함
RENAME TABLE 원래이름 TO 바꿀이름; -- 테이블명 여러 개 이름 변경할 수 있음.
RENAME TABLE 원래이름1 TO 바꿀이름1, 원래이름2 TO 바꿀이름2, ....;
둘 중 하나 선택 사용할 수 있음
*/
ALTER TABLE MANAGE RENAME MANAGE2;
SHOW TABLES;

RENAME TABLE MANAGE2 TO MANAGE;
SHOW TABLES;

CREATE TABLE ACCOUNT(
	LIST VARCHAR(40),
    TYPE VARCHAR(5),
    AMOUNT INT(11),
    DATE VARCHAR(30)
);

-- DML (Data Manifulation Language, 데이터 조작어)
-- 명령어 : insert, update, delete
-- insert 문 : 행(레코드) 추가 (행 갯수 증가)
-- delete 문 : 행(레코드) 삭제 (행 갯수 감소)
-- update 문 : 컬럼(필드, 속성)  값 수정 (도메인 안의 값 여러 개 수정)

-- insert 문
/*
테이블의 컬럼 전체에 값을 기록하는 경우 : 
구문 1 : 컬럼명 모두 나열
insert into 테이블명 (컬럼명, 컬럼명, ...)
values(컬럼에 기록할 값, 기록할 값, ...); -- 위에 나열된 컬럼명과 순서가 같아야 함
-- 원하는 컬럼에만 값을 기록하면서 행 추가함
-- 누락된 컬럼에는 null (값 없는 빈 칸) 처리됨 (제약조건 확인할 것)

구문 2 : 컬럼명 생략
insert into 테이블명 values(기록할 값, 기록할 값, ....);
-- 모든 컬럼에 값을 기록해야 함
-- 테이블 생성시 컬럼 생성 순수에 맞추어 값 기록해야 함
*/

INSERT INTO ACCOUNT (LIST, TYPE, AMOUNT, DATE)
VALUES ('보험료', '지출', 20, '05-01');
INSERT INTO ACCOUNT VALUES  ('급여', '수입', 450, '05-08');
INSERT INTO ACCOUNT VALUES  ('상여금', '수입', 100, '05-08');
INSERT INTO ACCOUNT VALUES  ('통신비', '지출', 10, '05-11');
INSERT INTO ACCOUNT VALUES  ('식비', '지출', 20, '05-11');
INSERT INTO ACCOUNT VALUES  ('기타소득', '수입', 50, '05-08');

-- 테이블에 기록된 데이터 조회 확인 : SELECT 문
-- 테이블 전체 정보 조회시 : SELECT * FROM 테이블명;
SELECT * FROM ACCOUNT;