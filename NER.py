from LAC import LAC
# 自定义的类
import txtTest
from buildJson import buildJson

# 获取分段过的语料文件
all_section = txtTest.getSection("corpus4.txt")

# 装载LAC模型
lac = LAC(mode='lac')

# 单个样本输入，输入为Unicode编码的字符串

lac_result = lac.run(all_section[100:1000])

# person_name 存储识别出的实体以及出现次数
# adjacency_list 储存实体，以及与实体相连的其他实体,以及相连的次数 {entity:{connect_entity:times}}
# TODO
# 在一段落中，人物可能是先以全名的形式出现，然后再以缩写的形式出现，如 "董卓......卓曰："
# 所以在一段分析中，当前面出现全人名的时候，可以建立一个段落人名词典，把出现过的姓、名加入词典
# 如果在后面发现PER标记的实体，且该实体不存在总字典中，且该实体的字符在人名词典中出现，则跳过该实体的统计（）
person_name = {}
adjacency_list = {}
for i in range(len(lac_result)):
    section_entity = set()
    for j in range(len(lac_result[i][0])):
        # 当前实体识别为PER，即人名
        if lac_result[i][1][j] == 'PER':
            cur_entity = lac_result[i][0][j]
            if '。' in cur_entity or '曰' in cur_entity or '喜' in cur_entity or '怒' in cur_entity or '兵' in cur_entity or '视' in cur_entity: continue
            if cur_entity in person_name:
                person_name[cur_entity] += 1
            else:
                person_name[cur_entity] = 1
                adjacency_list[cur_entity] = {}

            # 建立邻接表
            for e in section_entity :
                if e == cur_entity: continue
                if e in adjacency_list[cur_entity].keys():
                    adjacency_list[cur_entity][e] += 1
                else:
                    adjacency_list[cur_entity][e] = 1
                if cur_entity in adjacency_list[e].keys():
                    adjacency_list[e][cur_entity] += 1
                else:
                    adjacency_list[e][cur_entity] = 1
            # print(adjacency_list)
            section_entity.add(cur_entity)
    section_entity.clear()

# result 存储根据条件过滤过的实体以及出现次数
result = {}
temp_adjacency = {}
result_adjacency_list = {}
for i in person_name.keys():
    if person_name[i] != 1 and 1 < len(i) <= 4:
        result[i] = person_name[i]
        temp_adjacency[i] = adjacency_list[i]

for i in temp_adjacency.keys():
    result_adjacency_list[i] = {}
    for j in temp_adjacency[i].keys():
        if j in result:
            result_adjacency_list[i][j] = temp_adjacency[i][j]

print(result)
print(result_adjacency_list)
# 将数据转换为Json格式提供G6可视化
buildJson(result, result_adjacency_list)

