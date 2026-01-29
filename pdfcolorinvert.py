import sys
import subprocess
import os
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageOps
import tempfile
import shutil

def run(cmd):
    subprocess.run(cmd, check=True)

def parse_pages(expr):
    pages = set()
    for part in expr.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

def make_very_white(img):
    """
    Force background to white and text to black.
    """
    # 1. Grayscale
    g = img.convert("L")

    # 2. Invert
    g = ImageOps.invert(g)

    # 3. Strong contrast stretch
    g = ImageOps.autocontrast(g, cutoff=1)

    # 4. Threshold (push gray -> white)
    g = g.point(lambda x: 255 if x > 200 else 0)

    return g.convert("RGB")

def main():
    if len(sys.argv) != 4:
        print("Usage: python fix_black_pages.py input.pdf output.pdf 10-13")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    pages = parse_pages(sys.argv[3])

    work = tempfile.mkdtemp()

    try:
        # 1. Rasterize selected pages
        run([
            "gs",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=png16m",
            "-r300",
            f"-sPageList={','.join(map(str, pages))}",
            f"-sOutputFile={work}/page_%03d.png",
            input_pdf
        ])

        # 2. Force very white
        imgs = sorted(f for f in os.listdir(work) if f.endswith(".png"))
        out_imgs = []

        for f in imgs:
            im = Image.open(f"{work}/{f}")
            fixed = make_very_white(im)
            out = f"{work}/inv_{f}"
            fixed.save(out)
            out_imgs.append(out)

        # 3. Images → PDF
        pil_imgs = [Image.open(p) for p in out_imgs]
        inv_pdf = f"{work}/inverted.pdf"
        pil_imgs[0].save(inv_pdf, save_all=True, append_images=pil_imgs[1:])

        # 4. Merge back
        orig = PdfReader(input_pdf)
        inv = PdfReader(inv_pdf)
        writer = PdfWriter()

        j = 0
        for i in range(len(orig.pages)):
            if (i + 1) in pages:
                writer.add_page(inv.pages[j])
                j += 1
            else:
                writer.add_page(orig.pages[i])

        with open(output_pdf, "wb") as f:
            writer.write(f)

        print(f"Your output is written to: {output_pdf}")

    finally:
        shutil.rmtree(work)

if __name__ == "__main__":
    main()

