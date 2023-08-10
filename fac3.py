#!/usr/bin/env python

import os
import os.path
import shutil
import bs4
import click
import frontmatter
import jinja2
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin


def get_title(md, tokens):
    title_tokens = []
    start = False
    for token in tokens:
        if token.type == "heading_open" and token.tag == "h1":
            start = True

        if start:
            title_tokens.append(token)

        if token.type == "heading_close" and token.tag == "h1":
            break

    if not title_tokens:
        return

    title_html = RendererHTML().render(title_tokens, md.options, {})
    return bs4.BeautifulSoup(title_html, "lxml").h1.text


@click.command()
@click.argument("src-dir", type=click.Path(exists=True))
@click.option("-b", "--build-dir", default=".", type=click.Path())
@click.option("-t", "--template-dir", default="_templates", type=click.Path(exists=True))
def main(src_dir, build_dir, template_dir):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        keep_trailing_newline=True,
    )
    md = (
        MarkdownIt("commonmark")
        .enable("table")
        .enable("strikethrough")
        .use(front_matter_plugin)
        .use(footnote_plugin)
    )

    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    for path, dirs, files in os.walk(src_dir):
        dst_path = os.path.normpath(os.path.join(build_dir, os.path.relpath(path, src_dir)))

        for dirname in dirs:
            dir_path = os.path.join(dst_path, dirname)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

        for filename in files:
            src_name = os.path.join(path, filename)
            if not filename.endswith(".md"):
                dst_name = os.path.join(dst_path, filename)
                print(src_name, "=>", dst_name)
                shutil.copyfile(src_name, dst_name)
                continue

            with open(src_name) as f:
                doc = frontmatter.load(f)

            if not doc.get("published", True):
                print(src_name, "ignored")
                continue

            text = env.from_string(doc.content).render(metadata=doc.metadata)
            tokens = md.parse(text)
            if "title" not in doc.metadata:
                doc.metadata["title"] = get_title(md, tokens)

            template = env.get_template(doc.metadata["template"])
            name = os.path.splitext(filename)[0]
            dst_name = os.path.join(dst_path, f"{name}.html")

            print(src_name, "=>", dst_name)
            with open(dst_name, "w") as f:
                f.write(template.render(
                    main=RendererHTML().render(tokens, md.options, {}),
                    metadata=doc.metadata,
                ))


if __name__ == "__main__":
    main()
