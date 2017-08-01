# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from datetime import datetime
import sys,time,os,json,struct
from PyQt5.QtCore import Qt,QSize,pyqtSignal, QPoint
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtOpenGL
import ModernGL
import re
import MySQLdb
import CYtest_v3
import itemcf_v3
# import
class Win(QWidget):
	def __init__(self):
		super().__init__()
		self.m_list = os.listdir('.\\clothes\\m')
		self.f_list = os.listdir('.\\clothes\\f')
		self.clothSelected = -1
		self.number = 0
		self.method_1 = {}
		self.method_3 = {}
		self.method_2 = {}
		self.address = {}
		self.signal = 0
		self.sex = "女" #1:女，2:男
		self.initUI()
	
	def initUI(self):
		self.dictview = {}
		self.listview = []
		self.setWindowTitle('py试衣模拟')
		self.setMinimumHeight(700)
		self.setMinimumWidth(700)
		self.setWindowIcon(QIcon('data\\icon.png'))
		Layout = QGridLayout()
		self.glWidget = GLWidget(self.sex)#class defined by author
		#self.glWidget = GLWidget()
		self.glWidget.setFixedWidth(8*50)
		self.glWidget.setFixedHeight(9*50)
		grid_1 = QGridLayout()
		grid_2 = QGridLayout()
		grid_3 = QGridLayout()
		grid_4 = QGridLayout()
		self.listW = QListWidget()
		self.listW.setSpacing(15)
		self.listW.setIconSize(QSize(130*2,190*2))
		self.listW.setFixedWidth(400)
		self.listW.setViewMode(QListWidget.IconMode)
		for i in range(len(self.f_list)):
			item = QListWidgetItem(QIcon('./clothes/f_thu/'+self.f_list[i]),'garment_{}'.format(i),self.listW)
			self.listW.addItem(item)
		"add new items"
		facelist = [" ","1"+u"  圆脸","2"+ u"  方脸","3"+ u"  长脸","4"+ u"  尖脸","5"+ u" 标准脸"]
		bodylist = [" ","1"+ u" 倒三角型","2"+ u" 窄小型","3"+ u" 瘦高型","4"+ u"  胖型","5"+ u" 三角型"]
		sexlist = [" ",u"女",u"男"]
		face_module = QLabel("Face_Module:")
		face_module.setFont(QFont("Times New Roman",12,QFont.Bold))
		self.face_label = QComboBox()
		self.face_label.addItems(facelist)
		body_module = QLabel("Body_Module:")
		body_module.setFont(QFont("Times New Roman",12,QFont.Bold))
		self.body_label = QComboBox()
		self.body_label.addItems(bodylist)
		sex_module = QLabel("Gender:")
		sex_module.setAlignment(Qt.AlignCenter)
		sex_module.setFont(QFont("Times New Roman",12,QFont.Bold))
		self.sex_label = QComboBox()
		self.sex_label.addItems(sexlist)

		Layout.addLayout(grid_1, 0, 0)
		Layout.addLayout(grid_4, 0, 1)
		grid_4.addWidget(sex_module, 0,0,1,1)
		grid_4.addWidget(self.sex_label, 0,1,1,1)
		grid_1.addWidget(face_module,0,0,1,1)
		grid_1.addWidget(body_module,1,0,1,1)
		#grid_1.addWidget(sex_module,0,2,1,1)
		#grid_1.addWidget(self.sex_label,0,3,1,1)
		grid_1.addWidget(self.face_label,0,1,1,1)
		grid_1.addWidget(self.body_label,1,1,1,1)
		
		tall = QLabel("Tall:")
		tall.setFont(QFont("Times New Roman",12,QFont.Bold))
		grid_2.addWidget(tall,0,0,1,1)
		fat = QLabel("Fat:")
		fat.setFont(QFont("Times New Roman",12,QFont.Bold))
		grid_2.addWidget(fat,1,0,1,1)
		chest = QLabel("Chest:")
		chest.setFont(QFont("Times New Roman",12,QFont.Bold))
		grid_2.addWidget(chest,2,0,1,1)
		waist = QLabel("Waist:")
		waist.setFont(QFont("Times New Roman",12,QFont.Bold))
		grid_2.addWidget(waist,3,0,1,1)
		hip = QLabel("Hip:")
		hip.setFont(QFont("Times New Roman",12,QFont.Bold))
		grid_2.addWidget(hip,4,0,1,1)

		bybutton = QPushButton(u"购买",self)
		bybutton.setCheckable(True)
		grid_3.addWidget(bybutton,0,0,1,1)
		collbutton = QPushButton(u"收藏",self)
		collbutton.setCheckable(True)
		grid_3.addWidget(collbutton,0,1,1,1)
		self.face_label.currentIndexChanged.connect(self.updateUI)
		self.body_label.currentIndexChanged.connect(self.updateUI)
		self.sex_label.currentIndexChanged.connect(self.updateUI)
		self.sex_label.currentIndexChanged.connect(self.backUI)
		bybutton.clicked.connect(self.buttonUI)
		collbutton.clicked.connect(self.buttonUI)
		self.listW.currentItemChanged.connect(self.updateCloth)
		#self.updateUI()
		#self.buttonUI()
		self.setWindowTitle("The Recommend System Demo")
		
		
		# self.coeffInput = QSlider(Qt.Horizontal)
		# self.coeffInput.setMinimum(-100)
		# self.coeffInput.setMaximum(100)
		# self.coeffInput.setSingleStep(1)
		# self.coeffInput.valueChanged.connect(self.coeffChanged)



		Layout.addWidget(self.listW,1,1,4,1)
		Layout.addWidget(self.glWidget,1,0,4,1)
		Layout.addLayout(grid_2, 5, 0)
		Layout.addLayout(grid_3,5,1)
		self.setLayout(Layout)

		#hLayout = QHBoxLayout()
		#vLayout = QVBoxLayout()
		#hLayout.addWidget(self.glWidget,1)
		#hLayout.addLayout(vLayout,1)
		#vLayout.addWidget(self.listW,1)

		inputNames = ['tall','fat','chest','waist','hip']
		self.coeffInputs = dict()
		for _key in inputNames:
			self.coeffInputs[_key] = QSlider(Qt.Horizontal)
			self.coeffInputs[_key].setMinimum(-100)
			self.coeffInputs[_key].setMaximum(100)
			self.coeffInputs[_key].setSingleStep(1)
			self.coeffInputs[_key].setToolTip(_key)
			self.coeffInputs[_key].valueChanged.connect(self.coeffChanged)
			grid_2.addWidget(self.coeffInputs[_key],inputNames.index(_key),1,1,1)
		# self.setLayout(hLayout)
	"update the cloth in listW and get the face and body module"
	def updateUI(self):
		dict_gender = {1:"女",2:"男"}
		pre_sex = self.sex
		facevalue = self.face_label.currentIndex()
		bodyvalue = self.body_label.currentIndex()
		gender = self.sex_label.currentIndex()
		if gender:
			self.sex = dict_gender[gender]
		if facevalue and bodyvalue and gender:
			self.signal = 1
			#self.listview=[]
			#self.dictview={}
			self.listW.clear()
			namelist = "%d,%d"%(int(facevalue),int(bodyvalue))
			name_list = [int(facevalue), int(bodyvalue)]
			# print(namelist)
			self.method_1,self.method_2,self.address = CYtest_v3.main(namelist,self.sex)
			# print(self.method_1)
			# print(self.address)
			for cloth_i in self.method_1.keys():
				tempitem = self.address[cloth_i]
				#tempitem = re.sub(r"\\","/",tempitem)
				items = QListWidgetItem(QIcon(tempitem),'garment_{}'.format(int(cloth_i)),self.listW)
				self.listW.addItem(items)
			if not self.listview:
				self.listview.append(name_list)
			else:
				if len(self.listview) >= 5:
					CYtest_v3.update_redu(self.listview,pre_sex,namelist)
					#re_du = CYtest_v3.redu()
					#re_du.newredu_1(self.listview)
					#if self.sex == "男":
						#redu_list = "./data/redu_m.txt"
					#else:
						#redu_list = "./data/redu_f.txt"
					#re_du.oldredu(redu_list)
					itemcf_v3.update_k(self.dictview,pre_sex)
				self.listview = []
				self.dictview = {}
				self.listview.append(name_list)

	def buttonUI(self, pressed):
		listWid = self.listW.currentRow()
		print(listWid)
		if listWid != -1 and self.method_1.keys():
			clothid = list(self.method_1.keys())[listWid]
			source = self.sender()
			flag = 0
			if pressed:
				print("button press")
			if source.text() == "购买":
				self.number = 0.8
			if source.text() == "收藏":
				self.number = 0.6

			for i in range(len(self.listview)-1):
				if clothid not in self.listview[i+1]:
					continue
				else:
					flag = 1
					if self.listview[i][-1] < self.number:
						self.listview[i][-1] = self.number
						break
			if flag == 0:
				temp = [int(clothid), int(self.number)]
				self.listview.append(temp)

			if clothid not in self.dictview.keys():
				self.dictview[clothid] = self.number
			else:
				if self.dictview[clothid] < self.number:
					self.dictview[clothid] = self.number

	def coeffChanged(self,coeff):
		#print(self.coeffInput.value())
		self.glWidget.setShape({
			'tall':self.coeffInputs['tall'].value()*0.01,
			'fat':self.coeffInputs['fat'].value()*0.01,
			'chestP':self.coeffInputs['chest'].value()*0.01,
			'waist':self.coeffInputs['waist'].value()*0.01,
			'hip':self.coeffInputs['hip'].value()*0.01,
			})
		
	def keyReleaseEvent(self,e):
		if e.key() == Qt.Key_Down:
			print('hit~')
	
	def updateCloth(self,item):
		i = self.listW.currentRow()
		print(i)
		if i != -1 and self.method_1 and self.signal:
			c_id = list(self.method_1.keys())[i]
			print(c_id)
			signal = 0
			if len(self.listview) > 1:
				for j in range(len(self.listview)-1):
					if c_id in self.listview[j+1]:
						signal = 1
						break
			if signal == 0:
				temp1 = [int(c_id),0.4]
				self.listview.append(temp1)
			if str(c_id) not in self.dictview.keys():
				self.dictview[c_id] = 0.4
			print(i)
			if len(self.dictview) >= 5:
				time_1 = datetime.now()
				self.method_3 = itemcf_v3.main(self.dictview,self.sex)
				time_2 = datetime.now()
				print("the time of  method 3 is ",(time_2-time_1).microseconds)
		if i != self.clothSelected and i != -1:
			print("cloth chose ok")
			self.clothSelected = i
			if self.signal == 0:
				img_cloth = Image.open('.\\clothes\\f\\' + self.f_list[i])
			else:
				# print(self.address[c_id])
				img_cloth = Image.open(self.address[c_id])
				# print(img_cloth)
			self.glWidget.setCloth(img_cloth)

	def backUI(self):
		self.glWidget.initShapeRenCfg(self.sex)

class Shape:
	def __init__(self,shapesFilename=None,facesFilename=None):
		self.gender = 0
		self.coeffNames = [
			'tall', 'fat', 'thin', 'leglen',
			'chestP', 'chestN', 'waist',
			'hip', 'leg', 'arm', 'shoulderW',
			'shoulderSlop'
			]
		if shapesFilename is None:
			return
		f = open(shapesFilename)
		dataJson = json.loads(f.read())
		f.close()
		f = open(facesFilename)
		faces = json.loads(f.read())
		f.close()
		self.indexBuffer = np.array(faces,'i')#face data
		self.uvCoord = np.array(dataJson[0]['vertices'],'f')#body data
		self.vertices_std = self.uvCoord + np.array(dataJson[13]['vertices'],'f')#body+cloth
		self.offset = dict()
		self.offset['tall'] = np.array(dataJson[1]['vertices'],'f')
		self.offset['fat'] = np.array(dataJson[2]['vertices'],'f')
		self.offset['thin'] = np.array(dataJson[3]['vertices'],'f')
		self.offset['leglen'] = np.array(dataJson[4]['vertices'],'f')
		self.offset['chestP'] = np.array(dataJson[5]['vertices'],'f')
		self.offset['chestN'] = np.array(dataJson[6]['vertices'],'f')
		self.offset['waist'] = np.array(dataJson[7]['vertices'],'f')
		self.offset['hip'] = np.array(dataJson[8]['vertices'],'f')
		self.offset['leg'] = np.array(dataJson[9]['vertices'],'f')
		self.offset['arm'] = np.array(dataJson[10]['vertices'],'f')
		self.offset['shoulderW'] = np.array(dataJson[11]['vertices'],'f')
		self.offset['shoulderSlop'] = np.array(dataJson[12]['vertices'],'f')
	
	def generate(self,coeff):
		"to computer the body shape after change the body characters"
		#coeff is a dict(),about body data,such as tall:67
		_coeff = coeff.copy()
		for _key in self.coeffNames:
			if _key not in _coeff.keys():
				_coeff[_key] = 0.0

		if _coeff['fat'] < 0.0:
			_coeff['thin'] = -_coeff['fat']
			_coeff['fat'] = 0.0
		if _coeff['chestP'] < 0.0:
			_coeff['chestN'] = -_coeff['chestP']
			_coeff['chestP'] = 0.0

		shapeUsr = self.vertices_std.copy()
		for _key in self.coeffNames:
			shapeUsr += self.offset[_key]*_coeff[_key]
		return shapeUsr


class GLWidget(QtOpenGL.QGLWidget):
	"to show the body and the cloth "
	def __init__(self,sex,parent=None):
		self.Gender = sex
		self.lastPos = QPoint()

		fmt = QtOpenGL.QGLFormat()
		fmt.setVersion(4, 3)
		fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
		fmt.setSampleBuffers(True)
		super(GLWidget, self).__init__(fmt, parent)

	def minimumSizeHint(self):
		return QSize(50, 50)

	def sizeHint(self):
		return QSize(400, 400)

	def initBgrRenCfg(self):
		img_bgr = Image.open('data\\bgr.jpg')
		self.texture_bgr = self.ctx.texture(img_bgr.size,3,img_bgr.tobytes())#background images
		prog_bgr = self.ctx.program([
			self.ctx.vertex_shader('''
				#version 330

				in vec2 vert;
				in vec2 tex_coord;
				out vec2 v_tex_coord;

				void main() {
					gl_Position = vec4(vert, 0.0, 1.0);
					v_tex_coord = tex_coord;
				}
			'''),
			self.ctx.fragment_shader('''
				#version 330
				uniform sampler2D Texture;
				in vec2 v_tex_coord;
				out vec4 color;

				void main() {
					color = texture(Texture,v_tex_coord);
				}
			'''),
		])
		vbo_bgr = self.ctx.buffer(struct.pack(
			'24f',
			-1.0, -1.0,0.00, 1.00,
			1.00, 1.00,1.00, 0.00,
			-1.0, 1.00,0.00, 0.00,
			-1.0, -1.0,0.00, 1.00,
			1.00, -1.0,1.00, 1.00,
			1.00, 1.00,1.00, 0.00,
		))
		self.vao_bgr = self.ctx.simple_vertex_array(prog_bgr, vbo_bgr,['vert','tex_coord'])

	def initShapeRenCfg(self,sex):
		Gender = sex
		if Gender == "女":
			img = Image.open('data\\f_text.png')
		else:
			img = Image.open('data\\m_text.png')
		self.texture_body = self.ctx.texture(img.size,4,img.tobytes())
		self.texture_cloth = None
		prog = self.ctx.program([
			self.ctx.vertex_shader('''
				#version 330

				in vec2 vert;
				in vec2 tex_coord;
				out vec2 v_tex_coord;

				void main() {
					gl_Position = vec4(vert[0]/1300.0,vert[1]/1900.0, 0.0, 1.0);
					v_tex_coord = vec2(tex_coord[0]/2600.0+0.5,0.5-tex_coord[1]/3800.0);
				}
			'''),
			self.ctx.fragment_shader('''
				#version 330
				uniform sampler2D Texture;
				in vec2 v_tex_coord;
				out vec4 color;

				void main() {
					color = texture(Texture,v_tex_coord);
				}
			'''),
		])
		if Gender == "女":
			self.shape = Shape('data\\f_shapes2d170630.json','data\\faces.json')
		else:
			self.shape = Shape('data\\m_shapes2d170417.json', 'data\\faces.json')
		self.vbo_p = self.ctx.buffer(self.shape.vertices_std)
		self.vbo_uv = self.ctx.buffer(self.shape.uvCoord)
		ibo = self.ctx.buffer(self.shape.indexBuffer)
		vao_content = [
			(self.vbo_p,'2f',['vert']),
			(self.vbo_uv,'2f',['tex_coord']),
		]
		self.vao = self.ctx.vertex_array(prog,vao_content,ibo)
		self.update()

	def initializeGL(self):
		self.ctx = ModernGL.create_context()
		self.initBgrRenCfg()
		self.initShapeRenCfg(self.Gender)

	def paintGL(self):
		self.ctx.viewport = (0, 0, self.width(), self.height())
		self.ctx.clear(0.5, 0.5, 0.5)
		self.ctx.enable(ModernGL.BLEND)
		self.texture_bgr.use()
		self.vao_bgr.render()
		self.texture_body.use()
		self.vao.render()
		if self.texture_cloth is not None:
			self.texture_cloth.use()
			self.vao.render()
		self.ctx.finish()

	def setCloth(self,img):
		if self.texture_cloth is None:
			self.texture_cloth = self.ctx.texture(img.size,4,img.tobytes())
		else:
			self.texture_cloth.write(img.tobytes())
		self.update()

	def setShape(self,coeff):
		self.vbo_p.orphan()
		self.vbo_p.write(self.shape.generate(coeff))
		self.update()

	def resizeGL(self, width, height):
		side = min(width, height)
		if side < 0:
			return


	def mousePressEvent(self, event):
		self.lastPos = event.pos()

	def mouseMoveEvent(self, event):
		dx = event.x() - self.lastPos.x()
		dy = event.y() - self.lastPos.y()
		self.lastPos = event.pos()


def makeThumbnails():
	m_list = os.listdir('.\\clothes\\m')
	f_list = os.listdir('.\\clothes\\f')
	for clothfile in f_list:
		img = Image.open('.\\clothes\\f\\'+clothfile)
		img.thumbnail((260,380),resample = Image.BILINEAR)
		img.save('.\\clothes\\f_thu\\'+clothfile)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = Win()
	win.show()
	#app.exec_()
	sys.exit(app.exec_())
