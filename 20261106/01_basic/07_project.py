"""실습 07~08. 이미지 탐지와 영상 추적을 수행하고 결과를 저장합니다."""
from pathlib import Path
import cv2
import torch
import pandas as pd
from ultralytics import YOLO

# 현재 파일이 있는 폴더를 기준으로 입력·출력 경로를 만듭니다.
BASE = Path(__file__).resolve().parent
# PyTorch의 CPU 연산 스레드 수를 1개로 제한합니다.
torch.set_num_threads(1)

# 1. 학습된 가중치를 불러와 검증 이미지에서 객체를 탐지합니다.
model = YOLO(str(BASE / "data/demo.pt"))
rows = []
# conf: 최소 신뢰도, imgsz: 모델 입력 크기, device: 연산 장치
# verbose=False는 상세 로그를 숨깁니다. r은 이미지 한 장의 탐지 결과입니다.
for r in model.predict(source=str(BASE/"data/images/val"), conf=0.25, imgsz=160, device="cpu", verbose=False):
    # xyxy: 박스의 좌상단·우하단 좌표, cls: 클래스 번호, conf: 신뢰도
    # cpu().tolist()로 텐서를 CPU의 리스트로 바꾸고 zip으로 함께 순회합니다.
    for box, cls, score in zip(r.boxes.xyxy.cpu().tolist(), r.boxes.cls.cpu().tolist(), r.boxes.conf.cpu().tolist()):
        # 객체 하나를 한 행으로 기록합니다. *box는 좌표 4개를 각각 펼칩니다.
        rows.append([Path(r.path).name, int(cls), score, *box])
# 이미지 이름·클래스·신뢰도·좌표를 CSV로 저장합니다. index=False는 행 번호를 제외합니다.
pd.DataFrame(rows, columns=["image", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv(BASE/"p07_predictions.csv", index=False)

# 2. 영상 추적을 준비합니다. 새 모델 인스턴스로 이전 추적 상태와 분리합니다.
tracker = YOLO(str(BASE / "data/demo.pt"))
# OpenCV로 원본 영상의 초당 프레임 수와 화면 크기(너비, 높이)를 읽습니다.
cap = cv2.VideoCapture(str(BASE / "data/demo.avi"))
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 영상 정보만 읽고 닫습니다. 실제 프레임 처리는 아래 tracker.track이 담당합니다.
cap.release()
# MJPG 코덱을 사용해 원본과 같은 fps·크기의 결과 영상을 저장할 준비를 합니다.
writer = cv2.VideoWriter(str(BASE / "p07_tracked.avi"), cv2.VideoWriter_fourcc(*"MJPG"), fps, size)
tracks = []  # 객체별 추적 기록
frame_rows = []  # 프레임별 탐지 개수
# >>> B08
# 요구: demo.avi를 ByteTrack으로 읽는 stream=True 결과 generator를 만드세요.
# persist=False는 새로운 파일 스트림의 시작입니다. 같은 파일 내부 프레임은 이어집니다.
# ByteTrack은 프레임 간 탐지 결과를 연결하여 같은 객체에 추적 ID를 부여합니다.
# stream=True는 결과를 한꺼번에 모으지 않고 프레임별로 꺼내는 generator를 반환합니다.
results = tracker.track(
    source=str(BASE / "data/demo.avi"),
    tracker="bytetrack.yaml",
    stream=True,
    persist=False,
    conf=0.25,
    imgsz=160,
    device="cpu",
    verbose=False,
)
# <<< B08
# 3. generator를 순회하며 프레임별 결과를 처리합니다. frame은 0부터 시작합니다.
for frame, result in enumerate(results):
    # plot()은 박스·클래스·추적 ID 등의 표시가 그려진 프레임을 반환합니다.
    writer.write(result.plot())
    # 해당 프레임에서 탐지된 박스 수를 기록합니다.
    frame_rows.append([frame, len(result.boxes)])
    # 추적 ID가 있는 경우에만 객체별 추적 정보를 기록합니다.
    if result.boxes.id is not None:
        for box, cls, score, tid in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.cls.cpu().tolist(), result.boxes.conf.cpu().tolist(), result.boxes.id.cpu().tolist()):
            # cls는 객체의 종류이고, tid는 추적 중인 개별 객체의 식별 번호입니다.
            tracks.append([frame, int(tid), int(cls), score, *box])
# 영상 파일 저장을 마무리하고 자원을 해제합니다.
writer.release()
# >>> B09
# 요구: tracks를 지정한 열 이름의 CSV로 저장하세요. index=False를 사용합니다.
# append에서 넣은 순서대로 프레임·추적 ID·클래스·신뢰도·좌표 열을 지정합니다.
pd.DataFrame(
    tracks,
    columns=["frame", "track_id", "class_id", "confidence", "x1", "y1", "x2", "y2"],
).to_csv(BASE / "p07_tracks.csv", index=False)
# <<< B09
# 4. 프레임별 탐지 개수를 저장하고 입력 정보와 실제 처리한 프레임 수를 출력합니다.
pd.DataFrame(frame_rows, columns=["frame", "detections"]).to_csv(BASE/"p07_frames.csv", index=False)
print("입력 fps/size:", fps, size, "처리 Frame:", len(frame_rows))
print("실습 08: 설정을 바꾸지 말고 다시 실행해 Frame 수·CSV·영상을 확인하세요.")
