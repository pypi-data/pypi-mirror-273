import jinja2
import os


def indent(d, width=10, result="", newline=True):
    if isinstance(d, str) or isinstance(d, bool) or isinstance(d, int):
        if isinstance(d, str):
            lines = d.split("\n")
            first = True
            for line in lines:
                if first:
                    result += line + '\n'
                    first = False
                else:
                    result += " " * width + line + "\n"
        else:
            result += " " * width + str(d)
    elif isinstance(d, dict):
        if newline:
            result += "\n"
        first = True
        for key, value in d.items():
            if newline or not first:
                result += " " * width + str(key)
            else:
                result += str(key)
            if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int):
                result += ": " + str(value) + "\n"
            else:
                result += ": " + indent(value, width+2, '')
                result += "\n"
            first = False
    elif isinstance(d, list):
        if newline:
            result += "\n"
        if isinstance(d[0], str) or isinstance(d[0], bool) or isinstance(d[0], int):
            result += ' ' * width
            result += "- " + d[0]
        else:
            result += ' ' * width
            result += "- "
            result += indent(d[0], width+2, '', newline=False)
        for item in d[1:]:
            result += indent(item, width+2, '')
    if result.endswith("\n"):
        result = result[0:-1]
    return result


class Jinja2Processor:

    def process(self, file_path, parameters, output_path):
        # 打开文件
        # 创建Jinja环境并添加自定义过滤器
        file_dir = os.path.dirname(file_path)
        file_name = os.path.split(file_path)[-1]
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(file_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )
        env.filters['indent'] = indent

        template = env.get_template(file_name)
        str = template.render(parameters)
        with open(output_path, "w") as f:
            f.write(str)
