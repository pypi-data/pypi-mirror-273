import random

import requests, uuid
from bgeditor.common.utils import cache_file, download_file, upload_file, upload_static_file, upload_file_resource
from bgeditor.dao.FootageHelper import split_videos, zip_video_file, extract_zip_files, make_footage_video
from gbackup import DriverHelper
from moviepy.editor import *
from bgeditor.common.utils import get_dir
import os
class FootageController:
    def put_req_normalize_video(self, vid, arr_split_vids):
        zip_path = zip_video_file(arr_split_vids)
        dh = DriverHelper()
        x = dh.upload_file_auto("moonseo", [zip_path])
        vid['video_normalize']=x[0]
        url = f"https://moonseo.app/api/source/data/update"
        headers = {"platform": "autowin"}
        os.remove(zip_path)
        res = requests.post(url,headers=headers,json=vid).json()
        print(res)
    def get_list_source(self, source_id, duration):
        url=f"https://moonseo.app/api/source/user/footage/{source_id}/{duration}"
        headers={"platform" : "autowin"}
        res=requests.get(url, headers=headers).json()
        arr_list_vid=[]
        if res and res['status']==1:
            for vid in res['data']:
                arr_list_vid.append(self.normalize_vid_source(vid))
            return arr_list_vid
        return None

    def normalize_vid_source(self,vid):
        if not vid['video_normalize']:
            video_path=download_file(vid['download_link'],ext='mp4')
            arr_split_vds=split_videos(video_path)
            self.put_req_normalize_video(vid, arr_split_vds)
            arr_rs=arr_split_vds
        else:
            zip_path = download_file(vid['video_normalize'],ext='zip')
            arr_rs = extract_zip_files(zip_path)
        return arr_rs

    def make_footage_videos(self, source_id, duration):
        arr_list_video= self.get_list_source(source_id, duration)
        if arr_list_video:
            return make_footage_video(arr_list_video)
        return None
    def check_and_remove_bg(self, arr_composite):
       for item in arr_composite:
           if item.size[0]==1920 and item.start==0 and item.duration>500 :
               arr_composite.remove(item)
       return arr_composite

    def create_video_with_effect_composite(self, bg_video, arr_composite):
        vid_intro_bg = VideoFileClip(bg_video)
        vid_intro_bg.set_start(0)
        arr_composite.insert(0, vid_intro_bg)
        tmp_path_composite_intro = os.path.join(get_dir('coolbg_ffmpeg'),
                                                str(uuid.uuid4()) + "-comp-effect-vid.mp4")
        tmp_clip = CompositeVideoClip(arr_composite).subclip(0, vid_intro_bg.duration)
        tmp_clip.write_videofile(tmp_path_composite_intro, bitrate='4M', fps=30, codec='libx264', audio=False)
        return tmp_path_composite_intro
    def make_footage_videos_with_effect(self, source_id, audio_path, arr_composite_intro, arr_composite_no_intro):
        if not arr_composite_intro or len(arr_composite_intro)<1 :
            arr_composite_intro=arr_composite_no_intro
        arr_composite_intro = self.check_and_remove_bg(arr_composite_intro)
        arr_composite_no_intro = self.check_and_remove_bg(arr_composite_no_intro)
        audio_compilation = AudioFileClip(audio_path)
        arr_list_video = self.get_list_source(source_id, audio_compilation.duration)
        video_path_footage=None
        if arr_list_video:
            if len(arr_composite_intro)>0:
                intro_bg = arr_list_video[0][1]
                arr_list_video[0][1]=self.create_video_with_effect_composite(intro_bg, arr_composite_intro)
            if len(arr_composite_no_intro)>0:
                i=1
                while i < len(arr_list_video):
                    if i< 5:
                        arr_list_video[i][0] = self.create_video_with_effect_composite(arr_list_video[i][0],
                                                                                       arr_composite_no_intro)
                        arr_list_video[i][1] = self.create_video_with_effect_composite(arr_list_video[i][1], arr_composite_no_intro)
                        arr_list_video[i][2] = self.create_video_with_effect_composite(arr_list_video[i][2], arr_composite_no_intro)
                    elif random.randint(0, 10)>7:
                        arr_list_video[i][0] = self.create_video_with_effect_composite(arr_list_video[i][0],
                                                                                       arr_composite_no_intro)
                        arr_list_video[i][1] = self.create_video_with_effect_composite(arr_list_video[i][1],
                                                                                       arr_composite_no_intro)
                        arr_list_video[i][2] = self.create_video_with_effect_composite(arr_list_video[i][2],
                                                                                       arr_composite_no_intro)
                    i+=1



            video_path_footage=make_footage_video(arr_list_video)
        audio_compilation.close()
        return video_path_footage


