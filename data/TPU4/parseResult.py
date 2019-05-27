import json
from collections import Counter
lg = 0
labels = ['SUPPORTS','REFUTES','NOT ENOUGH INFO']
with open('recall-70-60/test.json','r') as resource_f:
    with open('recall-70-60/test_results.tsv','r') as score_f:
        with open('recall-70-60/test_label.json','w') as result_f:
            my_dict = json.load(resource_f)
            ids = list(my_dict.keys())
            ids.sort()
            result_dict = {}
            for cur_id in ids:
                # evidences = my_dict[cur_id]['evidence']
                # for evidence in evidences:
                #     scores = score_f.readline().strip().split()
                #     max_score = float(scores[0])
                #     max_idx = 0
                #     for i in range(1,3):
                #         if float(scores[i]) > max_score:
                #             max_score = float(scores[i])
                #             max_idx = i
                #     result_f.write(str(max_idx)+"  ")
                #     result_f.write(labels[max_idx])
                #     result_f.write('\n')

                result_dict[cur_id] = {}
                result_dict[cur_id]['claim'] = my_dict[cur_id]['claim']
                result_dict[cur_id]['evidence'] = []
                evidences = my_dict[cur_id]['evidence']
                if len(evidences) == 0:
                    result_dict[cur_id]['label'] = 'NOT ENOUGH INFO'
                    continue
                evidence_labels = []
                scores = [[0,0],[1,0],[2,0]]
                for evidence in evidences:
                    cur_scores = score_f.readline().strip().split()
                    if len(cur_scores) != 3:
                        print(cur_id)
                        print(evidence)

                    cur_max_idx = 0
                    cur_max_score = float(cur_scores[0])
                    for i in range(1,3):
                        if float(cur_scores[i]) > cur_max_score:
                            cur_max_score = float(cur_scores[i])
                            cur_max_idx = i
                    #print(cur_max_idx)
                    #print(cur_max_score)
                    evidence_labels.append(cur_max_idx)
                    scores[cur_max_idx][1] += cur_max_score
                    #print(evidence_labels)
                    #print(scores)   
                scores.sort(key = lambda t : t[1], reverse = True)
                #print(scores)
                  
                #final_label_count = Counter(evidence_labels).most_common()
                #there are only one label
                if scores[1][1] == 0:
                    final_label = scores[0][0]
                else:
                    if scores[0][0] == 2:
                        final_label = scores[1][0]
                    else:
                        final_label = scores[0][0]
                result_dict[cur_id]['label'] = labels[final_label]
                if final_label != 2:
                    for i, cur_label in enumerate(evidence_labels):
                        if cur_label == final_label:
                            evidence = evidences[i].split()
                            result_dict[cur_id]['evidence'].append([evidence[0],int(evidence[1])])
            json.dump(result_dict,result_f,indent=4)



                    



