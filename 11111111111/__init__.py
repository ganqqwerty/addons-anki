# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QAction, QDialog, QVBoxLayout, QPushButton, QTextEdit
from aqt import mw
import re

from PyQt5.QtWidgets import QAction, QDialog, QVBoxLayout, QPushButton, QTextEdit
from aqt import mw
from anki.hooks import addHook
import re

N5_KANJI = set("人何分見大前子行出気今一生日話間時女来本中入上年聞長後食男先下金高父学名国母外小電車友書月山白木水校天万語二火川休半読十南土毎三東北西千八左右五雨百四午七円六九")  # Dummy data
N4_KANJI = set("私言手事思者会知自家物理目音心待方力死悪持場同作体動度意地明仕不親的楽通世用切立早発着帰使員田真問味少教考別代新正開元夜野強終界近安題止始以屋社道業空口起足海急兄主運族多店重画飲料買集送特売病品計転室試風朝歌文歩住花質医週黒色去映院赤有験犬服答写公走姉弟台習字注肉広銀町旅工古青飯英紙妹春貸堂図借夏魚鳥建研京究茶曜夕館勉秋昼牛洋冬駅漢")
N3_KANJI = set("彼君当最合部全違変夫殺所様感取声性戦回要信実好勝戻決解必連助次対番愛神失緒落美初確残関頼面配引命相達警王調法供伝込機現向然身直成情覚続逃呼願任選太報他内笑件付返守受乗数息定能平由顔優婚絶頭約過組消置負放係皆備指記得寝状原追飛犯危官利忘礼化葉務客察反怖望認断進許果流痛説娘完夢告役点師苦歳船加可幸捕探予罪経良表術想期活光突険治判抜座難倒念怒薬遅在馬遠常恐構渡民議破号談束欲鳴存位打未害遊格単式交石満産支払退昔和妻速形限徒共演球若悲観両投深盗似収済働政閉制酒静求育職容降権冷敗腹局争昨市疑首責居資喜熱参園与困科押精疲眠曲吸寄越段雪申増類種例除示際差杯処余具迎絵識亡割髪論登才暮迷席労側路洗暗末値都御米散背婦恥抱刻忙非陽舞留浮庭更互晴因宿横商老吹辞雑耳折掛適途宅晩誤祖程箱福慣便靴費偉到歯規候招給草訪財猫等欠景積努否寒港窓頂列富勤賛偶泳貧煙易阪幾")  # Continue for all your JLPT levels
N2_KANJI = set("無村査仲血捜軍星兵恋島準介装了絡爆練裏技再捨像久帯門普復武線令触暴団香移設況奥接城将協乱希造勢焼衣谷宇超簡録療効州毒届領丸逆弱片低減跡禁根腕周巻階防細個量被殿刺管担骨材辺極波菜補胸汚史導歴替森総戸甘栄永脳圧囲順温勇宝荒荷患祝混臓乾玉紹秒児燃改象棒軽型毛鉄庫換賞輪専境踊泉課橋氷芸府角営詰署印巨祈羽陸河植虫賢坂依副域承叫固砂鼻岩蔵悩泊並底純算雇枚布短黄祭清劇額損皮停油掃卵比訓敬卒袋競乳孫幼区照編党億咲延測快伸複預林包塗泥紅農倍尊略封贈板埋辛省液雲築則委律床群占昇寺憎各航誌涙肩章沈塩採浴珍腰岸央薄拾震凍臣掘匹粉緑革干池針菓諸双械績帽召札枝豊輸層含湯講柔竹溶童肌皿厚版齢拝汗灰駐般税浅磨麦湖販硬濃筆貨炭募鋭翌券糸塔灯旧濯述庁仏詞涼季傾挟脂伺漁胃著均瓶貯貝湾滴柱缶蒸粒机鉱県幅軟鈍兆籍筒欧郵符隅湿喫膚軒畜舟銅沸綿隻刷冊零郊枯燥刊姓畳曇貿耕肯")
N1_KANJI = set("僕結郎士撃張魔我嫌奴離証護隊傷保応貴謝敵第隠頑悟救器態銃泣藤黙刑義素検井視壊影密秘驚撮攻聖弁邪監佐独姿案故弾脱興司松雄宮統崎誘剣拠功怪異狙闘殴奈奪街携振派修輩宙冗射従訳矢援価氏霊激吉遺惑衛麻瞬艦志岡鬼襲騒裁授基審響緊滅条幕竜提博也織避尾慢之悔壁操憶症歓逮酔樹沢誕整製級聴恵妙描姫健厳江奇督脅駄鈴挑訴沙継抗評穴勘障善標尽納皇稼獄偽染端筋魂率隣盛策恩徳華紀拍診創養扱寅輝陛屈握翔嬢耐至脚帝契踏迫暇詳琴亜衝懸津儀挙系吐侵票為妊施源魅罰看桜展寂浜秀載企誓臭賊伊幽宗択伏房誠桃誇執裂仮雷索犠牲康刀牧剤乃炎那郷砲忍節遭潜縁瀬己揺飾駆模崩遣裕陰忠呂慮柄句獲鮮豆免鏡騎哲慎距威渉倉拒弥葬脈綾獣環尉請狩締唯繰徹巡焦宣及褒酸奮奏敷討推釣阿冒属露楠釈幻嫁娠揮愚致鎖仙陣智叔腐償妃孤梨紫虎飼拐麗恨旦穂趣抑班懐抵扉就丁尋添邦匠須譲斗衆拳墓謀遂滑徴益豚偵舎酷豪惨称裸暑詩漏嵐紋胞塚析笛顧既糖狂幹災透仁揚銭却彦覧典肝株躍巣眼亀芝凶菊随飽廷僚芽浦縛縮冴惜杉催辱僧戒誉刃伯撤桐覆洞廃雰虐削跳即賀微囚棄狭仰絞悠哀桑履潮峰排維砕貫憩甲蓮控睡慈斎玄稿拘喪熟潔舌勧還羅滞晶臨融欺圭烈霧陥栗賃鑑盤斉癒充暖範鹿錠堅胆献厄遇縦伴帳杏李隔批阻懲殊漫沖翼后堀猿鍛俳鶏曹縫敢煮縄菌妨郡穏劣核爵卑哉憧薫旗慰隷没繁拓肺倫拡滝沼鷹侮摘肢紛彩癖莉泰奉盟虚蛇柚嬉浪託詐盾羊猛桂噴寧敏妄浄鋼酬棚熊乙鼓鎮披粋赦励汁鐘冠佳孝序柳腸渋祐朗侑浸瞳茂膨唱飢網眺稲蝶征架尿閣薦泡瑚雅鶴紗汽貢軌扶漬兼寛寸乏拷弓尚磁漠侍叶項殻摩垂沿廊卓淳訟錬稚聡蛍寮俊玲醜亮簿購嘆邸塊克把渚駒怠唇凡偏摂宴膜荘蘭愉紳繊丘棟撲緩恭彫圏婆貞穫憲疫陪梅傑掲苗暦肥墜蒼漂湧剛椎汰往珠遮喚涯垣傘巧虜瑞殖壇頻概妥耶朱扇丹謙粗壮奨萌剰猟覇炉昌慶隆徐粘疎蛮渇遥魁培胎浩綱葵澄痴帆崇促賄搭綺虹鳳凝銘怜挿窮暁酢巴翻秩搬肪堕昭溝澪椿如矛恒勲婿啓祥楓遼俗眉錯芳弦憂疾径雛刈糧傍髄債陳亭輔枠逸匿斜淡朋棺蓄枢佑併孔諾較辰鞠掌昆茜彰衰橘栽磯陵窒緋粛悼旋睦是皐潤絹礎鉛抹墨蚊鉢渦又需舗剖栓弘逝岳炊堪搾凪謹凱丞軸盲轄猶鳩瑠槽拙緯窃戯藍猪帥詠忌迅伍陶鯨郁慕朽艇藻塾岐喝芋胴丑礁爽抽萩矯擦祉措呉酵宜敦巳毬廉塁宏柊宰践碁据璃擁娯淑庶悦顕閥准庄秦篤旨煩宵渓媒侯鎌姻漆耗赴酪伐胡隼擬錦旭穀洪凜賠繭蒔苑繕騰箇該笹括棋晃郭塀鯉懇痢盆旬玖濁殉斐餓薪朕尼靖暫循訂笙麟紘弔倣茎禅堤逐朴肖憤吏嚇弊雌楼嗣譜韻欄諭泌岬賜呈幣槙硫閲屯瞭梢駿彗謁甚翠吟紺采冶衡楊旺蕗襟鯛硝峡坪尺藩坑毅賓茅碑唆朔峠勅奔醸嘉謡菖愁遍滋壌嶺酌樺卸茉伽霞槻蓉只碧禄唄慨汐杜亥惰俵桟霜媛享稜禍晋琢叡昴遷絢稀某紡皓芹糾菫附褐叙鮎憾窯梓惟慧耀斥凌艶寡潟閑洲畔儒芙伎舶詔黛絃洸痘翁俸卯檀罷劾累禎胤栞惣莞倹黎亨弐鴻鋳甫賦租迪濫蕉偲墳升弧梧嫡昂稔巽曙庸欽瑛巌遵柾邑熙琉凹厘渥斤颯鵬諮凸裟詢袈衷允舜欣孟燎蚕丙酉暉榛嘱款迭峻穣壱暢喬但匡倭墾謄亘肇衿茄馨悌綜爾惇燦滉諒脹嵩捺捷錘竣倖漱伶塑且抄紬亦虞麿綸燿椰逓蔦眸勁嵯畝匁頌漸於椋崚彬啄誼赳晟頒碩宥晏脩奎彪恕尭晨侃銑瑳洵瑶勺諄琳")

def get_kanji_count_by_note(cards, field_name):
    kanji_dict = {}
    no_field_count = 0

    for card_id in cards:
        card = mw.col.getCard(card_id)
        note = card.note()

        if field_name not in note:
            no_field_count += 1
            continue

        for char in note[field_name]:
            if is_kanji(char):
                kanji_dict[char] = kanji_dict.get(char, 0) + 1

    return kanji_dict, no_field_count

def get_sorted_list(kanji_dict, criteria_set):
    filtered_items = {k: v for k, v in kanji_dict.items() if k in criteria_set}.items()
    return sorted(filtered_items, key=lambda item: item[1], reverse=True)

def classify_kanji_by_jlpt(kanji_dict):
    n5_list = get_sorted_list(kanji_dict, N5_KANJI)
    n4_list = get_sorted_list(kanji_dict, N4_KANJI)
    n3_list = get_sorted_list(kanji_dict, N3_KANJI)
    n2_list = get_sorted_list(kanji_dict, N2_KANJI)
    n1_list = get_sorted_list(kanji_dict, N1_KANJI)

    jlpt_union = N5_KANJI | N4_KANJI | N3_KANJI | N2_KANJI | N1_KANJI
    not_in_jlpt = sorted({k: v for k, v in kanji_dict.items() if k not in jlpt_union}.items(), key=lambda item: item[1], reverse=True)

    return n5_list, n4_list, n3_list, n2_list, n1_list, not_in_jlpt


def format_kanji_statistics(kanji_dict, jlpt_lists, total_cards, no_field_count, kanji_count, kana_count, field_name):
    n5_list, n4_list, n3_list, n2_list, n1_list, not_in_jlpt = jlpt_lists

    stats = f"""Total cards: {total_cards}
    Cards that don't have the "{field_name}" field: {no_field_count}
    Total japanese characters in "{field_name}" field: {kanji_count + kana_count}
    Kanji: {kanji_count}
    Unique kanji: {len(kanji_dict)}
    Kana: {kana_count}
    ------
    N5 Kanji: {", ".join([f"{k} ({v})" for k, v in n5_list])}
    N4 Kanji: {", ".join([f"{k} ({v})" for k, v in n4_list])}
    N3 Kanji: {", ".join([f"{k} ({v})" for k, v in n3_list])}
    N2 Kanji: {", ".join([f"{k} ({v})" for k, v in n2_list])}
    N1 Kanji: {", ".join([f"{k} ({v})" for k, v in n1_list])}
    not in JLPT: {", ".join([f"{k} ({v})" for k, v in not_in_jlpt])}"""

    return stats

def on_browser_init(browser):
    action = QAction("Count characters", browser)
    action.triggered.connect(lambda _, b=browser: show_dialog(b))
    browser.form.menuEdit.addAction(action)
    

addHook("browser.setupMenus", on_browser_init)


# Helper function to check if a character is Kanji
def is_kanji(ch):
    return 0x4E00 <= ord(ch) <= 0x9FFF


# Helper function to check if a character is Kana
def is_kana(ch):
    return (0x3040 <= ord(ch) <= 0x309F) or (0x30A0 <= ord(ch) <= 0x30FF)


def count_characters(cards, field_name):
    total_cards = len(cards)
    no_field_count = 0
    kanji_count = 0
    unique_kanji = set()
    kana_count = 0

    for card_id in cards:
        card = mw.col.getCard(card_id)
        note = card.note()
        if field_name in note:
            for char in note[field_name]:
                if is_kanji(char):
                    kanji_count += 1
                    unique_kanji.add(char)
                elif is_kana(char):
                    kana_count += 1
        else:
            no_field_count += 1

    kanji_dict, no_field_count = get_kanji_count_by_note(cards, field_name)
    jlpt_lists = classify_kanji_by_jlpt(kanji_dict)
    stats = format_kanji_statistics(kanji_dict, jlpt_lists, total_cards, no_field_count, kanji_count, kana_count, field_name)

    return stats

def add_context_menu_items(browser, menu):
    config = mw.addonManager.getConfig(__name__)
    
    action = QAction("Count characters", browser)
    action.triggered.connect(lambda _, b=browser: show_dialog(b))
    menu.addAction(action)

def show_dialog(browser):
    cards = browser.selected_cards()
    if not cards:
        return

    config = mw.addonManager.getConfig(__name__)
    default_field_name = config.get("default_field_name", "Your Field Name Here")

    dialog = QDialog(browser)
    dialog.setWindowTitle("Count Characters")

    layout = QVBoxLayout()

    field_name_input = QTextEdit()
    field_name_input.setPlainText(default_field_name)
    count_button = QPushButton("Count")
    result_display = QTextEdit()

    def on_count():
        field_name = field_name_input.toPlainText()
        stats = count_characters(cards, field_name)
        result_display.setPlainText(stats)

    count_button.clicked.connect(on_count)

    layout.addWidget(field_name_input)
    layout.addWidget(count_button)
    layout.addWidget(result_display)

    dialog.setLayout(layout)
    dialog.exec_()


addHook("browser.onContextMenu", add_context_menu_items)
