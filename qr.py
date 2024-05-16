import qrcode
from PIL import Image

def create_qr_with_logo(data, logo_path, output_path, qr_size=700, logo_size_ratio=0.3):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Load logo image
    logo_img = Image.open(logo_path)

    # Calculate logo size maintaining the aspect ratio
    logo_width, logo_height = logo_img.size
    logo_ratio = logo_size_ratio * qr_size / max(logo_width, logo_height)
    new_logo_width = int(logo_ratio * logo_width)
    new_logo_height = int(logo_ratio * logo_height)
    logo_img = logo_img.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)

    # Calculate position to paste the logo
    pos = ((qr_img.size[0] - new_logo_width) // 2,
           (qr_img.size[1] - new_logo_height) // 2)

    # Ensure the logo has an alpha channel (for transparency) if it doesn't already
    if logo_img.mode != 'RGBA':
        logo_img = logo_img.convert('RGBA')

    # Create an alpha composite image (QR code with logo)
    qr_img = qr_img.convert('RGBA')
    qr_img.paste(logo_img, pos, logo_img)

    # Save the resulting image
    qr_img.save(output_path)

# Example usage
data = "https://mmpp.com.sg/our-team/?id=1"
logo_path = "mmpp.png"
output_path = "qr_with_logo.png"
create_qr_with_logo(data, logo_path, output_path)