import cv2

def retangulo(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hole = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in hole:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]

    return coords

def variacao(coords, coords_anterior, i, img):
    if coords != None:
        if len(coords) == 4:
            if (coords[0] > coords_anterior):
                delta = coords[0] - coords_anterior
            else:
                delta = coords_anterior - coords[0]

            if (delta > 20):
                cv2.imwrite('localizacao/coordenada{}.jpg'.format(i), img)
                with open('localizacao/coordenada{}.txt'.format(i), 'w') as coordenada:
                    coordenada.write(str(coords))
                    #print(coords)
                    #print('anterior', coords_anterior)
                    return 1
    return 0

def detect(img, cascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0)}
    coords = retangulo(img, cascade, 1.1, 10, color['blue'], "buraco")
    return img, coords

cascade = cv2.CascadeClassifier('cascade.xml')

video = cv2.VideoCapture(0)

coords_anterior = 0
i = 0

while True:

    _, img = video.read()
    img, coords = detect(img, cascade)

    #print("ant", coords)
    if coords != None:
        if len(coords) == 4:
            zero = variacao(coords, coords_anterior, i, img)
            coords_anterior = coords[0]
            if zero == 1:
                i += 1

    cv2.imshow('imagem', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
