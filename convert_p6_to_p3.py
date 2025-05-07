import sys

def parse_header(f):
    magic_number = f.readline().strip()
    
    def read_non_comment():
        line = f.readline()
        while line.startswith(b'#'):
            line = f.readline()
        return line

    dims = read_non_comment().split()
    width, height = map(int, dims)

    maxval = int(read_non_comment())
    return width, height, maxval

def convert_p6_to_p3(in_path, out_path):
    with open(in_path, 'rb') as f:
        width, height, maxval = parse_header(f)
        num_samples = width * height * 3
        pixel_data = f.read(num_samples)

    pixels = list(pixel_data)

    with open(out_path, 'wb') as f:
        header = f"P3\n{width} {height}\n{maxval}\n".encode('ascii')
        f.write(header)
        for idx in range(0, len(pixels), 3):
            r, g, b = pixels[idx], pixels[idx + 1], pixels[idx + 2]
            f.write(f"{r} {g} {b}".encode('ascii'))
            if ((idx // 3) + 1) % width == 0:
                f.write(b"\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write(
                "Usage: python convert_p6_to_p3.py <input.ppm> <output.ppm>\n")
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    convert_p6_to_p3(in_path, out_path)
    sys.stdout.write(
            f"Converted {in_path} to ASCII P3 format at {out_path}\n")
