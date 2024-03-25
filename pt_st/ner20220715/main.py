import PyPDF2

# path = r"/Users/zhiyue/Downloads/PDF文本数据_0709005/WinDealer dealing on the side _ Securelist.pdf"
# # 使用open的‘rb’方法打开pdf文件（这里必须得使用二进制rb的读取方式）
# mypdf = open(path, mode='rb')
# # 调用PdfFileReader函数
# pdf_document = PyPDF2.PdfFileReader(mypdf)
# # 使用pdf_document变量，获取各个信息
# # 或者PDF文档的页数
# print(pdf_document.numPages)
# content = []
# # 输出PDF文档的每一页内容
# for i in range(pdf_document.numPages):
#     print('>>>>>>>>>>start extracting content from {0} page'.format(str(i+1)))
#     every_page = pdf_document.getPage(i)
#     print('>>>>extracted content from {0} page'.format(str(i+1)))
#     print(every_page.extractText())
#     content.append(every_page.extractText())
# print(content)

line = 'The latest WinDealer sample we discovered in 2020 doesn’ t contain a hardcoded C2 server but instead relies on a complex IP generation algorithm to determine which machine to contact.'
import spacy

nlp = spacy.load('en_core_web_sm')
# doc = nlp("The 22-year-old recently won ATP Challenger tournament.")
doc = nlp(line)
for tok in doc:
    print(tok.text, "...", tok.dep_)
