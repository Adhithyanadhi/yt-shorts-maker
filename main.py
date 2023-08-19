import shutil
import os
import time
from data_loader import main as data_loader
from image_scraper import main as image_scraper
from video_maker import main as video_maker
from voice_maker import main as voice_maker
from merge_audio_video import main as merge_audio_video
from video_uploader import main as video_uploader

def main():
    try:
        movie = data_loader.get_content(file_name="movie_summaries.csv")
        topic = movie["title"] + " " + str(movie["release_year"])
        plot = movie["plot"]
        sentences = plot.split(' ')
        plot = ' '.join(sentences[:min(30, len(sentences))])
        downloads = os.path.join(os.getcwd() + "/downloads")
        if os.path.exists(downloads):
            shutil.rmtree(downloads)
        # image_scraper.scrape_image(photos_folder, topic)
        photos_folder = image_scraper.download_image(topic)
        
        video_file_name = f"/Users/adhithyans/Desktop/{topic.replace(' ', '_').lower()}.avi"
        audio_file_name = f"/Users/adhithyans/Desktop/{topic.replace(' ', '_').lower()}.wav"
        shorts_file_name = f"/Users/adhithyans/Desktop/{topic.replace(' ', '_').lower()}_shorts.avi"
        
        video_maker.generate_video(video_name=video_file_name, image_folder=photos_folder)
        voice_maker.generate_voice(text=plot, file_name=audio_file_name)
        voice_maker.check_audio_length(file_name=f"/Users/adhithyans/Desktop/{topic.replace(' ', '_').lower()}.wav")
        merge_audio_video.merge_audio_video(audio_file_name=audio_file_name, video_file_name=video_file_name, file_name=shorts_file_name)
        
        options = {
            "title" : topic + " AI generated Movie Plot", # The video title
            "description" : "This is a test video upload", # The video description
            "tags" : ["#videouploadtest", "#kindlyIgnore", "#EducationPurpose"],
            "categoryId" : "22",
            "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
            "kids" : True, # Specifies if the Video if for kids or not. Defaults to False.
        }
        video_uploader.yt_uploader(shorts_file_name, options=options)
        return True
    except Exception as e:
        print("Exception occured ", e)
        return False
if __name__ == "__main__":
   
    while not main():  time.sleep(10); continue