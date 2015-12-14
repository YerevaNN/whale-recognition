from random import uniform, choice
from math import pi, sin, cos, fabs
from os import path, chmod
import stat

def round_int(number): return int(round(number))


def generate_next_augment(input_image_path, output_image_path):
    flip = choice([True, False])
    rotation = round_int(uniform(0, 360))
    center_x = round_int(uniform(0.4, 0.6) * imageEdge)
    center_y = round_int(uniform(0.4, 0.6) * imageEdge)
    radius = min([center_x, center_y, imageEdge - center_x, imageEdge - center_y])
    rotate_pi = float(rotation) / 180 * pi
    max_square_edge = 2 * float(radius) / (fabs(sin(rotate_pi)) + fabs(cos(rotate_pi)))
    square_edge = round_int(uniform(400, max_square_edge))
    brightness = round_int(uniform(-20, 20))
    contrast = round_int(uniform(-20, 20))

    flip_option = "-flip" if flip else ""
    crop_x = center_x - radius
    crop_y = center_y - radius
    crop_edge = 2 * radius
    crop_square_option = "-crop {0}x{1}+{2}+{3}".format(crop_edge, crop_edge, crop_x, crop_y)
    rotate_option = "-rotate {0}".format(rotation)

    crop2_option = "+repage -gravity center -crop {0}x{1}+{2}+{3}".format(square_edge, square_edge, 0, 0)
    resize_option = "-resize {0}".format(outputImageEdge)
    brightness_contrast_option = "-brightness-contrast {0}x{1}".format(brightness, contrast)

    result_command = "convert {0} {1} {2} {3} {4} {5} {6} {7}".format(input_image_path,
                                                                      flip_option,
                                                                      crop_square_option,
                                                                      rotate_option,
                                                                      crop2_option,
                                                                      resize_option,
                                                                      brightness_contrast_option,
                                                                      output_image_path)
    return result_command


imageEdge = 1024
outputImageEdge = 512

fileNameCSV = "whale_heads.csv"
headsCSV = open(fileNameCSV).readlines()[1:]
imagesDir = "../crop1024/"
outputDir = "../augmented_images/"

augment_file_name = "augment.sh"

augment_file = open(augment_file_name, "w")

for line in headsCSV:
    st = line.split(',')
    image_name = st[0]

    image_path = imagesDir + image_name
    image_basename = path.splitext(path.basename(image_name))[0]
    image_extension = path.splitext(path.basename(image_name))[1]
    augment_file.write("echo {} \n".format(image_basename))
    augment_file.write("# {} \n".format(image_basename))
    for i in range(100):
        augmented_image_path = outputDir + image_basename + '_' + str(i).zfill(2) + image_extension
        command = generate_next_augment(image_path, augmented_image_path)
        augment_file.write(command + "\n")


augment_file.close()

#chmod(augment_file_name, stat.S_IXUSR | stat.S_IXGRP| stat.S_IXOTH)


run_file_name = "run.sh"
run_file = open(run_file_name, "w")

run_file.write("trap \"kill 0\" SIGINT SIGTERM\n")
run_file.write("\n")
run_file.write("rm -rf {}\n".format(outputDir))
run_file.write("mkdir {}\n".format(outputDir))
run_file.write("\n")
run_file.write("bash {} &\n".format(augment_file_name))
run_file.write("\n")
run_file.write("wait\n")

run_file.close()
