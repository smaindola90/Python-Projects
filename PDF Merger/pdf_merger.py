import PyPDF2 as pypdf

noOfFiles = int(input("How many pdfs do you want to merge: "))
pdfFiles = []
for i in range(1, noOfFiles+1):
    pdfile = input(f"Enter the {i} pdf file name: ")
    pdfFiles.append(pdfile)

newFile = input("What do you want your merged file name to be: ")

pdfMerge = pypdf.PdfMerger()

for filename in pdfFiles:
    pdfFile = open(filename, 'rb')
    pdfReader = pypdf.PdfReader(pdfFile)
    pdfMerge.append(pdfReader)

pdfFile.close()
pdfMerge.write(newFile)