import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import warnings

def test_qr_recognition():
    # 경고 메시지 필터링
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # 사용할 카메라 장치 인덱스 (필요에 따라 수정)
    camera_ids = [2, 4, 6, 8]
    
    print("카메라를 여는 중...")
    # 각 카메라에 대한 정보 저장: VideoCapture, 인식 횟수, 마지막 데이터, 마지막 감지 시간
    cameras = {}
    for cam_id in camera_ids:
        cap = cv2.VideoCapture(cam_id)
        if not cap.isOpened():
            print(f"카메라 {cam_id}를 열 수 없습니다. 연결 상태를 확인하세요.")
        else:
            # 해상도 설정 (선택 사항)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cameras[cam_id] = {
                'capture': cap,
                'detection_count': 0,
                'last_data': None,
                'last_detection_time': 0
            }
            # 각 카메라에 대해 별도 창 생성
            cv2.namedWindow(f"QR 코드 테스트 - Camera {cam_id}", cv2.WINDOW_NORMAL)
    
    if not cameras:
        print("사용 가능한 카메라가 없습니다. 프로그램을 종료합니다.")
        return
        
    print("카메라가 열렸습니다. 각 카메라에 QR 코드를 비춰주세요.")
    print("종료하려면 'q' 키를 누르세요.")
    
    while True:
        for cam_id, info in cameras.items():
            cap = info['capture']
            ret, frame = cap.read()
            if not ret:
                print(f"카메라 {cam_id}에서 프레임을 읽을 수 없습니다.")
                continue
            
            current_time = time.time()
            # QR 코드 검색
            qr_codes = decode(frame)
            
            for qr in qr_codes:
                qr_data = qr.data.decode('utf-8')
                # 같은 QR 코드를 너무 자주 출력하지 않도록 조건 체크
                if qr_data != info['last_data'] or (current_time - info['last_detection_time']) > 2:
                    info['detection_count'] += 1
                    print(f"[Camera {cam_id}] QR 코드 감지 #{info['detection_count']}: {qr_data}")
                    info['last_data'] = qr_data
                    info['last_detection_time'] = current_time
                
                # QR 코드 주위에 녹색 사각형 그리기
                points = qr.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
                else:
                    pts = np.array(points, dtype=np.int32)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                
                # QR 코드 데이터 표시
                cv2.putText(frame, qr_data, (qr.rect.left, qr.rect.top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # 안내 텍스트 추가 (선택 사항)
            cv2.putText(frame, "QR 코드를 화면에 비춰주세요", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # 각 카메라 창에 결과 표시
            cv2.imshow(f"QR 코드 테스트 - Camera {cam_id}", frame)
        
        # 'q' 키 입력 시 모든 창 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 최종 결과 출력 및 자원 해제
    for cam_id, info in cameras.items():
        print(f"카메라 {cam_id}: 총 {info['detection_count']}개의 QR 코드를 인식했습니다.")
        info['capture'].release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_qr_recognition()


# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# import time
# import warnings

# def test_qr_recognition():
#     # 경고 메시지 필터링
#     warnings.filterwarnings("ignore", category=RuntimeWarning)
    
#     print("카메라를 여는 중...")
#     # 기본 카메라 장치 (일반적으로 0번)
#     cap = cv2.VideoCapture(2)
    
#     # 카메라를 열 수 없는 경우
#     if not cap.isOpened():
#         print("카메라를 열 수 없습니다. 카메라가 연결되어 있고 다른 프로그램에서 사용 중이 아닌지 확인하세요.")
#         return
        
#     print("카메라가 열렸습니다. QR 코드를 카메라에 비춰주세요.")
#     print("종료하려면 'q'키를 누르세요.")
    
#     # 해상도 설정 (선택 사항)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
#     # QR 코드 인식 횟수 카운터
#     detection_count = 0
#     last_data = None
#     last_detection_time = 0
    
#     # 화면 미리 생성 (선택 사항)
#     cv2.namedWindow("QR 코드 테스트", cv2.WINDOW_NORMAL)
    
#     while True:
#         # 프레임 읽기
#         ret, frame = cap.read()
        
#         if not ret:
#             print("프레임을 읽을 수 없습니다.")
#             break
            
#         # QR 코드 검색
#         qr_codes = decode(frame)
        
#         current_time = time.time()
        
#         # 찾은 QR 코드 처리
#         for qr in qr_codes:
#             # QR 코드 데이터 추출
#             qr_data = qr.data.decode('utf-8')
            
#             # 같은 QR 코드를 너무 자주 출력하지 않도록 함
#             if qr_data != last_data or (current_time - last_detection_time) > 2:
#                 detection_count += 1
#                 print(f"QR 코드 감지 #{detection_count}: {qr_data}")
#                 last_data = qr_data
#                 last_detection_time = current_time
            
#             # QR 코드 주위에 녹색 사각형 그리기
#             points = qr.polygon
#             if len(points) > 4:
#                 hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
#                 cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
#             else:
#                 pts = np.array(points, dtype=np.int32)
#                 cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            
#             # QR 코드 데이터 화면에 표시
#             cv2.putText(frame, qr_data, (qr.rect.left, qr.rect.top - 10),
#                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
#         # 안내 텍스트 추가 (선택 사항)
#         cv2.putText(frame, "QR 코드를 화면에 비춰주세요", (10, 30),
#                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
#         # 화면에 표시
#         cv2.imshow("QR 코드 테스트", frame)
        
#         # 'q'를 누르면 종료
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     print(f"총 {detection_count}개의 QR 코드를 인식했습니다.")
#     # 자원 해제
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     test_qr_recognition()

# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# import time

# def test_qr_recognition():
#     print("카메라를 여는 중...")
#     # 기본 카메라 장치 (일반적으로 0번)
#     cap = cv2.VideoCapture(2)
    
#     # 카메라를 열 수 없는 경우
#     if not cap.isOpened():
#         print("카메라를 열 수 없습니다. 카메라가 연결되어 있고 다른 프로그램에서 사용 중이 아닌지 확인하세요.")
#         return
        
#     print("카메라가 열렸습니다. QR 코드를 카메라에 비춰주세요.")
#     print("종료하려면 'q'키를 누르세요.")
    
#     # QR 코드 인식 횟수 카운터
#     detection_count = 0
#     last_data = None
#     last_detection_time = 0
    
#     while True:
#         # 프레임 읽기
#         ret, frame = cap.read()
        
#         if not ret:
#             print("프레임을 읽을 수 없습니다.")
#             break
            
#         # QR 코드 검색
#         qr_codes = decode(frame)
        
#         current_time = time.time()
        
#         # 찾은 QR 코드 처리
#         for qr in qr_codes:
#             # QR 코드 데이터 추출
#             qr_data = qr.data.decode('utf-8')
            
#             # 같은 QR 코드를 너무 자주 출력하지 않도록 함
#             if qr_data != last_data or (current_time - last_detection_time) > 2:
#                 detection_count += 1
#                 print(f"QR 코드 감지 #{detection_count}: {qr_data}")
#                 last_data = qr_data
#                 last_detection_time = current_time
            
#             # QR 코드 주위에 녹색 사각형 그리기
#             points = qr.polygon
#             if len(points) > 4:
#                 hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
#                 cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
#             else:
#                 pts = np.array(points, dtype=np.int32)
#                 cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            
#             # QR 코드 데이터 화면에 표시
#             cv2.putText(frame, qr_data, (qr.rect.left, qr.rect.top - 10),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
#         # 화면에 표시
#         cv2.imshow("QR 코드 테스트", frame)
        
#         # 'q'를 누르면 종료
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     print(f"총 {detection_count}개의 QR 코드를 인식했습니다.")
#     # 자원 해제
#     cap.release()
#     cv2.destroyAllWindows()