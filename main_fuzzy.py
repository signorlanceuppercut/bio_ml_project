from concept import Concept
from edge import Edge
from map import Map
import pandas as pd

df_n = pd.read_excel('resources//fuzzy_rules//nodes.xlsx')
df_n=df_n.iloc[:,:-1]
#print(df_n.head())
df_a = pd.read_excel('resources//fuzzy_rules//archs.xlsx')
df_v = pd.read_excel('resources//fuzzy_rules//fuzzy_conf.xlsx')

key_list=[]
for key in df_n.iloc[:,2]:
    if (key in key_list) is False:
        key_list.append(key)
#print(key_list)

my_dict={}
#print(df_n.iloc[:,1],df_n.iloc[:,2])
print(df_n.columns.values)

for key in key_list:
    concept_list = []
    result_df=df_n[df_n['nodes_level']==key]
    #print(result_df.head())
    for concept in result_df.iloc[:,0]:
        concept_list.append(concept)
    my_dict={key : concept_list}
    print(my_dict)


new_df=df_a.groupby('arch_node_2')['arch_node_1'].apply(list).reset_index(name='child_node_list')
print(new_df)
new_df_2=df_a.groupby('arch_node_2').agg(lambda x:list(x))
print(new_df_2)




