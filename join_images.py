from PIL import Image

def join_images_by_concepto(image_list, concepto):
    image_list = [Image.open(img) for img in image_list]

    # Obtener ancho y alto total
    total_width = sum(img.width for img in image_list)
    max_height = max(img.height for img in image_list)

    # Crear imagen nueva vacía
    new_img = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))

    # Pegar imágenes una al lado de otra
    x_offset = 0
    for img in image_list:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.width

    # Guardar resultado
    new_img.save(f'{concepto}.png')