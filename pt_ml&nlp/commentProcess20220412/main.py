import pandas as pd
import jieba
import os


def stopwordslist(stopwords_path):
    stopwords = [line.strip() for line in open(stopwords_path, encoding='UTF-8').readlines()]
    return stopwords


# 常见停用词
sw = stopwordslist('stopword.txt')


# 分词并且去停用词
def cut_word(word):
    cws = jieba.cut(word)
    finals = []
    for cw in cws:
        if cw not in sw:
            finals.append(cw)
    return set(finals)


def parse(words):
    result = {}
    for word in words:
        keywords = []
        score = 0
        label = None
        if word in pos or word in neg:
            keywords.append(word)
            if word in pos:
                score += 1
            elif word in neg:
                score += -1
            else:
                score += 0
        result['keywords'] = keywords
        if score > 0:
            label = '正向'
        elif score < 0:
            label = '负向'
        else:
            label = '中立'
        result['label'] = label
    return result


pos1 = pd.read_csv('/Users/zhiyue/Downloads/正面评价词语（中文）.txt', encoding='gb18030')
pos2 = pd.read_csv('/Users/zhiyue/Downloads/正面情感词语（中文）.txt', encoding='gb18030')
neg1 = pd.read_csv('/Users/zhiyue/Downloads/负面评价词语（中文）.txt', encoding='gb18030')
neg2 = pd.read_csv('/Users/zhiyue/Downloads/负面情感词语（中文）.txt', encoding='gb18030')
# print(pos1.sample(10))
# print(pos2.sample(10))
# print(neg1.sample(10))
# print(neg2.sample(10))
pos = []
neg = []
for w in pos1.loc[:].values:
    if w[0] not in pos:
        pos.append(w[0])
for w in pos2.loc[:].values:
    if w[0] not in pos:
        pos.append(w[0])
for w in neg1.loc[:].values:
    if w[0] not in neg:
        neg.append(w[0])
for w in neg2.loc[:].values:
    if w[0] not in neg:
        neg.append(w[0])

pos_def = ['关注','好看','比心','美美','好好看','跪求','期待']
pos = pos+pos_def

neg_def = ['取消','难看','不好看','离开','差','太差','不好']
neg = neg+neg_def

sheets = pd.read_excel('/Users/zhiyue/Downloads/人气峰值1小时区段弹幕.xlsx', sheet_name=None)
print(sheets.keys())

if os.path.exists('result.xlsx'):
    os.remove('result.xlsx')

with pd.ExcelWriter('result.xlsx') as writer:
    for key, value in sheets.items():
        print(key)
        df = value[['时间', '昵称', '内容']]
        df['分词'] = df['内容'].apply(lambda x: cut_word(str(x)))
        df['关键词'] = df['分词'].apply(lambda x: parse(x).get('keywords'))
        df['情感分类'] = df['分词'].apply(lambda x: parse(x).get('label'))
        print(df.shape)
        df.to_excel(writer, sheet_name=key)
