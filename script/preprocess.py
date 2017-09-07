import codecs
import re
import glob
import numpy as np

def get_overlapped_chunks(textin, chunksize, overlapsize):
    return [ textin[a:a+chunksize] for a in range(0,len(textin), chunksize-overlapsize)]

def create_pipe(text,pipeInd):
    if(len(text)!=len(pipeInd)):
        print(len(text))
        print(len(pipeInd))
        print(text)
        print(pipeInd)
        return False

    ans=""
    for c,i in zip(text,pipeInd):
        if(i=="1"):ans+="|"
        ans+=c
    return ans
create_pipe("TEST","0010")


def prepare_features(filename, sen_len=100, overlap=20):
    f = codecs.open(filename, "r", "utf-8")
    text = f.read()
    # Make that | become only start of word
    if (text[0] != "|"): text = "|" + text
    if (text[-1] == "|"): text = text[:-1]
    stopwords = ["<NE>", "</NE>", "<AB>", "</AB>", "\r\n", ""]
    for word in stopwords:
        text = text.replace(word, "")
    isStart = "".join(["1" if c == "|" else "0" for c in text])
    isStart = isStart.replace("10", "1")
    text = text.replace("|", "")

    assert len(text) != len(isStart)

    X = get_overlapped_chunks(text, sen_len, overlap)
    Y = get_overlapped_chunks(isStart, sen_len, overlap)

    return X, Y


def load_data(sen_len=100, overlap=20,file_num = 75):
    # print all possible
    import glob
    file_list = glob.glob("../dataset/train/*/*.txt")
    X, Y = [], []

    for file in file_list[:file_num]:
        x, y = prepare_features(file, sen_len, overlap)
        X.extend(x)
        Y.extend(y)
    return np.array(X), np.array(Y)