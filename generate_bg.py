import struct
import math

def generate_bmp(width, height, filename):
    # BMP Header
    file_size = 54 + width * height * 3
    header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
    dib_header = struct.pack('<IIIHHIIIIII', 40, width, height, 1, 24, 0, width * height * 3, 0, 0, 0, 0)
    
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(dib_header)
        
        # Pixel Data (Bottom-up)
        for y in range(height):
            for x in range(width):
                # Default Background: Dark Blue/Grey
                b, g, r = 40, 30, 30
                
                # Floor
                if y < 100:
                    b, g, r = 60, 50, 50
                    # Grid on floor
                    if (x + y) % 40 < 2 or (x - y) % 40 < 2:
                         b, g, r = 100, 90, 90

                # --- DRAW SPIKES (Red) ---
                # Spike 1
                if draw_spike(x, y, 500, 100, 60):
                    b, g, r = 20, 20, 200 # Red (BGR)
                # Spike 2
                if draw_spike(x, y, 580, 100, 50):
                    b, g, r = 20, 20, 200
                # Spike 3
                if draw_spike(x, y, 650, 100, 70):
                    b, g, r = 20, 20, 200

                # --- DRAW ROBOT (Cyan) ---
                # Center X: 200, Floor Y: 100
                # Scale: 100px reference
                
                # Legs
                if draw_rect(x, y, 180, 100, 30, 80) or draw_rect(x, y, 220, 100, 30, 80):
                    b, g, r = 200, 200, 0 # Cyan (BGR)
                
                # Body
                if draw_rect(x, y, 170, 180, 90, 100):
                    b, g, r = 200, 200, 0
                
                # Head
                if draw_rect(x, y, 190, 290, 50, 50):
                    b, g, r = 200, 200, 0
                
                # Arms
                if draw_rect(x, y, 130, 200, 30, 80) or draw_rect(x, y, 270, 200, 30, 80):
                    b, g, r = 200, 200, 0

                f.write(struct.pack('BBB', b, g, r))

def draw_rect(x, y, rx, ry, w, h):
    return rx <= x < rx + w and ry <= y < ry + h

def draw_spike(x, y, cx, cy, size):
    # Simple triangle
    # y base is cy
    # height is size
    if y < cy or y > cy + size:
        return False
    half_width = (size - (y - cy)) * 0.5
    return cx - half_width <= x <= cx + half_width

if __name__ == "__main__":
    generate_bmp(800, 600, "Assets/MenuBackground.bmp")
