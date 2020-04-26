import os
from PIL import Image

print("Création des images en cours")
for image in os.listdir():
    if os.path.splitext(image)[-1] == ".png":
        img = Image.open(image)

        data = list(img.getdata())

        for i, (r, g, b, a) in enumerate(data):
            if a != 255:
                data[i] = (0, 75, 20, 255)

        img.putdata(data)
        img = img.resize((88, 128))
        img.save(os.path.splitext(image)[0] + ".gif")
print("Terminé !")
