from pyzjr.core.general import is_numpy, is_tensor, is_pil, is_gray_image

def get_num_channels(image):
    return image.shape[2] if len(image.shape) == 3 else 1

def get_image_size(image):
    if is_numpy(image):
        h, w = image.shape[:2]
        return h, w

    if is_pil(image):
        w, h = image.size
        return h, w

    if is_tensor(image):
        if len(image.shape) == 4 or len(image.shape) == 3:
            w, h = image.shape[-2:]
            return h, w
    else:
        raise ValueError("Unsupported input type")

def get_image_num_channels(img):
    if is_tensor(img):
        if img.ndim == 2:
            return 1
        elif img.ndim > 2:
            return img.shape[-3]

    if is_pil(img):
        return 1 if img.mode == 'L' else 3

    if is_numpy(img):
        return 1 if is_gray_image else 3