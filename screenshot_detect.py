#!/usr/bin/env python

import multiprocessing as mp
import os
import sys
import numpy as np
import cv2

MIN_MATCH_COUNT = 30 # adjust this param for more or less sensitivity

def mkQueue(path, queue):
    for root, dirs, files in os.walk(path,):
        for name in files:
            f = os.path.join(root, name)
            queue.put(f)

def detect(work_q, output_q, kp1, des1, flann):
    while work_q.empty() is False:
        f = work_q.get_nowait()

        img2 = cv2.imread(f, 0)
        sift = cv2.SIFT()
        try:
            kp2, des2 = sift.detectAndCompute(img2,None)
        except:
            print("Error analyzing %s" % f)
            continue

        if des2 is None:
            out_q.put("%s has insufficient descriptors for processing" % f)
            work_q.task_done()
            continue


        try:
            matches = flann.knnMatch(des1, des2, k=2)
        except:
            work_q.task_done()
            out_q.put("Error comparing %s" % f)
            continue

        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            out_q.put("Found match! %s" % f)
        else:
            out_q.put("No match. %s" % f)

        if work_q.qsize() % 100 == 0:
            print work_q.qsize()

if __name__ == '__main__':

    # process args
    if not len(sys.argv) == 4:
        sys.exit("Usage: %s target image_dir/ results.txt" % sys.argv[0])
    src = sys.argv[1]
    path = sys.argv[2]
    output = sys.argv[3]

    manager = mp.Manager()
    work_q = manager.Queue()
    out_q = manager.Queue()
    mkQueue(path, work_q)
    print "Scanning %s items from %s" % (work_q.qsize(), src)
    
    src_image = cv2.imread(src, 0)
    sift = cv2.SIFT()
    kp1, des1 = sift.detectAndCompute(src_image, None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    print "Starting %i processes" % mp.cpu_count()
    processes = [mp.Process(target=detect,args=(work_q, out_q, kp1, des1, flann)) for i in range(mp.cpu_count())]
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    with open(output, "wb") as fout:
        while out_q.empty() is False:
            result = out_q.get()
            fout.write("%s\n" % result)

