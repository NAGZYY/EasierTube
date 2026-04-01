from lxml import etree
import os

def export_fcp_xml(video_path, segments, output_path):
    fps = 30
    video_name = os.path.basename(video_path)
    
    # Préparation du chemin propre
    abs_path = os.path.abspath(video_path).replace("\\", "/")
    if not abs_path.startswith("/"):
        abs_path = "/" + abs_path
    path_url = "file://localhost" + abs_path.replace(" ", "%20")
    
    # Calcul de la durée totale du fichier source
    total_duration_frames = int((segments[-1][1] / 1000) * fps) + 300 if segments else 3000
    
    # Calcul de la durée totale de la séquence finale (OBLIGATOIRE POUR PREMIERE)
    seq_duration = sum(int((e / 1000) * fps) - int((s / 1000) * fps) for s, e in segments)

    xmeml = etree.Element("xmeml", version="4")
    
    # 1. Envelopper la séquence dans un projet (Premiere est plus stable ainsi)
    project = etree.SubElement(xmeml, "project")
    etree.SubElement(project, "name").text = "EasierTube Project"
    children = etree.SubElement(project, "children")
    
    sequence = etree.SubElement(children, "sequence", id="sequence-1")
    etree.SubElement(sequence, "name").text = "EasierTube Timeline"
    etree.SubElement(sequence, "duration").text = str(seq_duration)
    
    rate = etree.SubElement(sequence, "rate")
    etree.SubElement(rate, "timebase").text = str(fps)
    etree.SubElement(rate, "ntsc").text = "FALSE"
    
    media = etree.SubElement(sequence, "media")
    video = etree.SubElement(media, "video")
    
    # 2. Caractéristiques complètes de la séquence
    format_node = etree.SubElement(video, "format")
    sample = etree.SubElement(format_node, "samplecharacteristics")
    s_rate = etree.SubElement(sample, "rate")
    etree.SubElement(s_rate, "timebase").text = str(fps)
    etree.SubElement(s_rate, "ntsc").text = "FALSE"
    etree.SubElement(sample, "width").text = "1920"
    etree.SubElement(sample, "height").text = "1080"
    etree.SubElement(sample, "anamorphic").text = "FALSE"
    etree.SubElement(sample, "pixelaspectratio").text = "square"
    
    track = etree.SubElement(video, "track")

    current_timeline_frame = 0

    for i, (start_ms, end_ms) in enumerate(segments):
        start_frame = int((start_ms / 1000) * fps)
        end_frame = int((end_ms / 1000) * fps)
        duration_frames = end_frame - start_frame
        
        if duration_frames <= 0:
            continue

        clipitem = etree.SubElement(track, "clipitem", id=f"clip-{i}")
        etree.SubElement(clipitem, "name").text = video_name
        etree.SubElement(clipitem, "duration").text = str(total_duration_frames)
        
        c_rate = etree.SubElement(clipitem, "rate")
        etree.SubElement(c_rate, "timebase").text = str(fps)
        etree.SubElement(c_rate, "ntsc").text = "FALSE"
        
        etree.SubElement(clipitem, "start").text = str(current_timeline_frame)
        etree.SubElement(clipitem, "end").text = str(current_timeline_frame + duration_frames)
        etree.SubElement(clipitem, "in").text = str(start_frame)
        etree.SubElement(clipitem, "out").text = str(end_frame)
        
        if i == 0:
            # 3. Le premier fichier source doit inclure toutes ses métadonnées média
            file_node = etree.SubElement(clipitem, "file", id="file-1")
            etree.SubElement(file_node, "name").text = video_name
            etree.SubElement(file_node, "pathurl").text = path_url
            
            f_rate = etree.SubElement(file_node, "rate")
            etree.SubElement(f_rate, "timebase").text = str(fps)
            etree.SubElement(f_rate, "ntsc").text = "FALSE"
            etree.SubElement(file_node, "duration").text = str(total_duration_frames)
            
            f_media = etree.SubElement(file_node, "media")
            f_video = etree.SubElement(f_media, "video")
            f_sample = etree.SubElement(f_video, "samplecharacteristics")
            fs_rate = etree.SubElement(f_sample, "rate")
            etree.SubElement(fs_rate, "timebase").text = str(fps)
            etree.SubElement(fs_rate, "ntsc").text = "FALSE"
            etree.SubElement(f_sample, "width").text = "1920"
            etree.SubElement(f_sample, "height").text = "1080"
            etree.SubElement(f_sample, "anamorphic").text = "FALSE"
            etree.SubElement(f_sample, "pixelaspectratio").text = "square"
        else:
            # 4. Référence vide stricte pour les clips suivants
            etree.SubElement(clipitem, "file", id="file-1")

        current_timeline_frame += duration_frames

    tree = etree.ElementTree(xmeml)
    with open(output_path, "wb") as f:
        # Ajout du DOCTYPE pour forcer Premiere à bien l'interpréter
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype='<!DOCTYPE xmeml>')