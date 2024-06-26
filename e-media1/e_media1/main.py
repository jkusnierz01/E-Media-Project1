import PIL
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from chunksclasses import Image
from fourier import createFourierPlots
from encrypt import ECB
from logger_setup import setup_color_logging
import png
import struct
import zlib
import os

parser = argparse.ArgumentParser(description="Process PNG File")
parser.add_argument('path',help = 'Path to PNG file')
parser.add_argument('-r','--removeAll', action='store_true', required=False, dest='remove_all',help="Remove all Ancillary Chunks from file")
parser.add_argument('-e', '--ecbencrypt', action='store_true',required=False,dest ='ECBencrypt',help="Encrypt Image with ECB algorithm")
parser.add_argument('-c', '--cbcencrypt', action='store_true',required=False,dest ='CBCencrypt',help="Encrypt Image with CBC algorithm")
parser.add_argument('-compressed', action='store_true', required=False, dest='encryptcompressed',help='Encrypt Compressed Image Data')
args = parser.parse_args()



def main():
    #setting up logger
    logger = setup_color_logging()
    logger.info("Starting the application")

    #sprawdzenie czy istnieje plik pod podana sciezka
    if Path(args.path).is_file():

        # odczytanie i transformacja do grayscale 
        img = plt.imread(args.path)
        grayscale_image = img[:, :, :3].mean(axis=2)

        # tworzenie / upewnienie sie o istnieniu folderu do zapisu obrazow wyjsciowych
        save_path:str = os.path.dirname(os.path.abspath(__file__))+"/../output_images/"
        os.makedirs(save_path, exist_ok=True)

        with open(args.path,'r+b') as image_binary:

            # sprawdzenie sygnatury
            signature = image_binary.read(8)
            if signature == b'\x89PNG\r\n\x1a\n':
                image = Image(image_binary, save_path)
                # image.displayImageData()
                # createFourierPlots(grayscale_image)
                if(args.ECBencrypt):
                    image.encrypt_image_using_ecb(encrypt_compressed=args.encryptcompressed, library_func=True)
                if(args.CBCencrypt):
                    image.encrypt_image_using_cbc()
                # zapisanie zdjecia koncowego - z usunietymi wszystkimi chunkami dodatkowymi lub z pozostawionymi 3
                # with open(save_path+"/restored.png",'wb') as out_image:
                #     out_image = image.restoreImage(out_image, signature, args.remove_all)
            else:
                logger.error("Wrong file format!")
    else:
        logger.error(f"Invalid path to file! - {Path(args.path)}")


if __name__ == '__main__':
    main()
