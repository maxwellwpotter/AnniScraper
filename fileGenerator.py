from PIL import Image

img = Image.new('RGBA', (128, 48),(255, 255, 255, 0))

for num in range(96):
    x = num * 8 % 128
    y = (num * 8 // 128) * 8

    binary = format(num, "07b")
    print(binary)
    img.putpixel((x, y), (255, 255, 255, 255))
    for i in range(7):
        print(binary[-1 - i])
        if binary[-1 - i] == '1':
            print('Got in if')
            img.putpixel((x, y + i + 1), (255, 255, 255, 255))

img.save('font.png', 'PNG')
