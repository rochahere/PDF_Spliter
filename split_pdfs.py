import shutil # Moves and renames files in linux
import glob # Finds all pathnames
import os # Portable way of using operating system dependent functionality
import sys # Stops python script
from PyPDF2 import PdfFileReader, PdfFileWriter # Reads and splits PDF documents
from secrets import * # Gets variables

print("\n#################################################################")
print("\nApp will split the newest file at /home/USER/Downloads by default\n")

#################################
####### Initial variables #######
#################################
# Change variables to your preferred location
directory_location = DOWNLOAD_DIRECTORY
final_location = YOUR_FINAL_LOCATION

#################################
########### Functions ###########
#################################
def get_newest_file(files_location):
  '''
  Fucntion will get the newest file on assigned location (with PDF extension)
  '''
  try:
    # List all files in directory
    files_in_folder = glob.glob(files_location)
    # Gets the newest file in directory
    newest_file = max(files_in_folder, key=os.path.getctime)
    print('This is newest file: ' + newest_file)
    return newest_file
  except:
    # This will be print if there is no PDF file in the directory
    print("There is no file with PDF extension")
    print("App will close")
    sys.exit()

def get_number_of_pages(file):
  '''
  Function will get the number of pages
  '''  
  try:
    # Gets the number of pages in file
    pages = PdfFileReader(file).getNumPages()
    # If the number of pages is equal to one app will end showing message
    if pages == 1:
      print("There is no need to split when pdf has only one page")
      print('App will close')
      sys.exit()
    print("The number of pages in document: " + str(pages))
    return pages
  except Exception as e:
    # If there is a issue with the file error will be print and app will finish
    print("There is an issue with the number of pages.")
    print(e)
    sys.exit()

def split_by():
  '''
  Get the split page number
  '''
  # Gets the number of pages to split by
  split = input("Number of page to split by:\n")
  try:
    # Change variable from string to int value
    split = int(split)
    # Prevents error if split by is bigger than total_pages
    if split >= total_pages:
      print('The split number has to be less than the total of pages. App wont run.')
      sys.exit()
    # Prevent error if split by is equal to zero
    if split == 0:
      print('The split number cannot be 0. App wont run.')
      sys.exit()
    return split
  except Exception as e:
    print('Split number has to be an intenger. App wont run')
    print(e)
    sys.exit()

def split_pdf(file, total_pages, split_by):
  try:
    # This variable helps assign the name to new pdf file
    counter = 1
    # 'For' will create splitted files depending in the split by number
    for page in range(0, total_pages, split_by):
      print('this is page: ' + str(page))
      # If 'split_by' is '1' will create a file per page
      if split_by == 1:
        pdf_writer = PdfFileWriter()
        current_page = (PdfFileReader(file).getPage(page))
        pdf_writer.addPage(current_page)
        # Location where files are going to be saved
        outputFilename = "splited_doc({}).pdf".format(counter)
        with open(final_location +  outputFilename, "wb") as out:
          pdf_writer.write(out)
          print("created", outputFilename)
        counter += 1
      # If 'split_by' is 'N' will create a file every 'N' pages
      if split_by >= 2:
        # Start PdfFileWriter() before the 'for' cycle start to prevent erase its content
        pdf_writer = PdfFileWriter()
        # Another 'for' is needed inside the main 'for' to create files with 2 or more pages
        for i in range(split_by):
          if (page + 1) <= total_pages:
            current_page = (PdfFileReader(file).getPage(page))
            pdf_writer.addPage(current_page)
            print('Document ' + str(page) + ' added')
            # If page value is zero we need to add '1' to get the right value for 'page' on the first run
            if i == 0:
              page = page + 1
            page = page + i
        # Location where files are going to be saved
        outputFilename = "splited_doc({}).pdf".format(counter)
        with open(final_location +  outputFilename, "wb") as out:
          pdf_writer.write(out)
          print("created", outputFilename)
        counter += 1
  except Exception as e:
    print("There is an issue with the file.")
    print(e)
    sys.exit()

# Get the newest file on /home/USER/Downloads
file = get_newest_file(directory_location)

# Get the number of pages
total_pages = get_number_of_pages(file)

# Get the split_by number
split_by = split_by()

# Creates the pdf file(s)
split_pdf(file, total_pages, split_by)
