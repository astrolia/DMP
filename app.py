import cv2

#passa os valores para definir os parametros de detecção e desenhar o retangulo na mesma
def retangulo(img, classifier, scaleFactor, minNeighbors, color, text):
    #passa a imagem para cinza
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #detecta objetos de varios tamanhos com base no cascade utilizado na imagem e repassa em formato de retangulos
    hole = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    #define as coordenadas da detecção e os parametros para desenhar o retangulo
    for (x, y, w, h) in hole:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]

    return coords

#tirar print da detecção e armazenar em uma pasta juntamente as coordenadas da mesma
def variacao(coords, coords_anterior, i, img):
    #condição para não fazer o mesmo armazenamento repetidas vezes
    if coords != None:
        if len(coords) == 4:
            if (coords[0] > coords_anterior):
                delta = coords[0] - coords_anterior
            else:
                delta = coords_anterior - coords[0]
            #armazena a imagem da detecção e as coordenadas
            if (delta > 10):
                cv2.imwrite('localizacao/coordenada{}.jpg'.format(i), img)
                with open('localizacao/coordenada{}.txt'.format(i), 'w') as coordenada:
                    coordenada.write(str(coords))
                    return 1
    return 0

#passa os valores da imagem e do classifier/cascade para fazer a detecção
def detect(img, cascade):
    color = {"azul": (255, 0, 0), "vermelho": (0, 0, 255), "verde": (0, 255, 0)}
    coords = retangulo(img, cascade, 1.1, 10, color['azul'], "deterioracao")
    return img, coords

#define o haarcascade(o classifier do nosso programa) utilizado
#o cascade sera o classificador de detecção, aquele que define oque deve ser detectado na imagem
cascade = cv2.CascadeClassifier('cascade.xml')

#define a entrada de video
video = cv2.VideoCapture(0)

coords_anterior = 0
i = 0

#loop infinito para a fazer a captura de imagem continuamente
while True:

#faz a leitura de video
    _, img = video.read()
    #passa os parametros da imagem e coordenadas para as variaveis
    img, coords = detect(img, cascade)

#caso a detecção não tenha valor nulo e nem tamanho de vetor menor que 4 faz a comparação e amarzenamento da mesma
    if coords != None:
        if len(coords) == 4:
            zero = variacao(coords, coords_anterior, i, img)
            coords_anterior = coords[0]
            if zero == 1:
                i += 1
#abre uma janela para mostrar a captura de video em tempo real
    cv2.imshow('imagem', img)
    #se precionar a tecla "q" o loop é finalizado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#encerra o video e fecha a janela de captura
video.release()
cv2.destroyAllWindows()
