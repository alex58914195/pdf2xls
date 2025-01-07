from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import numpy as np
# np.int=np.int_

def pdfOcr(pdf_path):
    """
    使用 PaddleOCR 对输入的 PDF 文件进行中文文本识别。

    Args:
        pdf_path (str): 输入的 PDF 文件路径。

    Returns:
        str: 识别后的文本内容。
    """
    # 初始化 OCR 模型，语言设置为中文，使用 CPU
    ocr_model = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
    print("OCR 模型初始化完成。")

    # 将 PDF 文件转换为图像
    try:
        images = convert_from_path(pdf_path)
        print("PDF 转换为图像完成。")
    except Exception as e:
        print(f"PDF 转换失败: {e}")
        return ""

    # 存储 OCR 提取的文本
    extracted_text = ""

    # 对每页图像进行 OCR 识别
    for page_number, image in enumerate(images, start=1):
        print(f"开始识别第 {page_number} 页。")
        try:
            # 转换 Pillow 图像为 numpy 数组
            np_image = np.array(image)

            # OCR 识别
            result = ocr_model.ocr(np_image, cls=True)
            # print(result[0])
            print(f"第 {page_number} 页识别完成。")

            # 提取识别结果文本
            page_text = " ".join([line[1][0] for line in result[0]])
            print(page_text)
            extracted_text += page_text        
        except Exception as e:
            print(f"第 {page_number} 页识别失败: {e}")

    return extracted_text

if __name__ == "__main__":
    pdf_path = r"C:\Users\alex\Desktop\1\1.pdf"
    result=pdfOcr(pdf_path)
    print(result)