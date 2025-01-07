# 从PDF文件提取信息填写excel表单项目说明（Please scroll down for the English version）
## 项目用途
本项目名为pdf2xls，但并不是实现单个pdf转为xls的工具，而是在一个文件夹下放置一个xlsx文件以及若干pdf（可以是扫描件），去实现从多个pdf中提取信息到xlsx文件的功能。例如，xlsx文件首行第一列写入“本文主要内容”，第二列写入“本文作者”，经本程序运算后回将文件夹内若干个pdf中的信息提取出来，并写入到xlsx文件中，文件夹如有i个pdf文件，则xlsx文件中会从第二行行开始写入信息，写到i+1行结束。第2至i+1行第一列内容为pdf的“本文主要内容”以及pdf的“本文作者”。每行信息末尾会自动添加本行是从哪个pdf文件提取的信息以供校验。

本文主要内容 | 本文作者 | 信息来源
--- | --- | ---
pdf1内容 | pdf1作者 | pdf1文件名
pdf2内容 | pdf2作者 | pdf2文件名
... | ... | ... 

## 大体思路
- 遍历data文件夹下的pdf文件。
- 对每个文件使用paddleocr进行文字识别，暂存为txt文件。
- 将txt内容发送给ollama接口，采用大模型对文档进行分析，并返回lsx中首行每一列的需填写项目，写入到xlsx文件中。

## 使用方法


### docker使用（推荐）
1. 安装ollama并启动服务（本机或异地服务器均可），确保接口地址正确。
2. 在命令行下运行以下命令：
   ```
   docker run --env=OllamaServer=http://10.8.0.3:11434 --env=ModelName=qwen2.5:7b --volume=/home/username/desktop/test/:/app/data --network=bridge alex5891/pdf2xls:latest
   # 其中的OllamaServer=http://10.8.0.3:11434为ollama服务地址和端口。
   # ModelName=qwen2.5:7b为ollama使用的模型名称，请确保该模型可以正常运行。
   # /home/username/desktop/test/是存放xlsx以及pdf的文件夹位置，需要挂载到容器内。需要注意此处的文件路径为linux格式下的路径。windows系统需要注意文件路径中“/”和“\”的使用差异。
   ```

### windows系统下使用
1. 安装ollama并启动服务（本机或异地服务器均可），确保接口地址正确。
2. 安装python，实测python3.12.1可用，建议使用该版本，其余版本请自行尝试。
3. 根据requiments.txt安装依赖包。
4. 在fillTable.py中修改

    ```python 
    ollamaServer = os.getenv("OllamaServer", "http://10.8.0.3:11434")  # 设置默认值
    modelName = os.getenv("ModelName", "qwen2.5:7b")  # 设置默认值
    ```
  
   `http://10.8.0.3:11434`和`qwen2.5:7b`设置为自己的服务器地址和模型名称。
5. 在data文件夹放置xlsx文件和需要提取信息的pdf文档。
6. 运行fillTable.py脚本，等待程序运行，完成会提示已完成运行，查验xlsx文件结果。
7. 对于中文或夹杂少量英文字符的pdf文件，本项目直接适用，如果pdf文件主要为英语，则建议修改pdfOcr.py中的

   ```python
   ocr_model = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
   ```

  将`lang="ch"`设置为`lang="en"`，以提高英文识别准确率。gpu用户也可在此修改为`use_gpu=True`以提高识别速度。（未经测试）

### linux系统下使用
未经测试，但大致方式同windows，请自行尝试。请注意文件路径中“/”和“\”的使用差异。

# 其他注意事项
1. excel文件只支持xlsx格式，xls不支持，pdf文件可以是扫描件，但要保证内容是可读的，文件的排版越简单越好，本项目对图片、表格、公式的支持未经测试（我自己用不上），如对此方面有要求请结合[MinerU项目](https://github.com/opendatalab/MinerU)调整代码。如果xlsx不存在本代码不会运行，如果xlsx存在但为空表，则会在表内写入所有文件夹内文件名称。
2. 受制于ollama本地部署模型能力，读取的pdf转成的文本字数如果太多，可能会导致大模型幻觉。经测试，在Qwen2.5:7b模型下，单个pdf文件在5000字以下时本程序使用效果尚可。
3. 本项目为开源免费使用，不得用于商业用途，请注意遵守相关法律法规。

***

# Project Description for Extracting Information from PDF Files to Fill in Excel Forms (中文版说明往上翻)

## Project Purpose
This project, named "pdf2xls", is not a tool for converting a single PDF into an XLS file. Instead, it is designed to extract information from multiple PDFs in a folder and consolidate it into a single XLSX file. For example, place an XLSX file in a folder along with several PDFs (including scanned documents). The program processes the PDFs, extracts relevant information, and writes it into the XLSX file. If there are i PDFs files in the folder, the data will be written starting from the second row of the XLSX file and ending at the `(i+1)`th row.

The first row of the XLSX file serves as the header. For example, Column 1 might be "Main Content," and Column 2 might be "Author." After processing, the extracted data will populate the XLSX file as follows:

Main Content | Author | Source File 
--- | --- | ---
| PDF1 Content | PDF1 Author | PDF1 Name   |
| PDF2 Content | PDF2 Author | PDF2 Name   |
| ...  | ... | ... |

Each row will include the source PDF filename for verification purposes.

## General Approach
- Traverse through the PDF files in the `data` folder.
- Use `paddleocr` to perform text recognition on each file and temporarily save the content as a TXT file.
- Send the TXT content to the Ollama API. A large language model processes the text and returns the information to populate the columns in the XLSX file.

## Usage Instructions

### Using Docker (Recommended)
1. Install and start the Ollama service (either locally or on a remote server) and ensure the API address is configured correctly.
2. Run the following command in the terminal:

   ```bash
   docker run --env=OllamaServer=http://10.8.0.3:11434 --env=ModelName=qwen2.5:7b --volume=/home/username/desktop/test/:/app/data --network=bridge alex5891/pdf2xls:latest
   #Replace http://10.8.0.3:11434 with your Ollama service address and port.
   #Replace qwen2.5:7b with the model you intend to use, ensuring it is functional.
   #/home/username/desktop/test/ is the folder containing the XLSX file and PDFs, which needs to be mounted into the container. Note: For Windows, ensure the appropriate adjustments to file paths (e.g., replacing \ with /).
   ```

### On Windows
1. Install and start the Ollama service (either locally or on a remote server) and ensure the API address is configured correctly.
2. Install Python. Python 3.12.1 is recommended; other versions may require testing.
3. Install dependencies using requirements.txt.
4. Modify the following lines in fillTable.py:
   ```python
   ollamaServer = os.getenv("OllamaServer", "http://10.8.0.3:11434")  # Default server address
   modelName = os.getenv("ModelName", "qwen2.5:7b")  # Default model name
   ```

   Update the values `http://10.8.0.3:11434` and `qwen2.5:7b` to your server address and model name.
5. Place the XLSX file and the PDF files to be processed in the data folder.
6. Run the fillTable.py script. The program will notify you upon completion, and the results will be available in the XLSX file.
7. For PDFs in Chinese or those containing mixed Chinese and English, the program is directly applicable. For English-only PDFs, modify the following line in pdfOcr.py:

   ```python
   ocr_model = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
   ```

   Change `lang="ch"` to `lang="en"` to improve English OCR accuracy. If using a GPU, set `use_gpu=True` to enhance speed (untested).

### On Linux
The process is similar to Windows but has not been explicitly tested. Ensure file paths use forward slashes (/) instead of backslashes (\).

# Additional Notes
1. The Excel file must be in XLSX format; XLS is not supported. PDFs can include scanned documents but must have readable content. Simpler layouts work better. Support for images, tables, or formulas is untested. For such use cases, consider modifying the code with the MinerU Project. If the XLSX file is missing, the program will not run. If it exists but is empty, the program will populate it with filenames from the folder.
2. Due to limitations of locally deployed Ollama models, processing PDFs with extensive text may lead to hallucination issues. Testing with the Qwen2.5:7b model shows the program performs well with PDFs under 5,000 characters(Chinese).
3. This project is open-source and free for non-commercial use. Please comply with all relevant laws and regulations.