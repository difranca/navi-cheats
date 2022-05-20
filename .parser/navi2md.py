import pathlib
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Command:
    description: str = ""
    cmd: str = ""


@dataclass
class Topic:
    title: str
    command_list: list[Command]
    description: str = ""


def parse_file(file: str) -> tuple[list[Topic], str]:

    with open(file) as cheat:

        command = None
        topic = None
        topic_list = []
        cheat = cheat.readlines()

        for line in cheat:

            line = line.strip()

            if line.startswith('% '):

                if topic:
                    topic_list.append(topic)

                title = re.sub(r'.+\>\s*', '', line)
                topic = Topic(title, [])

            elif line.startswith('# '):
                command = Command(line.replace('# ', ''))

            elif line.startswith(';; '):
                topic.description = line.replace(';; ', '')

            elif len(line) > 0 and line[0] not in ['#', '@', ';', '$']:
                line = line.replace('<', '{')
                line = line.replace('>', '}')

                if line.startswith('navi fn url::open '):
                    line = line.replace('navi fn url::open ', '')
                    line = line.replace('\'', '')

                command.cmd = line
                topic.command_list.append(command)

        if topic:
            topic_list.append(topic)

    return topic_list, ''.join(cheat)


def _load_md_template() -> str:
    with open('.parser/md.template', 'r') as template:
        lines = template.readlines()
        return ''.join(lines)


def _load_topic_template() -> str:
    with open('.parser/topic.template', 'r') as template:
        lines = template.readlines()
        return ''.join(lines)


def _gen_front_matter(template: str, path: pathlib.Path) -> str:
    path_parts = [part for part in path.parent.parts]
    path_parts.append(path.name.replace('.md', ''))

    keywords = ""
    slug = ""
    for part in path_parts:
        part = part.lower()
        keywords = keywords + f', "{part}"'
        slug = slug + f'/{part}'

    template = template.replace('${KW}', keywords)
    template = template.replace('${SLUG}', slug)

    return template


def _gen_title(template: str, title_topic: Topic) -> str:
    template = template.replace(
        '${TITLE}', title_topic.title.replace('% ', ''))
    template = template.replace('${DESCRIPTION}', title_topic.description)
    return template


def _gen_commands(command_list: list[Command]) -> str:
    commands = [
        f'|**{command.cmd}**|{command.description}|\n' for command in command_list
    ]
    return ''.join(commands)


def _gen_topic_title(topic: Topic) -> str:
    topic_template = _load_topic_template()
    topic_template = topic_template.replace('${TITLE}', topic.title)
    topic_template = topic_template.replace(
        '${DESCRIPTION}', topic.description
    )
    topic_template = topic_template.replace(
        '${COMMANDS}', _gen_commands(topic.command_list)
    )
    return topic_template


def _gen_topics(template: str, topic_list: list[Topic]) -> str:
    topics = ""

    if len(topic_list[0].command_list) > 0:
        topics = topics + _gen_topic_title(Topic('General', '', topic_list[0]))

    if len(topic_list) > 1:
        for topic in topic_list[1:]:
            topics = topics + _gen_topic_title(topic)

    return template.replace('${TOPICS}', topics)


def _gen_cheat(template: str, cheat: str) -> str:
    return template.replace('${NAVI_CHEAT}', cheat)


def gen_content(topic_list: list[Topic], cheat: str, file: str) -> tuple[str, pathlib.Path]:

    md_file = 'cheats/' + file.replace('.cheat', '.md')
    md_path = pathlib.Path(md_file)

    md_content = _load_md_template()

    md_content = _gen_front_matter(md_content, md_path)
    md_content = _gen_title(md_content, topic_list[0])
    md_content = _gen_topics(md_content, topic_list)
    md_content = _gen_cheat(md_content, cheat)

    return md_content, md_path


def write_md(content: str, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as md:
        md.write(content)


if __name__ == '__main__':

    cheat_paths = []
    for path in Path().rglob('*.cheat'):
        cheat_paths.append(str(path))

    for path in cheat_paths:
        topic_list, cheat = parse_file(path)
        md_content, md_path = gen_content(topic_list, cheat, path)
        write_md(md_content, md_path)
