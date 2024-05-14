# Instalation

**Pypi**
```
pip install bigjpg
```

**GitHub**
```
pip install git+https://github.com/1Marcuth/py.bigjpg.git
```

# Simple use example
```py
from bigjpg import Bigjpg, Styles, Noises, EnlargeValues

bigjpg = Bigjpg("YOUR API TOKEN HERE")

image_info = bigjpg.enlarge(
    style = Styles.Art, # Type of image
    noise = Noises._None, # Noise level to be removed
    enlarge_value = EnlargeValues._4x, # Enlargement value
    image_url = "https://avatars.githubusercontent.com/u/91915075?v=4" # Url of image to be enlarged
)

image_url = image_info.get_url() # Enlarged image url
image_info.download("enlarged_image.png") # Method to download enlarged image

print(image_url)
```