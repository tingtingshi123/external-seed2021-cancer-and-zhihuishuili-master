from enum import Enum


class ErrorCode(Enum):
    SystemErrorCode = 3201
    TestDataDirNotExists = "样本目录不存在。"
    TestDataDirIsEmpty = "样本集合为空。"
    AnswerDataDirNotExists = "答案目录不存在。"
    AnswerDataDirIsEmpty = "答案集合为空。"
    DataError = "答案集合不是样本集合子集"
    TCImagesNameListNotFound = "样本坐标信息文件不存在"
    TCImagesNameFormatIncorrect = "样本坐标信息文件格式不正常"
    LabelFileErrorCode = 1003
    LabelFileName="提交标签文件不是result.zip"
    # LabelFileIsDir = "提交的标签文件应该是文件而不是目录"

    # LabelFileIsNotZip = "提交的标签文件没有采用ZIP格式"
    # LabelDirExpectDirNotFound = "无法检测到约定的目录，检测到的目录名为："
    # LabelNoEffectiveDirs = "提交的标签文件没有找到符合约定的目录"
    # TransferJsonFailed = "文件无法解析为JSON格式，具体原因："
    LabelFileIsDir = "提交作品不是ZIP格式，请查看提交指南"

    LabelFileIsNotZip = "提交作品不是ZIP格式，请查看提交指南"
    LabelDirExpectDirNotFound = "文件夹目录结构不正确，请查看提交指南"
    LabelNoEffectiveDirs = "文件夹目录结构不正确，请查看提交指南"
    # LabelFileName = "标签文件名称不对"
    TransferJsonErrorCode = 11014

    LabelFileNotCompleteCode = 1105
    LabelFileNotComplete = "提交内容不完整"

    LabelFileContentCode = 1105  # 内容错误
    EncodingWrongCode = 1106 # 编码格式错误
    EncodingWrong = '文件编码格式错误'

    ImagesPixelRangeFileNotFoundCode =1106 #坐标轴没有找到
    ImagesPixelRangeFileNotFoundMsg = "图片像素文件无法找到"
    ImagesTimeRangeFileNotFoundCode = 1107  # 时间范围没有找到
    ImagesTimeRangeFileNotFoundMsg = "图片时间范围文件无法找到"

    TimeOutCode = 1108 # 超时提醒
    TimeOutMsg = "提交作品超时"

    FileIsMask = 1109 # 文件名不含mask
    FileIsMaskMsg = "文件名命名格式不符合"
    LabelFileNotExistscode=1110
    LabelFileNotExists = "提交的标签文件result.csv不存在"
    ColumnNameNotExistsCode=1111
    ColumnNameNotExists="标签文件中的列名不符合要求"
    ImageNameNotExistsCode=1112
    ImageNameNotExists ="图片名称不存在"