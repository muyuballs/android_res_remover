#-*-coding:utf-8-*-
import os
import codecs

res={}
respath={}
refs={}
frefs={}

def optpng(dir,topdown=True):
	for root, dirs, files in os.walk(dir, topdown):
		for name in files:
			full_path = os.path.join(root,name)
			if full_path[-4:]==".png" :
				os.system("optipng "+full_path)

def list_res(lst,dir,t):
	for x in os.listdir(dir):
		print(x)
		name,ext=os.path.splitext(x)
		print(name+"-->"+ext)
		if name[-2:]=='.9':
			name=name[:-2]
		print("%s: %s->%s" %(t,x,name))
		if name not in lst:
			lst[name]=0
		if name not in respath:
			respath[name]=list()
		respath[name].append(os.path.join(dir,x))
	pass
	

def list_res_dir(dir):
	for x in os.listdir(dir):
		name=x.split('-')[0]
		if "drawable" == name or "layout" == name or "anim" == name:
			if name not in res:
				res[name]={}
			print("resource dir: %s->%s" %(x,name))
			list_res(res[name],os.path.join(dir,x),name)
		else:
			print("unknown resource %s" %x)

def test_refs(full_path,pr,charset="utf8"):
	print("test %s use %s" %(full_path,charset))
	file_obj=codecs.open(full_path,"rU",charset)
	try:
		ln=0
		for line in file_obj:
			ln+=1
		#print("test %s" %line)
			if len(line)<4:
				continue
			for x in res:				
				if pr==0:
					f="R."+x+"."
				else:
					f="@"+x+"/"
				for y in res[x]:
					t=f+y
					#print("test %s" %t)
					if line.find(t)!=-1:
						res[x][y]+=1
						if y not in frefs:
							frefs[y]=list()
						frefs[y].append("%s:%d" %(full_path,ln))
		file_obj.close()
	except Exception as ex:
		file_obj.close()
		print(ex)
		if charset is "utf8":
			print("utf8 test failed,trying gbk")
			test_refs(full_path,pr,"gbk")
		else:
			print("test file:%s failed" %full_path)

def check_resources(dir,topdown=True):
	for root, dirs, files in os.walk(dir, topdown):
		for name in files:
			full_path = os.path.join(root,name)
			p,ext=os.path.splitext(name)
			d=p.split('-')
			if ext==".java":
				test_refs(full_path,0)
			elif ext ==".xml":
				test_refs(full_path,1)



if __name__ =='__main__':
	#optpng('./src/main/res')
	list_res_dir('./src/main/res')
	print('===========================')
	for x in res:
		print(x+"->",len(res[x]))
	check_resources("./src/main")

	for x in res:
		print("[%s]" %x)
		for p in res[x]:
			print(p)
		tn = sorted(res[x],key =lambda d:res[x][d],reverse=True)
		c=0
		for y in tn:
			print("%s used %d" %(y,res[x][y]))
			if res[x][y]==0:
				for p in respath[y]:
					print("remove %s/%s" %(os.getcwd(),p))
					os.remove("%s/%s" %(os.getcwd(),p))
					c+=1
				print("\n")
			if  y not in frefs:
				continue
			for fp in frefs[y]:
				print(fp)
			print("\n")
		print("removed:%d" %c)

	print("job done.")
	

	
	
