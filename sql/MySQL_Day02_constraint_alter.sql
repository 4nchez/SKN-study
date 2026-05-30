-- MySQL_Day02_constraint_alter.sql

-- DDL (데이터 정의어, Data Definition Language)
/*
데이터베이스 객체 생성, 변경, 제거
명령어 : create, alter, drop
- 테이블 생성(create table), 변경(alter table), 제거(drop table), 이름 변경(rename)
- 제약조건 (constraints) :
	데이터 무결성을 보장하는 중요한 기능임
    종류 : primary key, unique, foreign key, check, not null
*/
use mydb;
-- 테이블 생성 예 :
CREATE TABLE user_account (
	user_id	int	primary key	comment '사용자 번호',
    user_name	varchar(50)	not null	comment '사용자 이름',
    user_pwd	varchar(30)	not null	comment '비밀번호',
    email	varchar(50)	not null	unique	comment '이메일',
    created_at	datetime	default current_timestamp	comment '최초 가입 날짜'
) comment='사용자 계정 정보 저장 테이블';

-- 테이블 제거
-- drop table 테이블명;
-- drop table 테이블명, 테이블명, ...;
-- drop table if exists 테이블명;
drop table if exists manage;
drop table user_account;

/*
create table 테이블명 (
	컬럼명	숫자자료형(자릿수) [default 컬럼에 기록할 기본값] [컬럼레벨 제약조건] [comment '컬럼설명'],
    컬럼명 문자자료형(최대기록바이트수) ......,
    
    -- 컬럼 지정 완료한 다음 제약조건만 따로 아래쪽에 모아서 지정할 수 있음 (테이블 레벨)
    -- mysql 에서는 테이블 레벨에서만 제약조건 이름 지정할 수 있음
    [constraint 제약조건이름] 제약조건종류 (적용할 컬럼명) <= 단일키 (컬럼 하나에 제약조건 설정한 것)
    [constraint 제약조건이름] 제약조건종류 (적용할 컬럼명, 컬럼명, ....) <= 복합키 (여러 컬럼을 묶어서 제약조건 설정한 것)
    -- 주의 : not null은 컬럼 레벨에서만 설정할 수 있음
) comment='테이블명설명';
*/

-- 테이블 생성:
create table orders ( 
	ORDER_NO CHAR(4)	comment '주문번호',
	CUST_NO CHAR(4)	comment '고객번호',
	ORDER_DATE DATETIME DEFAULT current_timestamp 	comment '주문일시',
	SHIP_DATE DATETIME comment '배송일자',
	SHIP_ADDRESS VARCHAR(100) comment '배송주소',
	QUANTITY int comment '주문수량'
);

select * from orders;

insert into orders values ('a123', 'c777', default, default, '서울시 서초구 플레이데이터', 12);

-- 제약조건 (constraints)
-- 1. not null 제약조건
-- 지정한 컬럼에 null (값 없음, 빈 칸) 사용 못 하게 하는 제약조건임
-- null 사용되면 에러 발생함
-- 필수 입력 항목에 해당하는 컬럼일 때 지정함

create table tbl_notnull (
	nid	char(3)	not null,	-- 컬럼 레벨
    sname	varchar(20)
);

-- 데이터 기록 저장
insert into tbl_notnull (nid, sname)
values ('100', 'mysql');

select * from tbl_notnull;


insert into tbl_notnull values (null, 'mysql');	-- error
insert into tbl_notnull values ('200', null);	-- ok

-- not null 제약조건은 테이블 레벨에서는 설정 못 함
create table tbl_notnull2 (
	nid	char(3)
    ,	sname	varchar(20)
    -- 테이블 레벨
    ,	constraint	nn_tn2_nid	not null (nid)	-- error
);

-- 2. unique 제약조건
-- 지정한 컬럼에 같은 값 중복 기록 안 되게 검사하는 제약조건임
-- 컬럼 레벨, 테이블 레벨 둘 다 지정할 수 있음
-- 단일키, 복합키 모두 지정 가능함

create table tbl_unique (
	uid	char(3)	unique
    , sname	varchar(20)
);

insert into tbl_unique	values ('100', 'mysql');

select * from tbl_unique;

insert into tbl_unique	values ('100', 'sql'); -- error : 중복 에러
insert into tbl_unique	values ('200', 'mysql'); -- ok

-- 단일키 : 하나의 컬럼에 제약조건 하나 설정한 것
-- 복합키 : 여러 개의 컬럼을 묶어서 하나의 제약조건을 설정한 것 (테이블 레벨에서 지정함)
create table tbl_unique2 (
	uid	char(3)	
    , sname	varchar(20)
    , scode	char(2)
    -- 테이블 레벨
    , constraint uq_tun2_comp unique (uid, sname)
);

insert into tbl_unique2	values ('100', 'mysql', '01');

select * from tbl_unique2;

-- 복합키의 중복 판단
insert into tbl_unique2	values ('200', 'mysql', '01'); -- ok
insert into tbl_unique2	values ('300', 'web', '02'); -- ok
insert into tbl_unique2	values ('100', 'mysql', '03'); -- error : 중복 에러
-- '100 mysql' == '100 mysql'

-- unique 설정 컬럼에는 null 사용할 수 있음
insert into tbl_unique2	values (null, 'mysql', '01'); -- ok
insert into tbl_unique2	values ('100', null, '01'); -- ok
insert into tbl_unique2	values (null, null, '01'); -- ok, 여러 번 실행해도 됨
insert into tbl_unique2	values (null, null, null); -- ok, 여러 번 실행해도 됨

select * from tbl_unique2;

-- 3. primary key 제약조건
-- 테이블의 한 행(row, record)의 정보를 찾아내기 위한 식별(identifier) 키가 될 컬럼에 사용함
-- 한 테이블에 한번만 사용할 수 있음
-- not null + unique
-- 단일키, 복합키 둘 다 지정 가능함
-- 컬럼 레벨, 테이블 레벨 둘 다 설정할 수 있음

create table tbl_pk (
	pid	char(3) primary key 
    , sname	varchar(20)
);

insert into tbl_pk values ('100', 'mysql');

select * from tbl_pk;

insert into tbl_pk values ('100', 'python'); -- error : 중복검사
insert into tbl_pk values (null, 'mysql'); -- error : 필수 입력

-- 테이블 하나당 한번만 사용할 수 있음
create table tbl_pk2 (
	pid	char(3) primary key 
    , sname	varchar(20) primary key 
); -- error

create table tbl_pk2 (
	pid	char(3)
    , sname	varchar(20)
    -- 테이블 레벨
    , primary key (pid)
    , primary key (sname)
); -- error

-- primary key 도 복합키로 지정할 수 있음
create table tbl_pk2 (
	pid	char(3) 
    , sname	varchar(20)
    , scode	char(2)
    -- table level
    , constraint pk_tpk2_comp	primary key (pid, sname)
);

insert into tbl_pk2 values ( '100', 'mysql', '01');

select * from tbl_pk2;

insert into tbl_pk2 values ( '100', 'mysql', '01'); -- error
-- '100 mysql' == '100 mysql' 중복 에러 발생

insert into tbl_pk2 values ( '200', 'mysql', '01'); -- ok
insert into tbl_pk2 values ( null, 'mysql', '01'); -- error : null 사용 못 함
insert into tbl_pk2 values ( '300', null, '01'); -- error : null 사용 못 함

-- 4. check 제약조건
-- mysql 8.0 이상에서만 정상 동작됨
-- InnoDB 엔진에서 작동됨
-- 컬럼에 조건을 지정해서 조건을 만족하는 값만 기록되게 하는 제약조건임
-- 컬럼 레벨 : 컬럼명 자료형 check (컬럼명 비교연산자 조건값)
-- 테이블 레벨 : constraint 제약조건이름 check (컬럼명 비교연산 조건값)

create table tbl_check (
	emp_id	char(3)	primary key	comment '사번'
    , salary	int	check (salary > 0)	comment '급여'
    , marriage	char(1)	comment '결혼 여부'
    -- 테이블 레벨
    , constraint ch_tbchk_marriage	check (marriage in ('Y', 'N'))
) ENGINE=InnoDB;

insert into tbl_check	values ('100', 350, 'Y'); -- ok
insert into tbl_check	values ( '120', -450, 'Y'); -- error
insert into tbl_check	values ('120', 450, 'y'); -- ok : mysql bug 임
insert into tbl_check	values ('110', 550, 'K'); -- ok

select * from tbl_check;

-- 주의 : 체크 조건값에 변경되는 값 (실행될 때마다 바뀌는 값)은 사용할 수 없음
-- 설정 시 사용하면 에러임
create table tbl_check2 (
	emp_id	char(3)	primary key
    , hiredate	datetime	check(hiredate < current_timestamp)
) ENGINE=InnoDB; -- ERROR

-- 테이블 레벨에서 여러 조건들을 한 번에 지정할 수 도 있음
create table tbl_check3 (
	emp_id	char(3)	primary key,
    emp_name	varchar(20)	not null,
    salary	int,
    marriage	char(1),
    
    constraint ck_tblchk3_sal	check	(salary > 0 and salary < 100000000)
);

-- 5. foreign key (외래키, 외부키) 제약조건
-- 수업용 테이블 확인
select * from sal_grade;
select count(*) from sal_grade; -- 5행
select * from country;
select count(*) from country; -- 5행
select * from location;
select count(*) from location; -- 5행
select * from department;
select count(*) from department; -- 7행
select * from job;
select count(*) from job; -- 7행
select * from employee;
select count(*) from employee; -- 22행

/*
- 외부(다른) 테이블의 값을 가져다 기록에 사용하는 컬럼에 설정하는 제약조건임
- 외부 참조 컬럼(값을 제공하는 컬럼)을 의미함
- 참조하는 테이블 (parent table, 부모 테이블 이라고 함)과 이용하는 테이블 간의 관계 (Relationship)을 맺음
- 참조 테이블의 참조 컬럼에서 제공하는 값만 기록에 사용할 수 있게 됨
- 제공되지 않는 값을 기록에 사요하면 에러임
- null 은 사용할 수 있음
- 일반적으로 참조되는 테이블(부모 테이블, 값 제공자)의 참조 컬럼은
	반드시 primary key 또는 unique 제약조건이 설정되어 있어야 함
    
- 컬럼 레벨:
컬럼명 자료형 references 참조부모테이블명 (참조값 제공 컬럼명)

- 테이블 레벨:
constraint 제약조건이름지정 foreign key (적용할 컬럼명) references 참조할부모테이블명 (값제공참조컬럼명)
		[on delete 삭제방법 [on update 업데이트방법]]
        
        -- 삭제 옵션 [수정 옵션]:
        기본은 값을 사용하고 있는 자식 레코드가 있으면, 부모키(제공값)은 삭제[수정] 못 함 (Restricted)
        단, 컬럼에 외래키 지정할 때 삭제 옵션을 변경할 수 있음 : set null, casecade
        - set null : 부모키가 삭제되면, 자식 레코드를 null 로 바꿈
        - casecade : 부모키가 삭제되면, 자식 레코드도 같이 삭제됨
*/

-- 작성된 테이블들에 대한 ERD 만들기 (Workbench 에서도 제공됨)
-- Database 메뉴 > Reverse Engineer... 선택 > root 에 대한 암호 입력 > next > ... > 테이블 선택 > excute
-- erd 생성 > finish > 편집 (이동, 삭제) > File > export : png, svg, pdf 형식으로 추출

-- 자식 레코드 테이블 만들기
create table tbl_fk (
	fid			char(3)
    , sname	varchar(20)
    , loc_id		char(2)	references	location (location_id) -- 외래키(foreign key)로 지정
);

select * from location;

insert into tbl_fk values ('100', 'mysql', 'A1'); -- 참조키가 제공하는 값 사용 : ok
insert into tbl_fk values ('100', 'mysql', 'C1'); -- 부모키가 제공하지 않는 값 사용 : error
-- 외래키 제약조건이 작동되니 않았다면 (에러 발생이 안 된 경우)
-- 외래키 제약조건은 테이블 저장 엔진이 InnoDB 가 아니면 작동되지 않음

-- 해결 1: 테이블 변경 => 테이블 엔진 추가함
alter table tbl_fk ENGINE=InnoDB;

-- 현재 엔진 확인
show table status like 'tbl_fk';

-- 해결 2: 외래키 제약조건 설정이 비활성화된 경우
show variables like 'FOREIGN_KEY_CHECKS';
SET FOREIGN_KEY_CHECKS=1;

-- 해결 3: 외래키 제약조건 설정이 제대로 안 된 경우
ALTER TABLE tbl_fk ADD constraint fk_tblfk_lid foreign key (loc_id) references location (location_id);
-- 현재 테이블에 기록된 값에 부모키가 제공하지 않는 값이 기록되어 있으면 제약조건 추가할 수 없음

select * from tbl_fk;
delete from tbl_fk; -- 테이블 안에 저장된 모든 데이터 삭제함
commit;

-- fk test2
create table tbl_fk2 (
	fid			char(3)
    , sname	varchar(20)
    , loc_id		char(2)	references	location (location_id) -- 외래키(foreign key)로 지정
) ENGINE=InnoDB;
-- 테이블 생성시 InnoDB 엔진 꼭 적용할 것!!!

insert into tbl_fk2 values ('333', 'web', 'B2'); -- ok : mysql 버그임
-- 컬럼 레벨에서 fk 지정시 제대로 작동하지 않는 문제가 있음
-- 테이블 레벨에서 fk 지정하도록 할 것!!!
create table tbl_fk3 (
	fid			char(3)
    , sname	varchar(20)
    , loc_id		char(2)
	-- 테이블 레벨
    , constraint	fk_tblfk3_lid	foreign key (loc_id)	references	location (location_id) -- 외래키(foreign key)로 지정
) ENGINE=InnoDB;

insert into tbl_fk3 values ('333', 'web', 'B2'); -- error : 외래키 제약조건 위배됨

-- 참조 컬럼(부모 키)은 primary key 또는 unique 제약조건이 설정된 컬럼만 가능함
create table tbl_nopk (
	tid	char(3),
    sname	varchar(20)
) ENGINE=InnoDB;

create table tbl_fk4 (
	fid	char(3),
    fname	varchar(10)
    
    , constraint fk_tfk4_fid foreign key (fid) references tbl_nopk (tid) -- error
) ENGINE=InnoDB;

-- 참조(부모) 테이블의 참조컬럼(부모키)이 복합키이면,
-- 외래키 설정하는 자식 컬럼도 동일한 복합키로 만들어야 함
-- primary key 또는 unique 컬럼이 복합키인 경우임
-- 주의 : 자식 레코드에서 복합키를 단일키로 바꿀 수는 없음

select * from tbl_pk2;
desc tbl_pk2;

create table tbl_fk5 (
	fid	char(3),
    fname	varchar(20),
    fcode	char(2),
    
    constraint fk_tfk5_comp foreign key (fid, fname) references tbl_pk2 (pid, sname)
					on delete set null	-- 부모키가 삭제되면 자식 레코드 컬럼은 null 이 됨
                    on update cascade	-- 부모키가 값을 수정하면, 자식 레코드의 컬럼값도 함께 변경됨
) ENGINE=InnoDB;

insert into tbl_fk5 values (100, 'mysql', '33'); -- ok
insert into tbl_fk5 values (300, 'mysql', '33'); -- error : 부모키에 없음

select * from tbl_fk5;

-- 부모 키 변경 : dml의 update 문 사용
select * from tbl_pk2;

-- DML (데이터 조작어, Data Manipulation Language) update 문
-- 명령어 : insert, update, delete 문
-- 테이블에 데이터를 한 행 추가 (insert)
-- 테이블에 기록된 데이터 수정 (값 변경, update)
-- 테이블에 특정 행을 삭제 (delete)

-- update 사용 형식
/*
update 테이블명
set		변경할컬럼명 = 변경값, 변경할컬럼명 = 변경값, ...
where	변경할대상컬럼명 연산자 찾을 값;
*/
update tbl_pk2
set pid = '333', sname = 'python'
where pid = '100';
commit;

select * from tbl_fk5; -- 부모키 변경시 같이 변경 확인

-- 부모키 삭제시 자식 레코드의 컬럼값 null 로 변경 확인
-- dml 의 delete 문 작성형식:
/*
delete from 테이블명
[where 삭제할 대상 커럼명 연산자 찾을값];
- 조건을 만족하는 값이 기록된 행들을 골라내서 삭제함
- where 절 사용 안 하면, 테이블에 기록된 전체 행 삭제함
*/
select * from tbl_pk2;
select * from tbl_fk5;

delete from tbl_pk2
where pid = '333';

-- 실습 : 제약조건이 설정된 테이블 만들기
-- 테이블명 : PHONEBOOK
-- 컬럼명 :  ID  CHAR(3) 기본키(저장이름 : PK_PBID)
--         PNAME      VARCHAR(20)  널 사용못함.
--         PHONE      VARCHAR(15)  널 사용못함
--                                 중복값 입력못함
--                                 (UN_PBPHONE)
--         ADDRESS    VARCHAR(100) 기본값 지정함
--                                 '서울시 구로구'

-- NOT NULL을 제외하고, 모두 테이블 레벨에서 지정함.
create table `PHONEBOOK` (
	ID	CHAR(3),
    PNAME	VARCHAR(20)	NOT NULL,
    PHONE	VARCHAR(15)	NOT NULL,
    ADDRESS	VARCHAR(100)	DEFAULT	'서울시 구로구',
    
    CONSTRAINT PK_PBID PRIMARY KEY (ID),
    CONSTRAINT UN_PBPHONE UNIQUE (PHONE)
) ENGINE=InnoDB;

insert into phonebook
values ('A01', '홍길동', '010-1234-5678', default);
commit; -- 저장 완료

select * from phonebook;

-- 서브쿼리 (subquery)를 사용해서 새 테이블 만들기
-- 테이블 복사본 만들기임
-- select 한 결과를 테이블로 저장하고자 할 때 주로 이용함
-- 메인(외부)쿼리 (서브(내부)쿼리)
/* 
CREATE TABLE 테이블명
AS
SELECT 구문 ;
*/

-- 직원 테이블에서 90번 부서에 근무하는 직원 명단을 조회해서 EMP_CPY90 테이블에 저장
CREATE TABLE EMP_CPY90
AS
SELECT * FROM employee
WHERE DEPT_ID = '90';

select * from EMP_CPY90;

desc employee;
desc EMP_CPY90; -- NOT NULL, DEFAULT 복사해 옴
-- 다른 제약 조건은 복사 안 됨

-- 테이블 복제
create table dept_cpy
as
select * from department;

select * from dept_cpy;

desc department;
desc dept_cpy;

-- ****************************************************
-- alter table : 테이블 구조 또는 정보 변경
-- 테이블명 바꾸기
-- 컬럼 추가, 컬럼 삭제, 컬럼 자료형 변경, DEFAULT 값 변경, 컬럼명 바꾸기
-- 제약조건 추가 / 삭제 / 이름바꾸기

-- DEPARTMENT 테이블 복사본 이용
desc dept_cpy;

-- 컬럼 추가 : add column 사용
alter table dept_cpy
add column mgr_id char(3);

-- 확인
select * from dept_cpy;

-- 컬럼 제거 : drop column 사용
alter table dept_cpy
drop column mgr_id;

desc dept_cpy;
select * from dept_cpy;

-- 컬럼 추가시 기본값 같이 지정할 수 있음
alter table dept_cpy
add column mgr_id char(3) default '100';

select * from dept_cpy;

-- 컬럼 자료형 변경 : modify column 사용
create table empcpy
as
select emp_id, emp_name, hire_date
from employee;

select * from empcpy;

-- char => varchar, varchar => char 변경 가능함
-- 기록된 문자값보다 작은 크기로 줄일 수는 없음
-- 기록된 문자값보다 큰 크기로는 변경할 수 있음
desc empcpy;

alter table empcpy
modify column emp_id varchar(5); 

alter table empcpy
add column mgr_id char(3);

select * from empcpy;

-- 값이 비어 있는 빈 컬럼은 아무 자료형으로 변경할 수 있음
alter table empcpy
modify column mgr_id int;

desc empcpy;

alter table empcpy
modify column mgr_id datetime;

-- default 값 변경
select * from dept_cpy;
desc dept_cpy;

alter table dept_cpy
modify column mgr_id char(3) default '333';
-- mysql 에서는 default 값 변경시 컬럼명 자료형(크기)도 같이 기술해야 함

-- 해당 컬럼에 기록되어 있는 값은 변경되지 않음
-- 변경 이후 default 사용시 변경값이 적용됨
insert into dept_cpy values ('77', '기획팀', 'OT', default);
select * from dept_cpy;

-- NOT NULL 제약조건 변경 : MODIFY COLUMN 사용
-- ADD constraint 사용 안 함
-- 컬럼에 NULL 사용 여부 상태를 변경하는 것임
DESC DEPT_CPY;

alter table dept_cpy
modify column mgr_id char(3) not null;

-- 나머지 제약조건들 추가 / 제거
-- add constraint 제약조건이름 제약조건종류 (적용할 컬럼명)
-- drop constraint 제약조건이름 | primary key
-- 제약변경은 삭제하고 다시 추가하는 방식임
alter table dept_cpy
add constraint fk_dcopy_locid foreign key (loc_id)
references location (location_id);

alter table dept_cpy
drop constraint fk_dcopy_locid;

desc dept_cpy;

-- 컬럼명 바꾸기 : CHANGE Column 사용
-- change column 원래컬럼명 바꿀 컬럼명 원래 자료형(크기) [default 기본값] [null / not null]
alter table dept_cpy
change column mgr_id manager_id char(3) default '200' null;

-- 제약조건 이름 바꾸기는 MySQL 에서는 제공되지 않음
-- 필요시 제약조건 제거하고, 다시 추가하는 것으로 해결함

-- VIEW 객체 *****************************************
-- select 문 저장 용도로 사용함
/*
create view 뷰이름
as
select 문;

drop view 뷰이름;

뷰 실행 : 뷰에 저장된 select 문을 실행함
select * from 뷰이름;

뷰는 alter 제공 안함
create or replace 뷰이름
as
select 문;
*/
create or replace view v_emp
as
select * from employee
where salary > 5000000;

select * from v_emp;

-- TCL (Transaction Control Language, 트랜잭션 제어어)
-- 명령어 : commit, rollback, savepoint
-- DML 명령 구문 실행 후에 반드시 필요함

/*
트랜잭션 (작업 구간) 의 시작 :
1. 이전 트랜잭션이 종료(commit | rollback)되고 나서,
	DML(INSERT, UPDATE, DELETE) 명령 구문을 실행시켰을 때
2. 하나의 트랜잭션이 진행 중인 상태에서 DDL(CREATE, ALTER, DROP) 구문 실행하면,
	자동 현재 트랜잭션이 종료되면서 새 트랜잭션 시작됨
    
트랜잭션 종료 :
- commit (저장 완료), rollback(트랜잭션 시작 위치까지 모두 취소, undo)
- 자동 종료 : DDL 명령 실행시 auto commit
*/

-- mysql 은 모든 명령구문 실행시 자동 커밋되게 설정되어 있음 => 롤백 안 됨
-- 자동 커밋 안 되게 설정을 바꿈 => 롤백할 수 있음
show variables like 'autocommit'; 
SET autocommit = 0;

-- DDL 실행
alter table empcpy
add constraint pk_ecopy_eid primary key (emp_id);
-- 자동 커밋됨, 새 트랜잭션 시작

select * from dept_cpy;

SET SQL_SAFE_UPDATES=0; -- safe mode error 시 사용
update dept_cpy
set dept_id = '99'
where dept_id='77';

rollback; -- 취소

update dept_cpy
set dept_id = '99'
where dept_id='77';

commit; -- 저장 완료, 트랜잭션 종료, 롤백 못 함

rollback;

select * from dept_cpy;