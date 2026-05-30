-- 과제
use homeworkdb;

-- 1. 계열 정보를 저장핛 카테고리 테이블을 맊들려고 핚다. 다음과 같은 테이블을 작성하시오.
create table TB_CATEGORY (
	NAME	VARCHAR(10),
	USE_YN	CHAR(1)	default 'Y'
)ENGINE=InnoDB;
-- desc TB_CATEGORY;

-- 2. 과목 구분을 저장핛 테이블을 맊들려고 핚다. 다음과 같은 테이블을 작성하시오.
create table TB_CLASS_TYPE (
	NO	VARCHAR(5) PRIMARY KEY,
	NAME	VARCHAR(10)
)ENGINE=InnoDB;
-- desc TB_CLASS_TYPE;

-- 3. TB_CATAGORY 테이블의 NAME 컬럼에 PRIMARY KEY 를 생성하시오.
-- (KEY 이름을 생성하지 않아도 무방함. 만일 KEY 이를 지정하고자 한다면 이름은 본인이 알아서 적당한 이름을 사용한다.)
-- 테이블명 오타;;
alter table TB_CATEGORY
add constraint PK_TBCY primary key (name);
-- desc TB_CATEGORY;

-- 4. TB_CLASS_TYPE 테이블의 NAME 컬럼에 NULL 값이 들어가지 않도록 속성을 변경하시오.
alter table TB_CLASS_TYPE
modify column NAME VARCHAR(10) not null;
-- desc TB_CLASS_TYPE;

-- 5. 두 테이블에서 컬럼 명이 NO 인 것은 기존 타입을 유지하면서 크기는 10. 으로, 컬럼명이 NAME 인 것은 마찪가지로 기존 타입을 유지하면서 크기 20 으로 변경하시오.
alter table TB_CLASS_TYPE
modify column NO VARCHAR(10),
modify column NAME VARCHAR(20);
-- desc TB_CLASS_TYPE;

alter table TB_CATEGORY
modify column NAME VARCHAR(20);
-- desc TB_CATEGORY;

-- 6. 두 테이블의 NO 컬럼과 NAME 컬럼의 이름을 각 각 TB_ 를 제외핚 테이블 이름이 앞에 붙은 형태로 변경핚다.
-- (ex. CATEGORY_NAME)
alter table TB_CLASS_TYPE
change column NO CLASS_TYPE_NO VARCHAR(10),
change column NAME CLASS_TYPE_NAME VARCHAR(20);
-- desc TB_CLASS_TYPE;

alter table TB_CATEGORY
change column NAME CATEGORY_NAME VARCHAR(20);
-- desc TB_CATEGORY;

-- 7. TB_CATAGORY 테이블과 TB_CLASS_TYPE 테이블의 PRIMARY KEY 이름을 다음과 같이 변경하시오.
-- Primary Key 의 이름은 ‚PK_ + 컬럼이름‛으로 지정하시오. (ex. PK_CATEGORY_NAME )
alter table TB_CLASS_TYPE
drop constraint `PRIMARY`;
-- desc TB_CLASS_TYPE;

alter table TB_CATEGORY
drop constraint `PRIMARY`;
-- desc TB_CATEGORY;

alter table TB_CATEGORY
add constraint PK_CATEGORY_NAME primary key (CATEGORY_NAME);
-- desc TB_CATEGORY;

alter table TB_CLASS_TYPE
add constraint PK_CLASS_TYPE_NO primary key (CLASS_TYPE_NO);
-- desc TB_CLASS_TYPE;

/*
8. 다음과 같은 INSERT 문을 수행핚다.
INSERT INTO TB_CATEGORY VALUES ('공학','Y');
INSERT INTO TB_CATEGORY VALUES ('자연과학','Y');
INSERT INTO TB_CATEGORY VALUES ('의학','Y');
INSERT INTO TB_CATEGORY VALUES ('예체능','Y');
INSERT INTO TB_CATEGORY VALUES ('인문사회','Y');
COMMIT; 
*/
INSERT INTO TB_CATEGORY VALUES ('공학','Y');
INSERT INTO TB_CATEGORY VALUES ('자연과학','Y');
INSERT INTO TB_CATEGORY VALUES ('의학','Y');
INSERT INTO TB_CATEGORY VALUES ('예체능','Y');
INSERT INTO TB_CATEGORY VALUES ('인문사회','Y');
COMMIT; 

/*
9.TB_DEPARTMENT 의 CATEGORY 컬럼이 TB_CATEGORY 테이블의 CATEGORY_NAME 컬럼을 부모
값으로 참조하도록 FOREIGN KEY 를 지정하시오. 이 때 KEY 이름은
FK_테이블이름_컬럼이름으로 지정핚다. (ex. FK_DEPARTMENT_CATEGORY )
*/
-- desc TB_DEPARTMENT;
-- desc TB_CATEGORY;

alter table TB_DEPARTMENT
modify column CATEGORY VARCHAR(20);
-- desc TB_DEPARTMENT;

alter table TB_DEPARTMENT
add constraint FK_DEPARTMENT_CATEGORY foreign key (CATEGORY)
references TB_CATEGORY (CATEGORY_NAME);
-- desc TB_DEPARTMENT;

/*
10. 춘 기술대학교 학생들의 정보맊이 포함되어 있는 학생일반정보 VIEW 를 맊들고자 핚다.
아래 내용을 참고하여 적젃핚 SQL 문을 작성하시오.
뷰 이름
VW_학생일반정보
컬럼
학번
학생이름
주소
*/

-- desc tb_student;

create or replace view `VW_학생일반정보`
as
select STUDENT_NO as `학번`, STUDENT_NAME as `학생이름`, STUDENT_ADDRESS as `주소` from tb_student;

/*
11. 춘 기술대학교는 1 년에 두 번씩 학과별로 학생과 지도교수가 지도 면담을 진행핚다.
이를 위해 사용핛 학생이름, 학과이름, 담당교수이름 으로 구성되어 있는 VIEW 를 맊드시오.
이때 지도 교수가 없는 학생이 있을 수 있음을 고려하시오 (단, 이 VIEW 는 단순 SELECT
맊을 핛 경우 학과별로 정렬되어 화면에 보여지게 맊드시오.)
뷰 이름
VW_지도면담
컬럼
학생이름
학과이름
지도교수이름
*/

CREATE OR REPLACE view `VW_지도면담`
as
select S.STUDENT_NAME as `학생이름`, D.DEPARTMENT_NAME as `학과이름`, P.PROFESSOR_NAME as `지도교수이름`
from tb_student as S
left join tb_department as D on D.DEPARTMENT_NO = S.DEPARTMENT_NO
left join tb_professor as P on P.PROFESSOR_NO = S.COACH_PROFESSOR_NO
where S.COACH_PROFESSOR_NO is not null -- 고려?? JOIN 만??
order by  D.DEPARTMENT_NAME ASC
;

/*
12. 모든 학과의 학과별 학생 수를 확인핛 수 있도록 적젃핚 VIEW 를 작성해 보자.
뷰 이름
VW_학과별학생수
컬럼
DEPARTMENT_NAME
STUDENT_COUNT
*/

CREATE OR REPLACE VIEW `VW_학과별학생수`
as
SELECT D.DEPARTMENT_NAME, COUNT(S.STUDENT_NAME) as `STUDENT_COUNT`
from tb_student as S
left join tb_department as D on D.DEPARTMENT_NO = S.DEPARTMENT_NO
group by D.DEPARTMENT_NO;

/*
13. 위에서 생성핚 학생일반정보 View 를 통해서 학번이 A213046 인 학생의 이름을 본인
이름으로 변경하는 SQL 문을 작성하시오.
*/
-- select * from `vw_학생일반정보`
-- where STUDENT_NO = 'A213046';

update  `vw_학생일반정보`
set STUDENT_NAME = '4nchez'
where STUDENT_NO = 'A213046';

/*
14. 13 번에서와 같이 VIEW 를 통해서 데이터가 변경될 수 있는 상황을 막으려면 VIEW 를
어떻게 생성해야 하는지 작성하시오.
*/
create or replace view `VW_학생일반정보`
as
select DISTINCT  STUDENT_NO, STUDENT_NAME, STUDENT_ADDRESS from tb_student;

/*
15. 춘 기술대학교는 매년 수강신청 기갂맊 되면 특정 인기 과목들에 수강 신청이 몰려
문제가 되고 있다. 최근 3 년을 기준으로 수강인원이 가장 맋았던 3 과목을 찾는 구문을
작성해보시오.
과목번호 과목이름 누적수강생수(명)
---------- ------------------------------ ----------------
C1753800 서어방언학 29
C1753400 서어문체롞 23
C2454000 원예작물번식학특롞 22
*/

select g.CLASS_NO as `과목번호`, c.CLASS_NAME as `과목이름`, count(c.CLASS_NAME) as `누적수강생수(명)` from tb_grade g
left join tb_class as c on c.CLASS_NO = g.CLASS_NO
where PERIOD_DIFF(DATE_FORMAT(CURDATE(), '%Y%m'), term_NO) <= 36
group by g.CLASS_NO, c.CLASS_NAME
order by `누적수강생수(명)` desc
limit 3;



-- DML ***********************************************************
/*
1. 과목유형 테이블(TB_CLASS_TYPE)에 아래와 같은 데이터를 입력하시오.
번호, 유형이름
------------
01, 전공필수
02, 전공선택
03, 교양필수
04, 교양선택
05. 논문지도
*/
insert into TB_CLASS_TYPE 
values 
	('01', '전공필수'),
	('02', '전공선택'),
	('03', '교양필수'),
	('04', '교양선택'),
	('05', '논문지도');

-- select * from TB_CLASS_TYPE;

/*
2. 춘 기술대학교 학생들의 정보가 포함되어 있는 학생일반정보 테이블을 맊들고자 핚다.
아래 내용을 참고하여 적젃핚 SQL 문을 작성하시오. (서브쿼리를 이용하시오)
테이블이름
TB_학생일반정보
컬럼
학번
학생이름
주소
*/
create table `TB_학생일반정보`
as
select STUDENT_NO as `학번`, STUDENT_NAME as `학생이름`, STUDENT_ADDRESS as `주소` from tb_student;

/*
3. 국어국문학과 학생들의 정보맊이 포함되어 있는 학과정보 테이블을 맊들고자 핚다.
아래 내용을 참고하여 적젃핚 SQL 문을 작성하시오. (힌트 : 방법은 다양함, 소신껏
작성하시오)
테이블이름
TB_국어국문학과
컬럼
학번
학생이름
출생년도 <= 네자리 년도로 표기
교수이름
*/
-- * 데이터 오류 * : 00년생 이후 주민번호 뒷자리 잘못 들어가있음;;
SELECT S.STUDENT_NO as `학번`, S.STUDENT_NAME as `학생이름`, 
   CASE 
        WHEN SUBSTR(S.STUDENT_SSN, 8, 1) IN ('1', '2') THEN CONCAT('19', LEFT(S.STUDENT_SSN, 2))
        WHEN SUBSTR(S.STUDENT_SSN, 8, 1) IN ('3', '4') THEN CONCAT('20', LEFT(S.STUDENT_SSN, 2))
    END as `출생년도`,  P.PROFESSOR_NAME as `지도교수이름`
from tb_student as S
left join tb_professor as P on P.PROFESSOR_NO = S.COACH_PROFESSOR_NO
WHERE S.DEPARTMENT_NO IN (SELECT DEPARTMENT_NO FROM tb_department WHERE DEPARTMENT_NAME = '국어국문학과');

/*
4. 현 학과들의 정원을 10% 증가시키게 되었다. 이에 사용핛 SQL 문을 작성하시오. (단,
반올림을 사용하여 소수점 자릿수는 생기지 않도록 핚다)
*/
-- select * from tb_department;
SET SQL_SAFE_UPDATES=0;
update tb_department
set CAPACITY = ROUND(CAPACITY * 1.1, 0);

/*
5. 학번 A413042 인 박건우 학생의 주소가 "서울시 종로구 숭인동 181-21 "로 변경되었다고
핚다. 주소지를 정정하기 위해 사용핛 SQL 문을 작성하시오.
*/
-- select * from tb_student where STUDENT_NO = 'A413042';
update tb_student
set STUDENT_ADDRESS = '서울시 종로구 숭인동 181-21 '
where STUDENT_NO = 'A413042';

/*
6. 주민등록번호 보호법에 따라 학생정보 테이블에서 주민번호 뒷자리를 저장하지 않기로
결정하였다. 이 내용을 반영핛 적젃핚 SQL 문장을 작성하시오.
(예. 830530-2124663 ==> 830530 )
*/
-- select * from tb_student;
update tb_student
set STUDENT_SSN = LEFT(STUDENT_SSN, 6);

/*
7. 의학과 김명훈 학생은 2005 년 1 학기에 자신이 수강핚 '피부생리학' 점수가
잘못되었다는 것을 발견하고는 정정을 요청하였다. 담당 교수의 확인 받은 결과 해당
과목의 학점을 3.5 로 변경키로 결정되었다. 적젃핚 SQL 문을 작성하시오.
*/
-- 데이터 없음
update tb_grade
set POINT = 3.5
where 
    CLASS_NO = (select CLASS_NO from tb_class where CLASS_NAME = '피부생리학')
and
    STUDENT_NO = (
        select STUDENT_NO 
        from tb_student 
        where STUDENT_NAME = '김명훈'
        and DEPARTMENT_NO = (select DEPARTMENT_NO from tb_department where DEPARTMENT_NAME = '의학과')
    )
and TERM_NO = '200501';

-- 8. 성적 테이블(TB_GRADE) 에서 휴학생들의 성적항목을 제거하시오.
delete 
from tb_grade
where STUDENT_NO
in (
	select STUDENT_NO from tb_student where ABSENCE_YN = 'Y'
    );
/*
select * from tb_grade
where STUDENT_NO
in (
	select STUDENT_NO from tb_student where ABSENCE_YN = 'Y'
    );
*/