from gameLib import *
import os

def numberCogs():
    #Coordinates of the inventory for cogs
    dims = (*rel2scr(*coords["inventory"][:2]), *rel2scr(*coords["inventory"][2:4]))
    Screenshot()
    CropImage("screen.png", *dims, f)
    places = contourBWImage("crop.png")
    image = cv2.imread("crop.png")
    tol = 8
    # Remove small contours
    places = sorted([list(i) for i in places if i[2] - i[0] > tol or i[3] - i[1] > tol], key=lambda tup:(tup[1], tup[0]))
    x, y, x2, y2 = zip(*places)

    x = sorted(set(x))
    y = sorted(set(y))
    x2 = sorted(set(x2))
    y2 = sorted(set(y2))

    # Remove stacking squares
    for j in x, y, x2, y2:    
        base = j[0]
        rem = []
        for i in j[1:]:
            if i-base < 10:
                j.remove(i)
                rem.append(i)
            base = i

    # Settle small divergences
    for cur in places:
        vec = [x, y, x2, y2]
        for j in range(4):
            for i in vec[j][::-1]:
                if cur[j] >= i:
                    cur[j] = i
                    break

    # Remove duplicates and sort top-down, left-right
    places = sorted(set([tuple(i) for i in places]), key=lambda tup:(tup[1], tup[0]))

    # Find then remove the %'s and middle blocks
    rem = []
    for i in range(1, len(places)):
        if places[i][0] - places[i-1][0] > 20 or places[i][0] < places[i-1][0]:
            rem.append(places[i - 1])
    for i in rem:
        places.remove(i)

    places = [list(i) for i in places[:-1]]

    p = places[0]
    new = [places[0]]
    end = []
    for cur in places[1:]:
        if abs(cur[0] - p[0]) > 40:
            end.append(p)
            base = cur
            new.append(cur)
        p = cur
    end.append(places[-1])

    os.system("cp crop.png coginv.png")
    image = cv2.imread("crop.png")
    ret = []
    for i in range(len(new)):
        if new[i][1] != end[i][1]:
            continue
        dx = dy = 1
        cv2.rectangle(image, (new[i][0] - dx, new[i][1] - dy), (end[i][2] + dx, end[i][3] + dy),(36, 255, 12), 1)
        CropImage("coginv.png", *(new[i][0] - dx, new[i][1] - dy), *(end[i][2] + dx, end[i][3] + dy), f)
        ret.append(''.join([i for i in img2text("crop.png", t) if i in "0123456789"]))
    cv2.imshow("Filtered Contours", image)
    cv2.waitKey()
    cv2.destroyAllWindows() 
    for i in range(len(ret)):
        if ret[i] != '' :
            ret[i] = int(ret[i])
        else:
            ret[i] = 0
    return ret

if __name__== "__main__":
    coords = {
            "inventory": (15, 146, 160, 584),
            "invCogs" : [(26, 150), (26, 236), (26, 322), (26, 408), (26, 493), (72, 150), (72, 236), (72, 322), (72, 408), (72, 493), (119, 150), (119, 236), (119, 322), (119, 408), (119, 493)],
#[abs2rel(i, j) for i in [4210, 4300, 4390] for j in [194, 284, 373, 463, 552]],
    }
    t = True
    f = False
    os.chdir("./aux")
    print(numberCogs())

else:
    x, y, x2, y2 = zip(*places)
    x = sorted(set(x))
    y = sorted(set(y))
    x2 = sorted(set(x2))
    y2 = sorted(set(y2))
    for j in x, x2:
        base = j[0]
        for i in j[1:]:
            if i-base < 10:
                j.remove(i)
            elif i - base > 30:
                if base in j:
                    j.remove(base)
                base = i
            else:
                base = i

    w = [x2[i] - x[i] for i in range(min(len(x), len(x2)))]
    w = [i for i in w if i < 20]
    h = [y2[i] - y[i] for i in range(min(len(y), len(y2)))]
    h = [i for i in h if i < 20]

    w = sum(w)//len(w)
    h = sum(h)//len(h)

    print(x)
    x = [x[0]] + [x[i + 1] for i in range(len(x) - 1) if x[i + 1] - x[i] > 2*w]
    print(x)
    image = cv2.imread("crop.png")
    for i in x:
        for j in y:
            cv2.rectangle(image, (i,j), (i+w,j+h),(36, 255, 12), 1)
    cv2.imshow("Numbers", image)
    cv2.waitKey()
    cv2.destroyAllWindows() 

    #print(contourImage("crop.png"))
    #print(img2text("crop.png", True))
