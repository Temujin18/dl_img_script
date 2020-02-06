from urllib import request
import pandas
import xlrd


def download_image(image_link, file):
    try:
        file.write(request.urlopen(image_link).read())
        file.close()
    except:
        print("Download not allowed")


def read_excel(excel_file):
    df = pandas.read_excel(excel_file)
    values = df['Image Links'].values

    return values


excel_file = 'images.xlsx'
for image_link in read_excel(excel_file):
    file = open(image_link.split('/')[-1], 'wb')
    download_image(image_link, file)