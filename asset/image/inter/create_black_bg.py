from PIL import Image
img = Image.new("RGB", (640, 480), (0, 0, 0))
img.save("black.jpeg", "JPEG")