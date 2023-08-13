#!/usr/bin/env python

import datetime
import os
import os.path
import shutil
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

import bs4
import click
import frontmatter
import jinja2
import yaml
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin


PORT = 8080


def serve_local(directory):
    class Server(ThreadingHTTPServer):
        def finish_request(self, request, client_address):
            self.RequestHandlerClass(request, client_address, self, directory=directory)

    class SlightlyBetterHttpRequestHandler(SimpleHTTPRequestHandler):
        def send_head(self):
            path = os.path.join(directory, "." + self.path)
            if not os.path.exists(path) and os.path.exists(path + ".html"):
                self.path = self.path + ".html"
            return super().send_head()

    with Server(("", PORT), SlightlyBetterHttpRequestHandler) as httpd:
        try:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


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
    return bs4.BeautifulSoup(title_html, "html.parser").h1.text


def images_to_figures(tokens):
    for i, token in enumerate(tokens):
        if (
            token.type == "inline"
            and token.children
            and token.children[0].type == "image"
        ):
            tokens[i - 1].tag = "figure"
            tokens[i + 1].tag = "figure"
            token.children.extend(
                [
                    Token("figcaption_open", "figcaption", nesting=1),
                    Token(
                        type="text",
                        tag="",
                        nesting=0,
                        level=1,
                        content=token.children[0].children[0].content,
                    ),
                    Token("figcaption_close", "figcaption", nesting=-1),
                ]
            )

    return tokens


def music_links_to_audio_figures(tokens):
    for i, token in enumerate(tokens):
        if (
            token.type == "inline"
            and token.children
            and token.children[0].type == "link_open"
        ):
            href = token.children[0].attrs["href"]
            if os.path.splitext(urlparse(href).path)[1] not in [".mp3", ".wav"]:
                continue

            children = [
                Token("figcaption_open", "figcaption", nesting=1),
                *token.children,
                Token(
                    type="figcaption_close",
                    tag="figcaption",
                    nesting=-1,
                ),
                Token(
                    type="audio_open",
                    tag="audio",
                    nesting=1,
                    attrs={
                        "controls": "controls",
                        "src": href,
                    },
                ),
                *token.children[:3],
                Token("audio_close", "audio", nesting=-1),
            ]

            if i >= 2 and tokens[i - 2].type != "list_item_open":
                tokens[i - 1].tag = "figure"
                tokens[i + 1].tag = "figure"

            else:
                children.insert(0, Token("figure_open", "figure", nesting=1))
                children.append(Token("figure_close", "figure", nesting=-1))

            token.children = children

    return tokens


@click.command()
@click.argument("src-dir", type=click.Path(exists=True))
@click.option("-b", "--build-dir", default=".", type=click.Path())
@click.option("-t", "--template-dir", default="templates", type=click.Path(exists=True))
@click.option("-e", "--env", "vars_file", type=click.Path(exists=True))
@click.option("-s", "--server", default=False, is_flag=True)
def main(src_dir, build_dir, template_dir, vars_file, server):
    today = datetime.datetime.now()
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        keep_trailing_newline=True,
    )
    md = (
        MarkdownIt("commonmark")
        .enable("strikethrough")
        .enable("table")
        .use(anchors_plugin)
        .use(footnote_plugin)
        .use(front_matter_plugin)
        .use(tasklists_plugin)
    )

    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    vars = {}
    if vars_file:
        with open(vars_file) as f:
            vars.update(yaml.load(f.read(), yaml.Loader))

    for path, dirs, files in os.walk(src_dir):
        dst_path = os.path.normpath(
            os.path.join(build_dir, os.path.relpath(path, src_dir))
        )

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

            text = env.from_string(doc.content).render(
                metadata=doc.metadata,
                env=vars,
                today=today,
            )
            tokens = md.parse(text)
            tokens = images_to_figures(tokens)
            tokens = music_links_to_audio_figures(tokens)

            if "title" not in doc.metadata:
                doc.metadata["title"] = get_title(md, tokens)

            template = env.get_template(doc.metadata["template"])
            name = os.path.splitext(filename)[0]
            dst_name = os.path.join(dst_path, name + ".html")

            print(src_name, "=>", dst_name)
            with open(dst_name, "w") as f:
                f.write(
                    template.render(
                        main=RendererHTML().render(tokens, md.options, {}),
                        metadata=doc.metadata,
                        env=vars,
                        today=today,
                    )
                )

    if server:
        serve_local(build_dir)


if __name__ == "__main__":
    main()
