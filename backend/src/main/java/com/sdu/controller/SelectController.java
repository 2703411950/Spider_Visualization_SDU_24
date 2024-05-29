package com.sdu.controller;

import com.sdu.entity.CityCount;
import com.sdu.mapper.SelectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping
public class SelectController {

    @Autowired
    private SelectMapper selectMapper;

    @GetMapping("/selectJobCount")
    public List<Map<String, Object>> selectJobCount() {
        List<Map<String, Object>> res = selectMapper.selectJobCount();
        List<Map<String, Object>> filteredRes = new ArrayList<>();
        for (Map<String, Object> re : res) {
            String s = (String) re.get("name");
            String[] parts = s.split("-");
            String newName = parts[parts.length - 1];
            re.put("name", newName);

            Long value = (Long) re.get("value");
            if (value > 2) {
                filteredRes.add(re);
            }
        }
        return filteredRes;
    }

    @GetMapping("/selectEducationCount")
    public List<Map<String, Object>> selectEducationCount(){
        return selectMapper.selectEducationCount();
    }

    @GetMapping("/selectJobSalary")
    public List<Map<String, Object>> selectJobSalary(){
        List<Map<String, Object>> res = selectMapper.selectJobSalary();

        for (Map<String, Object> re : res) {
            String s = (String) re.get("name");
            String[] parts = s.split("-");
            String newName = parts[parts.length - 1];
            re.put("name", newName);
        }
        return res;
    }

    @GetMapping("/selectJobDistribution")
    public List<Map<String, Object>> selectJobDistribution(){
        return selectMapper.selectJobDistribution();
    }
}
