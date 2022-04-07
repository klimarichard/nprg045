import os
import re


if __name__ == '__main__':
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1])

    with open(resdir + r'\diary.md', mode='r', encoding='utf-8') as diary:
        diary_lines = diary.readlines()

    # count the time
    time = 0
    for line in diary_lines:
        if '**EWT:**' in line:
            if len(line.split(' ')) > 1:
                if line.split(' ')[1].isdigit():
                    time += int(line.split(' ')[1])
                else:
                    print(f'There was not a valid time value in a line containing **EWT:** '
                          f'(line no. {diary_lines.index(line) + 1}), value: {line.split(" ")[1]}')
            else:
                print(f'No space found in a line containing **EWT:** (line no. {diary_lines.index(line) + 1})')

    # change total time line
    diary_lines[4] = f'**Total working-time:** {time} minutes *({int(time / 60)}:{time % 60} hours)*\n'

    with open(resdir + r'\diary.md', mode='w', encoding='utf-8') as diary:
        diary.writelines(diary_lines)
