#!/usr/bin/env python3
# coding: utf-8

import io
import sys
import re
import codecs
from struct import *

class AviUtlElement:
	def __init__(self):
		self.start = 0
		self.end = 0
		self.text = "";

def toUtf8(s):
	ss = len(s)
	t = ""
	for x in range(0,ss-1,4):
		c = int(s[x:x+2],16)+int(s[x+2:x+4],16)*256
		if c == 0: break
		t += chr(c)
	return re.sub(r"\r?\n","",t);

def replaceWord(s):
	s = s.replace("パスポーン", " Passed Pawn ")
	s = s.replace("ポーン", " Pawn ")
	s = s.replace("ルーク", " Rook ")
	s = s.replace("ナイト", " Knight ")
	s = s.replace("ビショップ", " Bishop ")
	s = s.replace("クイーン", " Queen ")
	s = s.replace("キング", " King ")
	s = s.replace("データベース", " Database ")
	s = s.replace("ギャンビット", " Gambit ")
	s = s.replace("サクリファイス", " Sacrifice ")
	s = s.replace("トラップ", " Trap ")
	s = s.replace("テイク", " Take ")
	s = s.replace("プッシュ", " Push ")
	s = s.replace("フィックスド", " Fixed ")
	s = s.replace("オープニング", " Opening ")
	s = s.replace("ミドルゲーム", " Middle game ")
	s = s.replace("エンドゲーム", " End game ")
	s = s.replace("エンディング", " Ending ")
	s = s.replace("序盤", " Opening ")
	s = s.replace("中盤", " Middle game ")
	s = s.replace("終盤", " End game ")
	s = s.replace("指す", " Move ")
	s = s.replace("指し", " Move ")
	s = s.replace("指す手", " Move ")
	s = s.replace("展開", " Develop ")
	s = s.replace("支配", " Control ")
	s = s.replace("ディスカバードチェック", " Discovered Check ")
	s = s.replace("ディスカバードアタック", " Discovered Attack ")
	s = s.replace("フォーク", " Fork ")
	s = s.replace("ピン", " Pin ")
	s = s.replace("スキュア", " Skewer ")
	s = s.replace("ダウン", " down ")
	s = s.replace("アップ", " up ")
	s = s.replace("ピース", " piece ")
	s = s.replace("マス", " Square ")
	s = s.replace("ドロー", " Draw ")
	s = s.replace("プロモーション", " Promotion ")
	s = s.replace("ツークツワンク", " zugzwang ")
	s = s.replace("棋譜", " Score ")
	s = s.replace("手筋", " Strategy ")
	s = s.replace("定跡", " Theory ")
	s = s.replace("定石", " Theory ")
	s = s.replace("狙い", " threat ")
	s = s.replace("手数", " Tempo ")
	s = s.replace("間駒", " interpose ")
	s = s.replace("合駒", " interpose ")
	s = s.replace("合い駒", " interpose ")
	s = s.replace("白マス", " light square ")
	s = s.replace("黒マス", " dark square ")
	s = s.replace("最善手", " optimal move ")
	s = s.replace("ヴァンキュラポジション", " Vancura Position ")
	s = s.replace("フィリドールポジション", " Philidor Position ")
	s = s.replace("ルセナポジション", " Lucena Position ")
	return s

def formatForSrt(s):
	sec = float(s%1800)/30
	hm = s/1800
	h = int(hm/60)
	m = int(hm%60)
	return re.sub(r"\,",",","{0:01d}:{1:02d}:{2:06.3f}".format(h,m,sec));


sys.stdin = io.TextIOWrapper(sys.stdin.buffer,encoding='cp932')

did = args = sys.argv[1]
fid = args = sys.argv[2]

lines = open("C:/Users/hmori/Documents/Youtube/KihitoChess/" + did + "/" + fid + ".exo").readlines()

sid = 0
element = {}
start_ = 0
end_ = 0
text = ""

for line in lines:
	m = re.match(r"\[([0-9]+)\]",line)
	if m:
		sid = int(m.group(1))
	else:
		mm = re.search(u'_name=テキスト',line)
		if mm:
			element[sid] = AviUtlElement()
			element[sid].start = start_
			element[sid].end = end_
		else:
			m3 = re.match(r'^text=3c003f0073003d005b003d003d005b000d000a00(.+)',line)
			if m3:
				t = toUtf8(m3.group(1))
				t = re.sub(r"\]==\];.+","", t)
				element[sid].text = replaceWord(t)
			else:
				m4 = re.match(r"(start|end)=(\d+)",line)
				if m4:
					if m4.group(1) == "start":
						start_ = m4.group(2)
					elif m4.group(1) == "end":
						end_ = m4.group(2)

with open("C:/Users/hmori/Documents/Youtube/KihitoChess/" + did + "/" + fid + ".sbv", "a") as f:
	for k,v in sorted(element.items()):
		if len(v.text) > 0:
			print (formatForSrt(int(v.start)-1)+","+formatForSrt(int(v.end))+"\r"+v.text+"\r", file=f)
