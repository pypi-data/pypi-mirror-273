from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
from re import Match

FONT_BLACK = r"\*\*\*(.*?)\*\*\*"
FONT_BOLD = r"\*\*(.*?)\*\*"
FONT_MEDIUM = r"\*(.*?)\*"
FONT_THIN = r"\!\!(.*?)\!\!"
FONT_LIGHT = r"\!(.*?)\!"
FONT_UNDERLINE = r"__(.*?)__"
FONT_ITALIC = r"_(.*?)_"
FONT_LINE_THROUGH = r"--(.*?)--"
FONT_SPOILER = r"\|\|(.*?)\|\|"


def spoiler_text(text: str):
    parent = etree.Element("v-hover")
    parent.set("v-slot", "{ hover }")
    child = etree.SubElement(parent, "span")
    spoiled = "▒" * len(text)
    child.set("v-text", f"hover ? '{text}' : '{spoiled}'")
    return parent


class VuetifyTreeProcessor(Treeprocessor):
    def run(self, root):
        for elem in root:
            if elem.tag == 'h1':
                elem.set('class', 'text-h1')
            elif elem.tag == 'h2':
                elem.set('class', 'text-h2')
            elif elem.tag == 'h3':
                elem.set('class', 'text-h3')
            elif elem.tag == 'h4':
                elem.set('class', 'text-h4')
            elif elem.tag == 'h5':
                elem.set('class', 'text-h5')
            elif elem.tag == 'h6':
                elem.set('class', 'text-h6')
            elif elem.tag == 'p':
                elem.set('class', 'text-body-1')
            elif elem.tag == 'a':
                elem.set('class', 'text-decoration-none')


class VuetifyInlineProcessor(InlineProcessor):
    def handleMatch(self, m: Match, data: str):
        try:
            el = etree.Element("span")
            el.text = m.group(1)
            match = m.group(0).split(m.group(1))[0]
            # Yes this isn't ideal, but it works :)
            if match == "*":
                el.set("class", "font-weight-medium")
            elif match == "**":
                el.set("class", "font-weight-bold")
            elif match == "**":
                el.set("class", "font-weight-black")
            elif match == "***":
                el.set("class", "font-weight-medium")
            elif match == "!":
                el.set("class", "font-weight-light")
            elif match == "!!":
                el.set("class", "font-weight-thin")
            elif match == "_":
                el.set("class", "font-italic")
            elif match == "__":
                el.set("class", "font-decoration-underline")
            elif match == "--":
                el.set("class", "font-decoration-line-through")
            elif match == "||":
                el = spoiler_text(m.group(1))
            return el, m.start(0), m.end(0)
        except ValueError:
            return m.group(0), m.start(0), m.end(0)


class PythonVuetifyMarkdown(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(VuetifyTreeProcessor(md), "pythonvuetifymarkdown", 10)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_BLACK, md), "font-weight-black", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_BOLD, md), "font-weight-bold", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_MEDIUM, md), "font-weight-medium", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_THIN, md), "font-weight-thin", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_LIGHT, md), "font-weight-light", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_UNDERLINE, md), "font-underline", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_ITALIC, md), "font-italic", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_LINE_THROUGH, md), "font-line-through", 175)
        md.inlinePatterns.register(VuetifyInlineProcessor(FONT_SPOILER, md), "font-spoiler", 175)
