import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageGrab
import cv2

charset1 = "@%#*+=-:. "
charset2 = "MWNBEHKRmA#@XQbd8DFGwPhkZUS69xTpqO4egV0af5%2$LYns&C3uzJyovIrtcli1j?7=><\"+*][}(){/\!;|:^-~',_.` "

def get_font_bitmaps(fontsize, boldness, reverse, background, chars, font):
    '''
    Returns a list of font bitmaps.

    Parameters
        fontsize    - Font size to use for ASCII characters.
        boldness    - Stroke size to use when drawing ASCII characters.
        reverse     - Reverse the ordering of the ASCII characters.
        background  - Background color.
        chars       - ASCII characters to use in media.
        font        - Font to use.

    Returns
        List of font bitmaps corresponding to the characters in 'chars'.
    '''
    bitmaps = {}
    min_width = min_height = float('inf')
    font_ttf = ImageFont.truetype(font, size=fontsize)

    for char in chars:
        if char in bitmaps:
            continue
        w, h = font_ttf.getsize(char)
        min_width, min_height = min(min_width, w), min(min_height, h)
        # Draw font character as a w x h image.
        image = Image.new('RGB', (w, h), (background,) * 3)
        draw = ImageDraw.Draw(image)
        draw.text(
            (0, -(fontsize // 6)),
            char,
            fill=(255 - background,) * 3,
            font=font_ttf,
            stroke_width=boldness,
        )
        bitmap = np.array(image)
        if background == 255:
            np.subtract(255, bitmap, out=bitmap)
        bitmaps[char] = bitmap.astype(np.uint8)

    # Crop the font bitmaps to all have the same dimensions based on the
    # minimum font width and height of all font bitmaps.
    fonts = [bitmaps[char][: int(min_height), : int(min_width)] for char in chars]
    # Sort font bitmaps by pixel density.
    fonts.sort(key=lambda x: x.sum(), reverse=not reverse)
    return np.array(fonts)

def draw_ascii(frame, chars, background, clip, monochrome, font_bitmaps, buffer=None):
    '''
    Draws an ASCII Image.

    Parameters
        frame           - Numpy array representing image. Must be 3 channels RGB.
        chars           - ASCII characters to use in media.
        background      - Background color.
        clip            - Clip characters to not go outside of image bounds.
        monochrome      - Color to use for monochromatic. None if not monochromatic.
        font_bitmaps    - List of font bitmaps.
        buffer          - Optional buffer for intermediary calculations.
                          Must have shape: ((h // fh + 1) * fh, (w // fw + 1) * fw, 3) where
                          h, w are the height and width of the frame and fw, fh are the font width and height.

    NOTE: Characters such as q, g, y, etc... are not rendered properly in this implementation
    due to the lower ends being cut off.
    '''
    # fh -> font height, fw -> font width.
    fh, fw = font_bitmaps[0].shape[:2]
    # oh -> Original height, ow -> Original width.
    oh, ow = frame.shape[:2]
    # Sample original frame at steps of font width and height.
    frame = frame[::fh, ::fw]
    h, w = frame.shape[:2]

    if buffer is None:
        buffer = np.empty((h * fh, w * fw, 3), dtype=np.uint16 if len(chars) < 32 else np.uint32)

    buffer_view = buffer[:h, :w]
    if len(monochrome) != 0:
        buffer_view[:] = 1
        if background == 255:
            monochrome = 255 - monochrome
        np.multiply(buffer_view, monochrome, out=buffer_view)
    else:
        if background == 255:
            np.subtract(255, frame, out=buffer_view)
        else:
            buffer_view[:] = frame
    
    colors = buffer_view.repeat(fw, 1).astype(np.uint16, copy=False).repeat(fh, 0)

    # Grayscale original frame and normalize to ASCII index.
    buffer_view = buffer_view[..., 0]
    np.sum(frame * np.array([3, 4, 1]), axis=2, dtype=buffer.dtype, out=buffer_view)
    buffer_view *= len(chars)
    buffer_view >>= 11

    # Create a new list with each font bitmap based on the grayscale value.
    image = (
        font_bitmaps[buffer_view]
        .transpose(0, 2, 1, 3, 4)
        .reshape(h * fh, w * fw, 3)
    )

    if clip:
        colors = colors[:oh, :ow]
        image = image[:oh, :ow]
        buffer = buffer[:oh, :ow]

    np.multiply(image, colors, out=buffer)
    np.floor_divide(buffer, 255, out=buffer)
    buffer = buffer.astype(np.uint8, copy=False)
    if background == 255:
        np.subtract(255, buffer, out=buffer)
    return buffer

def convert_ascii(
    img,
    chars,
    monochrome,
    fontsize=4,
    boldness=5,
    reverse=False,
    background=255,
    clip=True,
    font='cour.ttf',
):
    image = img[:, :, :3]
    font_bitmaps = get_font_bitmaps(fontsize, boldness, reverse, background, chars, font)
    image = draw_ascii(image, chars, background, clip, monochrome, font_bitmaps)
    # cv2.imshow("Output", image)
    cv2.imwrite('../output.jpg', image)

chars = np.array(list(charset2))
monochrome = np.array(
    [],
    dtype=np.uint16,
)
while True:
    # (x, y, w, h), slect portion of the screen to screenshot
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    img_np = np.array(img)
    convert_ascii(img_np, chars, monochrome)
    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

cv2.destroyAllWindows()