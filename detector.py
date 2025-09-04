import cv2
from pyzbar.pyzbar import decode

def detect_and_decode(frame):
    decoded_objects = decode(frame)
    decoded_data = []

    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = cv2.approxPolyDP(hull, 1, True)

        n = len(points)
        for i in range(n):
            cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % n]), (0, 255, 0), 3)

        decoded_info = obj.data.decode("utf-8")
        decoded_type = obj.type
        decoded_data.append({"type": decoded_type, "data": decoded_info})

        cv2.putText(frame, decoded_info, (points[0][0], points[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame, decoded_data
