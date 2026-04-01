import qrcode
import os

def generate_qr_code(booking_id, student_reg_no):
    """
    Generates a QR code for a confirmed booking.
    """
    data = f"BookingID:{booking_id}|Student:{student_reg_no}|Status:Confirmed"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure directory exists
    save_dir = "static/qr_codes"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    filename = f"booking_{booking_id}.png"
    filepath = os.path.join(save_dir, filename)
    img.save(filepath)
    
    return filename
