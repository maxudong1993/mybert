import json
from collections import Counter

labels = ['SUPPORTS','REFUTES','NOT ENOUGH INFO']
with open('recall-60/test.json','r') as resource_f:
    with open('recall-60/test_results.tsv','r') as score_f:
        with open('recall-60/test_label.json','w') as result_f:
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
                for evidence in evidences:
                    scores = score_f.readline().strip().split()
                    if len(scores) != 3:
                        print(cur_id)
                        print(evidence)
                    max_score = float(scores[0])
                    max_idx = 0
                    for i in range(1,3):
                        if float(scores[i]) > max_score:
                            max_score = float(scores[i])
                            max_idx = i
                    evidence_labels.append(max_idx)
                final_label_count = Counter(evidence_labels).most_common()
                #there are only one label
                if len(final_label_count) == 1:
                    final_label =  final_label_count[0][0]
                 #there are two labels   
                elif len(final_label_count) == 2:
                    if final_label_count[0][0] == 2:
                        final_label = final_label_count[1][0]
                    elif final_label_count[1][0] == 2:
                        final_label = final_label_count[0][0]
                    else:
                        if final_label_count[0][1] == final_label_count[1][1]:
                            final_label = 0
                        else:
                            final_label = final_label_count[0][0]
                #there are three labels
                else:
                    for i, (lab,count) in enumerate(final_label_count):
                        if lab == 2:
                            del final_label_count[i]
                            break
                    if final_label_count[0][1] == final_label_count[1][1]:
                        final_label = 0
                    else:
                        final_label = final_label_count[0][0]
                        
                result_dict[cur_id]['label'] = labels[final_label]
                if final_label != 2:
                    evidence_number = 1
                    for i, cur_label in enumerate(evidence_labels):
                        if cur_label == final_label:
                            evidence = evidences[i].split()
                            result_dict[cur_id]['evidence'].append([evidence[0],int(evidence[1])])
                            evidence_number += 1
                            if evidence_number > 5:
                                break
            json.dump(result_dict,result_f,indent=4)



                    



