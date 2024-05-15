"""
1. generate the automation test html report
2. can filter testcases by tag/package

@author: Wang Lin
"""
import os
import datetime
import traceback
import linktest
import collections


try:
    import settings
except BaseException:
    traceback.print_exc()
    raise BaseException("there are no settings/__init__.py found in your project ...")

from .ui_testcase import UITestCase
from .xml_report import convert_to_seconds


# used to map all the testcases
def map_testcases_package(all_testcases_package, testcase_map_tag, testcase_filter_tag, testcase):
    if "." not in testcase_filter_tag:
        testcase.testcase_filter_tag += testcase_filter_tag
        testcase.testcase_filter_tag += "~"
        all_testcases_package.add(testcase_filter_tag)
        testcase_map_tag[testcase_filter_tag].append(testcase)
    else:
        all_testcases_package.add(testcase_filter_tag)
        if testcase_filter_tag in testcase_map_tag.keys():
            testcase_map_tag[testcase_filter_tag].append(testcase)
            testcase.testcase_filter_tag += testcase_filter_tag
            testcase.testcase_filter_tag += "~"
        else:
            testcase_map_tag[testcase_filter_tag] = []
            testcase_map_tag[testcase_filter_tag].append(testcase)
            testcase.testcase_filter_tag += testcase_filter_tag
            testcase.testcase_filter_tag += "~"

        testcase_filter_tag = testcase_filter_tag[0:testcase_filter_tag.rfind(".")]
        map_testcases_package(all_testcases_package, testcase_map_tag, testcase_filter_tag, testcase)


class Reporter(object):

    def __init__(self, output_folder, passed_cases, failed_cases, error_cases, start_time, platform_info, create_global_data_list_flag=False, rerun_flag=False):
        try:
            self.generate_html_report(output_folder, passed_cases, failed_cases, error_cases, start_time,
                                      platform_info, create_global_data_list_flag, rerun_flag)
        except BaseException:
            traceback.print_exc()

    def generate_html_report(self, output_folder, passed_cases, failed_cases, error_cases, start_time, platform_info,
                             create_global_data_list_flag, rerun_flag):
        with open(output_folder + os.sep + "report.html", "w") as report_file_handler:
            end_time = datetime.datetime.now()
            execution_time = end_time - start_time
            execution_time = convert_to_seconds(execution_time)

            failed_cases_count = len(failed_cases)
            if failed_cases_count > 1:
                if settings.RERUN_FLAG:
                    failed_cases_count = failed_cases_count / 2

            failed_cases_count = int(failed_cases_count)

            css = """
            <style type="text/css">
                a:link,a:visited{
                    text-decoration:none;
                }
                a:hover{
                    text-decoration:underline;
                    background-color:#8E8E8E;
                }
            </style>
            """

            # java script code for filter function
            java_script_code_for_filter = """
            <script type="text/javascript">

                function changeTag(){
                    var my_select = document.getElementById("testcase_tag");
                    if (my_select.value == "tests"){
                        //all_failed_test_cases is represent for all failed testcases
                        if(document.getElementById("all_failed_test_cases")){
                            all_failed_test_case = document.getElementById("all_failed_test_cases");
                            all_failed_test_case.style.display="none";
                            all_failed_test_case.style.display="block";

                            all_failed_case_list = document.getElementsByClassName("all_failed_case");
                            for(var i=0;i<all_failed_case_list.length;i++){
                                all_failed_case_list[i].style.display="block";
                            }
                            if (i > 1){
                                var new_str = i + " Failed Test Cases";
                                document.getElementById("num_fail").innerHTML=new_str;
                            } else {
                                var new_str = i + " Failed Test Case";
                                document.getElementById("num_fail").innerHTML=new_str;
                            }
                        }

                        //all_passed_test_cases is represent for all passed testcases
                        if (document.getElementById("all_passed_test_cases")){
                            all_passed_test_case = document.getElementById("all_passed_test_cases");
                            all_passed_test_case.style.display="none";
                            all_passed_test_case.style.display="block";
                            all_passed_case_list = document.getElementsByClassName("all_passed_case");

                            for(var j=0;j<all_passed_case_list.length;j++){
                                all_passed_case_list[j].style.display="block";
                            }
                            if (j > 1){
                                var new_str = j + " Passed Test Cases";
                                document.getElementById("num_pass").innerHTML=new_str;
                                } 
                            else {
                                var new_str = j + " Passed Test Case";
                                document.getElementById("num_pass").innerHTML=new_str;
                            }
                        }
                    }

                    var l = new Array()
                    k = 0;
                    all_failed_case_list = document.getElementsByClassName("all_failed_case");

                    for(var i=0;i<all_failed_case_list.length;i++){
                        all_failed_case_list[i].style.display="none";

                        if (all_failed_case_list[i].getAttribute("name").indexOf(my_select.value) != -1){
                            l[k] = all_failed_case_list[i];
                            k = k + 1;
                        }
                    }

                    all_passed_case_list = document.getElementsByClassName("all_passed_case");

                    for(var i=0;i<all_passed_case_list.length;i++){
                        all_passed_case_list[i].style.display="none";
                        if (all_passed_case_list[i].getAttribute("name").indexOf(my_select.value) != -1){
                            l[k] = all_passed_case_list[i];
                            k = k + 1;
                        }
                    }

                    if (document.getElementById("all_failed_test_cases")){
                        all_failed_test_case = document.getElementById("all_failed_test_cases");
                        all_failed_test_case.style.display="none";
                        all_failed_test_case.style.display="block";
                    }

                    if (document.getElementById("all_passed_test_cases")){
                        all_passed_test_case = document.getElementById("all_passed_test_cases");
                        all_passed_test_case.style.display="none";
                        all_passed_test_case.style.display="block";
                    }

                    num_failed_case = 0;
                    num_passed_case = 0;

                    for(var i=0;i<l.length;i++){
                        l[i].style.display="block";
                        if ("all_failed_case"==l[i].className){
                            num_failed_case = num_failed_case + 1;
                        }
                        if ("all_passed_case"==l[i].className){
                            num_passed_case = num_passed_case + 1;
                        }
                    }

                    %s
                    
                    if (document.getElementById("num_fail")){
                        var button = document.getElementById("failed_testcase_names");
                        if (num_failed_case > 1){
                            var new_str = num_failed_case + " Failed Test Cases";
                            document.getElementById("num_fail").innerHTML=new_str;
                            button.style.display = "";
                        } else {
                            var new_str = num_failed_case + " Failed Test Case";
                            document.getElementById("num_fail").innerHTML=new_str;
                            if (num_failed_case == 0){
                                button.style.display = "none";
                            } else if (num_failed_case == 1){
                                button.style.display = "";
                            }
                        }
                    }
                    if (document.getElementById("num_pass")){
                        var new_str = num_passed_case + " Passed Test Cases";

                        if (num_passed_case > 1){
                            var new_str = num_passed_case + " Passed Test Cases";
                            document.getElementById("num_pass").innerHTML=new_str;
                        } else {
                            var new_str = num_passed_case + " Passed Test Case";
                            document.getElementById("num_pass").innerHTML=new_str;
                        }
                    }
                }

            </script>
            """ % ("num_failed_case = Math.floor(num_failed_case / 2);" if rerun_flag else "")

            java_script_code_for_filter

            java_script_copy_failed_testcases = """
            <script>
                function copyFailedTestCase(){
                    var button = document.getElementById("failed_testcase_names");
                    button.style.opacity = "0"; // Set opacity to 0 to make the button invisible
                    document.getElementById("copy_status_info").innerHTML = "<font color=#DC3912>Copied</font>";
                    
                    setTimeout(function(){
                        document.getElementById("copy_status_info").innerHTML = "";
                        button.style.opacity = "1"; // Reset opacity to make the button visible again
                    }, 1000);
                    
                    // 获取页面中所有 class="all_failed_case" 的 <tr> 元素
                    var trElements = document.querySelectorAll('tr.all_failed_case');
                    
                    // 准备一个数组来存放满足条件的faield test case name
                    var selectedFailedCaseNames = [];
                    
                    // 遍历所有选取的 <tr> 元素
                    trElements.forEach(function(tr) {
                        // 检查每个 <tr> 的显示状态是否为 'block'
                        // 获取实际应用的样式
                        var computedStyle = window.getComputedStyle(tr);
                        
                        // 检查 'display' 属性是否为 'block' 或者没有明确设置
                        if (computedStyle.display === 'block' || !tr.hasAttribute('style')) {
                            // 获取第二个 <td> 元素
                            var secondTd = tr.children[1]; // 假设 <td> 元素是按顺序的
                            if (secondTd) {
                                // 获取第一个 <a> 标签
                                var firstA = secondTd.querySelector('a');
                                if (firstA) {
                                    // 获取 <a> 标签的文本
                                    var fullText = firstA.textContent.trim();
                                    // 找到左括号 '(' 的位置
                                    var index = fullText.indexOf('(');
                                    // 如果存在左括号，只取左括号之前的文本
                                    if (index !== -1) {
                                        fullText = fullText.substring(0, index).trim();
                                    }
                                    // 替换所有的 '/' 为 '.'
                                    var modifiedText = fullText.replace(/\//g, '.');
                                    // 添加到数组中
                                    selectedFailedCaseNames.push(modifiedText);
                                }
                            }
                        }
                    });
                    
                    selectedFailedCaseNames = Array.from(new Set(selectedFailedCaseNames));
                    
                    // Join the array into a single string with commas separating the values
                    const textToCopy = selectedFailedCaseNames.join(' ');
                    
                    // Using the Clipboard API to copy text
                    navigator.clipboard.writeText(textToCopy).then(function() {
                        // Success action, e.g., showing a message
                        document.getElementById('copy_status_info').textContent = 'Copied!';
                    }, function(err) {
                        // Error action
                        document.getElementById('copy_status_info').textContent = 'Failed to copy!';
                    });
                    
                }
            </script>
            """

            js_code_str = """
            <html>
                <head>
                    <title>Automation Test Report</title>
                    %s
                    %s
                    %s
                </head>
                
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/clipboard.js/1.5.12/clipboard.min.js"></script>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5.0.2/dist/echarts.min.js"></script>
                
                <style>
                .screenshot-img {
                    width: 100%%; /* Ensure it takes the full width of its parent */
                    max-width: none; /* Remove any max-width restrictions */
                }
    
                .tooltip-inner {
                  max-width: 280px;
                  color: whitesmoke;
                  text-align: right;
                  text-decoration: none;
                  background-color: darkcyan;
                  border-radius: 4px;
                }
                .tooltip-arrow {
                  position: absolute;
                  width: 0;
                  height: 0;
                  border-color: darkcyan;
                  border-style: solid;
                }
                </style>
                
            """ % (
                css,
                java_script_code_for_filter,
                java_script_copy_failed_testcases
            )

            report_file_handler.write(js_code_str)

            environment = settings.ENVIRONMENT

            str_top_table = """
            <body>
            <table align='center' width='1120px;'>
                <tr>
                    <td>
                        <div id='chart_div' style="min-width: 621px; height: 360px; migin: 10 auto"></div>
                    </td>
                    <td>
                        <table border='0' class="table table-hover">
                            <tr style='background-color: whitesmoke; min-width: 621px;'>
                                <th>Start Time</th>
                                <td align="center">%s</td>
                            </tr>
                            <tr>
                                <th>Duration(s)</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Total Executed</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Passed</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Failed</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Environment</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Threads</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>OS</th>
                                <td align='center'>%s</td>
                            </tr>
                            <tr>
                                <th>Framework</th>
                                <td align='center'><a target="_blank" style="color: #3366C5;" href="https://plugins.jetbrains.com/plugin/21600-linktest/versions">linktest %s</a></td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            """ % (
                start_time.strftime("%Y-%m-%d %H:%M:%S"),
                execution_time,
                len(passed_cases) + failed_cases_count,
                len(passed_cases),
                failed_cases_count,
                environment,
                settings.QUEUE_SIZE,
                platform_info,
                linktest.__version__
            )

            report_file_handler.write(str_top_table)

            all_testcases = passed_cases + failed_cases
            all_testcases_package = set()
            if len(all_testcases) > 0:
                all_testcases_package = set()
                tc_map_tag = dict()
                tc_map_tag["tests"] = []

                # begin to fetch all the testcase's tags(according to the testcase' package)
                for testcase in all_testcases:
                    testcase.testcase_filter_tag = "~"
                    testcase_filter_tag = testcase.__module__[0:testcase.__module__.rfind(".")]
                    map_testcases_package(all_testcases_package, tc_map_tag, testcase_filter_tag, testcase)

            # generate the drop down list for all the different tags
            html_drop_down_list = """
            <table border='0' align='center' width='1120'>
                <tr>
                    <td width='285'><strong style='color: #555555; font-size: 18;'>Select Package: </strong></td>
                    <td>
            """

            report_file_handler.write(html_drop_down_list)

            all_testcases_package_list = []
            for testcase in all_testcases_package:
                all_testcases_package_list.append(testcase)

            all_testcases_package_list.sort()
            report_file_handler.write("<select class='form-select' style='margin-left: -128px; overflow: hidden; text-overflow: ellipsis; width: 780;' id=\"testcase_tag\" onchange=\"changeTag()\">")
            for testcase in all_testcases_package_list:
                report_file_handler.write("<option value='%s'>" % testcase)
                report_file_handler.write("%s" % testcase)
                report_file_handler.write("</option>")
            report_file_handler.write("</select>")
            report_file_handler.write("</td>")

            if create_global_data_list_flag:
                view_global_data_str = """<td style="padding-left: 10px; padding-right: 10px;"> <!-- Adjust padding as needed -->
                                            <a target='_blank' role='button' href='%s' 
                                            style="background-color: #3366C5;
                                            color: white; 
                                            border: none; 
                                            border-radius: 5px; 
                                            padding: 5px 8px;
                                            font-size: 16px; 
                                            font-weight: 500;
                                            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2); 
                                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                                            transition: background-color 0.3s, box-shadow 0.3s; 
                                            cursor: pointer;
                                            outline: none;">View Global Data</a>
                                        </td>""" % (output_folder + os.sep + "global_data_list.py")
                report_file_handler.write(view_global_data_str)

            if len(failed_cases) > 0:
                str_failed_testcase_names = ""

                for failed_testcase in failed_cases:
                    str_failed_testcase_names += failed_testcase.__class__.__name__ + " "

            report_file_handler.write("</tr></table>")
            report_file_handler.write("<br>")

            if len(failed_cases) > 0:
                str_failed_testcases = """
                                <button style="
                                    background-color: #DC3912;
                                    color: white; 
                                    border: none; 
                                    border-radius: 5px; 
                                    padding: 2px 6px;
                                    font-size: 14px; 
                                    font-weight: 500;
                                    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2); 
                                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                                    transition: background-color 0.3s, box-shadow 0.3s; 
                                    cursor: pointer;
                                    outline: none;
                                "
                                id="failed_testcase_names" class='failed_testcase_names'
                                title="Click to copy the names of all failed test cases to the clipboard"
                                 data-clipboard-text="%s" onclick="copyFailedTestCase()">
                                    <font color='white'>Copy Failures</font>
                                </button>
                                <font id='copy_status_info' style='margin-left: -100px;'></font>
                                <script>
                                    new Clipboard('.failed_testcase_names');
                                </script>
                                """ % str_failed_testcase_names

                failed_testcase_table = """
                <table align='center'>
                <tr><td>
                <table class='table table-hover' border='0'>
                    <tr id='all_failed_test_cases' style='color:black; background-color: whitesmoke;'>
                        <th width='80'>
                               CaseID
                        </th>
                    
                        <th width='880' style='color: #DC3912;'>
                                <font id='num_fail'>%s &nbsp; Failed %s</font>
                                <font style='margin-left: 18px;'>%s</font>
                        </th>
                        <th width='160'>
                            Duration(Seconds)
                        </th>
                        
                    </tr>
                """ % (
                    failed_cases_count,
                    "Test Cases" if failed_cases_count > 1 else "Test Case",
                    str_failed_testcases
                )

                report_file_handler.write(failed_testcase_table)

                sorted_failed_cases = []

                if settings.RERUN_FLAG:
                    failed_cases_dict = {}
                    for tc in failed_cases:
                        module_name = tc.__module__.replace(".", "_") + os.sep + tc.__class__.__name__
                        if tc.rerun_tag == 1:
                            module_name = module_name + "_rerun"
                        failed_cases_dict[module_name] = tc
                    od = collections.OrderedDict(sorted(failed_cases_dict.items()))
                    for k in od.keys():
                        sorted_failed_cases.append(od[k])
                else:
                    sorted_failed_cases = failed_cases

                for index, failed_testcase in enumerate(sorted_failed_cases):
                    # screenshot_exists = isinstance(failed_testcase, UITestCase) and getattr(failed_testcase,
                    #                                                                         'screenshot', None)
                    # screenshot_id = f"screenshot_{index}"

                    module_name = failed_testcase.__module__.replace(".", "_") + os.sep + failed_testcase.__class__.__name__
                    module_name_display = failed_testcase.__module__.replace("tests.", "&#x0009;")
                    module_name_display += os.sep + failed_testcase.__class__.__name__
                    report_file_handler.write(
                        "<tr class='all_failed_case' name=%s>" % failed_testcase.testcase_filter_tag)

                    report_file_handler.write(
                        "<td width='80' align='center' style='word-break:break-all;no-wrap:no-wrap'>")
                    report_file_handler.write("%s" % ('-' if getattr(failed_testcase, "testcase_id", "None") == None else getattr(failed_testcase, "testcase_id")))
                    report_file_handler.write("</font></td>")

                    testcase_information = """
                        <td width='880' style='word-break:break-all'>
                        <a  href='%s'>
                            <font color='#333'>
                                %s
                            </font>
                        </a>
                        """ % (
                        module_name,
                        module_name_display
                    )

                    report_file_handler.write(testcase_information)

                    try:
                        report_file_handler.write(
                            " <a title='%s'> (" % 'Please see the execution logs for more details' + failed_testcase.exception_info + ") </a>")
                    except BaseException:
                        print(traceback.format_exc())

                    if failed_testcase.rerun_tag == 0:
                        try:
                            report_file_handler.write(
                                "&nbsp; &nbsp; <strong style='color: #555555; '>Log Files: </strong><a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='left' title='View Detailed Log' href='%s'><font style='color: red'> &nbsp;[TXT </font></a>" %
                                failed_testcase.log_file_path)
                            report_file_handler.write(
                                " | &nbsp; <a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='right' title='View Detailed Log' href='%s'><font style='color: red'> HTML]</font></a>" %
                                failed_testcase.log_file_path.replace("test.log", "test.html"))
                        except BaseException:
                            print(traceback.format_exc())

                    elif failed_testcase.rerun_tag == 1:
                        try:
                            report_file_handler.write(
                                "&nbsp; &nbsp; <strong style='color: darkorange; '>rerun Log Files: </strong><a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='left' title='View Detailed rerun Log' href='%s'> <font color='#DC3912'> &nbsp; [TXT </font> </a>" %
                                failed_testcase.log_file_path)
                            report_file_handler.write(
                                " | &nbsp; <a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='right' title='View Detailed rerun Log' href='%s'> <font color='#DC3912'> HTML]</font> </a>" %
                                failed_testcase.log_file_path.replace("test.rerun.log", "test.rerun.html"))
                        except BaseException:
                            print(traceback.format_exc())

                    report_file_handler.write("</td>")

                    report_file_handler.write("<td width='160' align='center' ><font>")
                    if not hasattr(failed_testcase, "execution_time"):
                        failed_testcase.execution_time = ""

                    report_file_handler.write("%s" % failed_testcase.execution_time)
                    report_file_handler.write("</font></td></tr>")

                report_file_handler.write("</table></td></tr></table>")

            if len(passed_cases) > 0:
                passed_testcase_table = """
                <table align='center'>
                <tr><td>

                <table class='table table-hover' border='0'>
                    <tr id='all_passed_test_cases' style='color:balck; background-color: whitesmoke;'>
                        <th width='80'>
                            CaseID
                        </th>
                
                        <th width='880' style='color: #3366C5;'>
                            <font id='num_pass'>%s &nbsp;Passed %s</font>
                        </th>
                        
                        <th width='160'>
                            Duration(Seconds)
                        </th>
                        
                    </tr>
                """ % (
                    len(passed_cases),
                    "Test Cases" if len(passed_cases) > 1 else "Test Case"
                )
                report_file_handler.write(passed_testcase_table)

                for passed_testcase in passed_cases:
                    module_name = passed_testcase.__module__.replace(".", "_") + os.sep + passed_testcase.__class__.__name__
                    module_name_display = passed_testcase.__module__.replace("tests.", "&#x0009;")
                    module_name_display += os.sep + passed_testcase.__class__.__name__

                    report_file_handler.write(
                        "<tr class='all_passed_case' name=%s>" % getattr(passed_testcase,
                                                                                      "testcase_filter_tag",
                                                                                      "None"))

                    report_file_handler.write("<td width='80' align='center' >")
                    report_file_handler.write("%s" % ('-' if getattr(passed_testcase, "testcase_id", "None") == None else getattr(passed_testcase, "testcase_id")))
                    report_file_handler.write("</font></td>")

                    report_file_handler.write("<td width='880' style='word-break:break-all'>")
                    report_file_handler.write("<a title='Click to see the log & screenshot' href='")
                    report_file_handler.write(module_name)
                    report_file_handler.write(
                        "'><font color='%s'>" % (
                            "#333" if passed_testcase.rerun_tag == 0 else "green"))
                    report_file_handler.write(module_name_display)

                    # show re-run got passed in report
                    if passed_testcase.rerun_tag == 1:
                        report_file_handler.write("<font color='orange'> - rerun Passed</font>")

                    if passed_testcase in error_cases:
                        report_file_handler.write("<font color='orange'> - Miss Attribute</font>")

                    report_file_handler.write("</font>")
                    report_file_handler.write("</font></a>")

                    try:
                        if passed_testcase.rerun_tag == 0:
                            report_file_handler.write(
                                "&nbsp; &nbsp; <strong style='color: #555555; '>Log Files: </strong><a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='left' title='View Detailed Log' href='%s'>   <font color='#3366C5'>&nbsp; [TXT </font> </a>" %
                                passed_testcase.log_file_path)
                            report_file_handler.write(
                                " |&nbsp; <a target='_blank' style='white-space: nowrap;' data-bs-toggle='tooltip' data-bs-placement='right' title='View Detailed Log' href='%s'>   <font color='#3366C5'> HTML]</font> </a>" %
                                passed_testcase.log_file_path.replace("test.log", "test.html"))
                    except BaseException:
                        print(traceback.format_exc())

                    try:
                        if passed_testcase.rerun_tag == 1:
                            report_file_handler.write(
                                "&nbsp; &nbsp; <strong style='color: #555555; '>Log Files: </strong><a title='Log' href='%s'> &nbsp;[TXT </a>" %
                                passed_testcase.log_file_path.replace("test.rerun.log", "test.log"))
                            report_file_handler.write(
                                " | <a target='_blank' title='HTML Log' href='%s'> HTML] </a>" %
                                passed_testcase.log_file_path.replace("test.rerun.log", "test.html"))

                            report_file_handler.write(
                                "&nbsp; &nbsp; <strong style='color: #555555; '>rerun Log Files: </strong><a title='rerun_Log' href='%s'> &nbsp;[TXT </a>" %
                                passed_testcase.log_file_path)
                            report_file_handler.write(
                                " | <a target='_blank' title='rerun_Log' href='%s'> HTML] </a>" %
                                passed_testcase.log_file_path.replace("test.rerun.log", "test.rerun.html"))
                    except BaseException:
                        print(traceback.format_exc())

                    report_file_handler.write("</td>")

                    report_file_handler.write("<td width='160' align='center'>")
                    report_file_handler.write("<font color='#333'>")

                    if not hasattr(passed_testcase, "execution_time"):
                        passed_testcase.execution_time = ""

                    report_file_handler.write("%s" % passed_testcase.execution_time)
                    report_file_handler.write("</font></td></tr>")

                report_file_handler.write("</table></td></tr></table>")

            report_file_handler.write("<br><br>")

            echarts_str = """
            <script>
                    var chartDom = document.getElementById('chart_div');
                   
                    var myChart = echarts.init(chartDom);
                    var option = {
                        title: {
                            text: 'Automation Test Report',
                            left: 'center'
                        },
                        tooltip: {
                             trigger: 'item',
                             formatter: "{a} <br/>{b} : {c} ({d}%%)",
                             axisPointer: {
                               type: 'none'
                             }
                        },
                        legend: {
                         orient: 'vertical',
                         x: 'left',
                         data: ['Passed', 'Failed']
                        },
                        series: [
                            {
                                name: '',
                                type: 'pie',
                                radius: '65%%',
                                data: [
                                    {
                                        value: %s, 
                                        name: 'Passed',
                                        itemStyle: {
                                            color: "#3366C5"
                                        }
                                    },
                                    {
                                        value: %s, 
                                        name: 'Failed', 
                                        itemStyle: {
                                            color: "#DC3912"
                                        }
                                    }
                                ],
                                itemStyle: {
                                 normal: {
                                   label: {
                                     show: true,
                                     formatter: '{b}: {c}  ({d}%%)'
                                   },
                                   labelLine: {
                                     show: true
                                   }
                                 }
                               }
                                
                                
                            }
                        ]
                    };

                    option && myChart.setOption(option);
                    
                    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
                    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                      return new bootstrap.Tooltip(tooltipTriggerEl)
                    })
                    
            </script>
                                
                   """ % (len(passed_cases), failed_cases_count)

            report_file_handler.write(echarts_str)
            report_file_handler.write("</div></body></html>")
