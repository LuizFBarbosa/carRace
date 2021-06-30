#pip install opencv-python
import cv2
import mediapipe
import queue

q = queue.Queue()

class Controle:


    def __init__(self):
        global q
        self.cap = cv2.VideoCapture(0)
        print('incializando o controle')

    def start(self):
        medhands = mediapipe.solutions.hands
        hands = medhands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        draw = mediapipe.solutions.drawing_utils

        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = hands.process(imgrgb)

            lmlist = []
            tipids = [4, 20] #iremos contar apenas a ponta do polegar e do mindinho

            cv2.rectangle(img, (20, 350), (90, 440), (0, 255, 204), cv2.FILLED)
            cv2.rectangle(img, (20, 350), (90, 440), (0, 0, 0), 5)

            # desenha a linha
            h, w, c = img.shape
            x1 = w /2
            y1 = 0
            x2 = x1
            y2 = h
            # desenha uma linha no meio
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)),(255, 0, 255), 2)
            posicao = 'C'
            if res.multi_hand_landmarks:
                for handlms in res.multi_hand_landmarks:
                    # landmark is based on image size, multiply landmark x,y,z by image size
                    # to get location of landmark on image(x multiply with width, y multiply with height)
                    for id, lm in enumerate(handlms.landmark):
                        #print(lm.x,lm.y)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        #print(id, cx, cy)

                        lmlist.append([id, cx, cy])
                        #Cada ciclo traz os 21 pontos mapeados na mão [0-20]
                        if len(lmlist) != 0 and len(lmlist) == 21:
                            fingerlist = [] #0 - movimento para esquerda
                            posicao = 'C'
                            # verifica se é mão esquerda  ou direita
                            if lmlist[12][1] < lmlist[20][1]: #mao direita
                                if (lmlist[8][1] > x1):
                                    posicao = 'D'
                                if (lmlist[20][1] < x1):
                                    posicao = 'E'
                                if (lmlist[8][1] < x1 and lmlist[16][1] > x1):
                                    posicao = 'C'

                            if(posicao != 'C'):
                                q.put(posicao)
                            cv2.putText(img, posicao, (25, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

                        # altera cor de pontos e linhas
                        draw.draw_landmarks(img, handlms, medhands.HAND_CONNECTIONS,
                                            draw.DrawingSpec(color=(0, 255, 204), thickness=2, circle_radius=2),
                                            draw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=3))

            # mostra posicao
            cv2.putText(img, posicao, (25, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

            cv2.imshow("Air Control", img)

            # pressiona q para sair
            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()