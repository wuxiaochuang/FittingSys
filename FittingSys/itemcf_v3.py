## --*-- coding:utf-8 --*--  ##
###################################
## program name:CF based on items
## input :
## output:
## time  :
## author:
###################################
import math  
import mysql
class ItemBasedCF(object):  
    def __init__(self,train_file,viewlist,*test_file):
        self.train_file = train_file  
        # self.test_file = test_file
        self.viewfile = viewlist
        # self.readData()
    def readData(self):  
        self.all=[] 
        self.train = dict() 
        self.test = []
        self.hash = dict()
        if self.train_file:
           for line in self.train_file:
            data_line = str(line).strip().split("', ")[-1]
            data_line = data_line.strip().split(", 0")[0]
            for i in data_line.strip().split(", "):
                self.train.setdefault(i, {})
                if i not in self.hash:
                    self.hash[i] = 1
                else:
                    self.hash[i] = self.hash[i] + 1
                for j in data_line.strip().split(", "):
                    if i == j:
                        continue
                    else:
                        self.train[i].setdefault(j, 0)
                        self.train[i][j] += 1
        '''
        with open(self.train_file,"r") as line:
            for fileline in line:
                for i in fileline.strip().split(";"):
                    if i not in self.hash:
                        self.hash[i]=1
                    else:
                        self.hash[i]=self.hash[i]+1
            line.seek(0)
            for everyline in line:
                if ";" not in everyline:
                    items=everyline.strip()
                else:
                    for items in everyline.strip().split(";"):
                        self.train.setdefault(items,{})
                        for j in everyline.strip().split(";"):
                            if items == j:
                                continue
                            else:
                                self.train[items].setdefault(j,0)
                                self.train[items][j]+=1
        '''
        '''                      
        with open(self.test_file,"r") as testfile:
            for testline in testfile:
                if ";" not in testfile:
                    self.test.append(testline.strip())
                else:
                    self.test.extend([int(p) for p in testline.strip().split(";")])
       '''
    def ItemSimilarity(self):  
        "to creat matrix of items and items" 
        C = dict()
        "co-matrix of the items"
        N = dict()
        "how many users to buy"
        C=self.train
        N=self.hash
        # print(N)
        "compte the similarity martix" 
        self.W = dict()  
        for i,related_items in C.items():  
            self.W.setdefault(i,{})  
            for j,cij in related_items.items():  
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        # print self.W
        return self.W  
  
    "reommend the most K items to users" 
    def Recommend(self,K=3):  
        rank = dict()  
        # at=self.test
        at=self.viewfile
        # print at
        temp_item={}
        action_item=dict()
        for i,c in at.items():
            if str(i) in self.hash:
                temp_item[i]=c
        '''
        for j in range(len(temp_item)):
            if j<len(temp_item)/2:
                action_item[temp_item[j]]=at[temp_item[j]] 
        if len(temp_item)/2>1:
            N = len(temp_item)/2
        else:
            N=0
        '''
        # print temp_item
        for item,score in temp_item.items():  
            for j,wj in sorted(self.W[str(item)].items(),key=lambda x:x[1],reverse=True):
                # print j
                # print wj
                if int(j) in temp_item:  
                    continue 
                rank.setdefault(j,0)  
                rank[j] += float(score) * wj
        if len(rank) < K:
            K = len(rank)
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:K]) 
def main(view_list,sex):
    cf_mysql = mysql.mysql()
    select_r = "select * from records where sex = "+"'"+sex+"'"+";"
    train_data = cf_mysql.db_select(select_r)
    trainpath= "./data/itemcftrain.txt"
    list_view = view_list
    #testpath="./data/itemcftest.txt"
    "creat the project and initialization"
    Item = ItemBasedCF(train_data,list_view)
    "read the history data"
    Item.readData()
    # print Item.hash
    "compute the similarity"
    Item.ItemSimilarity()  
    # number=0
    # numerator=0
    # denominator=0
    "get the recommend list of the list_view"
    recommedDic = Item.Recommend(5)
    print("the answer list based on Method 3")
    print(recommedDic)
    return recommedDic

def update_k(list_view,sex):
    wr_mysql = mysql.mysql()
    numb = len(list_view)
    name_str = "(number,sex"
    values_str = "(" + str(numb) + ",'" + str(sex)+"'"
    for i in range(numb):
        name_str += ",r"+str(i+1)
        values_str += ","+str(list(list_view.keys())[i])
        if i == numb-1:
            name_str += ")"
            values_str += ")"
    insert_db = "insert into records " + name_str + " values " + values_str
    wr_mysql.db_insert(insert_db)
    wr_mysql.db_close()



    '''
    trainpath= "C:/Users/Administrator/Desktop/itemcftrain.txt"
    newdata=""
    with open(trainpath,"a+") as f:
        for i in range(len(list_view.keys())):           
            newdata+="%d"%(int(list_view.keys()[i]))
            if i < (len(list_view.keys())-1):
                # print i
                newdata+=";"
        f.write("\n")
        f.write(newdata)
    '''
if __name__ == '__main__':
    # list_view=raw_input("please input the view list:\n")
    list_view={1:0.7,2:0.1,3:0.1,4:0.1}
    a=main(list_view)
    update_k(list_view)
