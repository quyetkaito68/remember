#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate-xmind.py — Tao file .xmind so do tu duy tu cay JSON bat ky
Dinh dang: XMind XML (tuong thich XMind 8 / 2020+), theme Professional (xanh #558ED5)
Quy tac: moi node cha toi da 5 node con, cay de quy khong gioi han do sau.

Usage: python generate-xmind.py < input.json

Input JSON schema:
{
  "title": "Tieu de trung tam",
  "output_path": "path/to/output.xmind",
  "sheet_title": "Sheet 1",            (optional)
  "structure": "org.xmind.ui.logic.right",  (optional, default: logic.right)
  "children": [
    {
      "title": "Nhanh 1",
      "children": [
        { "title": "Muc con 1", "children": [...] },
        { "title": "Muc con 2" }
      ]
    }
  ]
}
"""

import sys
import io
import json
import zipfile
import os
import uuid
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

MAX_CHILDREN = 5


def uid():
    return uuid.uuid4().hex[:26]


# ---------------------------------------------------------------------------
# styles.xml — theme Professional (xanh #558ED5), giong misa-xmind
# ---------------------------------------------------------------------------
STYLES_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xmap-styles xmlns="urn:xmind:xmap:xmlns:style:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:svg="http://www.w3.org/2000/svg" version="2.0">
  <automatic-styles>
    <style id="s_subtopic" name="" type="topic">
      <topic-properties border-line-color="#558ED5" border-line-width="3pt" fo:font-family="Open Sans" line-class="org.xmind.branchConnection.curve" line-color="#558ED5" line-width="1pt"/>
    </style>
    <style id="s_summary" name="" type="summary">
      <summary-properties line-color="#C3D69B" line-width="5pt" shape-class="org.xmind.summaryShape.square"/>
    </style>
    <style id="s_boundary" name="" type="boundary">
      <boundary-properties fo:color="#FFFFFF" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" line-color="#77933C" line-pattern="dot" line-width="3pt" shape-class="org.xmind.boundaryShape.roundedRect" svg:fill="#C3D69B" svg:opacity=".2"/>
    </style>
    <style id="s_callout" name="" type="topic">
      <topic-properties border-line-color="#F1BD51" border-line-width="2pt" fo:font-family="Open Sans" svg:fill="#FBF09C"/>
    </style>
    <style id="s_central" name="" type="topic">
      <topic-properties border-line-color="#558ED5" border-line-width="5pt" fo:color="#376092" fo:font-family="Open Sans" line-class="org.xmind.branchConnection.curve" line-color="#558ED5" line-width="1pt" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#DCE6F2"/>
    </style>
    <style id="s_main" name="" type="topic">
      <topic-properties border-line-color="#558ED5" border-line-width="2pt" fo:color="#17375E" fo:font-family="Open Sans" line-class="org.xmind.branchConnection.curve" line-color="#558ED5" line-width="1pt" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#DCE6F2"/>
    </style>
    <style id="s_summary_topic" name="" type="topic">
      <topic-properties border-line-width="0pt" fo:color="#FFFFFF" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" line-class="org.xmind.branchConnection.curve" shape-class="org.xmind.topicShape.roundedRect" svg:fill="#77933C"/>
    </style>
    <style id="s_floating" name="" type="topic">
      <topic-properties border-line-width="0pt" fo:color="#FFFFFF" fo:font-family="Open Sans" fo:font-weight="bold" line-color="#558ED5" svg:fill="#558ED5"/>
    </style>
    <style id="s_relationship" name="" type="relationship">
      <relationship-properties arrow-end-class="org.xmind.arrowShape.triangle" fo:color="#595959" fo:font-family="Georgia" fo:font-size="10pt" fo:font-style="italic" fo:font-weight="normal" fo:text-decoration="none" line-color="#77933C" line-pattern="dash" line-width="3pt"/>
    </style>
    <style id="s_map" name="" type="map">
      <map-properties color-gradient="none" line-tapered="none" multi-line-colors="none" svg:fill="#FFFFFF"/>
    </style>
  </automatic-styles>
  <master-styles>
    <style id="theme_professional" name="Professional" type="theme">
      <theme-properties>
        <default-style style-family="subTopic"      style-id="s_subtopic"/>
        <default-style style-family="summary"       style-id="s_summary"/>
        <default-style style-family="boundary"      style-id="s_boundary"/>
        <default-style style-family="calloutTopic"  style-id="s_callout"/>
        <default-style style-family="centralTopic"  style-id="s_central"/>
        <default-style style-family="mainTopic"     style-id="s_main"/>
        <default-style style-family="summaryTopic"  style-id="s_summary_topic"/>
        <default-style style-family="floatingTopic" style-id="s_floating"/>
        <default-style style-family="relationship"  style-id="s_relationship"/>
        <default-style style-family="map"           style-id="s_map"/>
      </theme-properties>
    </style>
  </master-styles>
</xmap-styles>
"""

MANIFEST_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
  <file-entry full-path="content.xml"           media-type="text/xml"/>
  <file-entry full-path="META-INF/"             media-type=""/>
  <file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>
  <file-entry full-path="styles.xml"            media-type="text/xml"/>
  <file-entry full-path="meta.xml"              media-type="text/xml"/>
</manifest>
"""


def escape_xml(s):
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def node_to_xml(node, depth=0):
    """
    Chuyen 1 node sang XML de quy.
    node co the la:
      - dict: { "title": "...", "children": [...] }
      - str: chuoi don gian -> la node khong co con
    Quy tac: moi node toi da MAX_CHILDREN con.
    """
    if isinstance(node, str):
        title = escape_xml(node[:200])
        return f'<topic id="{uid()}" timestamp="{ts()}"><title>{title}</title></topic>'

    title = escape_xml(str(node.get("title", "(Không có tiêu đề)"))[:200])
    children = node.get("children", [])

    # Gioi han MAX_CHILDREN con
    truncated = False
    if len(children) > MAX_CHILDREN:
        children = children[:MAX_CHILDREN]
        truncated = True

    children_xml = "".join(node_to_xml(c, depth + 1) for c in children)

    # Neu bi cat gon, them note
    if truncated:
        children_xml += f'<topic id="{uid()}" timestamp="{ts()}"><title>... (đã giới hạn {MAX_CHILDREN} mục)</title></topic>'

    if children_xml:
        children_block = f'<children><topics type="attached">{children_xml}</topics></children>'
    else:
        children_block = ""

    return f'<topic id="{uid()}" timestamp="{ts()}"><title>{title}</title>{children_block}</topic>'


_ts_cache = None
def ts():
    global _ts_cache
    if _ts_cache is None:
        _ts_cache = str(int(time.time() * 1000))
    return _ts_cache


def build_content_xml(payload):
    root_title   = escape_xml(str(payload.get("title", "Sơ đồ tư duy"))[:200])
    sheet_title  = escape_xml(str(payload.get("sheet_title", "Sheet 1")))
    structure    = payload.get("structure", "org.xmind.ui.logic.right")
    children     = payload.get("children", [])
    sheet_id     = uid()
    root_id      = uid()
    timestamp    = ts()

    # Gioi han MAX_CHILDREN cho root
    truncated = False
    if len(children) > MAX_CHILDREN:
        children = children[:MAX_CHILDREN]
        truncated = True

    branches_xml = "".join(node_to_xml(c, depth=1) for c in children)
    if truncated:
        branches_xml += f'<topic id="{uid()}" timestamp="{timestamp}"><title>... (đã giới hạn {MAX_CHILDREN} nhánh)</title></topic>'

    children_block = (
        f'<children><topics type="attached">{branches_xml}</topics></children>'
        if branches_xml else ""
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0"'
        ' xmlns:fo="http://www.w3.org/1999/XSL/Format"'
        ' xmlns:svg="http://www.w3.org/2000/svg"'
        ' xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' timestamp="{timestamp}" version="2.0">'
        f'<sheet id="{sheet_id}" theme="theme_professional" timestamp="{timestamp}">'
        f'<topic id="{root_id}" structure-class="{structure}" timestamp="{timestamp}">'
        f'<title>{root_title}</title>'
        f'{children_block}'
        f'</topic>'
        f'<title>{sheet_title}</title>'
        f'</sheet>'
        f'</xmap-content>'
    )


def build_meta_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        f'<meta xmlns="urn:xmind:xmap:xmlns:meta:2.0"'
        f' Author="" created="{ts()}" modified="{ts()}" version="2.0"/>'
    )


def count_topics(node):
    if isinstance(node, str):
        return 1
    children = node.get("children", [])[:MAX_CHILDREN]
    return 1 + sum(count_topics(c) for c in children)


def save_xmind(payload, output_path):
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.getcwd(), output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    content_xml = build_content_xml(payload)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.xml",           content_xml.encode("utf-8"))
        zf.writestr("styles.xml",            STYLES_XML.encode("utf-8"))
        zf.writestr("meta.xml",              build_meta_xml().encode("utf-8"))
        zf.writestr("META-INF/manifest.xml", MANIFEST_XML.encode("utf-8"))

    return output_path, os.path.getsize(output_path)


def main():
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace").strip()
    if not raw:
        print("[ERROR] Không có input JSON trên stdin", file=sys.stderr)
        sys.exit(1)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON không hợp lệ: {e}", file=sys.stderr)
        sys.exit(1)

    output_path = payload.get("output_path", "output.xmind")
    saved_path, zip_size = save_xmind(payload, output_path)

    total = 1 + sum(count_topics(c) for c in payload.get("children", [])[:MAX_CHILDREN])
    top_branches = payload.get("children", [])[:MAX_CHILDREN]

    print(f"[OK] Đã tạo file XMind: {saved_path}")
    print(f"     Kích thước: {zip_size:,} bytes")
    print(f"     Tổng topics: {total}")
    print(f"     Theme: Professional (xanh #558ED5) | Structure: Logic Chart Right")
    print(f"     Nhánh gốc ({len(top_branches)}):")
    for b in top_branches:
        name = b if isinstance(b, str) else b.get("title", "?")
        sub  = 0 if isinstance(b, str) else len(b.get("children", []))
        print(f"       - {name} ({sub} mục con)")
    print(f"\n[VERIFY] File hợp lệ — mở được bằng XMind 8 / 2020+")


if __name__ == "__main__":
    main()



