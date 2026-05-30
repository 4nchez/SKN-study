-- Day03_select.sql
use mydb;

-- select 문
-- DQL (Data Query Language : 데이터 조회어) 라고도 함
-- 관계형 데이터베이스 (RDB)는 데이트를 테이블 저장한다.
-- 데이터의 항목(속성, Attribute)은 컬럼(column)이 됨 => 객체지향프로그래밍에서 클래스의 필드(멤버변수)가 됨
-- select 문은 테이블에 기록 저장된 데이터를 검색(조회 : 찾아내기 위한)하기 위해 사용되는 sql 구문임

-- select 구문 기본 작성법 :
/*
select * | 컬럼명, 컬럼명, ... , 함수 계산식, 계산식
from 조회할 테이블명;

- * : 테이블이 가진 모든 컬럼을 의미함 (테이블 데이터 전체 조회)
*/

-- 직원 (employee) 테이블 전체 조회
select * from employee;

-- 부서 (department) 테이블 전체 조회
select * from department;

-- 직급 (job) 테이블 전체 조회
select * from job;

-- 특정 컬럼의 값들을 조회하는 경우
-- 예 : 직원 테이블에서 사번(emp_id), 이름(emp_name), 주민번호(emp_no), 급여(salary) 조회
select emp_id, emp_name, emp_no, salary
from employee;

-- select 절에 계산식 사용할 수도 있음
-- 컬럼에 기록된 값들 (도메인)을 계산에 사용함 : 전체 행이 22행이면, 22번 계산이 수행됨
-- 예 : 직원 테이블에서 사번, 이름, 급여, 연봉 계산 조회
-- 연봉은 급여 * 12 로 계산함
select emp_id as 사번, emp_name 이름, salary 급여, salary * 12 as 연봉
from employee;

-- select 절에 함수식 (함수를 이용한 계산식)을 사용할 수도 있음
-- 함수 사용은 제공되는 함수를 파악하고, 사용법 확인하고 이용함
-- 함수 컬럼에 기록된 값들을 읽어서, 함수 안에서 처리한 다음 결과를 리턴함
-- 예 : 직원 테이블에서 사번, 이름, 주민번호 앞 6자리만 조회
select emp_id 사번, emp_name 이름, substr(emp_no, 1, 6) 주민번호
from employee;

-- where (조건)절 사용 규칙 :
-- from 절 다음에 작성할 것
-- where 컬럼명 비교연산자 비교값 [and | or 컬럼명 비교연산자 비교값]
-- where 절은 조건을 만족하는 값이 기록된 행(row, record)들을 골라냄
-- 예 : 직원 테이블에서 미혼자인 (결혼 안 함 : 값 'N' 임) 직원들만 조회
select *
from employee
-- where marriage = 'N';
where marriage = 'n'; -- 문자값은 대소문자 구분함

-- mysql 은 기본적으로 문자열값 비교시 대소문자를 구분하지 않음
-- 문자열값에 대해 대소문자 구분하도록 설정을 바꾸면 됨
-- 방법 1 : 테이블 단위로 설정 변경
alter table employee
modify marriage char(1)
character set utf8mb4 -- 대소문자 구분 안 함
collate utf8mb4_bin;  -- 대소문자 엄격히 구분함

-- 방법 2  : 데이터베이스 단위로 설정 변경 (root 계정에서)
-- 1. 데이터베이스 만들 때 지정하는 경우
create database testdb (
) character set utf8mb4
collate utf8mb4_bin;

-- 2. 만들어진 데이터베이스 설정 변경하는 경우
alter database testdb
character set utf8mb4
collate utf8mb4_bin;

show variables like 'lower_case_table_names';

-- 기혼자인 직원 정보 조회
select *
from employee
-- where marriage = 'Y'; -- 19 rows
where marriage = "Y";
-- 데이터베이스에서는 문자 하나와 문자나열값 구분 안 함 => 전부 문자열임 : '문자' (single quotation 사용)
-- mysql 에서는 문자열 표현에 작은 따옴표, 큰 따옴표 모두 인정함
-- 작은 따옴표만 사용하게 하려면 설정을 변경해야 함

-- 현재 설정 정보 확인 :
show variables like 'sql_mode';
-- STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION
-- ANSI_QUOTES 가 없는 상태이면, 큰 따옴표(") 사용하는 상태임
SET sql_mode = 'ANSI_QUOTES'; -- root 계정에서
-- **********************************************

-- where 절은 조건을 만족하는 행들을 골라냄 => 원하는 컬럼을 선택하는 조회임
-- 예 : 직원 정보에서 직급 코드가 'J4'인 직원들의 사번, 이름, 직급코드, 급여 조회
select emp_id 사번, emp_name 이름, job_id 직급코드, salary 급여
from employee
where job_id = 'J4'; -- 4 rows

-- 예: 직급 테이블(job)에서 직급코드가 'J4'의 직급명은 ?
select job_id, job_title
from job
where job_id = 'J4';

-- select 문은 기본 1개의 테이블에 대한 조회 구문임
-- 여러 개의 테이블이 가진 컬럼들을 select 해야 한다면, join 처리해야 함
-- join 구문 : 여러 개의 테이블을 하나로 합침 (relationship, 연결 컬럼을 사용함)
-- join 구문은 from 절에서 사용함 : 
-- from 테이블명 join 합칠테이블명 using (연결할컬럼명) : 두 테이블의 컬럼명 같을 때
-- from 테이블명 join 합칠테이블명 on (테이블이 가진 연결할컬럼명 = 합칠 테이블의 연결할컬럼명)

-- 예 : 직원 정보에서 직급코드가 'J4'인 직원들의
-- 사번, 이름, 직급코드, 직급명, 관리자사번 조회
select emp_id 사번, emp_name 이름, job_id 직급코드, job_title 직급명, mgr_id 관리자사번
from employee
join job using (job_id)
where job_id = 'J4';

-- 90 번 부서의 부서명은 :
select dept_id, dept_name
from department
where dept_id = '90';

-- 예 : 직원 정보에서 90번 부서에 근무하는 직원들의
-- 사번, 이름, 입사일, 부서코드, 부서명 조회
select emp_id 사번, emp_name 이름, hire_date 입사일, dept_id 부서코드, dept_name 부서명
from employee
join department using (dept_id)
where dept_id = '90'; -- 3 rows

-- 예 : 직급이 과장인 직원 정보 조회
-- 사번, 이름, 직급코드, 직급명, 급여, 보너스포인트
select emp_id 사번, emp_name 이름, job_id 직급코드, job_title 직급명, salary 급여, bonus_pct 보너스포인트
from employee
join job using (job_id)
where job_title = '과장'; -- 3 rows

-- 직원 정보에서 사번, 이름, 급여, 보너스포인트, 보너스포인트가 적용된 연봉 조회
-- 보너스포인트가 적용된 연봉 계산 : (급여 + (급여 * 보너스포인트)) * 12
select emp_id 사번, emp_name 이름, salary 급여, bonus_pct 보너스포인트,
			(salary + (salary * bonus_pct)) * 12 연봉
from employee;  -- 22 rows
-- 데이터베이스에서는 계산할 값이 null 이면 계산 결과도 null 임
-- 계산값이 null 이어도, 계산 결과가 나오게 하려면 null 을 다른 값으로 바꾸면 됨
-- 관련 함수 이용함 : ifnull(null이 있는 컬럼명, 바꿀값), coalesce(null이 있는 컬럼명, 바꿀값)
select emp_id 사번, emp_name 이름, salary 급여, bonus_pct 보너스포인트,
			(salary + (salary * ifnull(bonus_pct, 0))) * 12  as "1년 연봉"
from employee;

-- select 절에 리터럴 (Literal, 문자값) 사용할 수도 있음
-- 결과 뷰에 컬럼처럼 추가되면서 문자값이 채워져서 보여질 것임
select emp_id 사번, emp_name 이름, '재직' 근무상태
from employee;

-- select 구문 작성 형식 :
/*
실행순서 절 				작성내용
5			select			* | [distinct] 컬럼명 | 계산 [as] 별칭
1			from				테이블명 [join 합칠테이블명 using | on (연결컬럼명 [= 이름이 다른 컬럼명])]
2			where			컬럼명 비교연산자 비교값 [and | or 컬럼명 연산자 비교값] (행 추출)
3			group by		그룹묶을 컬럼명 | 그룹묶을 계산식
4			having			그룹함수 비교연산자 비교값 (조건을 만족하는 그룹을 골라냄)
6			order by		컬럼명 정렬방식 (asc | desc), select 절의 별칭 정렬방식, select 절의 항목순번 정렬방식
*/

-- distinct
-- select 절에서 컬럼명 또는 계산식 앞에 붙여서 사용함
-- select 절에서 한번만 사용할 수 있음
-- select ....., distinct 컬럼명 | 계산식
-- 컬럼 또는 계산 결과값에 중복 값을 한 개씩만 선택하라는 의미임
-- 주로 값의 종류를 파악할 때 사용함

select distinct marriage
from employee;

select distinct dept_id
from employee
order by 1 asc;

select distinct dept_id, distinct job_id -- error : 1번만 사용할 수 있음
from employee;

-- 연산자 ********************
-- 예 : 직원 중에 관리자인 직원들만 조회
select distinct mgr_id
from employee
-- where mgr_id != null -- null은 값이 아님, 빈 칸을 의미하는 상태임, 비교연산 불가능함
where mgr_id is not null
order by 1 asc;

/*
비교(관계) 연산자 :
> (크냐, 초과), < (작으냐, 미만), >= (크거나 같으냐, 이상), <= (작거나 같으냐, 이하)
= (같으냐), != (같지 않느냐)
in, not in, like, not like, between and, not between and

논리 연산자 : and, or
*/

-- 90 번 부서에 근무하는 직원 중 급여가 3백만원을 초과하는 직원 정보 조회
-- 사번, 이름, 급여, 부서코드 : 별칭 처리
select emp_id 사번, emp_name 이름, salary 급여, dept_id 부서코드
from employee
where dept_id = '90' and salary > 3000000;

-- 90번 또는 20번 부서에 근무하는 직원 조회
-- 사번, 이름, 주민번호, 전화번호, 부서코드 : 별칭 처리
-- 부서코드로 오름차순정렬 처리함
select emp_id 사번, emp_name 이름, emp_no 주민번호, phone 전화번호, dept_id 부서코드
from employee
-- where dept_id = '90' or dept_id = '20' -- in 연산자 사용해도 됨
where dept_id in ('90', '20')
-- order by dept_id asc; -- 6 rows
-- order by dept_id; -- 오름차순 정렬 asc (ascending) 기본값임, 생략할 수 있음
-- order by 부서코드;
order by 5;

-- MySQL 은 문자리터럴과 컬럼값 연결시에 concat() 함수 사용함
select concat('사번 ', emp_id, '인 직원 ', emp_name, '의 급여는 ', salary, '원 입니다.')
from employee;

-- 급여가 3백만원이상 5백만원이하인 직원 조회
-- 사번, 이름, 급여, 직급코드, 부서코드 : 별칭처리
-- 급여 뒤에 '(원)' 연결 표시할 것
select emp_id 사번, emp_name 이름, concat(salary, '(원)') 급여, job_id 직급코드, dept_id 부서코드
from employee
-- where salary >= 3000000 and salary <= 5000000;
where salary between 3000000 and 5000000;

-- between and 연산자
-- where 컬럼명 between 시작값 and 끝값
-- 시작값 이상이면서 끝값 이하를 의미함
-- 일반비교연산자 사용 : 컬럼명 >= 시작값 and 컬럼명 <= 끝값

-- 현재 날짜와 시간 출력 함수 확인 : 
select now() as '현재시각', current_timestamp as '시스템타임스템프';
-- MySQL 에서는 함수 또는 산술계산식 결과를 바로 확인 출력할 때 from 생략함

select 25 + 3 as 결과;

-- 날짜도 컴퓨터 내부에서는 숫자임 => 날짜도 연산이 가능함
-- 오늘부터 1000일 뒤 날짜는 ? => 오늘날짜 + 1000일
-- MySQL 에서는 날짜더하기 함수를 사용해야 함 : date_add(오늘날짜, 더하기할 날수)
select now() 오늘날짜, date_add(now(), interval 1000 day) "1000일 뒤 날짜";

-- 오늘부터 100일 전 날짜는 ? => 오늘날짜 - 100일
-- mysql 에서는 날짜 빼기 함수 사용함 : date_sub(오늘날짜, 빼기할 날수)
select now(), date_sub(now(), interval 100 day) "100일 전 날짜";

-- MySQL 에서는 컬럼에 날짜(yyyy-mm-dd)만 기록되게 하려면, date 자료형 사용함
-- datetime 자료형은 'yyyy-mm-dd hh:mi:ss' 날짜와 시간으로 표시함
-- 날짜 반환 함수 : curdate(), current_date()
-- 날짜와 시간 반환 함수 : now(), current_timestamp
select curdate(), current_date();

-- 날짜 데이터도 비교 연산할 수 있음
-- 예 :
-- 입사일이 2005년 1월 1일부터 2010년 12월 31일 사이에 입사한 직원 조회
-- 사번, 이름, 입사일, 부서코드 : 별칭처리
-- 날짜데이터도 작은 따옴표로 묶어서 표기해야 함 : '2005-01-01'
-- 날짜데이터 비교시 컬럼에 기록된 날짜 포멧(형식)과 일치되게 작성해야 함
select hire_date from employee;

select emp_id 사번, emp_name 이름, hire_date 입사일, dept_id 부서코드
from employee
-- where hire_date >= '2005-01-01' and hire_date <= '2010-12-31'; -- 7 rows
where hire_date between '2005-01-01' and '2010-12-31'; -- 7 rows

-- 연습 :
-- 2010년 1월 1일 이후에 입사한 기혼인 직원 조회
-- 이름, 입사일, 직급코드, 부서코드, 급여, 결혼여부 : 별칭
-- 입사날짜 뒤에 ' 입사' 문자 연결 출력함
-- 급여값 뒤에 ' (원)' 문자 연결 출력함
-- 결혼여부는 리터럴 사용 : '기혼' 으로 채움
select emp_name 이름, concat(hire_date, ' 입사') 입사일, 
			job_id 직급코드, dept_id 부서코드, concat(salary, ' (원)') 급여, 
            '기혼' 결혼여부
from employee
where hire_date >= '2010-01-01' and marriage = 'Y';  -- 12 rows

-- like 연산자 
-- 문자나 날짜의 패턴을 이용해서 조회하는 방식임
-- 와일드카드 문자 (%, _)를 이용해서 문자 패턴을 만들어서 조회에 사용함
-- 컬럼에 기록된 값이 문자패턴과 일치하는 값들을 골라냄
-- where 컬럼명 like '문자패턴'
-- % : 0개 이상의 글자들을 의미함
-- _ : 글자 한 자리를 의미함

-- 직원 정보에서 성이 김씨인 직원 조회
-- 사번, 이름 전화번호, 이메일 : 별칭 처리
select emp_id, emp_name, phone, email
from employee
where emp_name like '김%'; -- 3 rows

-- 성이 김씨가 아닌 직원 조회
select emp_id, emp_name, phone, email
from employee
-- where emp_name not like '김%'; -- 19 rows
where not emp_name like '김%';

-- 직원들의 이름에 '해' 자가 들어있는 직원 조회
-- 사번, 이름, 전화번호, 이메일
select emp_id, emp_name, phone, email
from employee
where emp_name like '%해%'; -- 1 rows

-- 전화번호의 국번(기지국번호)이 9로 시작하는 번호를 가진 직원 조회
-- 전화번호 구성 : 통신사3자리-기지국번호3~4자리-개인번호4자리
-- 집/사무실 전화번호 : 지역번호2~3자리-국번3~4자리-개인번호4자리
-- 이름, 전화번호 : 별칭 처리

-- 기록값 확인
select phone from employee;  -- 4번째부터 국번임

select emp_name 이름, phone 전화번호
from employee
where phone like '___9%'; -- 3 rows

