import json
with open('devset_big.json','r') as f1:
    with open('devset.json','w') as f2:
        my_dict = json.load(f1)
        output = {}
        count = 0
        for id in my_dict:
            if count <= 100:
                output[id] = my_dict[id]
                count += 1
        output = json.dump(output,f2)
