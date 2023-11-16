import cv2
import numpy as np

# solidityに対するジャンケン判定用閾値
ROCK_MAX = 1.0   # グーと判定する上限の閾値
ROCK_MIN = 0.8   # グーと判定する下限の閾値

SCISSOR_MAX = 0.8 # チョキと判定する上限の閾値
SCISSOR_MIN = 0.6 # チョキと判定する下限の閾値

PAPER_MAX = 0.6   # パーと判定する上限の閾値
PAPER_MIN = 0.4   # パーと判定する下限の閾値

# HSV表色系の各下限と上限の値
H_MIN = 0   # 度
H_MAX= 180  # 度（180度で一周するとみなす）
S_MIN = 0   # 0.0 <-> 1.0 を 0 <-> 255 で表現 
S_MAX = 255 # 0.0 <-> 1.0 を 0 <-> 255 で表現 
V_MIN = 0   # 0.0 <-> 1.0 を 0 <-> 255 で表現 
V_MAX = 255 # 0.0 <-> 1.0 を 0 <-> 255 で表現 

# 各変数の初期値
hMin = H_MIN
hMax = H_MAX
sMin = S_MIN
sMax = S_MAX
vMin = V_MIN
vMax = V_MAX

# ウィンドウ名
WIN_NAME ='frame'

# Convert choice to string and map the integer to the corresponding label
hand_labels = {
    0: "Rock",
    1: "Scissors",
    2: "Paper",
    -1: "Unknown"
}


# スライダーが呼ばれたときのコールバック関数
def setHMin(val):
    # 関数内からグローバル変数を参照する場合にはglobalをつける
    global hMin
    hMin = val

def setHMax(val):
    global hMax
    hMax = val

def setSMin(val):
    global sMin
    sMin = val

def setSMax(val):
    global sMax
    sMax = val

def setVMin(val):
    global vMin
    vMin = val

def setVMax(val):
    global vMax
    vMax = val

'''
    肌色の画素に対応する画素を255，そうでない画素を0とする，マスク画像を生成
'''
def extractSkinMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # HSV空間で肌色の範囲を定義
    # 0 <= hue <= 15, 50 <= saturation <= 255, 50 <= value <= 255
    lower_skin = np.array([hMin,sMin,vMin])     
    upper_skin = np.array([hMax,sMax,vMax])

    # HSV イメージから青い物体だけを取り出すための閾値
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    return mask

'''
    膨張・縮小処理による欠損領域の補完
'''
def interpolate(mask):
    kernel = np.ones((5,5),np.uint8)
    # 膨張処理
    dilation = cv2.dilate(mask, kernel, iterations = 2)
    # 縮小処理
    mask = cv2.erode(dilation, kernel, iterations = 2)

    return mask
'''
    いくつかの領域から最大画素数を持つ領域を求める
    引数　：いくつかのブロブを持つ２値画像
    戻り値：領域に含まれる画素数, 最大画素数を持つ領域のみの画像
'''
def getMaximumBlob(mask):
    # ラベリング処理
    # 引数は背景が0，オブジェクトが0以外の2値画像
    # 戻り値は，オブジェクトの個数，背景が0,オブジェクトが1以上の値のついたラベル画像, 各輪郭，各オブジェクトの重心位置
    nlabels, labelimg, contours, CoGs = cv2.connectedComponentsWithStats(mask)

    if nlabels > 0:
        maxLabel = 0
        maxSize = 0
        for nlabel in range(1,nlabels): 
            x,y,w,h,size = contours[nlabel]
            xg,yg = CoGs[nlabel]
            if maxSize < size:
                maxSize = size
                maxLabel = nlabel

        # 最大領域を表すラベルを持つ画素値を255にする
        mask[labelimg == maxLabel] = 255
        # それ以外の領域はすべて0にする
        mask[labelimg != maxLabel] = 0

        return maxSize, mask
    else:
        return maxSize, mask

'''
    領域に外接する多角形(convex hull)を求める
    引数　：１つのブロブのみを含む２値画像
    戻り値：多角形内の画素数, 多角形の角を表す点のリスト, 元の領域の輪郭上の点のリスト 
'''
def getConvexHull(mask):
    
    # 輪郭を検出
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return 0, [], []

    hull = cv2.convexHull(contours[0], returnPoints=True)
    hullSize = cv2.contourArea(hull)
    
    return hullSize, hull, contours[0]


'''
    Solidity（凸包(領域を囲む最小の外接多角形)の面積に対する輪郭の面積の比）に基づくジャンケンの手の判定
    引数　：ブロブに含まれる画素数
    戻り値：ブロブの外接ポリゴン内に含まれる画素数
'''
def decide(handBlob, handHull):
    
    choice = -1
    solidity = 0

    if handHull != 0:
        solidity = handBlob / handHull
        if ROCK_MIN <= solidity and solidity <= ROCK_MAX:
            choice = 0
        elif SCISSOR_MIN <= solidity and solidity <= SCISSOR_MAX:
            choice = 1
        elif PAPER_MIN <= solidity and solidity <= PAPER_MAX:
            choice = 2
        else:
            choice = -1

    return choice, solidity

def tutorial_RockScissorPaper():

    cv2.namedWindow(WIN_NAME)
    # HSVの範囲設定のためのトラックバーの生成
    cv2.createTrackbar('HMin', WIN_NAME, hMin, H_MAX, setHMin)
    cv2.createTrackbar('HMax', WIN_NAME, hMax, H_MAX, setHMax)
    
    cv2.createTrackbar('SMin', WIN_NAME, sMin, S_MAX, setSMin)
    cv2.createTrackbar('SMax', WIN_NAME, sMax, S_MAX, setSMax)
    
    cv2.createTrackbar('VMin', WIN_NAME, vMin, V_MAX, setVMin)
    cv2.createTrackbar('VMax', WIN_NAME, vMax, V_MAX, setVMax)

    # カメラの初期化
    capture = cv2.VideoCapture(0)

    if capture.isOpened() is False:
        raise("IO Error")

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    capture.set(cv2.CAP_PROP_FPS, 30)

    # ループ
    while True:
        # 画像を１枚キャプチャ
        ret, frame = capture.read()
        if ret == False:
            continue

        # キャプチャした画像をimgにコピー
        img = frame.copy()

        # 各種処理
        mask = extractSkinMask(img)
        mask = interpolate(mask)
        maxSize, maxBlob = getMaximumBlob(mask)
        hullSize, hull, contour = getConvexHull(maxBlob)
        img = cv2.drawContours(frame, contour, -1, (255, 255,0), 3)
        
        # 描画：hullリストを一つだけ持つリストを第２引数で渡す
        img = cv2.drawContours(img, [hull], 0, (0, 255, 0), 2)
       
        # 判定
        choice, solidity = decide(maxSize, hullSize)

        if choice == 0:
            print("Rock: solidity = ", solidity)
            choice_text = "Rock"
        elif choice == 1:
            print("Scissors: solidity = ", solidity)
            choice_text = "Scissors"
        elif choice == 2:
            print("Paper: solidity = ", solidity)
            choice_text = "Paper"
        else:
            print("Unknown: solidity = ", solidity)
            choice_text = "Unknown"
 
        cv2.putText(img, choice_text, (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 255), 8, cv2.LINE_AA)

        # 画像の表示
        # 第一引数：ウィンドウを識別するための名前
        # 第二引数：表示する画像
        cv2.imshow(WIN_NAME, img)
        
        cv2.imshow('mask', maxBlob)
        # cv2.imshow('result', result)

        key = cv2.waitKey(1) & 0xff
        if key == 0x1b or key == ord('q') or key == ord('Q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    tutorial_RockScissorPaper()