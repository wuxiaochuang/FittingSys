## --*-- coding:utf-8 --*-- ##
####################################
## program name : chuanyidapei
## input :
## output:
## time　：
## author:
####################################

#wuxhuangnishi wo de jiuxing

import numpy as np
from datetime import datetime
import re
#import mysql
#import itemcf
" the first method based on artificial rule "
def tuijianlist(a=[],b=[]):
    "a is the rules,b is the feature of person"
    if not a or not b:
        return -1
    else:
        candi=[]
        temp=[]
        fearture=[]
        number=0
        # print 'yes'
        for everylist in a:
            #print(everylist)
            #list_a,list_b,list_c = str(everylist).strip.split(',')
            feature,color,ling,detail,module = str(everylist).strip().split("', '")
            feature_1 = feature.strip().split("('")[-1]
            featur_1 = re.sub(r" ",",",feature_1)
            module_1 = module.strip().split("')")[0]
            # print feature
            # type(feature)
            if b==featur_1:
                # print 'yes'
                for everyco in color.strip().split(' '):
                    # print everyco
                    for everyli in ling.strip().split(' '):
                        # print everyli
                        for everyde in detail.strip().split(' '):
                            # print everyde
                            for everymo in module_1.strip().split(' '):
                                temp=[int(everyco),int(everyli),\
                                      int(everyde),int(everymo)]
                                # print temp
                                candi.append(temp)
                                number+=1
                                temp=[]
        return number,candi
"compute the similarity of two vector"
def cosdistance(a=[],b=[]):
    mat_mu=np.mat(a)
    mat_re=np.mat(b)
    dot_product=0
    norma=0
    normb=0
    simi=0
    for m,n in zip(mat_mu,mat_re):  
        dot_product += m*n.T  
        norma += m*m.T  
        normb += n*n.T  
    if norma == 0.0 or normb==0.0:  
        return -1  
    else:
        simi=int(dot_product)/(int(norma*normb)**0.5)
        return simi

def fanyic(featuremap):
    list_color = {'红色':1,'橙色':2,'黄色':3,'青色':4,'蓝色':5,'紫色':6,\
                   '绿色':7,'灰色':8,'黑色':9,'白色':10,'咖啡色':11}
    list_ling = {'圆领':1,'v领':2,'立领':3,'方领':4,'翻领':5,'高领':6}
    # print list_ling
    list_detail = {'印花':1,'横条纹':2,'竖条纹':3,'纯色':4}
    list_module = {'修身':1,'正常':2,'加大':3}
    feature_map = str(featuremap)
    # print feature_map
    color,ling,detail,module=feature_map.strip().split(';')
    # print (str(color)).code("utf-8")
    # print color,ling,detail,module
    vectorlist=[list_color[color],list_ling[ling],\
                list_detail[detail],list_module[module]]
    # print feature_map,vectorlist
    return vectorlist

def readdata(filename):
    namemap={}
    nameadress={}
    # print(filename)
    if filename:
        #print("yes")
        for nameline in filename:
            #print("test file name is ok")
            # print(nameline)
            itemid,adress,feature = str(nameline).strip().split(", '")
            itemid = itemid.strip().split("(")[-1]
            address = adress.strip().split("'")[0]
            address=re.sub(r"\\\\","/",address)
            nameadress[int(itemid)] = address
            # print(nameadress)
            feature_1 = feature.strip().split("')")[0]
            numfeature = fanyic(feature_1)
            # print("ok")
            if int(itemid)in namemap.keys():
                continue
            else:
                namemap[int(itemid)] = numfeature
    else:
        print(" the file of repository  is None ")
    return namemap,nameadress

"the second method of recommendation with collaborative filtering based on users"            
class redu(object):
    def __init__(self):
        self.mapping = {'4':0.9,'3':0.8,'2':0.6,'1':0.4}
        self.redu_value = 0.9
        self.redudic = {}
        self.olddic = {}
        self.namelabel = 0

    "get the history of redu"
    def get_history_db(self,dateline):
        if dateline:
            date_u = str(dateline).strip().split("', None")[0]
            date_r = str(date_u).strip().split("', '")[1:]
            for date_du in date_r:
                c_id,c_score = str(date_du).strip().split(",")
                self.olddic[c_id] = float(c_score)
            return self.olddic

    def get_history(self,adfile,person):
        olddic={}
        with open(adfile, 'r') as oldlist:
            #print("***********")
            for everyline in oldlist:
                # print(everyline)
                # oldline=everyline
                # numberline+=1
                fname,namelist=everyline.strip().split(";",1)
                a,b=fname.split(",")
                f_name="%d,%d"%(int(a),int(b))
                if f_name == person:
                    #print ("get history list  ok")
                    for namell in str(namelist).split(";"):
                        m,n=str(namell).split(",")
                        #print("ok redu")
                        olddic[m] = float(n)
                    return olddic

    def union_dict(self,*objs):
        total={}
        keys = set(sum([list(obj.keys()) for obj in objs],[]))
        for key in keys:  
            total[key] = sum([obj.get(key,0) for obj in objs])/2  
        return total

    "new score"
    def newredu(self,viewlist):
        "viewlist=[[1,1],[2,4],[],[]]"
        if len(viewlist) > 5:
            self.namelabel=viewlist[0]
            for times in range(len(viewlist)-1):
                newlist = viewlist[times+1]
                # print newlist
                if newlist[0] in self.redudic.keys():
                    if self.mapping[newlist[-1]] > self.redudic[newlist[0]]:
                        self.redudic[newlist[0]] = self.mapping[newlist[-1]]
                else:                    
                    # self.redudic.setdefault(newlist[0],0)
                    # print newlist[0],newlist[-1]
                    # print self.mapping[str(newlist[-1])]
                    self.redudic[str(newlist[0])] = self.mapping[str(newlist[-1])]
    def newredu_1(self,viewlist):
        "viewlist=[[1,1],[2,0.8],[],[]]"
        if len(viewlist) > 5:
            self.namelabel = viewlist[0]
            for times in range(len(viewlist) - 1):
                newlist = viewlist[times + 1]
                # print newlist
                if newlist[0] in self.redudic.keys():
                    if newlist[-1] > self.redudic[newlist[0]]:
                        self.redudic[newlist[0]] = newlist[-1]
                else:
                    # self.redudic.setdefault(newlist[0],0)
                    # print newlist[0],newlist[-1]
                    # print self.mapping[str(newlist[-1])]
                    self.redudic[str(newlist[0])] = newlist[-1]

    def answer_db(self):
        scorelist = ""
        if self.olddic and self.redudic:
            answerlist = self.union_dict(self.olddic,self.redudic)
            len_an = len(answerlist)
            for mm,nn in answerlist.items():
                scorelist += ",'%d,%.2f'"%(int(mm),float(nn))
            return len_an,scorelist
    def oldredu(self,adfile):
        numberline=0
        scorelist=""
        oldline=""
        newdata=""
        with  open(adfile,'r+') as oldlist:
            for everyline in oldlist:
                oldline=everyline
                numberline+=1
                fname,namelist=everyline.strip().split(";",1)
                a,b=fname.split(",")
                f_name=[int(a),int(b)]
                # f_name="["+str(fname)+"]"
                # print f_name
                # print self.namelabel
                if f_name==self.namelabel:
                    # print "test 'fname' is ok"
                    for namell in str(namelist).split(";"):
                        m,n=str(namell).split(",")
                        self.olddic[m] = float(n)
                    break
            aa = self.olddic
            bb = self.redudic
            # print self.olddic
            # print self.redudic
            newone=self.union_dict(aa,bb)
            scorelist=str(fname)
            for mm,nn in newone.items():
                scorelist+=";%d,%.2f"%(int(mm),float(nn))
        "update the redu"
        scorelist+="\n"
        with open(adfile,'r') as oldfile:
            olddata=oldfile.read()
            newdata=re.sub(oldline,scorelist,olddata)
        "save the answer"
        # print newdata
        with open(adfile,'w') as newfile:
            newfile.write(newdata)

def main():
    time_1 = datetime.now()
    f_mysql = mysql.mysql()
    # print("mysql ok")
    feature_map = feature
    "first method"
    select_m = "select name,color,ling,detail,style from rules;"
    matchlist_m = f_mysql.db_select(select_m)
    time_2 = datetime.now()
    time_21 = (time_2-time_1).seconds
    print(time_21)
    # matchlists = open("./data/matchlistm.txt",'r')
    numb,candidate = tuijianlist(matchlist_m,feature_map)
    print("tuijian ok")
    # matchlists.close()
    #print (numb)
    #print (candidate)
    "depend on the different task"
    # repository_f = "E:/documen/f/f-filelist.txt"
    # repository_m = "E:/document/m/m-filelist.txt"
    select_re = "select id,ad_name,ch_name from clothid where sex_id = " + "'"+str(sex)+"'" + ";"
    repository_db = f_mysql.db_select(select_re)
    mapping_1,mapping_2 = readdata(repository_db)
    print("reddate ok")
    f_mysql.db_close()
    # print(mapping_1)
    # print ("flag11")
    dicscore = {}
    for i in range(numb):
        for idll,j in mapping_1.items():
            # print candidate[i],j
            newscore = cosdistance(candidate[i],j)
            # print(newscore)
            dicscore.setdefault(idll,0)
            if newscore > dicscore[idll]:
                dicscore[idll] = newscore
    answerdic=dict(sorted(dicscore.items(),key=lambda x:x[1],reverse=True)[0:10])
    print("the answer list based method 1")
    print(answerdic)
    time_3=datetime.now()
    time_32 = (time_3-time_2).microseconds
    print("time of method 1 is ",time_32)
    "second method"
    if sex == "男":
        redu_list = "./data/redu_m.txt"
    else:
        redu_list = "./data/redu_f.txt"
    Re_du = redu()

    print("the answer list based method 2")
    redu_answer = Re_du.get_history(redu_list,feature_map)
    print(redu_answer)
    # tuijian_list=open('C:\Users\Administrator\Desktop\tuijian.txt','a+')
    time_4 = datetime.now()
    time_43 = (time_4-time_3).microseconds
    print("the time of method 2 is ",time_43)
    "third method"
    # list_view=[15,83,64]
    # thirdm=itemcf.main(list_view)
    return answerdic,redu_answer,mapping_2

def update_redu(listview,sex,feature):
    mapping = {"1,1": 1, "1,2": 2, "1,3": 3, "1,4": 4, "1,5": 5,
               "2,1": 6, "2,2": 7, "2,3": 8, "2,4": 9, "2,5": 10,
               "3,1": 11, "3,2": 12, "3,3": 13, "3,4": 14, "3,5": 15,
               "4,1": 16, "4,2": 17, "4,3": 18, "4,4": 19, "4,5": 20,
               "5,1": 21, "5,2": 22, "5,3": 23, "5,4": 23, "5,5": 25}
    re_du = redu()
    redu_mysql = mysql.mysql()
    redu_read = "select * from redu where sex = "+"'"+str(sex)+"'" \
                + "and number = " + str(mapping[feature]) + ";"
    date_line = redu_mysql.db_select(redu_read)
    a = re_du.get_history_db(date_line)
    re_du.newredu_1(listview)
    numb,answer_list = re_du.answer_db()
    filename = "number,sex"
    dateid=answer_list.strip().split("','")
    dateid[0] = str(dateid[0]).strip().split(",'")[-1]
    dateid[-1] = str(dateid[-1]).strip().split("'")[0]
    updatename = ""
    for i in range(numb):
        filename += ",f"+str(i+1)
        updatename += "f"+str(i+1)+"="+"'"+str(dateid[i])+"'"
        if i < numb-1:
            updatename += ","
    if date_line:
        update_db = "update table redu set "+updatename+";"
        print(update_db)
        # redu_mysql.db_update(update_db)

    else:
        redu_write = "insert into redu (" + filename+") values" \
                    " (" + str(mapping[feature])+","+"'"+str(sex)+"'"+answer_list+");"
        print(redu_write)
        # redu_mysql.db_insert(redu_write)


if __name__ == '__main__':
    #face_label = int(input("please input face_label :\n"))
    #body_label = int(input("please input body_label :\n"))
    #feature_map = '%d,%d'%(face_label,body_label)
    feature_map = '1,1'
    a,b,c = main()
    #print candidate
