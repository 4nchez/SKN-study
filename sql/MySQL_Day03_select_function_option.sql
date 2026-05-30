-- Day03_select_function_option.sql
-- 함수, 조인, 서브쿼리

-- MySQL 에서 제공하는 함수 (function)
-- 사용 : 함수명(컬럼명[, 값, ........])
-- 단일행함수와 그룹함수로 구분됨 : 결과행의 갯수가 다름
-- 단일행 함수 (single row function) :
-- 		지정하는 컬럼의 값이 N개이면, 함수 처리 결과도 N개임 (1개 읽어서 1개 반환 => N번 반복)
-- 그룹 함수 (group function) :
-- 		읽은 값이 N개이면, 리턴 결과값은 1개임

-- 예 : 직원 정보에서 이메일을 모두 대문자로 변환 처리한다면
select email, -- 22 rows
			upper(email) -- 22 rows : 단일행함수
from employee;

-- 예 : 직원들의 급여의 총합을 구한다면
select sum(salary) -- 1 row : 그룹함수
from employee;

-- 주의 1:
-- select 절에 단일행함수와 그룹함수 같이 사용 못 함
select substr(emp_no, 1, 6), sum(salary)
from employee;
-- 현재 데이터베이스는 관계형 데이터베이스(RDB)임
-- RDB는 데이터를 2차원 테이블(반드시 사각형)로 표현함 => 사각형이 아닌 결과는 같이 출력 못 함

-- 주의 2 :
-- where 절에 그룹함수 사용 못 함
-- 예 : 직원들 중에서 직원 전체 급여의 평균보다 급여를 많이 받는 직원 조회
select *
from employee
where salary > avg(salary);   -- error
-- where 절은 한 행씩 검사하는 조건절임

-- 해결 1 :
-- 1. 급여 평균 조회
select avg(salary)  -- 3961818.1818
from employee;

-- 2. 평균값을 조건에 사용
select *
from employee
where salary > 3961818.1818; -- 7행

-- 해결 2 : 서브쿼리 사용
select *
from employee
where salary > (select avg(salary) from employee); -- 7행

-- 그룹 함수 ************************
-- sum(), avg(), min(), max(), count()

-- sum(컬럼명) | sum(distinct 컬럼명)
-- 해당 컬럼의 숫자값들의 합계를 구해서 리턴함
-- 예 : 소속부서가 50이거나 부서가 배정되지 않은 직원들의 급여 합계 조회
select sum(salary) 급여합계,
		  sum(distinct salary) '중복 제외한 급여합계'
from employee
where dept_id = '50' or dept_id is null;

-- 합계 계산에 사용된 값들 확인 : 
select dept_id, salary
from employee
where dept_id = '50' or dept_id is null; -- 8 rows

-- avg(컬럼명) | avg(distinct 컬럼명)
-- 해당 컬럼의 숫자값들의 평균을 구해서 리턴
-- 예 : 소속부서가 50 또는 90 또는 null 인 직원들의 보너스포인트 평균 조회
select avg(bonus_pct) 기본평균, -- /4
			avg(distinct bonus_pct) 중복제거평균, -- /3
            avg(ifnull(bonus_pct, 0)) null포함평균 -- /11
from employee
where dept_id in ('50', '90')  or dept_id is null;

-- 계산에 사용된 값 확인
select dept_id, bonus_pct
from employee
where dept_id in ('50', '90')  or dept_id is null; -- 11 rows

-- max(컬럼명) | max(distinct 컬럼명)
-- 지정한 컬럼에서 가장 큰 값 리턴 (숫자, 문자, 날짜/시간 모두 사용할 수 있음)
-- min(컬럼명) | min(distinct 컬럼명)
-- 지정한 컬럼에서 가장 작은 값 리턴 (숫자, 문자, 날짜/시간 모두 사용할 수 있음)

-- 예 : 부서코드가 50 또는 90인 직원들의
-- 직급코드(char)의 최댓값, 최솟값
-- 입사일(date)의 최댓값, 최솟값
-- 급여(int)의 최댓값, 최솟값 조회
select max(job_id), min(job_id),
			max(hire_date), min(hire_date),
            max(salary), min(salary)
from employee
where dept_id in ('50', '90');

-- count(*) | count(컬럼명) | count(distinct 컬럼명)
-- count(*) : 테이블 전체 행 갯수 리턴 (null 포함) 또는 조건을 만족하는 행 갯수
-- count(컬럼명) : 지정한 컬럼에 기록된 값(행) 갯수 (null 제외됨)

-- 예 : 50번 부서 또는 부서코드가 null인 직원 수 조회
select dept_id
from employee
where dept_id = '50' or dept_id is null; -- 8 rows (8명)

select count(*), -- 8 (null 포함 전체 행 갯수)
			count(dept_id), -- 6 (null 제외)
            count(distinct dept_id) -- 1
from employee
where dept_id = '50' or dept_id is null;

-- *************************************
-- group by 절
/*
지정한 컬럼에 같은 값들끼리 묶어서 그룹함수 적용할 때 사용함
작성 방법 :
	group by 컬럼명 | 그룹핑을 위한 계산식
-  group by 가 사용되면, select 절에는 그룹함수 사용해야 함
- 작성 위치 : where 절 다음
- 실행 순서 : where 에서 행들을 골라낸 다음에, group by 가 작동됨
*/

-- 컬럼에 기록된 값 확인
select dept_id
from employee;

-- 사용된 값 확인
select distinct dept_id
from employee;

-- 부서별 급여의 합계 조회
select dept_id, sum(salary)
from employee
group by dept_id    -- 같은 부서코드 값들끼리 그룹이 묶임
order by dept_id desc;

select dept_id 부서코드,
		  sum(salary) 부서별급여합계,
          floor(avg(salary)) 부서별급여평균,
          count(salary) 부서별직원수,
          max(salary) 부서별최대급여,
          min(salary) 부서별최소급여
from employee
group by dept_id -- 같은 부서코드 값들끼리 그룹이 묶임
order by dept_id desc;

-- group by 절에는 그룹으로 묶기 위한 계산식을 사용할 수도 있음
-- 예 : 직원 정보에서 성별별 급여합계, 급여평균(천단위에서 반올림처리), 직원수 조회
-- 성별 오름차순정렬함
select case when substr(emp_no, 8, 1) in ('1', '3') then '남'
				else '여'
				end  성별, 
               sum(salary) 급여합계,
               round(avg(salary), -4) 급여평균,
               count(*) 직원수
from employee
group by case when substr(emp_no, 8, 1) in ('1', '3') then '남'
			   else '여'
			   end
order by 성별;

-- having 절 -----------------------------------
/*
사용 위치 : group by 절 아래에 사용함
작성 형식 : having 그룹함수(계산에 적용할 컬럼명) 비교연산자 비교값
group by의 조건절임
=> 그룹별로 그룹함수가 계산한 결과들을 가지고, 조건을 만족하는 그룹을 골라낸
=> 골라낸 그룹과 그룹함수 계산 결과를 select 절에 작성함

작동 순서 :
from => where => group by => having => select => order by
*/

-- 예 : 부서별 급여 합계 중 가장 큰 값 조회
select max(sum(salary)) -- 1개
from employee
group by dept_id; -- 7개 그룹
-- error 1 : select 절에는 7개 그룹에 대한 계산 결과 7개 나와야 함
-- error 2 : mysql 에서는 그룹함수 중첩 사용 못 함

-- 해결 1 : 
-- 서브쿼리를 사용하는 방법
select max(a.급여합계) 최대급여합계
from (select sum(salary) 급여합계
		  from employee
          group by dept_id) a; -- 테이블명 대신 서브쿼리 실행 결과뷰(인라인 뷰)를 사용할 수 있음
          
-- 해결 2 :
-- having 절 사용
select dept_id, sum(salary)
from employee
group by dept_id
-- having sum(salary) = 21100000;
having sum(salary) = (select max(a.급여합계) 최대급여합계
								   from (select sum(salary) 급여합계
											from employee
											group by dept_id) a);

-- ****************************************************
-- 조인 (join)
-- 여러 개의 테이블을 하나로 합쳐서 큰 테이블을 만드는 것
-- 조인한 결과 테이블에서 원하는 컬럼을 선택함
-- mysql 은 ansi 표준구문을 지원함
-- 조인은 기본 equal join 임 (두 테이블의 지정한 컬럼의 같은 값끼리 연결되면서 합쳐짐)
-- 두 테이블에서 equal 이 아닌 값들은 조인 결과에서 제외됨 (inner join 임 : 기본임)

select *
from employee
-- inner join department using (dept_id); -- 20 rows
join department using (dept_id);
-- inner 생략해도 됨

-- 일치하지 않는 값도 조인에 포함시키고자 한다면
-- outer join 을 사용함
-- left outer join, right outer join
-- outer 는 생략해도 됨
select *
-- from employee left outer join department using (dept_id);
-- employee 의 모든 행을 포함시킨다면
from department  right  join employee using (dept_id);

-- self join
-- 자신과 조인
-- 같은 테이블로 2번 조인
-- 상사-부하 관계, 관리자-일반 직원, 계층 구조로 표현할 때 사용
-- 한 테이블 안에 pk 와 fk 관계가 존재해야 함

-- 예 : 관리자 명단과 관리자가 관리하는 직원 명단 조회
-- self join 시에는 테이블 별칭을 붙여줘야 함 => 테이블 별칭 사용시에는 on 사용해야 함
select count(mgr_id) -- 15개
from employee;

select distinct mgr_id
from employee; -- 7 rows

select e.emp_name 직원명단, m.emp_name 관리자명단
from employee e
join employee m on (e.mgr_id = m.emp_id)
order by 관리자명단; -- 15 rows

-- N개의 테이블 조인시, 연결관계 주의할 것
-- 직원이름, 직급명, 부서명, 근무지역명, 소속국가명 조회
-- 단, 직원 전체 조회임
select emp_name, job_title, dept_name, loc_describe, country_name
from employee
left join job using (job_id)
left join department using (dept_id)
left join location on (loc_id = location_id)
left join country using (country_id); -- 22 rows