import os

from jinja2 import Environment, FileSystemLoader


def render_report(cases, test_time, report_path):
    # 计算数据
    total_cases = len(cases)
    passed_cases = len([case for case in cases if case['run_status'] == 200])

    path = os.path.dirname(os.path.abspath(__file__))
    # 加载模板文件
    file_loader = FileSystemLoader(path)
    env = Environment(loader=file_loader)

    # 选择模板
    template = env.get_template('report_template.html')

    # 渲染模板
    output = template.render(cases=cases, test_time=test_time, total_cases=total_cases, passed_cases=passed_cases)

    # 将渲染后的HTML写入到文件
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(output)


# 测试数据
cases = [
    {
        'case_name': 'Test Case 1',
        'case_desc': 'This is a test case.',
        'priority': 'High',
        'mark': 'Login',
        'run_status': 200,
        'run_msg': 'Test passed.'
    },
    {
        'case_name': 'Test Case 2',
        'case_desc': 'This is another test case.',
        'priority': 'Low',
        'mark': 'Signup',
        'run_status': 500,
        'run_msg': 'Test failed.'
    },
]

# 输出报告
# render_report(cases, datetime.now(), 'report.html')
