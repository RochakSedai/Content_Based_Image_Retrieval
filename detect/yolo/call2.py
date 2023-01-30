
def calling():
    import nbformat
    import os
    from nbconvert.preprocessors import ExecutePreprocessor
    filename = 'D:\Major Project on CBIR and Recommendation\CBIR\detect\yolo\yolov5_detection.ipynb'

    with open(filename) as ff:
        nb_in = nbformat.read(ff, nbformat.NO_CONVERT)
    ep = ExecutePreprocessor()
    nb_out = ep.preprocess(nb_in)
# import subprocess

# def calling():
#     subprocess.call(["python", r"D:\Major Project on CBIR and Recommendation\CBIR\detect\yolo\detect.py"])
#     subprocess.call(["python", r"D:\Major Project on CBIR and Recommendation\CBIR\detect\yolo\detect1.py"])
#     subprocess.call(["python", r"D:\Major Project on CBIR and Recommendation\CBIR\detect\yolo\detect2.py"])


