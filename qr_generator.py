import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw
import qrcode
import uuid
from datetime import datetime

qr_image = None
logo_path = None
qr_color = "black"
shape_style = "square"

# ------------------------
# Generate QR Function
# ------------------------
def generate_qr():
    global qr_image

    phone = phone_entry.get()
    email = email_entry.get()
    website = website_entry.get()
    location = location_entry.get()

    if not phone or not email or not website or not location:
        messagebox.showerror("Error", "Please fill all fields")
        return

    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = f"""
    BEGIN:VCARD
    VERSION:3.0
    FN:JN Car Accessories
    TEL:+254{phone[-9:]}
    EMAIL:{email}
    URL:https://{website}
    ADR:{location}
    END:VCARD

    https://{website}
    mailto:{email}
    tel:+254{phone[-9:]}
    """

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    if shape_style == "rounded":
        img = make_rounded(data)
    else:
        img = qr.make_image(fill_color=qr_color, back_color="white").convert("RGB")



    # Add logo if available
    if logo_path:
        img = add_logo(img, logo_path)

    qr_image = img

    # Preview
    preview = img.resize((220, 220))
    img_tk = ImageTk.PhotoImage(preview)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk


# ------------------------
# Rounded Effect
# ------------------------
def make_rounded(data):
    qr = qrcode.QRCode(
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    size = len(matrix)

    img_size = size * 10
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if matrix[y][x]:
                x1 = x * 10
                y1 = y * 10
                x2 = x1 + 10
                y2 = y1 + 10

                draw.ellipse([x1, y1, x2, y2], fill=qr_color)

    return img


# ------------------------
# Add Logo
# ------------------------
def add_logo(qr_img, logo_path):
    logo = Image.open(logo_path)

    # Resize logo
    size = qr_img.size[0] // 4
    logo = logo.resize((size, size))

    pos = (
        (qr_img.size[0] - size) // 2,
        (qr_img.size[1] - size) // 2
    )

    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    return qr_img


# ------------------------
# Save QR
# ------------------------
def save_qr():
    if qr_image is None:
        messagebox.showerror("Error", "Generate QR first")
        return

    path = filedialog.asksaveasfilename(defaultextension=".png")
    if path:
        qr_image.save(path)
        messagebox.showinfo("Saved", "QR saved successfully!")


# ------------------------
# Pick Color
# ------------------------
def pick_color():
    global qr_color
    color = colorchooser.askcolor()[1]
    if color:
        qr_color = color


# ------------------------
# Upload Logo
# ------------------------
def upload_logo():
    global logo_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if path:
        logo_path = path
        messagebox.showinfo("Logo", "Logo uploaded successfully")


# ------------------------
# Shape Selection
# ------------------------
def set_shape(shape):
    global shape_style
    shape_style = shape


# ------------------------
# UI
# ------------------------
root = tk.Tk()
root.title("QR Generator Pro")
root.geometry("520x650")
root.configure(bg="#f4f6f8")

title = tk.Label(root, text="QR Code Generator Pro", font=("Arial", 16, "bold"), bg="#f4f6f8")
title.pack(pady=10)

frame = tk.Frame(root, bg="#f4f6f8")
frame.pack(pady=10)

def create_input(label):
    tk.Label(frame, text=label, bg="#f4f6f8").pack(anchor="w")
    entry = tk.Entry(frame)
    entry.pack(fill="x", pady=5)
    return entry

phone_entry = create_input("Phone")
email_entry = create_input("Email")
website_entry = create_input("Website")
location_entry = create_input("Location")

# Buttons
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Pick Color", command=pick_color).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Upload Logo", command=upload_logo).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Generate", command=generate_qr).grid(row=0, column=2, padx=5)

# Shape selector
shape_frame = tk.Frame(root, bg="#f4f6f8")
shape_frame.pack(pady=5)

tk.Label(shape_frame, text="Shape Style:", bg="#f4f6f8").pack(side="left")

tk.Button(shape_frame, text="Square", command=lambda: set_shape("square")).pack(side="left", padx=5)
tk.Button(shape_frame, text="Rounded", command=lambda: set_shape("rounded")).pack(side="left", padx=5)

# Preview
qr_label = tk.Label(root, bg="#f4f6f8")
qr_label.pack(pady=20)

# Save button
tk.Button(root, text="Download QR", command=save_qr, bg="#4CAF50", fg="white").pack(pady=10)

root.mainloop()