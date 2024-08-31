from database.database_types import ServiceType

achievement_list_old = [
    # Video achievements
    {"name": "Music Lover", "description": "Perform 3 conversions from mp4 to mp3", "service": ServiceType.video,
     "image_name": "ada1.png"},
    {"name": "Video Editor", "description": "Edit 5 video files", "service": ServiceType.video,
     "image_name": "ada2.png"},
    {"name": "Director", "description": "Create a movie with at least 10 scenes", "service": ServiceType.video,
     "image_name": "ada3.png"},

    # image_name achievements
    {"name": "Photographer", "description": "Upload 10 images", "service": ServiceType.image,
     "image_name": "leon1.png"},
    {"name": "Image Enhancer", "description": "Enhance the quality of 5 images", "service": ServiceType.image,
     "image_name": "leon2.png"},
    {"name": "Collage Creator", "description": "Create 3 image_name collages", "service": ServiceType.image,
     "image_name": "leon3.png"},

    # Audio achievements
    {"name": "Audiophile", "description": "Upload 20 audio files", "service": ServiceType.audio,
     "image_name": "ashley1.png"},
    {"name": "Audio Mixer", "description": "Mix 5 audio tracks", "service": ServiceType.audio,
     "image_name": "ashley2.png"},
    {"name": "Podcast Creator", "description": "Create a podcast episode", "service": ServiceType.audio,
     "image_name": "ashley3.png"}
]

achievement_list_new = [
    # Video achievements
    {"name": "MP3 Fan", "description": "Convert 3 your video to mp3", "service": ServiceType.video,
     "image_name": "ada1.png", "target": 3},
    {"name": "WAV Devotee", "description": "Convert 5 your video to wav", "service": ServiceType.video,
     "image_name": "ada2.png", "target": 5},
    {"name": "YT Shorts Lover", "description": "Cut 5 videos. YouTube Shorts are waiting for you",
     "service": ServiceType.video,
     "image_name": "ada3.png", "target": 5},

    # image_name achievements
    {"name": "Photographer", "description": "Upload 10 images", "service": ServiceType.image,
     "image_name": "leon1.png", "target": 5},
    {"name": "Image Enhancer", "description": "Enhance the quality of 5 images", "service": ServiceType.image,
     "image_name": "leon2.png", "target": 10},
    {"name": "Collage Creator", "description": "Create 3 image_name collages", "service": ServiceType.image,
     "image_name": "leon3.png", "target": 15},

    # Audio achievements
    {"name": "Audiophile", "description": "Upload 20 audio files", "service": ServiceType.audio,
     "image_name": "ashley1.png", "target": 5},
    {"name": "Audio Mixer", "description": "Mix 5 audio tracks", "service": ServiceType.audio,
     "image_name": "ashley2.png", "target": 10},
    {"name": "Podcast Creator", "description": "Create a podcast episode", "service": ServiceType.audio,
     "image_name": "ashley3.png", "target": 15}
]
