import os
import urllib.request
import tarfile

BASE_DIR = "app/models_data"
os.makedirs(BASE_DIR, exist_ok=True)

# ============================================
# MobileNet SSD V2 — Official TensorFlow Model Zoo
# Verified working URLs (No V3 issues)
# ============================================
MODEL_URL  = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"
TAR_PATH   = f"{BASE_DIR}/ssd_mobilenet_v2_coco.tar.gz"
PB_FILE    = f"{BASE_DIR}/frozen_inference_graph.pb"

# pbtxt (OpenCV-compatible graph config)
PBTXT_URL  = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
PBTXT_FILE = f"{BASE_DIR}/ssd_mobilenet_v2.pbtxt"

# COCO label names
NAMES_URL  = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
NAMES_FILE = f"{BASE_DIR}/coco.names"


def download(url, path):
    if not os.path.exists(path):
        print(f"Downloading {path}...")
        urllib.request.urlretrieve(url, path)
        print(f"✔ Downloaded {path}")
    else:
        print(f"✔ Already exists: {path}")


# Download model .tar.gz
download(MODEL_URL, TAR_PATH)

# Extract frozen_inference_graph.pb (model weight) from tar.gz
if not os.path.exists(PB_FILE):
    print("Extracting model...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        for m in tar.getmembers():
            if "frozen_inference_graph.pb" in m.name:
                tar.extract(m, BASE_DIR)
                os.rename(f"{BASE_DIR}/{m.name}", PB_FILE)
                break
    print(f"Extracted {PB_FILE}")
else:
    print("frozen_inference_graph.pb already present")

# Download pbtxt + labels
download(PBTXT_URL, PBTXT_FILE)
download(NAMES_URL, NAMES_FILE)

print("\nMobileNet-SSD V2 Model downloaded!")
