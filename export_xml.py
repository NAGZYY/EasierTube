from lxml import etree

def ms_to_seconds(ms):
    return round(ms / 1000, 3)

def export_fcp_xml(video_path, segments, output_path):
    fcpxml = etree.Element("fcpxml", version="1.8")
    resources = etree.SubElement(fcpxml, "resources")

    asset = etree.SubElement(
        resources,
        "asset",
        id="r1",
        src=f"file:///{video_path}",
        start="0s",
        hasVideo="1",
        hasAudio="1",
        format="r2"
    )

    format_tag = etree.SubElement(
        resources,
        "format",
        id="r2",
        frameDuration="1/30s",
        width="1920",
        height="1080"
    )

    library = etree.SubElement(fcpxml, "library")
    event = etree.SubElement(library, "event", name="EasierTube")
    project = etree.SubElement(event, "project", name="AutoCut")
    sequence = etree.SubElement(
        project,
        "sequence",
        duration="3600s",
        format="r2"
    )

    spine = etree.SubElement(sequence, "spine")

    offset = 0.0

    for i, (start, end) in enumerate(segments):
        duration = ms_to_seconds(end - start)
        clip = etree.SubElement(
            spine,
            "asset-clip",
            name=f"Clip {i+1}",
            ref="r1",
            offset=f"{round(offset,3)}s",
            start=f"{ms_to_seconds(start)}s",
            duration=f"{duration}s"
        )
        offset += duration

    tree = etree.ElementTree(fcpxml)
    tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")