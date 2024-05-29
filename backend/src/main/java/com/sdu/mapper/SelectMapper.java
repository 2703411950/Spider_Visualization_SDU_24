package com.sdu.mapper;

import com.sdu.entity.CityCount;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface SelectMapper {

    @Select("SELECT job as name, count(*) as value from employ GROUP BY job;")
    List<Map<String, Object>> selectJobCount();

    @Select("SELECT education as name, count(*) as value FROM employ GROUP BY education;")
    List<Map<String, Object>> selectEducationCount();

    @Select("SELECT AVG(salary) as value, job as name FROM employ WHERE salary IS NOT NULL GROUP BY job;")
    List<Map<String, Object>> selectJobSalary();

    @Select("SELECT city as name, COUNT(*) as value FROM employ GROUP BY city;")
    List<Map<String, Object>> selectJobDistribution();
}
