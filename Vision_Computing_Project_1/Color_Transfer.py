import cv2
import numpy as np

class ColorTransfer:
    def __init__(self):
        self.source_path="sunset.jpg"
        self.target_path="target.png"
    def show_image(self,name,img,size=300):
        r = size / float(img.shape[1])
        dim = (size, int(img.shape[0] * r))
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        # show the resized image
        cv2.imshow(name, resized)
    def change_color_space(self,color_space):

        source=cv2.imread(self.source_path)
        target=cv2.imread(self.target_path)


        for i in dir(cv2):
            if i.startswith("COLOR_"):
                print(i)
        self.show_image('source', source)
        self.show_image('target', target)
        #input_color_space=cv2.COLOR_BGR2RGB
        if color_space == 'LAB':
            input_color_space=cv2.COLOR_BGR2LAB
            output_color_space=cv2.COLOR_LAB2BGR
        #(l,a,b)=source.split()
        elif color_space == 'LUV':
            input_color_space = cv2.COLOR_BGR2Luv
            output_color_space = cv2.COLOR_Luv2BGR
        elif color_space == 'YCRCB':
            input_color_space = cv2.COLOR_BGR2YCR_CB
            output_color_space = cv2.COLOR_YCR_CB2BGR

        source = cv2.cvtColor(source, input_color_space).astype("float32")
        target = cv2.cvtColor(target, input_color_space).astype("float32")
        #cv2.imshow('source in hsv',source)
        #cv2.imshow('target',target)
        (lmean_s,amean_s,bmean_s,lstd_s,astd_s,bstd_s)=self.imgsplit(source)
        (lmean_t, amean_t, bmean_t, lstd_t, astd_t, bstd_t) = self.imgsplit(target)
        #(l_std_ratio,a_std_ratio,b_std_ratio)=(lstd_t,astd_t,bstd_t)/(lstd_s,astd_s,bstd_s)
        b_std_ratio=bstd_t/bstd_s
        a_std_ratio=astd_t/astd_s
        l_std_ratio=lstd_t/lstd_s


        #print(l_s,a_s,b_s)
        """
        (l_s,a_s,b_s)=cv2.split(source)
        l_s -= lmean_s
        a_s -= amean_s
        b_s -= bmean_s
        """
        (l_t, a_t, b_t) = cv2.split(target)
        l_t -= lmean_t
        a_t -= amean_t
        b_t -= bmean_t

        #(l_t, a_t, b_t)=(l_t,a_t,b_t)-(lmean_t,amean_t,bmean_t)
        #(l,a,b)=((l_std_ratio, a_std_ratio, b_std_ratio) * (l_s,a_s,b_s) )+ (lmean_t,amean_t,bmean_t)
        l = (l_std_ratio * l_t) + lmean_s
        a = (a_std_ratio * a_t) + amean_s
        b = (b_std_ratio * b_t) + bmean_s

        l = np.clip(l, 0, 255)
        a = np.clip(a, 0, 255)
        b = np.clip(b, 0, 255)

        output=cv2.merge([l,a,b])

        output=cv2.cvtColor(output.astype("uint8"),output_color_space)


        self.show_image('output',output)
        cv2.waitKey(0)


        #print(lmean,amean,bmean,lstd,astd,bstd)

        #cv2.waitKey(0)

        #print(source," ",target)
    def imgsplit(self,img):
        (l,a,b)=cv2.split(img)
        lMean=l.mean()
        aMean=a.mean()
        bMean=b.mean()
        lstd=l.std()
        astd=a.std()
        bstd=b.std()
        return (lMean,aMean,bMean,lstd,astd,bstd)
obj=ColorTransfer()
obj.change_color_space("LAB")
