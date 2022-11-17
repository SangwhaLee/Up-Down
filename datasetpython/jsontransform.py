import json

file_path = './prototype.json'
with open(file_path,'r', encoding='UTF-8') as file:
    datas = json.load(file)

    print(len(datas))
    dataset = []

    for i in range(len(datas)):
        dataset.append({
            'model' : 'myapp.movie',
            'pk' : i+1,
            'fields': datas[i]
        }) #해당 부분은 프로젝트 이름에 맞춰 수정
print(dataset[1])

file_path = './datasets.json'
with open(file_path,'w', encoding='UTF-8') as outfile:
    json.dump(dataset, outfile, indent = 4,ensure_ascii=False)