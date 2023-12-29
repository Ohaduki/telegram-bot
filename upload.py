import cloudinary
import cloudinary.uploader
from config import CLOUDINARY_KEY, CLOUDINARY_SECRET

cloudinary.config(
    cloud_name = "denzwvfde",
    api_key = CLOUDINARY_KEY,
    api_secret = CLOUDINARY_SECRET
)

def upload(path, id):
    cloudinary.uploader.upload(path, public_id = id)
    src = cloudinary.CloudinaryImage(id).build_url()
    return src

