from lxml import etree
import os

def export_fcpxml(video_path, segments, output_path):
    fps = 30
    video_name = os.path.basename(video_path)
    
    # Préparation du chemin propre
    abs_path = os.path.abspath(video_path).replace("\\", "/")
    if not abs_path.startswith("/"):
        abs_path = "/" + abs_path
    path_url = "file://localhost" + abs_path.replace(" ", "%20")
    
    # Calcul des durées
    total_duration_frames = int((segments[-1][1] / 1000) * fps) + 300 if segments else 3000
    seq_duration = sum(int((e / 1000) * fps) - int((s / 1000) * fps) for s, e in segments)

    xmeml = etree.Element("xmeml", version="4")
    
    # 1. Envelopper la séquence dans un projet
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
    
    # --- CONFIGURATION VIDÉO ---
    video = etree.SubElement(media, "video")
    v_format = etree.SubElement(video, "format")
    v_sample = etree.SubElement(v_format, "samplecharacteristics")
    v_rate = etree.SubElement(v_sample, "rate")
    etree.SubElement(v_rate, "timebase").text = str(fps)
    etree.SubElement(v_rate, "ntsc").text = "FALSE"
    etree.SubElement(v_sample, "width").text = "1920"
    etree.SubElement(v_sample, "height").text = "1080"
    etree.SubElement(v_sample, "anamorphic").text = "FALSE"
    etree.SubElement(v_sample, "pixelaspectratio").text = "square"
    
    v_track = etree.SubElement(video, "track")

    # --- CONFIGURATION AUDIO (Nouveau) ---
    audio = etree.SubElement(media, "audio")
    a_format = etree.SubElement(audio, "format")
    a_sample = etree.SubElement(a_format, "samplecharacteristics")
    etree.SubElement(a_sample, "depth").text = "16"
    etree.SubElement(a_sample, "samplerate").text = "48000"
    
    # Création de deux pistes pour la stéréo (Gauche / Droite)
    a_track1 = etree.SubElement(audio, "track")
    a_track2 = etree.SubElement(audio, "track")

    current_timeline_frame = 0

    # Fonction utilitaire pour lier les clips A/V dans Premiere
    def add_links(parent_element, v_id, a1_id, a2_id):
        links_data = [(v_id, "video", "1"), (a1_id, "audio", "1"), (a2_id, "audio", "2")]
        for link_id, media_type, track_index in links_data:
            link = etree.SubElement(parent_element, "link")
            etree.SubElement(link, "linkclipref").text = link_id
            etree.SubElement(link, "mediatype").text = media_type
            etree.SubElement(link, "trackindex").text = track_index
            etree.SubElement(link, "clipindex").text = "1"

    for i, (start_ms, end_ms) in enumerate(segments):
        start_frame = int((start_ms / 1000) * fps)
        end_frame = int((end_ms / 1000) * fps)
        duration_frames = end_frame - start_frame
        
        if duration_frames <= 0:
            continue

        # IDs uniques pour lier les clips entre eux
        v_clip_id = f"vclip-{i}"
        a1_clip_id = f"aclip-{i}-1"
        a2_clip_id = f"aclip-{i}-2"

        # --- CLIPITEM VIDÉO ---
        v_clipitem = etree.SubElement(v_track, "clipitem", id=v_clip_id)
        etree.SubElement(v_clipitem, "name").text = video_name
        etree.SubElement(v_clipitem, "duration").text = str(total_duration_frames)
        
        c_rate = etree.SubElement(v_clipitem, "rate")
        etree.SubElement(c_rate, "timebase").text = str(fps)
        etree.SubElement(c_rate, "ntsc").text = "FALSE"
        
        etree.SubElement(v_clipitem, "start").text = str(current_timeline_frame)
        etree.SubElement(v_clipitem, "end").text = str(current_timeline_frame + duration_frames)
        etree.SubElement(v_clipitem, "in").text = str(start_frame)
        etree.SubElement(v_clipitem, "out").text = str(end_frame)
        
        if i == 0:
            # Le premier fichier déclare les médias globaux (Vidéo ET Audio)
            file_node = etree.SubElement(v_clipitem, "file", id="file-1")
            etree.SubElement(file_node, "name").text = video_name
            etree.SubElement(file_node, "pathurl").text = path_url
            
            f_rate = etree.SubElement(file_node, "rate")
            etree.SubElement(f_rate, "timebase").text = str(fps)
            etree.SubElement(f_rate, "ntsc").text = "FALSE"
            etree.SubElement(file_node, "duration").text = str(total_duration_frames)
            
            f_media = etree.SubElement(file_node, "media")
            
            # Caractéristiques vidéo du fichier
            f_video = etree.SubElement(f_media, "video")
            f_sample = etree.SubElement(f_video, "samplecharacteristics")
            fs_rate = etree.SubElement(f_sample, "rate")
            etree.SubElement(fs_rate, "timebase").text = str(fps)
            etree.SubElement(fs_rate, "ntsc").text = "FALSE"
            etree.SubElement(f_sample, "width").text = "1920"
            etree.SubElement(f_sample, "height").text = "1080"
            etree.SubElement(f_sample, "anamorphic").text = "FALSE"
            etree.SubElement(f_sample, "pixelaspectratio").text = "square"
            
            # Caractéristiques audio du fichier (Nouveau)
            f_audio = etree.SubElement(f_media, "audio")
            fa_sample = etree.SubElement(f_audio, "samplecharacteristics")
            etree.SubElement(fa_sample, "depth").text = "16"
            etree.SubElement(fa_sample, "samplerate").text = "48000"
            etree.SubElement(f_audio, "channelcount").text = "2"
        else:
            etree.SubElement(v_clipitem, "file", id="file-1")

        # Liaison A/V pour la vidéo
        add_links(v_clipitem, v_clip_id, a1_clip_id, a2_clip_id)

        # --- CLIPITEMS AUDIO ---
        # On boucle pour créer le clip sur la piste 1, puis sur la piste 2
        for track_idx, a_track, a_clip_id in [(1, a_track1, a1_clip_id), (2, a_track2, a2_clip_id)]:
            a_clipitem = etree.SubElement(a_track, "clipitem", id=a_clip_id)
            etree.SubElement(a_clipitem, "name").text = video_name
            etree.SubElement(a_clipitem, "duration").text = str(total_duration_frames)
            
            ca_rate = etree.SubElement(a_clipitem, "rate")
            etree.SubElement(ca_rate, "timebase").text = str(fps)
            etree.SubElement(ca_rate, "ntsc").text = "FALSE"
            
            etree.SubElement(a_clipitem, "start").text = str(current_timeline_frame)
            etree.SubElement(a_clipitem, "end").text = str(current_timeline_frame + duration_frames)
            etree.SubElement(a_clipitem, "in").text = str(start_frame)
            etree.SubElement(a_clipitem, "out").text = str(end_frame)
            
            # Référence au MÊME fichier source
            etree.SubElement(a_clipitem, "file", id="file-1")
            
            # Mapping de la piste source (Canal 1 du MP4 vers Piste 1, Canal 2 vers Piste 2)
            sourcetrack = etree.SubElement(a_clipitem, "sourcetrack")
            etree.SubElement(sourcetrack, "mediatype").text = "audio"
            etree.SubElement(sourcetrack, "trackindex").text = str(track_idx)
            
            # Liaison A/V pour l'audio
            add_links(a_clipitem, v_clip_id, a1_clip_id, a2_clip_id)

        current_timeline_frame += duration_frames

    tree = etree.ElementTree(xmeml)
    with open(output_path, "wb") as f:
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8", doctype='<!DOCTYPE xmeml>')