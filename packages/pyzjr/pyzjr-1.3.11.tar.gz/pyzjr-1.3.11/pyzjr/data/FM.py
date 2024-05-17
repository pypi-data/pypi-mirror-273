# --------------------------------------- #
# Used for some operations on files,
# file management is abbreviated as FM.
# --------------------------------------- #
import os
import datetime
import csv
from datetime import datetime
from pathlib import Path
import logging

__all__=[
    "get_logger",
    "getFilePath",
    "mkdirs",
    "mkdir",
    "logdir",
    "Data2csv",
    "file_age",
    "file_date",
    "file_size",
]

def get_logger(filename='./exp.log', verbosity=1, name=None):
    """示例
    logger.debug('This is a DEBUG message.')  # DEBUG 级别的日志
    logger.info('This is an INFO message.')    # INFO 级别的日志
    logger.warning('This is a WARNING message.')  # WARNING 级别的日志
    try:
        result = 10 / 0
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}', exc_info=True)
    logger.critical('This is a CRITICAL message.')  # CRITICAL 级别的日志
    """
    level_dict = {0: logging.DEBUG, 1: logging.INFO, 2: logging.WARNING}
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s]%(message)s"
    )
    logger = logging.getLogger(name)
    logger.setLevel(level_dict[verbosity])

    fh = logging.FileHandler(filename, "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger

def getFilePath(filedir, format='png'):
    """What is returned is a list that includes all paths under the target path that match the suffix."""
    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith(format)
                 ]
    return file_list if file_list else []

def mkdirs(*args):
    for path in args:
        if not os.path.exists(path):
            os.makedirs(path)

def mkdir(path, *paths, inc=False):
    """
    如果构建的输出目录路径不存在，它将创建该目录。
    如果 inc 为 True，它将检查是否已经存在相同的目录。如果存在，将在目录名称末尾附加一个数字后缀，直到找到一个不存在的目录。
    返回最终的输出目录路径。
    """
    outdir = os.path.join(path, *paths)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    elif inc:
        count = 1
        outdir_inc = outdir + '_' + str(count)
        while os.path.exists(outdir_inc):
            count = count + 1
            outdir_inc = outdir + '_' + str(count)
            assert count < 100
        outdir = outdir_inc
        os.makedirs(outdir)
    return outdir


def logdir(dir="logs", format=True, prefix="", suffix=""):
    """
    Logging generator
    :param dir: Default "logs"
    :param format: DATE_FORMAT = '%A_%d_%B_%Y_%Hh_%Mm_%Ss'
                   SIMPLEDATE_FORMAT = '%Y_%m_%d_%H_%M_%S'
    :param prefix: Add folder name before time string
    :param suffix: After adding the folder name to the time string
    :return:
    """
    DATE_FORMAT = '%A_%d_%B_%Y_%Hh_%Mm_%Ss'
    SIMPLEDATE_FORMAT = '%Y_%m_%d_%H_%M_%S'
    formats = DATE_FORMAT if format else SIMPLEDATE_FORMAT
    time_str = datetime.now().strftime(formats)

    folder_names = [prefix, time_str, suffix]
    folder_names = [folder for folder in folder_names if folder]

    log_dir = os.path.join(dir, *folder_names)
    os.makedirs(log_dir, exist_ok=True)

    return log_dir

def Data2csv(header, value, log_dir, savefile_name):
    """Export data to CSV format
    Args:
        header (list): 列的标题
        value (list): 对应列的值
        log_dir (str): 文件夹路径
        savefile_name (str): 文件名（包括路径）
    """
    os.makedirs(log_dir, exist_ok=True)
    file_existence = os.path.isfile(savefile_name)

    if not file_existence:
        with open(savefile_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(value)
    else:
        with open(savefile_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(value)

def file_age(path, detail=False):
    """Returns the number of days since the last file update."""
    dt = (datetime.now() - datetime.fromtimestamp(Path(path).stat().st_mtime))  # delta
    se = 0
    if detail:
        se = dt.seconds / 86400
    return f"{dt.days + se} days"

def file_date(path=__file__):
    """Return readable file modification date,i.e:'2021-3-26'."""
    t = datetime.fromtimestamp(Path(path).stat().st_mtime)
    return f'{t.year}-{t.month}-{t.day}'

def file_size(path):
    """Return file/dir size (MB)."""
    if isinstance(path, (str, Path)):
        mb = 1 << 20  # bytes -> MiB (1024 ** 2)
        path = Path(path)
        if path.is_file():
            size_mb = path.stat().st_size / mb
            return f"{size_mb:.5f} MB"
        elif path.is_dir():
            total_size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
            size_mb = total_size / mb
            return f"{size_mb:.5f} MB"
    return "0.0 MB"