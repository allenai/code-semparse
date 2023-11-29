# read "datamodel.py" file and rewrite it as "python_datamodel.py" file
# (1) skip functions with "@skip" decorator
# (2) skip "__main__" function


START_LINE = "# START"

if __name__ == "__main__":
    with open("datamodel.py") as fp:
        lines = fp.readlines()

    python_datamodel_lines = []

    skip_current_function_or_class = False
    started = False

    for i, line in enumerate(lines):
        if not started:
            if line.startswith(START_LINE):
                started = True
            continue

        if "@dataclass" in line:
            continue
        if line.strip().startswith("_"):
            continue

        if "@skip" in line:
            skip_current_function_or_class = True
            continue

        if "def " in line or "class " in line or "..." in line:
            should_skip = "@skip" in lines[i - 1] or "@skip" in lines[i - 2]
            should_skip = should_skip or "def func_repr" in line
            should_skip = should_skip or "def _" in line

            if should_skip:
                skip_current_function_or_class = True
                continue
            else:
                skip_current_function_or_class = False
        if skip_current_function_or_class:
            continue
        if line.startswith("if __name__ == \"__main__\":"):
            break
        python_datamodel_lines.append(line)

    print("".join(python_datamodel_lines))